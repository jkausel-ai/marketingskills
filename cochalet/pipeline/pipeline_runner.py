#!/usr/bin/env python3
"""
pipeline_runner.py — CoChalet Marketing Pipeline Orchestrator
Stages 1-5: GATE CHECK → DISPATCH → STAGING → VERIFY → PRODUCTION

Usage:
  Full pipeline (new task):
    python3 pipeline_runner.py run "write DW email sequence FR"

  Verify existing staged file:
    python3 pipeline_runner.py verify /path/to/STAGING-file.md

  Promote verified file to production:
    python3 pipeline_runner.py promote /path/to/STAGING-file.md

  Check pipeline status:
    python3 pipeline_runner.py status
"""

import json
import sys
import os
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timezone

# ── Model Router (failover chain) ──────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
try:
    from model_router import ModelRouter
    _model_router = ModelRouter()
except Exception as _mr_err:
    _model_router = None
    print(f"[pipeline_runner] WARNING: model_router unavailable — {_mr_err}", file=sys.stderr)

# ── Paths ──────────────────────────────────────────────────────────────────
BASE          = Path("/mnt/hermes-output/cochalet-skills/cochalet")
PIPELINE_DIR  = BASE / "pipeline"
FOUR_NEVERS   = BASE / "tracker/four_nevers_check.py"
AGGREGATE     = BASE / "tracker/aggregate.py"
GUARD_PATH    = BASE / "config/brand-voice-guard.json"
ITERATIONS    = Path("/mnt/hermes-output/memory/iterations")
SHARED_MEM    = Path("/mnt/hermes-output/memory/shared-memory.jsonl")
DELIVERABLES  = Path("/mnt/hermes-output/deliverables")

# ── Pattern 3: CMO Meta-Prompt ─────────────────────────────────────────────
CMO_META_PROMPT = """
You are the CoChalet CMO Coordinator. Customize the skill prompt template for this specific task.
TASK: {task}
SKILL TEMPLATE (excerpt): {template_excerpt}
DEPT EXPERTISE (recent): {expertise_excerpt}
Rules: Output improved prompt only. No explanation. Add task-specific context: persona (DW/PC), language (FR/EN), urgency, format. Max 200 words added. Do not remove Four Nevers rules. If template already fits perfectly, output exactly: TEMPLATE_OK
"""


# ── Model Router helpers ───────────────────────────────────────────────────

def get_dispatch_model(skill: str, task: str = "") -> str:
    """Return the best available model for a dispatch, with failover."""
    if _model_router is not None:
        return _model_router.get_model(skill, task=task)
    return "deepseek/deepseek-chat"


def get_verify_model() -> str:
    """Return the best available model for verify/patch stage."""
    if _model_router is not None:
        return _model_router.get_model("verify_patch", chain_override="verify_patch")
    return "anthropic/claude-sonnet-4-6"


def get_fallback_model(failed_model: str, skill: str = "") -> str:
    """Record a model failure and return the next in chain."""
    if _model_router is not None:
        return _model_router.next_fallback(failed_model, skill=skill)
    return "meta-llama/llama-3.3-70b-instruct:free"


# ── Stage 1: GATE CHECK ────────────────────────────────────────────────────

def run_gate_check(task: str) -> dict:
    """Run gate_check.py on task string. Returns parsed result dict."""
    gate_script = PIPELINE_DIR / "gate_check.py"
    try:
        result = subprocess.run(
            [sys.executable, str(gate_script), task],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {"approved": False, "error": str(e), "violations": [{"type": "SYSTEM", "message": str(e)}]}


# ── Pattern 3: CMO Prompt Engineer ─────────────────────────────────────────

def cmo_prompt_engineer(gate_result: dict, task: str) -> str:
    """CMO rewrites skill prompt for this specific task. Falls back to raw template on any error."""
    skill = gate_result.get('skill', '')
    dept = gate_result.get('department', '')
    # Read template
    template = ""
    adapted_path = BASE / f"skills-adapted/{skill}-cochalet.md"
    if adapted_path.exists():
        template = adapted_path.read_text(encoding='utf-8')[:2000]
    # Read expertise
    expertise = ""
    exp_path = BASE / f"agents/{dept}/expertise.md"
    if exp_path.exists():
        raw = exp_path.read_text(encoding='utf-8')
        expertise = raw[-500:] if len(raw) > 500 else raw
    if not template:
        return template
    meta_prompt = CMO_META_PROMPT.format(
        task=task,
        template_excerpt=template[:1500],
        expertise_excerpt=expertise or 'No prior executions yet.'
    )
    try:
        import requests, subprocess as sp
        key = sp.run(['bash', '-c', "grep 'OPENROUTER_API_KEY' /root/.hermes/.env | cut -d= -f2 | tr -d '\"'"],
                     capture_output=True, text=True).stdout.strip()
        resp = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            json={'model': 'nvidia/nemotron-3-super-120b-a12b:free',
                  'messages': [{'role': 'user', 'content': meta_prompt}],
                  'max_tokens': 400, 'temperature': 0.3},
            timeout=15)
        result = resp.json()['choices'][0]['message']['content'].strip()
        if 'TEMPLATE_OK' in result:
            return template
        return result
    except Exception as e:
        print(f'[cmo_prompt_engineer] fallback to raw template: {e}', file=sys.stderr)
        return template


