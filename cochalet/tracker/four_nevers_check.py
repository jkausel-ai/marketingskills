#!/usr/bin/env python3
"""Scan markdown content for Four Nevers violations and gated terms."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BANNED_PATTERNS = [
    ("timeshare", re.compile(r"\btimeshare\b", re.IGNORECASE)),
    ("time-share", re.compile(r"\btime-share\b", re.IGNORECASE)),
    ("vacation ownership", re.compile(r"\bvacation ownership\b", re.IGNORECASE)),
    ("points system", re.compile(r"\bpoints system\b", re.IGNORECASE)),
    ("fractional ownership", re.compile(r"\bfractional ownership\b", re.IGNORECASE)),
    ("fractional", re.compile(r"\bfractional\b(?!\s+ownership)", re.IGNORECASE)),
    (
        "investment returns guaranteed",
        re.compile(r"\binvestment returns guaranteed\b", re.IGNORECASE),
    ),
    ("guaranteed returns", re.compile(r"\bguaranteed returns\b", re.IGNORECASE)),
    ("passive income", re.compile(r"\bpassive income\b", re.IGNORECASE)),
    ("Engine Room", re.compile(r"\bengine room\b", re.IGNORECASE)),
    ("best-in-class", re.compile(r"\bbest-in-class\b", re.IGNORECASE)),
    ("world-class", re.compile(r"\bworld-class\b", re.IGNORECASE)),
    ("cutting-edge", re.compile(r"\bcutting-edge\b", re.IGNORECASE)),
    ("next-gen", re.compile(r"\bnext-gen\b", re.IGNORECASE)),
]

GATED_PATTERNS = [
    ("$112,300", re.compile(r"\$112,300", re.IGNORECASE)),
    ("FO Stake", re.compile(r"\bfo stake\b", re.IGNORECASE)),
    ("NOI margin", re.compile(r"\bnoi margin\b", re.IGNORECASE)),
    ("DSCR", re.compile(r"\bdscr\b", re.IGNORECASE)),
    ("take rate", re.compile(r"\btake rate\b", re.IGNORECASE)),
    ("LTV:CAC", re.compile(r"\bltv:cac\b", re.IGNORECASE)),
]


def scan(content: str) -> dict[str, object]:
    violations = [label for label, pattern in BANNED_PATTERNS if pattern.search(content)]
    gated_terms = [label for label, pattern in GATED_PATTERNS if pattern.search(content)]
    return {
        "clean": not violations,
        "violations": violations,
        "gated_terms": gated_terms,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: four_nevers_check.py <markdown-file>", file=sys.stderr)
        return 2

    source = Path(argv[1]).expanduser()
    if not source.is_file():
        print(f"File not found: {source}", file=sys.stderr)
        return 2

    result = scan(source.read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2))
    return 0 if result["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
