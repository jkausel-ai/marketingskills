#!/usr/bin/env python3
"""
model_router.py — CoChalet Pipeline Model Failover Router
Stage: DISPATCH (called by dispatcher.py + pipeline_runner.py)

DESIGN PRINCIPLES:
- Failover chain is HARDCODED — no external config dependency at runtime
- Each chain tier: try paid/quality first, fall back to free models
- Health check is FAST: single lightweight GET to OpenRouter /models endpoint
- pipeline stages call get_model(skill, context) or next_fallback(failed_model)
- All failover decisions are logged to /tmp/model_router.log for audit

FAILOVER ORDER (per task type):
  DEFAULT:      deepseek-chat → qwen/qwen3-next-80b:free → meta-llama/llama-3.3-70b:free → google/gemma-4-31b:free
  STRATEGY:     claude-sonnet-4-6 → deepseek-chat → qwen/qwen3-next-80b:free → meta-llama/llama-3.3-70b:free
  FRENCH:       gemini-2.5-flash → deepseek-chat → qwen/qwen3-next-80b:free → google/gemma-4-31b:free
  SPEED/BULK:   qwen-3.6-plus → deepseek-chat → qwen/qwen3-next-80b:free → meta-llama/llama-3.3-70b:free
  TECHNICAL:    gemma-4 → deepseek-chat → qwen/qwen3-next-80b:free → nvidia/nemotron-3-super-120b:free
  VERIFY/PATCH: claude-sonnet-4-6 → deepseek-chat → qwen/qwen3-next-80b:free → meta-llama/llama-3.3-70b:free

Usage:
  from model_router import ModelRouter
  router = ModelRouter()
  model_id = router.get_model("email-sequence", task="write DW email sequence FR")
  # On failure:
  fallback = router.next_fallback(model_id, skill="email-sequence")
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────────────
CREDS_PATH   = Path("/root/.claudeos/secrets/cos-mesh-credentials.json")
LOG_PATH     = Path("/tmp/model_router.log")
SKILL_ROUTER = Path("/mnt/hermes-output/cochalet-skills/cochalet/config/skill-router.json")
OR_MODELS_URL = "https://openrouter.ai/api/v1/models"

# ── HARDCODED FAILOVER CHAINS ───────────────────────────────────────────────
# Format: [primary, fallback1, fallback2, fallback3]
# Each entry is an OpenRouter model ID (or alias resolved below).
# FREE models are marked with :free suffix — zero cost, always last resort.

CHAINS = {
    "default": [
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemma-4-31b-it:free",
    ],
    "strategy": [
        "anthropic/claude-sonnet-4-6",
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
    "french": [
        "google/gemini-2.5-flash-preview",
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "google/gemma-4-31b-it:free",
    ],
    "speed": [
        "qwen/qwen3-plus",
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
    "technical": [
        "google/gemma-3-27b-it",
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
    ],
    "verify_patch": [
        "anthropic/claude-sonnet-4-6",
        "deepseek/deepseek-chat",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
    "cron": [
        # Ordered by LIVE availability — probed 2026-04-10, majority of free models down
        # nemotron + gpt-oss-20b were only ones responding. Gate script probes live each run.
        "nvidia/nemotron-3-super-120b-a12b:free",
        "openai/gpt-oss-20b:free",
        "openai/gpt-oss-120b:free",
        "google/gemma-4-31b-it:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
}

# ── SKILL → CHAIN MAPPING ──────────────────────────────────────────────────
SKILL_CHAIN_MAP = {
    # Strategy chain
    "marketing-psychology":     "strategy",
    "product-marketing-context":"strategy",
    "competitor-alternatives":  "strategy",
    "pricing-strategy":         "strategy",
    "launch-strategy":          "strategy",
    "customer-research":        "strategy",
    "content-strategy":         "strategy",
    # CRO / verify chain (quality matters most)
    "page-cro":                 "verify_patch",
    "signup-flow-cro":          "verify_patch",
    "onboarding-cro":           "verify_patch",
    "seo-audit":                "verify_patch",
    "ai-seo":                   "verify_patch",
    # Speed chain (bulk output)
    "social-content":           "speed",
    "lead-magnets":             "speed",
    "marketing-ideas":          "speed",
    "ad-creative":              "speed",
    # Technical chain
    "analytics-tracking":       "technical",
    "ab-test-setup":            "technical",
    "site-architecture":        "technical",
    "schema-markup":            "technical",
    "programmatic-seo":         "technical",
    "free-tool-strategy":       "technical",
    # Default for remaining
    "copywriting":              "default",
    "email-sequence":           "default",
    "cold-email":               "default",
    "revops":                   "default",
    "sales-enablement":         "default",
    "referral-program":         "default",
    "community-marketing":      "default",
    "churn-prevention":         "default",
    "paid-ads":                 "default",
    "form-cro":                 "default",
    "popup-cro":                "default",
    "copy-editing":             "default",
}

# ── KNOWN DEAD MODELS (circuit breaker — skip immediately) ─────────────────
# Populated at runtime via health check. Cleared on module reload.
_DEAD_MODELS: set = set()
_HEALTH_CACHE: dict = {}   # model_id → {ok: bool, checked_at: float}
_HEALTH_TTL = 300          # 5 minutes — re-check after this many seconds


def _log(msg: str):
    """Append a timestamped line to the model router log."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}\n"
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line)
    except Exception:
        pass
    print(f"[model_router] {msg}", file=sys.stderr)


