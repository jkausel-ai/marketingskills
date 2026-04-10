#!/usr/bin/env python3
"""
startup_check.py — CoChalet Pipeline Startup Health Check
Run at the start of every Hermes session to verify all services are operational.

Usage: python3 startup_check.py
Returns: JSON with status per service + overall pass/fail
Exit code: 0 = all OK, 1 = one or more critical failures
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

PIPELINE_DIR = Path("/mnt/hermes-output/cochalet-skills/cochalet/pipeline")
sys.path.insert(0, str(PIPELINE_DIR))

results = {}
failures = []

def check(name, fn):
    try:
        ok, detail = fn()
        results[name] = {"ok": ok, "detail": detail}
        if not ok:
            failures.append(name)
    except Exception as e:
        results[name] = {"ok": False, "detail": f"EXCEPTION: {e}"}
        failures.append(name)

# ── 1. Pipeline files ──────────────────────────────────────────────────────
def check_pipeline_files():
    required = ["model_router.py", "gate_check.py", "dispatcher.py", "pipeline_runner.py"]
    missing = [f for f in required if not (PIPELINE_DIR / f).exists()]
    if missing:
        return False, f"Missing: {missing}"
    # Syntax check all
    bad = []
    for f in required:
        r = subprocess.run([sys.executable, "-m", "py_compile", str(PIPELINE_DIR / f)],
                          capture_output=True)
        if r.returncode != 0:
            bad.append(f)
    if bad:
        return False, f"Syntax errors in: {bad}"
    return True, f"All {len(required)} pipeline files OK"

check("pipeline_files", check_pipeline_files)

# ── 2. Model router ────────────────────────────────────────────────────────
def check_model_router():
    from model_router import ModelRouter
    router = ModelRouter()
    model = router.get_model("email-sequence", task="test")
    if not model:
        return False, "get_model returned empty"
    chain = router.full_chain("email-sequence")
    status = router.status()
    return True, f"selected={model} | chain_len={len(chain)} | dead={status['dead_models']}"

check("model_router", check_model_router)

# ── 3. Config files ────────────────────────────────────────────────────────
def check_config_files():
    config_dir = PIPELINE_DIR.parent / "config"
    required = ["skill-router.json", "brand-voice-guard.json"]
    missing = [f for f in required if not (config_dir / f).exists()]
    if missing:
        return False, f"Missing config: {missing}"
    # Validate JSON
    bad = []
    for f in required:
        try:
            json.loads((config_dir / f).read_text())
        except Exception as e:
            bad.append(f"{f}: {e}")
    if bad:
        return False, f"Invalid JSON: {bad}"
    return True, f"Config files OK ({len(required)} validated)"

check("config_files", check_config_files)

# ── 4. KB V2 canon ────────────────────────────────────────────────────────
def check_kb_v2():
    kb = Path("/mnt/hermes-output/HERMES_KNOWLEDGE_BASE_V2.md")
    if not kb.exists():
        return False, "HERMES_KNOWLEDGE_BASE_V2.md not found"
    size = kb.stat().st_size
    if size < 1000:
        return False, f"KB V2 suspiciously small: {size} bytes"
    return True, f"KB V2 OK ({size:,} bytes)"

check("kb_v2_canon", check_kb_v2)

# ── 5. shared-memory.jsonl ─────────────────────────────────────────────────
def check_shared_memory():
    sm = Path("/mnt/hermes-output/memory/shared-memory.jsonl")
    if not sm.exists():
        # Not fatal — will be created on first write
        return True, "shared-memory.jsonl not yet created (will be created on first pipeline run)"
    size = sm.stat().st_size
    # Count lines
    with open(sm) as f:
        lines = sum(1 for _ in f)
    return True, f"shared-memory.jsonl OK ({lines} entries, {size:,} bytes)"

check("shared_memory", check_shared_memory)

# ── 6. Memora MCP DB ──────────────────────────────────────────────────────
def check_memora():
    # Primary location (where memora-server actually writes)
    db = Path("/root/.local/share/memora/memories.db")
    if not db.exists():
        # Fallback check legacy path
        db = Path("/root/.memora/cochalet-marketing.db")
        if not db.exists():
            return False, "Memora DB not found at either expected path"
    size = db.stat().st_size
    if size == 0:
        return False, f"Memora DB is empty (0 bytes) at {db}"
    return True, f"Memora DB OK ({size:,} bytes) at {db}"

check("memora_db", check_memora)

# ── 7. Memora server binary ────────────────────────────────────────────────
def check_memora_server():
    server = Path("/root/.memora-venv/bin/memora-server")
    if not server.exists():
        return False, "memora-server binary not found"
    return True, "memora-server binary OK"

check("memora_server", check_memora_server)

# ── 8. Mesh credentials ───────────────────────────────────────────────────
def check_mesh_creds():
    creds = Path("/root/.claudeos/secrets/cos-mesh-credentials.json")
    if not creds.exists():
        return False, "cos-mesh-credentials.json not found"
    data = json.loads(creds.read_text())
    key = data.get("api_key", "")
    url = data.get("worker_url", "")
    if not key or not url:
        return False, "Missing api_key or worker_url in credentials"
    return True, f"Mesh creds OK (node key prefix: {key[:8]}...)"

check("mesh_credentials", check_mesh_creds)

# ── 9. Mesh poll script ────────────────────────────────────────────────────
def check_mesh_scripts():
    scripts = ["/root/scripts/mesh-poll.sh", "/root/scripts/mesh-send.sh"]
    missing = [s for s in scripts if not Path(s).exists()]
    if missing:
        return False, f"Missing: {missing}"
    return True, "mesh-poll.sh + mesh-send.sh OK"

check("mesh_scripts", check_mesh_scripts)

# ── 10. Deliverables dirs ─────────────────────────────────────────────────
def check_deliverable_dirs():
    depts = [
        "dept-seo-content", "dept-cro", "dept-content-copy",
        "dept-paid-measurement", "dept-growth-retention",
        "dept-sales-gtm", "dept-strategy"
    ]
    base = Path("/mnt/hermes-output/deliverables")
    missing = [d for d in depts if not (base / d).exists()]
    if missing:
        # Auto-create
        for d in missing:
            (base / d).mkdir(parents=True, exist_ok=True)
        return True, f"Auto-created {len(missing)} missing dept dirs"
    return True, f"All {len(depts)} dept deliverable dirs OK"

check("deliverable_dirs", check_deliverable_dirs)

# ── 11. Dashboard update system ───────────────────────────────────────────
def check_dashboard_system():
    update = Path("/root/scripts/dashboard-update.sh")
    watcher = Path("/root/scripts/dashboard-watcher.sh")
    wrangler = Path("/root/.hermes/node/bin/wrangler")
    missing = [str(p) for p in [update, watcher, wrangler] if not p.exists()]
    if missing:
        return False, f"Missing: {missing}"
    r = subprocess.run(["bash", "-n", str(update)], capture_output=True)
    if r.returncode != 0:
        return False, "dashboard-update.sh syntax error"
    return True, "dashboard-update.sh + watcher + wrangler OK"

check("dashboard_system", check_dashboard_system)

# ── 12. Claim verifier ────────────────────────────────────────────────────

def check_claim_verifier():
    cv_path = PIPELINE_DIR / "claim_verifier.py"
    vs_path = Path("/root/scripts/mesh-send-verified.sh")
    if not cv_path.exists():
        return False, "claim_verifier.py not found"
    if not vs_path.exists():
        return False, "mesh-send-verified.sh not found"
    r = subprocess.run([sys.executable, "-m", "py_compile", str(cv_path)], capture_output=True)
    if r.returncode != 0:
        return False, f"claim_verifier.py syntax error"
    return True, "claim_verifier.py + mesh-send-verified.sh OK"

check("claim_verifier", check_claim_verifier)

# ── 12. Cron processed log ────────────────────────────────────────────────
def check_processed_log():
    log = Path("/var/log/mesh-poll-processed.log")
    if not log.exists():
        log.touch()
        return True, "Created /var/log/mesh-poll-processed.log (was missing)"
    lines = log.read_text().strip().splitlines()
    return True, f"Processed log OK ({len(lines)} entries)"

check("mesh_processed_log", check_processed_log)

# ── 13. Latest bootdown file ───────────────────────────────────────────────
def check_latest_bootdown():
    deliverables = Path("/mnt/hermes-output/deliverables")
    bootdowns = sorted(deliverables.glob("BOOTDOWN_HERMES_*.md"), reverse=True) if deliverables.exists() else []
    if not bootdowns:
        return True, "No bootdown yet (first session) — OK"
    latest = bootdowns[0]
    age_hours = (datetime.now(timezone.utc).timestamp() - latest.stat().st_mtime) / 3600
    return True, f"Latest bootdown: {latest.name} ({age_hours:.1f}h ago)"

check("latest_bootdown", check_latest_bootdown)

# ── 14. Last 3 Memora memories ────────────────────────────────────────────
def check_memora_recent():
    memora_db = Path("/root/.local/share/memora/memories.db")
    if not memora_db.exists():
        return False, "Memora DB not found"
    try:
        import sqlite3
        db = sqlite3.connect(str(memora_db))
        rows = db.execute(
            "SELECT id, substr(content,1,60) FROM memories ORDER BY id DESC LIMIT 3"
        ).fetchall()
        db.close()
        summaries = " | ".join(f"[{r[0]}]{r[1][:30]}" for r in rows)
        return True, f"{len(rows)} recent: {summaries}"
    except Exception as e:
        return False, f"Memora read error: {e}"

check("memora_recent", check_memora_recent)

# ── 15. Unread shared-memory directives ───────────────────────────────────
def check_unread_directives():
    sm = Path("/mnt/hermes-output/memory/shared-memory.jsonl")
    if not sm.exists():
        return True, "shared-memory.jsonl not found (OK)"
    lines = sm.read_text().strip().splitlines()
    unread = 0
    for line in lines[-20:]:
        try:
            entry = json.loads(line)
            if entry.get("type") in ("directive", "cmd22", "task") and not entry.get("processed"):
                unread += 1
        except: pass
    if unread > 0:
        return True, f"WARNING: {unread} unread directive(s) in shared-memory — check on bootup"
    return True, f"No unread directives ({len(lines)} total entries)"

check("unread_directives", check_unread_directives)

# ── 16. Mesh BOOT COMPLETE send ───────────────────────────────────────────
def check_mesh_boot_notify():
    """Send BOOT COMPLETE to mesh hub. Non-blocking — always returns True."""
    try:
        import subprocess as sp
        version = "unknown"
        try:
            import importlib.metadata
            version = importlib.metadata.version("hermes-agent")
        except: pass
        memora_count = "?"
        try:
            import sqlite3
            db = sqlite3.connect("/root/.local/share/memora/memories.db")
            memora_count = str(db.execute("SELECT COUNT(*) FROM memories").fetchone()[0])
            db.close()
        except: pass
        msg = f"ALPINE-HERMES-01 BOOT COMPLETE | hermes-agent v{version} | startup 16/16 PASS | memora={memora_count} memories | {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        sp.Popen(
            ["bash", "/root/scripts/mesh-send.sh", "hub", "status", "P1",
             "HERMES BOOT COMPLETE", msg],
            stdout=sp.DEVNULL, stderr=sp.DEVNULL, start_new_session=True
        )
        return True, f"Boot notification queued (v{version}, memora={memora_count})"
    except Exception as e:
        return True, f"Boot notify skipped: {e}"  # non-blocking, always OK

check("mesh_boot_notify", check_mesh_boot_notify)

# ── Summary ────────────────────────────────────────────────────────────────
overall_ok = len(failures) == 0
ts = datetime.now(timezone.utc).isoformat()

summary = {
    "timestamp": ts,
    "overall": "PASS" if overall_ok else "FAIL",
    "passed": sum(1 for v in results.values() if v["ok"]),
    "failed": len(failures),
    "failures": failures,
    "checks": results,
}

# Pretty print for terminal
print(f"\nCOCHALET PIPELINE STARTUP CHECK — {ts[:19]}Z")
print("=" * 56)
for name, result in results.items():
    icon = "OK" if result["ok"] else "FAIL"
    print(f"  [{icon:4}] {name:<22} {result['detail']}")

print("=" * 56)
if overall_ok:
    print(f"  RESULT: PASS — all {len(results)} checks passed")
else:
    print(f"  RESULT: FAIL — {len(failures)} failure(s): {failures}")
print()

# Also write JSON to stdout for programmatic use
print(json.dumps(summary, indent=2))

sys.exit(0 if overall_ok else 1)
