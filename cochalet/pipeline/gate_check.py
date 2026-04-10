#!/usr/bin/env python3
"""
gate_check.py — CoChalet Marketing Pipeline Stage 1: GATE CHECK
Validates a task string against Four Nevers + brand-voice-guard + scope check.
Returns JSON: {approved, violations, department, skill, model, task_clean}
Usage: python3 gate_check.py "write email sequence for DW persona"
       python3 gate_check.py --file /path/to/deliverable.md  (verify existing content)
       python3 gate_check.py --file /path/to/skill-file.md --type skill_definition

NOTE on skill definition files:
Skill definition files (cochalet/skills-adapted/*-cochalet.md) are META-DOCUMENTS.
They intentionally reference forbidden terms in prohibition context ("Never use timeshare").
Use --type skill_definition to skip Four Nevers scan on these files.
Four Nevers scan is ONLY for marketing OUTPUT (deliverables), not skill instruction files.
"""

import json
import sys
import re
import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = Path("/mnt/hermes-output/cochalet-skills/cochalet")
ROUTER_PATH = BASE / "config/skill-router.json"
GUARD_PATH  = BASE / "config/brand-voice-guard.json"

# ── Four Nevers (HARD REJECT — zero tolerance) ─────────────────────────────
FOUR_NEVERS = [
    (r"\btimeshare\b", "FOUR_NEVERS: 'timeshare' — use 'deeded co-ownership'"),
    (r"\bfractional ownership\b", "FOUR_NEVERS: 'fractional ownership' — use 'co-ownership'"),
    (r"\bguaranteed returns?\b", "FOUR_NEVERS: 'guaranteed returns' — use 'builds equity'"),
    (r"\bengine room\b", "FOUR_NEVERS: 'Engine Room' — use 'internal operations'"),
]

# ── Gated terms (WARN if in public-facing content, OK for internal) ─────────
GATED_TERMS = [
    r"\b112[,.]?300\b",         # FO Stake dollar amount
    r"\bFO Stake\b",
    r"\bNOI margin\b",
    r"\bDSCR\b",
    r"\btake rate\b",
    r"\bLTV:CAC\b",
    r"\bIRR\b",
    r"\bV31_14\b",
]

# ── Department routing keyword map ─────────────────────────────────────────
DEPT_ROUTING = {
    "dept-seo-content": [
        "seo", "pillar page", "schema markup", "site architecture",
        "programmatic seo", "ai seo", "search optimization", "keyword",
    ],
    "dept-cro": [
        "cro", "conversion", "landing page", "form", "popup", "a/b test",
        "ab test", "signup flow", "onboarding", "copy editing", "copy-editing",
    ],
    "dept-content-copy": [
        "copy", "email sequence", "email-sequence", "social content", "social post",
        "linkedin post", "caption", "cold email", "lead magnet", "copywriting",
        "blog post", "article", "newsletter",
    ],
    "dept-paid-measurement": [
        "paid ad", "facebook ad", "google ad", "ad creative", "analytics",
        "tracking", "utm", "attribution", "meta ad", "linkedin ad",
    ],
    "dept-growth-retention": [
        "referral", "community", "alpine circle", "fondateurs alpins",
        "churn", "retention", "renewal", "free tool", "calculator", "growth",
        "marketing ideas", "marketing-ideas",
    ],
    "dept-sales-gtm": [
        "revops", "revenue ops", "sales", "gtm", "go to market", "launch strategy",
        "pricing", "competitor", "discovery call", "pipeline", "battlecard",
        "sales enablement",
    ],
    "dept-strategy": [
        "strategy", "persona", "psychology", "positioning", "brand architecture",
        "insights", "editorial planning", "content strategy", "customer research",
        "marketing psychology",
    ],
}

