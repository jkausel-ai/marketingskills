#!/usr/bin/env python3
"""
dispatcher.py — CoChalet Marketing Pipeline Stage 2: DISPATCH
Assembles the full prompt (canon context + skill prompt + task brief)
and writes a dispatch payload JSON ready for delegate_task execution.

Usage: python3 dispatcher.py '{"approved": true, "skill": "email-sequence", "department": "dept-content-copy", "model": "gpt-oss-120b"}' "write DW nurture email sequence FR"
       python3 dispatcher.py --gate-output /tmp/gate_result.json "write DW nurture email sequence FR"
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

# ── Model Router (failover chain) ──────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
try:
    from model_router import ModelRouter
    _model_router = ModelRouter()
except Exception as _mr_err:
    _model_router = None
    print(f"[dispatcher] WARNING: model_router unavailable — {_mr_err}", file=sys.stderr)

# ── Paths ──────────────────────────────────────────────────────────────────
BASE          = Path("/mnt/hermes-output/cochalet-skills/cochalet")
KB_V2_PATH    = Path("/mnt/hermes-output/HERMES_KNOWLEDGE_BASE_V2.md")
ADAPTED_DIR   = BASE / "skills-adapted"
AGENTS_DIR    = BASE / "agents"
DELIVERABLES  = Path("/mnt/hermes-output/deliverables")
SHARED_MEM    = Path("/mnt/hermes-output/memory/shared-memory.jsonl")


def read_canon_context(lines: int = 80) -> str:
    """Read first N lines of KB V2 as canon context block."""
    if not KB_V2_PATH.exists():
        return "# CANON CONTEXT UNAVAILABLE — KB V2 not found at expected path"
    with open(KB_V2_PATH, encoding="utf-8") as f:
        all_lines = f.readlines()
    return "".join(all_lines[:lines])


def read_skill_prompt(skill: str) -> str:
    """Read the CoChalet-adapted skill prompt. Fall back to note if not found."""
    adapted_path = ADAPTED_DIR / f"{skill}-cochalet.md"
    if adapted_path.exists():
        return adapted_path.read_text(encoding="utf-8")
    # Check generic skill
    generic_path = BASE.parent / "skills" / skill / "SKILL.md"
    if generic_path.exists():
        return f"[WARNING: Using generic skill prompt — no CoChalet adaptation exists yet]\n\n" + \
               generic_path.read_text(encoding="utf-8")
    return f"[SKILL PROMPT NOT FOUND: {skill}]\nExecute this skill based on CoChalet context only."


def read_agent_context(department: str) -> str:
    """Read the department AGENT.md for context injection."""
    agent_path = AGENTS_DIR / department / "AGENT.md"
    if agent_path.exists():
        return agent_path.read_text(encoding="utf-8")
    return f"[AGENT.md not found for {department}]"


def build_output_path(department: str, skill: str, model: str) -> Path:
    """Construct the STAGING output file path."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    model_tag = model.split("/")[-1].upper().replace("-", "").replace(".", "")[:12]
    filename = f"{today}-{skill}-STAGING-{model_tag}.md"
    dept_dir = DELIVERABLES / department
    dept_dir.mkdir(parents=True, exist_ok=True)
    return dept_dir / filename