# ── Pattern 4: Parallel Dispatch for P0 Tasks ──────────────────────────────

def parallel_dispatch_p0(prompt: str, task: str) -> dict:
    """For P0 tasks: dispatch to 2 models in parallel, return winner."""
    import threading, requests, subprocess as sp
    key = sp.run(['bash', '-c', "grep 'OPENROUTER_API_KEY' /root/.hermes/.env | cut -d= -f2 | tr -d '\"'"],
                 capture_output=True, text=True).stdout.strip()
    models = {
        'gemma':    'google/gemma-4-31b-it',
        'nemotron': 'nvidia/nemotron-3-super-120b-a12b:free',
    }
    results = {}
    def run_model(name, slug):
        try:
            r = requests.post('https://openrouter.ai/api/v1/chat/completions',
                headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
                json={'model': slug, 'messages': [{'role': 'user', 'content': prompt}],
                      'max_tokens': 700, 'temperature': 0.7},
                timeout=60)
            results[name] = r.json()['choices'][0]['message']['content']
        except Exception as e:
            results[name] = f'ERROR: {e}'
    threads = [threading.Thread(target=run_model, args=(n, s)) for n, s in models.items()]
    for t in threads: t.start()
    for t in threads: t.join(timeout=65)
    # Pick winner: fewer violations + longer output
    def score(txt):
        bad = sum(1 for term in ['timeshare', 'fractional ownership', 'guaranteed return'] if term in txt.lower())
        return len(txt) - (bad * 500)
    winner = max(results, key=lambda k: score(results.get(k, '')))
    loser = [k for k in results if k != winner][0] if len(results) > 1 else None
    return {
        'winner': winner,
        'winner_output': results.get(winner, ''),
        'loser': loser,
        'loser_output': results.get(loser, '') if loser else '',
        'all': results
    }


# ── Stage 2: DISPATCH ──────────────────────────────────────────────────────

def run_dispatch(gate_result: dict, task: str) -> dict:
    """Run dispatcher.py to assemble prompt. Returns payload dict."""
    dispatch_script = PIPELINE_DIR / "dispatcher.py"
    gate_json = json.dumps(gate_result)
    try:
        result = subprocess.run(
            [sys.executable, str(dispatch_script), gate_json, task],
            capture_output=True, text=True, timeout=30
        )
        dispatch_result = json.loads(result.stdout)
        # Load full payload from file
        payload_file = dispatch_result.get("payload_file")
        if payload_file and Path(payload_file).exists():
            with open(payload_file) as f:
                payload = json.load(f)
            # Pattern 3: if CMO engineered prompt available, override skill_prompt
            if gate_result.get('engineered_prompt'):
                payload['skill_prompt'] = gate_result['engineered_prompt']
                payload['cmo_engineered'] = True
            dispatch_result["payload"] = payload
        return dispatch_result
    except Exception as e:
        return {"status": "DISPATCH_FAILED", "error": str(e)}


# ── Stage 4: VERIFY ────────────────────────────────────────────────────────

def load_guard_terms() -> list:
    """Load banned terms from brand-voice-guard.json."""
    try:
        with open(GUARD_PATH) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return data.get("banned", data.get("banned_terms", []))
    except Exception:
        return []