# ── Skill routing (maps skill names to departments) ────────────────────────
SKILL_TO_DEPT = {
    "seo-audit": "dept-seo-content",
    "ai-seo": "dept-seo-content",
    "content-strategy": None,  # context-dependent — resolved by keywords
    "site-architecture": "dept-seo-content",
    "schema-markup": "dept-seo-content",
    "programmatic-seo": "dept-seo-content",
    "page-cro": "dept-cro",
    "signup-flow-cro": "dept-cro",
    "onboarding-cro": "dept-cro",
    "form-cro": "dept-cro",
    "popup-cro": "dept-cro",
    "ab-test-setup": None,  # context-dependent
    "copy-editing": "dept-cro",
    "copywriting": "dept-content-copy",
    "email-sequence": "dept-content-copy",
    "social-content": "dept-content-copy",
    "cold-email": "dept-content-copy",
    "lead-magnets": "dept-content-copy",
    "paid-ads": "dept-paid-measurement",
    "ad-creative": "dept-paid-measurement",
    "analytics-tracking": "dept-paid-measurement",
    "referral-program": "dept-growth-retention",
    "free-tool-strategy": "dept-growth-retention",
    "churn-prevention": "dept-growth-retention",
    "community-marketing": "dept-growth-retention",
    "marketing-ideas": None,  # context-dependent
    "revops": "dept-sales-gtm",
    "sales-enablement": "dept-sales-gtm",
    "launch-strategy": "dept-sales-gtm",
    "pricing-strategy": "dept-sales-gtm",
    "competitor-alternatives": "dept-sales-gtm",
    "customer-research": None,  # context-dependent
    "marketing-psychology": "dept-strategy",
    "product-marketing-context": "dept-strategy",
}


def load_router():
    """Load skill-router.json, return skills dict."""
    try:
        with open(ROUTER_PATH) as f:
            data = json.load(f)
        return data.get("skills", {})
    except Exception:
        return {}


def load_guard():
    """Load brand-voice-guard.json, return banned terms list."""
    try:
        with open(GUARD_PATH) as f:
            data = json.load(f)
        # Support both list format and {banned: [...]} format
        if isinstance(data, list):
            return data
        return data.get("banned", data.get("banned_terms", []))
    except Exception:
        return []


def scan_four_nevers(text: str) -> list:
    """Return list of Four Nevers violations found in text."""
    violations = []
    text_lower = text.lower()
    for pattern, message in FOUR_NEVERS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            violations.append({"type": "FOUR_NEVERS", "message": message, "pattern": pattern})
    return violations


def scan_gated_terms(text: str) -> list:
    """Return list of gated term warnings found in text."""
    warnings = []
    for pattern in GATED_TERMS:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append({"type": "GATED_TERM", "pattern": pattern,
                             "message": f"Gated term found: {pattern} — OK for internal, never in public content"})
    return warnings


def scan_banned_brand_terms(text: str, guard_terms: list) -> list:
    """Return list of banned brand voice terms found in text."""
    violations = []
    text_lower = text.lower()
    for term in guard_terms:
        if isinstance(term, str) and term.lower() in text_lower:
            violations.append({"type": "BRAND_VOICE", "term": term,
                               "message": f"Banned brand term: '{term}'"})
    return violations


def classify_department(task: str) -> str:
    """Route task to department based on keyword matching."""
    task_lower = task.lower()

    # First: check for explicit skill name in task
    for skill, dept in SKILL_TO_DEPT.items():
        if skill in task_lower and dept is not None:
            return dept

    # Second: keyword-based routing
    dept_scores = {}
    for dept, keywords in DEPT_ROUTING.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score > 0:
            dept_scores[dept] = score

    if dept_scores:
        return max(dept_scores, key=dept_scores.get)

    # Default to strategy for ambiguous tasks
    return "dept-strategy"


def identify_skill(task: str) -> str:
    """Best-guess skill identification from task string."""
    task_lower = task.lower()
    # Direct skill name match
    for skill in SKILL_TO_DEPT.keys():
        if skill.replace("-", " ") in task_lower or skill in task_lower:
            return skill
    # Keyword fallbacks
    if "email" in task_lower:
        return "email-sequence"
    if "social" in task_lower or "linkedin" in task_lower or "instagram" in task_lower:
        return "social-content"
    if "copy" in task_lower and "ad" not in task_lower:
        return "copywriting"
    if "ad" in task_lower or "paid" in task_lower:
        return "paid-ads"
    if "seo" in task_lower:
        return "seo-audit"
    return "content-strategy"  # safe default