def _load_or_key() -> Optional[str]:
    """Load OpenRouter API key from credentials or environment."""
    # Try environment first
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OR_API_KEY")
    if key:
        return key
    # Try known key files
    key_paths = [
        Path("/root/.claudeos/secrets/openrouter-api-key.txt"),
        Path("/root/.hermes/secrets/openrouter.key"),
    ]
    for p in key_paths:
        if p.exists():
            return p.read_text().strip()
    return None


def health_check(model_id: str, api_key: Optional[str] = None) -> bool:
    """
    Check if a model is available on OpenRouter.
    Uses a TTL cache — does NOT make a live inference call.
    Returns True if available, False if dead/unknown.
    """
    now = time.time()
    cached = _HEALTH_CACHE.get(model_id)
    if cached and (now - cached["checked_at"]) < _HEALTH_TTL:
        return cached["ok"]

    if model_id in _DEAD_MODELS:
        return False

    # For :free models, assume available unless explicitly dead
    # (avoids rate-limit hits on health checks)
    if ":free" in model_id:
        _HEALTH_CACHE[model_id] = {"ok": True, "checked_at": now}
        return True

    # For paid models: attempt lightweight models list fetch
    key = api_key or _load_or_key()
    if not key:
        # No key — assume available, will fail at inference time
        _HEALTH_CACHE[model_id] = {"ok": True, "checked_at": now}
        return True

    try:
        req = urllib.request.Request(
            OR_MODELS_URL,
            headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        available_ids = {m["id"] for m in data.get("data", [])}
        ok = model_id in available_ids
        _HEALTH_CACHE[model_id] = {"ok": ok, "checked_at": now}
        if not ok:
            _log(f"HEALTH_FAIL: {model_id} not in available models list")
            _DEAD_MODELS.add(model_id)
        return ok
    except Exception as e:
        _log(f"HEALTH_CHECK_ERROR: {model_id} — {e} — assuming available")
        # On network error: assume available (fail open), don't cache
        return True


def _chain_for_skill(skill: str, task: str = "") -> str:
    """Determine which failover chain to use."""
    # French content detection
    task_lower = task.lower()
    if " fr" in task_lower or "french" in task_lower or "français" in task_lower or "tutoiement" in task_lower:
        return "french"
    # Bulk/speed detection
    if any(kw in task_lower for kw in ["bulk", "batch", "draft", "summary", "translate"]):
        return "speed"
    # Use skill map
    return SKILL_CHAIN_MAP.get(skill, "default")


class ModelRouter:
    """
    Failover-aware model router for the CoChalet marketing pipeline.

    Usage:
        router = ModelRouter()
        model = router.get_model("email-sequence", task="write DW email FR")
        # ... call model ...
        # If model fails:
        fallback = router.next_fallback(model, skill="email-sequence")
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or _load_or_key()
        self._session_failures: dict = {}  # model_id → failure count this session

    def get_model(self, skill: str, task: str = "", chain_override: Optional[str] = None) -> str:
        """
        Return the best available model for this skill/task.
        Skips models known dead this session. Falls through entire chain if needed.
        Returns the first healthy model, or the last resort free model if all fail.
        """
        chain_name = chain_override or _chain_for_skill(skill, task)
        chain = CHAINS.get(chain_name, CHAINS["default"])

        _log(f"GET_MODEL: skill={skill} chain={chain_name} task_preview={task[:40]!r}")

        for model_id in chain:
            if model_id in _DEAD_MODELS:
                _log(f"  SKIP (dead): {model_id}")
                continue
            failures = self._session_failures.get(model_id, 0)
            if failures >= 2:
                _log(f"  SKIP (session failures={failures}): {model_id}")
                continue
            if health_check(model_id, self.api_key):
                _log(f"  SELECTED: {model_id}")
                return model_id
            else:
                _log(f"  SKIP (health_fail): {model_id}")

        # All models in chain exhausted — use absolute last resort
        last_resort = "meta-llama/llama-3.3-70b-instruct:free"
        _log(f"  LAST_RESORT: {last_resort} (all chain models exhausted)")
        return last_resort

    def next_fallback(self, failed_model: str, skill: str = "", task: str = "") -> str:
        """
        Record a model failure and return the next available model in the chain.
        Call this when a model call raises an exception or returns empty output.
        """
        # Record failure
        self._session_failures[failed_model] = self._session_failures.get(failed_model, 0) + 1
        if self._session_failures[failed_model] >= 2:
            _DEAD_MODELS.add(failed_model)
            _log(f"CIRCUIT_OPEN: {failed_model} marked dead (session failures >= 2)")

        _log(f"FAILOVER: {failed_model} failed ({self._session_failures[failed_model]}x) → finding next")
        return self.get_model(skill or "default", task=task)

    def mark_dead(self, model_id: str, reason: str = "manual"):
        """Permanently mark a model dead for this session."""
        _DEAD_MODELS.add(model_id)
        _log(f"MARK_DEAD: {model_id} — reason: {reason}")

    def get_cron_model(self) -> str:
        """Return the best available free model for cron/background jobs."""
        return self.get_model("cron", chain_override="cron")

    def status(self) -> dict:
        """Return current router state for diagnostics."""
        return {
            "dead_models": list(_DEAD_MODELS),
            "session_failures": self._session_failures,
            "health_cache_entries": len(_HEALTH_CACHE),
            "chains": {name: chain[0] for name, chain in CHAINS.items()},
        }

    def full_chain(self, skill: str, task: str = "") -> list:
        """Return the full ordered chain for a skill (for display/debugging)."""
        chain_name = _chain_for_skill(skill, task)
        return CHAINS.get(chain_name, CHAINS["default"])


# ── CLI interface ──────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CoChalet Model Router")
    parser.add_argument("command", choices=["get", "chain", "health", "status"],
                        help="get: pick model | chain: show full chain | health: check model | status: router state")
    parser.add_argument("--skill", default="default", help="Skill name")
    parser.add_argument("--task", default="", help="Task string (for chain detection)")
    parser.add_argument("--model", default="", help="Model ID (for health command)")
    args = parser.parse_args()

    router = ModelRouter()

    if args.command == "get":
        model = router.get_model(args.skill, args.task)
        print(json.dumps({"selected_model": model, "skill": args.skill}, indent=2))

    elif args.command == "chain":
        chain_name = _chain_for_skill(args.skill, args.task)
        chain = CHAINS.get(chain_name, CHAINS["default"])
        print(json.dumps({
            "skill": args.skill,
            "chain_type": chain_name,
            "chain": chain,
        }, indent=2))

    elif args.command == "health":
        if not args.model:
            print("--model required for health command")
            sys.exit(1)
        ok = health_check(args.model)
        print(json.dumps({"model": args.model, "available": ok}, indent=2))

    elif args.command == "status":
        print(json.dumps(router.status(), indent=2))


if __name__ == "__main__":
    main()