def run_four_nevers_check(filepath: str) -> dict:
    """Run four_nevers_check.py on a deliverable file."""
    if not FOUR_NEVERS.exists():
        # Fallback: inline check
        return inline_four_nevers_check(filepath)
    try:
        result = subprocess.run(
            [sys.executable, str(FOUR_NEVERS), filepath],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        clean = result.returncode == 0 and "clean" in output.lower()
        return {
            "clean": clean,
            "exit_code": result.returncode,
            "output": output[:500],
        }
    except Exception as e:
        return {"clean": False, "error": str(e)}


def inline_four_nevers_check(filepath: str) -> dict:
    """Inline Four Nevers check when four_nevers_check.py is unavailable."""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore").lower()
    except Exception as e:
        return {"clean": False, "error": f"Could not read file: {e}"}

    violations = []
    patterns = [
        (r"\btimeshare\b", "timeshare"),
        (r"\bfractional ownership\b", "fractional ownership"),
        (r"\bguaranteed returns?\b", "guaranteed returns"),
        (r"\bengine room\b", "Engine Room"),
    ]
    for pattern, term in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(term)

    return {
        "clean": len(violations) == 0,
        "violations": violations,
        "source": "inline_check",
    }


def check_quality_score(filepath: str) -> dict:
    """Parse quality score from deliverable header."""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"score": None, "pass": False}

    match = re.search(r"##\s*Quality Score:\s*(\d+)/10", content)
    if match:
        score = int(match.group(1))
        return {"score": score, "pass": score >= 7}
    return {"score": None, "pass": None, "warning": "No quality score found in header"}


def check_structure(filepath: str) -> dict:
    """Check deliverable has required structural elements."""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"valid": False}

    checks = {
        "has_quality_score":  bool(re.search(r"## Quality Score:", content)),
        "has_canon_applied":  "Canon Context: APPLIED" in content or "HERMES_KNOWLEDGE_BASE" in content,
        "has_tuning_gaps":    "## TUNING GAPS" in content,
        "has_pipeline_stage": "Pipeline Stage:" in content,
        "min_content_size":   len(content) >= 1000,
    }
    checks["valid"] = all(checks.values())
    return checks