def get_model_for_skill(skill: str, router_skills: dict) -> str:
    """Look up assigned model for a skill from skill-router.json."""
    skill_data = router_skills.get(skill, {})
    return skill_data.get("model", "deepseek-chat")


def gate_check(task: str, mode: str = "task") -> dict:
    """
    Run full gate check on a task string or deliverable content.
    mode: "task" (pre-execution check) | "content" (post-execution verify)
    Returns dict with: approved, violations, warnings, department, skill, model
    """
    router_skills = load_router()
    guard_terms = load_guard()

    # Run all scans
    four_nevers_violations = scan_four_nevers(task)
    gated_warnings = scan_gated_terms(task)
    brand_violations = scan_banned_brand_terms(task, guard_terms)

    # Hard violations = Four Nevers + brand voice banned terms
    hard_violations = four_nevers_violations + brand_violations

    # Classification (always run regardless of violations)
    department = classify_department(task)
    skill = identify_skill(task)
    model = get_model_for_skill(skill, router_skills)

    approved = len(hard_violations) == 0

    result = {
        "approved": approved,
        "mode": mode,
        "violations": hard_violations,
        "warnings": gated_warnings,
        "violation_count": len(hard_violations),
        "warning_count": len(gated_warnings),
        "department": department,
        "skill": skill,
        "model": model,
        "task_preview": task[:100] + "..." if len(task) > 100 else task,
    }

    return result


def check_deliverable_file(filepath: str) -> dict:
    """Run gate check on an existing deliverable file."""
    path = Path(filepath)
    if not path.exists():
        return {"approved": False, "error": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8", errors="ignore")
    result = gate_check(content, mode="content")
    result["file"] = str(path)
    result["file_size_bytes"] = path.stat().st_size

    # Check quality score in header
    score_match = re.search(r"##\s*Quality Score:\s*(\d+)/10", content)
    if score_match:
        score = int(score_match.group(1))
        result["quality_score"] = score
        result["quality_pass"] = score >= 7
        if score < 7:
            result["violations"].append({
                "type": "QUALITY_GATE",
                "message": f"Quality score {score}/10 is below 7/10 threshold"
            })
            result["approved"] = False
    else:
        result["quality_score"] = None
        result["quality_pass"] = None

    # Check canon context applied
    result["canon_applied"] = "Canon Context: APPLIED" in content or "HERMES_KNOWLEDGE_BASE" in content

    # Check TUNING GAPS section present
    result["tuning_gaps_present"] = "## TUNING GAPS" in content

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gate_check.py 'task description'")
        print("       python3 gate_check.py --file /path/to/deliverable.md")
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Error: --file requires a path argument")
            sys.exit(1)
        # Check for --type skill_definition flag
        file_type = "content"
        if "--type" in sys.argv:
            type_idx = sys.argv.index("--type")
            if type_idx + 1 < len(sys.argv):
                file_type = sys.argv[type_idx + 1]
        result = check_deliverable_file(sys.argv[2])
        if file_type == "skill_definition":
            # Skill definition files: suppress Four Nevers violations (they reference terms in prohibition context)
            result["violations"] = [v for v in result.get("violations", []) if v.get("type") != "FOUR_NEVERS"]
            result["violation_count"] = len(result["violations"])
            result["approved"] = len(result["violations"]) == 0
            result["note"] = "SKILL_DEFINITION mode: Four Nevers scan suppressed (meta-document)"
    else:
        task = " ".join(sys.argv[1:])
        result = gate_check(task)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Exit code: 0 = approved, 1 = rejected
    sys.exit(0 if result.get("approved", False) else 1)


if __name__ == "__main__":
    main()