def assemble_prompt(gate_result: dict, task_brief: str) -> dict:
    """
    Assemble the full prompt for the department agent.
    Returns a dispatch payload dict.
    """
    skill      = gate_result.get("skill", "content-strategy")
    department = gate_result.get("department", "dept-strategy")
    # Use model_router failover chain — override gate_result model with healthy selection
    if _model_router is not None:
        task_brief_str = task_brief if isinstance(task_brief, str) else str(task_brief)
        model = _model_router.get_model(skill, task=task_brief_str)
    else:
        model = gate_result.get("model", "deepseek/deepseek-chat")

    # Read components
    canon_context  = read_canon_context(80)
    skill_prompt   = read_skill_prompt(skill)
    agent_context  = read_agent_context(department)
    output_path    = build_output_path(department, skill, model)

    # Detect persona and language from task brief
    task_lower = task_brief.lower()
    persona   = "DW" if "dw" in task_lower or "deep worker" in task_lower else \
                "PC" if "pc" in task_lower or "propriétaires" in task_lower else "Both"
    language  = "FR" if " fr" in task_lower or "french" in task_lower or "français" in task_lower else \
                "EN" if " en" in task_lower or "english" in task_lower else "Bilingual"

    # Build the full assembled prompt
    full_prompt = f"""# COCHALET MARKETING TASK — PIPELINE DISPATCH
**Department:** {department}
**Skill:** {skill}
**Model:** {model}
**Persona:** {persona}
**Language:** {language}
**Output path:** {output_path}
**Pipeline stage:** STAGING

---

## SECTION A — CANON CONTEXT (DO NOT SKIP — prepended mandatory)

{canon_context}

---

## SECTION B — DEPARTMENT AGENT CONTEXT

{agent_context}

---

## SECTION C — SKILL PROMPT (CoChalet-adapted)

{skill_prompt}

---

## SECTION D — TASK BRIEF

{task_brief}

---

## REQUIRED OUTPUT FORMAT

Begin your deliverable with this header (fill in all fields):

```
## Quality Score: [X]/10
## Canon Context: APPLIED
## Model: {model}
## Department: {department}
## Skill: {skill}
## Persona: {persona}
## Language: {language}
## Pipeline Stage: STAGING
## Output Path: {output_path}
```

Then write your deliverable content.

End your deliverable with:
```
## TUNING GAPS
[List what context was missing or what assumptions you made]
```

Write the complete deliverable to: **{output_path}**

Four Nevers compliance is mandatory. If you are about to write "timeshare," "fractional ownership," "guaranteed returns," or "Engine Room" — stop and use the approved alternative.
"""

    dispatch_payload = {
        "task_id": f"{skill}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "skill": skill,
        "department": department,
        "model": model,
        "persona": persona,
        "language": language,
        "output_path": str(output_path),
        "assembled_prompt": full_prompt,
        "canon_lines_used": 80,
        "adapted_prompt_used": (ADAPTED_DIR / f"{skill}-cochalet.md").exists(),
        "pipeline_stage": "DISPATCH",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return dispatch_payload


def log_dispatch(payload: dict):
    """Append dispatch event to shared-memory.jsonl."""
    entry = {
        "ts": payload["timestamp"],
        "from": "Hermes",
        "type": "dispatch",
        "id": payload["task_id"],
        "content": f"DISPATCH: {payload['skill']} → {payload['department']} | model: {payload['model']} | persona: {payload['persona']}",
        "output_path": payload["output_path"],
        "pipeline_stage": "DISPATCH",
    }
    try:
        with open(SHARED_MEM, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[WARNING] Could not write to shared-memory.jsonl: {e}", file=sys.stderr)


def save_payload(payload: dict, output_file: str = None):
    """Save dispatch payload to a temp JSON file for pipeline_runner.py to consume."""
    if output_file is None:
        output_file = f"/tmp/cochalet-dispatch-{payload['task_id']}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return output_file


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 dispatcher.py '<gate_result_json>' 'task brief'")
        print("       python3 dispatcher.py --gate-output /tmp/gate.json 'task brief'")
        sys.exit(1)

    if sys.argv[1] == "--gate-output":
        with open(sys.argv[2]) as f:
            gate_result = json.load(f)
        task_brief = " ".join(sys.argv[3:])
    else:
        gate_result = json.loads(sys.argv[1])
        task_brief = " ".join(sys.argv[2:])

    if not gate_result.get("approved", False):
        print(json.dumps({
            "error": "Cannot dispatch — gate check not approved",
            "violations": gate_result.get("violations", [])
        }, indent=2))
        sys.exit(1)

    payload = assemble_prompt(gate_result, task_brief)
    log_dispatch(payload)
    output_file = save_payload(payload)

    print(json.dumps({
        "status": "DISPATCH_READY",
        "task_id": payload["task_id"],
        "skill": payload["skill"],
        "department": payload["department"],
        "model": payload["model"],
        "output_path": payload["output_path"],
        "payload_file": output_file,
        "adapted_prompt_used": payload["adapted_prompt_used"],
        "next_step": f"Run department agent with payload from {output_file}, then pipeline_runner.py verify",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