def verify_deliverable(filepath: str, retry_count: int = 0) -> dict:
    """Full VERIFY stage: Four Nevers + brand voice + quality + structure."""
    path = Path(filepath)
    if not path.exists():
        return {"passed": False, "error": f"File not found: {filepath}"}

    # Run all checks
    four_nevers_result = run_four_nevers_check(filepath)
    quality_result     = check_quality_score(filepath)
    structure_result   = check_structure(filepath)
    guard_terms        = load_guard_terms()

    # Brand voice scan
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        content = ""
    brand_violations = [t for t in guard_terms if isinstance(t, str) and t.lower() in content.lower()]

    # Collect all failures
    failures = []
    if not four_nevers_result.get("clean", False):
        failures.append(f"FOUR_NEVERS: {four_nevers_result.get('violations', four_nevers_result.get('output', '?'))}")
    if quality_result.get("pass") is False:
        score = quality_result.get("score", "?")
        failures.append(f"QUALITY_GATE: score {score}/10 < 7/10 threshold")
    if not structure_result.get("valid", True):
        missing = [k for k, v in structure_result.items() if not v and k != "valid"]
        failures.append(f"STRUCTURE: missing {missing}")
    if brand_violations:
        failures.append(f"BRAND_VOICE: banned terms found: {brand_violations[:5]}")

    passed = len(failures) == 0

    return {
        "passed": passed,
        "filepath": str(filepath),
        "retry_count": retry_count,
        "four_nevers": four_nevers_result,
        "quality": quality_result,
        "structure": structure_result,
        "brand_violations": brand_violations[:10],
        "failures": failures,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ── Stage 5: PRODUCTION PROMOTE ────────────────────────────────────────────

def promote_to_production(staged_path: str, dispatch_payload: dict = None) -> dict:
    """Rename STAGING → PROD, write execution log, trigger aggregate, update shared-memory."""
    path = Path(staged_path)
    if not path.exists():
        return {"success": False, "error": f"Staged file not found: {staged_path}"}

    # Rename file
    prod_path = Path(str(path).replace("-STAGING-", "-PROD-"))
    if "-STAGING-" not in path.name:
        prod_path = path.parent / path.name.replace("STAGING", "PROD")
    shutil.move(str(path), str(prod_path))

    # Extract metadata from filename + content
    content = prod_path.read_text(encoding="utf-8", errors="ignore")
    skill = dispatch_payload.get("skill", "unknown") if dispatch_payload else extract_from_content(content, "Skill")
    model = dispatch_payload.get("model", "unknown") if dispatch_payload else extract_from_content(content, "Model")
    dept  = dispatch_payload.get("department", "unknown") if dispatch_payload else extract_from_content(content, "Department")

    # Write execution log
    timestamp = datetime.now(timezone.utc)
    log_name = timestamp.strftime("%Y%m%d_%H%M%S") + f"-{skill}.json"
    ITERATIONS.mkdir(parents=True, exist_ok=True)
    log_path = ITERATIONS / log_name

    word_count = len(content.split())
    quality_match = re.search(r"## Quality Score:\s*(\d+)/10", content)
    quality_score = int(quality_match.group(1)) if quality_match else None

    execution_log = {
        "timestamp": timestamp.isoformat(),
        "skill": skill,
        "model": model,
        "duration_seconds": 0,  # Not tracked in this implementation
        "output_file": str(prod_path),
        "output_word_count": word_count,
        "pipeline_stage": "PRODUCTION",
        "four_nevers_self_check": True,
        "canon_prepended": "Canon Context: APPLIED" in content,
        "retry_count": 0,
        "error": None,
    }
    if quality_score:
        execution_log["quality_score"] = quality_score

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(execution_log, f, indent=2, ensure_ascii=False)

    # Trigger aggregate.py
    if AGGREGATE.exists():
        try:
            subprocess.run([sys.executable, str(AGGREGATE)], capture_output=True, timeout=60)
        except Exception:
            pass  # Non-blocking — aggregate failure doesn't block production

    # Trigger dashboard update (non-blocking background process)
    dashboard_update = Path("/root/scripts/dashboard-update.sh")
    if dashboard_update.exists():
        try:
            subprocess.Popen(
                ["bash", str(dashboard_update), "--reason", f"pipeline-promote:{skill}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception:
            pass  # Non-blocking — dashboard failure never blocks production

    # Update shared-memory.jsonl
    summary_match = re.search(r"^## (.+?)$", content, re.MULTILINE)
    summary = summary_match.group(1) if summary_match else f"{skill} deliverable produced"
    sm_entry = {
        "ts": timestamp.isoformat(),
        "from": "Hermes",
        "type": "deliverable",
        "id": f"{skill}-{timestamp.strftime('%Y%m%d')}",
        "content": f"PRODUCTION: {summary}",
        "file": str(prod_path),
        "pipeline_stage": "PRODUCTION",
        "skill": skill,
        "model": model,
    }
    try:
        with open(SHARED_MEM, "a", encoding="utf-8") as f:
            f.write(json.dumps(sm_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        pass  # Non-blocking

    # Append to dept expertise file
    dept = dispatch_payload.get("department", "") if dispatch_payload else ""
    skill_exp = dispatch_payload.get("skill", "") if dispatch_payload else skill
    model_exp = dispatch_payload.get("model", "") if dispatch_payload else model
    if dept and skill_exp:
        append_expertise(dept, skill_exp, model_exp, quality_score)

    return {
        "success": True,
        "staged_path": staged_path,
        "prod_path": str(prod_path),
        "execution_log": str(log_path),
        "word_count": word_count,
        "quality_score": quality_score,
        "skill": skill,
        "model": model,
    }


def extract_from_content(content: str, field: str) -> str:
    """Extract a field value from deliverable header."""
    match = re.search(rf"##\s*{field}:\s*(.+?)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "unknown"


def append_expertise(dept: str, skill: str, model: str, score, what_worked: str = "", what_failed: str = "", insight: str = ""):
    """Append a learning block to the dept's expertise.md after each execution."""
    from datetime import datetime, timezone
    expertise_path = Path(f"/mnt/hermes-output/cochalet-skills/cochalet/agents/{dept}/expertise.md")
    if not expertise_path.parent.exists():
        return
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    score_str = f"{score}/10" if score else "not scored"
    block = f"""
## [{date_str}] Skill: {skill} | Score: {score_str} | Model: {model}
**What worked:** {what_worked or 'Execution completed — qualitative review pending'}
**What failed / needed patching:** {what_failed or 'None noted'}
**CoChalet insight:** {insight or 'Review deliverable for patterns to capture here'}
---
"""
    with open(expertise_path, "a", encoding="utf-8") as f:
        f.write(block)


def mark_blocked(filepath: str, failures: list):
    """Rename to BLOCKED and log to shared-memory."""
    path = Path(filepath)
    blocked_path = path.parent / path.name.replace("-STAGING-", "-BLOCKED-").replace("STAGING", "BLOCKED")
    if path.exists():
        shutil.move(str(path), str(blocked_path))

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "from": "Hermes",
        "type": "blocked",
        "id": f"blocked-{path.stem}-{datetime.now(timezone.utc).strftime('%H%M%S')}",
        "content": f"BLOCKED at VERIFY (attempt 3). Failures: {failures}. CMO review required.",
        "file": str(blocked_path),
        "pipeline_stage": "BLOCKED",
    }
    try:
        with open(SHARED_MEM, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return str(blocked_path)


# ── Status check ──────────────────────────────────────────────────────────

def check_status() -> dict:
    """Scan deliverables/ for STAGING and BLOCKED files."""
    staging = list(DELIVERABLES.rglob("*STAGING*.md"))
    blocked = list(DELIVERABLES.rglob("*BLOCKED*.md"))
    production = list(DELIVERABLES.rglob("*PROD*.md"))
    iterations = list(ITERATIONS.glob("*.json")) if ITERATIONS.exists() else []

    return {
        "staging_count": len(staging),
        "blocked_count": len(blocked),
        "production_count": len(production),
        "execution_logs": len(iterations),
        "staging_files": [str(p) for p in staging],
        "blocked_files": [str(p) for p in blocked],
        "recent_production": [str(p) for p in sorted(production, key=os.path.getmtime, reverse=True)[:5]],
    }


# ── Full pipeline runner ───────────────────────────────────────────────────

def run_full_pipeline(task: str) -> dict:
    """
    Execute the full 5-stage pipeline for a task string.
    Stages 3 (STAGING execution) requires a human agent or delegate_task — 
    this function runs stages 1, 2, and 4+5 after staging is complete.
    """
    print(f"\n{'='*60}")
    print(f"COCHALET PIPELINE STARTING")
    print(f"Task: {task[:80]}...")
    print(f"{'='*60}\n")

    # Stage 1: GATE CHECK
    print("[1/5] GATE CHECK...")
    gate_result = run_gate_check(task)
    if not gate_result.get("approved", False):
        print(f"  ✗ GATE REJECTED: {[v['message'] for v in gate_result.get('violations', [])]}")
        return {"status": "GATE_REJECTED", "gate_result": gate_result}
    # Override gate_result model with failover-aware selection
    gate_result["model"] = get_dispatch_model(gate_result.get("skill", ""), task=task)
    print(f"  ✓ Approved → {gate_result['department']} | skill: {gate_result['skill']} | model: {gate_result['model']} (router-selected)")

    # CMO Prompt Engineering (Pattern 3)
    print('  [2.5] CMO PROMPT ENGINEERING...')
    engineered_prompt = cmo_prompt_engineer(gate_result, task)
    if engineered_prompt:
        gate_result['engineered_prompt'] = engineered_prompt
        print(f'  CMO prompt: {len(engineered_prompt)} chars')

    # Stage 2: DISPATCH
    print("[2/5] DISPATCH — assembling prompt...")
    dispatch_result = run_dispatch(gate_result, task)
    if dispatch_result.get("status") != "DISPATCH_READY":
        print(f"  ✗ DISPATCH FAILED: {dispatch_result.get('error')}")
        return {"status": "DISPATCH_FAILED", "dispatch_result": dispatch_result}

    payload = dispatch_result.get("payload", {})
    output_path = dispatch_result.get("output_path")
    print(f"  ✓ Prompt assembled → output: {output_path}")
    print(f"  → Adapted prompt used: {dispatch_result.get('adapted_prompt_used')}")

    # P0 parallel dispatch check (Pattern 4)
    is_p0 = any(kw in task.lower() for kw in ['investor', 'p0', 'production-final', 'monday', 'justin presentation'])
    if is_p0:
        full_prompt = payload.get('prompt', '') if payload else ''
        if full_prompt:
            print('  [P0] Parallel dispatch: gemma + nemotron')
            parallel_result = parallel_dispatch_p0(full_prompt, task)
            print(f"  Winner: {parallel_result['winner']}")
            gate_result['p0_parallel_result'] = {
                'winner': parallel_result['winner'],
                'winner_length': len(parallel_result['winner_output']),
                'loser': parallel_result['loser'],
            }

    # Stage 3: STAGING (requires external agent execution)
    print("\n[3/5] STAGING — requires department agent execution")
    print(f"  → Department agent: {gate_result['department']}")
    print(f"  → Model: {gate_result['model']}")
    print(f"  → Output path: {output_path}")
    print(f"  → Dispatch payload: {dispatch_result.get('payload_file')}")
    print(f"\n  ⟳ Waiting for staged output at: {output_path}")
    print(f"  (Run department agent with the assembled prompt from payload file)")
    print(f"  (Then run: python3 pipeline_runner.py verify {output_path})\n")

    return {
        "status": "AWAITING_STAGING",
        "gate_result": gate_result,
        "dispatch_result": dispatch_result,
        "output_path": output_path,
        "next_command": f"python3 {PIPELINE_DIR}/pipeline_runner.py verify {output_path}",
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "run":
        task = " ".join(sys.argv[2:])
        result = run_full_pipeline(task)
        print(json.dumps({k: v for k, v in result.items() if k != "payload"}, indent=2, ensure_ascii=False))

    elif command == "verify":
        if len(sys.argv) < 3:
            print("Usage: pipeline_runner.py verify /path/to/STAGING-file.md")
            sys.exit(1)
        filepath = sys.argv[2]
        print(f"\n[4/5] VERIFY — {filepath}")
        result = verify_deliverable(filepath, retry_count=0)

        if result["passed"]:
            print(f"  ✓ VERIFY PASSED — quality: {result['quality'].get('score')}/10")
            print(f"  → Run: python3 pipeline_runner.py promote {filepath}")
        else:
            print(f"  ✗ VERIFY FAILED: {result['failures']}")
            print(f"  → Retry count: {result['retry_count']}")
            failures_str = str(result['failures'])
            # Determine fix suggestion based on failure type
            if "no quality score" in failures_str.lower() or "quality score" in failures_str.lower() and "score" not in failures_str.lower().replace("quality score",""):
                fix_suggestion = "Add ## Quality Score: X/10 header"
            elif "four_nevers" in failures_str.lower() or "FOUR_NEVERS" in failures_str:
                fix_suggestion = "Avoid all forbidden terms (timeshare, fractional ownership, guaranteed returns)"
            else:
                fix_suggestion = "Improve brand voice, emotional resonance, and specificity"
            score_val = result['quality'].get('score', '?')
            retry_prefix = f"PREVIOUS ATTEMPT FAILED (score {score_val}/10). Weakness: {failures_str}. On this attempt, specifically address: {fix_suggestion}."
            if result['retry_count'] < 2:
                print(f"  → Auto-patch with sonnet-hermes required, then re-verify")
                print(f"  → Retry note: {retry_prefix}")
            else:
                blocked = mark_blocked(filepath, result['failures'])
                print(f"  ✗ BLOCKED after 3 attempts → {blocked}")
                print(f"  → CMO review required — check shared-memory.jsonl")

        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "promote":
        if len(sys.argv) < 3:
            print("Usage: pipeline_runner.py promote /path/to/STAGING-file.md")
            sys.exit(1)
        filepath = sys.argv[2]
        print(f"\n[5/5] PRODUCTION PROMOTE — {filepath}")

        # Final verify before promotion
        verify_result = verify_deliverable(filepath)
        if not verify_result["passed"]:
            print(f"  ✗ Cannot promote — verify failed: {verify_result['failures']}")
            sys.exit(1)

        result = promote_to_production(filepath)
        if result["success"]:
            print(f"  ✓ PRODUCTION PROMOTED")
            print(f"  → Production file: {result['prod_path']}")
            print(f"  → Execution log: {result['execution_log']}")
            print(f"  → Word count: {result['word_count']}")
            print(f"  → Quality score: {result.get('quality_score')}/10")
        else:
            print(f"  ✗ PROMOTION FAILED: {result.get('error')}")

        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "status":
        result = check_status()
        print("\nCOCHALET PIPELINE STATUS")
        print(f"  Staging:    {result['staging_count']} files")
        print(f"  Blocked:    {result['blocked_count']} files")
        print(f"  Production: {result['production_count']} files")
        print(f"  Exec logs:  {result['execution_logs']}")
        if result['blocked_files']:
            print(f"\n  ⚠ BLOCKED (CMO review needed):")
            for f in result['blocked_files']:
                print(f"    {f}")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
