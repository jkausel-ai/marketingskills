#!/usr/bin/env python3
"""
claim_verifier.py — Hermes Reporting Integrity Enforcer
Pipeline stage: PRE-MESH-SEND gate

Classifies factual claims before they reach the mesh or TG.
Enforces: only OBSERVED or VERIFIED claims may be sent as authoritative facts.
INFERRED claims are automatically prefixed [UNVERIFIED] if sent without verification.

CLAIM TAXONOMY:
  OBSERVED  — agent ran a tool THIS turn, output IS the claim (direct evidence)
  VERIFIED  — agent ran a specific verification command THIS turn confirming claim
  INFERRED  — derived from: user message, prior session, another agent's report
  ASSUMED   — no supporting evidence — BLOCKED from authoritative mesh sends

Usage (CLI):
  python3 claim_verifier.py verify-file /path/to/file "N1 violations removed"
  python3 claim_verifier.py verify-cmd "grep -c pattern file" --expected 0
  python3 claim_verifier.py classify "files are deployed"
  python3 claim_verifier.py audit-report "Full status report body"

Usage (Python):
  from claim_verifier import ClaimVerifier
  cv = ClaimVerifier()
  result = cv.verify_file_exists("/path/to/file")
  result = cv.verify_grep_count("/path/file", "pattern", expected=0)
  result = cv.verify_cmd("ls -la /path/", expect_exit=0)
  safe_body = cv.annotate_body("files are deployed", claim_type="INFERRED")
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_PATH = Path("/var/log/hermes-claim-verifier.log")


@dataclass
class ClaimResult:
    verified: bool
    claim_type: str          # OBSERVED | VERIFIED | INFERRED | ASSUMED | BLOCKED
    evidence: str            # What command/check confirmed it
    value: Optional[str]     # Actual value found
    expected: Optional[str]  # What was expected
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "verified": self.verified,
            "claim_type": self.claim_type,
            "evidence": self.evidence,
            "value": self.value,
            "expected": self.expected,
            "error": self.error,
            "timestamp": self.timestamp,
        }

    def annotation(self) -> str:
        """Return prefix for mesh body based on claim type."""
        if self.verified:
            return f"[VERIFIED: {self.evidence}]"
        return f"[UNVERIFIED — {self.claim_type}: not confirmed this turn]"


def _log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}\n"
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line)
    except Exception:
        pass


# ── Inferred-claim pattern detector ──────────────────────────────────────
# Phrases that signal a claim is INFERRED rather than directly observed.
INFERRED_SIGNALS = [
    r"\byou (said|told|mentioned|confirmed|reported)\b",
    r"\bTG (session|message|comms?)\b",
    r"\banother (session|agent|instance)\b",
    r"\bprevious (session|turn|message)\b",
    r"\baccording to\b",
    r"\bshould (be|have)\b",
    r"\bI (believe|think|assume)\b",
    r"\bprobably\b",
    r"\blikely\b",
]

ASSUMED_SIGNALS = [
    r"\bshould be fine\b",
    r"\bpresumably\b",
    r"\bI imagine\b",
    r"\bI expect\b",
]


class ClaimVerifier:
    """
    Verify factual claims before reporting them on mesh or TG.

    Best practice — call before every mesh-send about external state:
      cv = ClaimVerifier()
      r = cv.verify_file_exists("/path/to/file")
      if r.verified:
          send_mesh("file exists")
      else:
          send_mesh(f"[UNVERIFIED] file may exist — not confirmed this turn")
    """

    def verify_file_exists(self, path: str) -> ClaimResult:
        """Verify a file exists and optionally has expected size."""
        p = Path(path)
        exists = p.exists() and p.is_file()
        size = p.stat().st_size if exists else None
        result = ClaimResult(
            verified=exists,
            claim_type="VERIFIED" if exists else "FAILED",
            evidence=f"Path.exists() + is_file() on {path}",
            value=f"{size} bytes" if size else "NOT FOUND",
            expected="file exists",
            error=None if exists else f"File not found: {path}",
        )
        _log(f"verify_file_exists({path}): {result.claim_type} | {result.value}")
        return result

    def verify_grep_count(self, path: str, pattern: str, expected: int = 0,
                          flags: str = "") -> ClaimResult:
        """
        Verify grep count matches expected value.
        Default: expected=0 (pattern NOT found = clean).
        """
        try:
            cmd = ["grep", "-c"]
            if flags:
                cmd.extend(flags.split())
            cmd.extend([pattern, path])
            result = subprocess.run(cmd, capture_output=True, text=True)
            count = int(result.stdout.strip() or "0")
            verified = count == expected
            return ClaimResult(
                verified=verified,
                claim_type="VERIFIED" if verified else "FAILED",
                evidence=f"grep -c '{pattern}' {path} → {count}",
                value=str(count),
                expected=str(expected),
                error=None if verified else f"Expected {expected}, found {count}",
            )
        except Exception as e:
            return ClaimResult(
                verified=False, claim_type="ERROR",
                evidence=f"grep_count failed: {e}",
                value=None, expected=str(expected), error=str(e),
            )

    def verify_cmd(self, cmd: str, expect_exit: int = 0,
                   expect_in_output: Optional[str] = None) -> ClaimResult:
        """
        Run a shell command and verify its exit code / output.
        Use for: ls, diff, md5sum, wc, systemctl is-active, etc.
        """
        try:
            import shlex as _shlex
            _ALLOWED_CMDS = frozenset({"grep", "ls", "diff", "md5sum", "wc", "systemctl", "cat", "head", "tail", "test", "stat"})
            argv = _shlex.split(cmd)
            if argv[0] not in _ALLOWED_CMDS:
                return ClaimResult(
                    verified=False, claim_type="BLOCKED",
                    evidence=f"Command not in allowlist: {argv[0]}",
                    value=None, expected=f"exit={expect_exit}",
                    error=f"Blocked command: {argv[0]}",
                )
            result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
            exit_ok = (result.returncode == expect_exit)
            output = (result.stdout + result.stderr).strip()
            content_ok = True
            if expect_in_output:
                content_ok = expect_in_output in output
            verified = exit_ok and content_ok
            return ClaimResult(
                verified=verified,
                claim_type="VERIFIED" if verified else "FAILED",
                evidence=f"cmd: {cmd[:60]} | exit={result.returncode} | out={output[:80]}",
                value=output[:120],
                expected=f"exit={expect_exit}" + (f" contains='{expect_in_output}'" if expect_in_output else ""),
                error=None if verified else f"exit={result.returncode}, content_ok={content_ok}",
            )
        except subprocess.TimeoutExpired:
            return ClaimResult(
                verified=False, claim_type="TIMEOUT",
                evidence=f"cmd timed out: {cmd[:60]}",
                value=None, expected=f"exit={expect_exit}", error="Timeout after 15s",
            )
        except Exception as e:
            return ClaimResult(
                verified=False, claim_type="ERROR",
                evidence=f"cmd failed: {e}",
                value=None, expected=f"exit={expect_exit}", error=str(e),
            )

    def verify_file_content(self, path: str, must_contain: list[str],
                            must_not_contain: list[str] = None) -> ClaimResult:
        """
        Verify file contains required strings and/or lacks forbidden strings.
        Used for: Four Nevers check, IRR figure check, deployed content verification.
        """
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return ClaimResult(
                verified=False, claim_type="ERROR",
                evidence=f"Could not read {path}", value=None,
                expected="readable file", error=str(e),
            )

        missing = [s for s in must_contain if s not in content]
        present_forbidden = [s for s in (must_not_contain or []) if s in content]
        verified = not missing and not present_forbidden

        evidence_parts = []
        if must_contain:
            evidence_parts.append(f"required present: {[s for s in must_contain if s in content]}")
        if must_not_contain:
            evidence_parts.append(f"forbidden absent: {len(must_not_contain) - len(present_forbidden)}/{len(must_not_contain)}")

        return ClaimResult(
            verified=verified,
            claim_type="VERIFIED" if verified else "FAILED",
            evidence=" | ".join(evidence_parts) or f"content check on {path}",
            value=f"missing={missing}, forbidden_found={present_forbidden}",
            expected=f"must_contain={must_contain}, must_not_contain={must_not_contain}",
            error=None if verified else f"Missing: {missing}. Forbidden found: {present_forbidden}",
        )

    def classify_text(self, text: str) -> str:
        """
        Classify a claim text as OBSERVED/INFERRED/ASSUMED based on language patterns.
        Used to auto-detect when an agent is about to report an unverified claim.
        """
        text_lower = text.lower()
        for pattern in ASSUMED_SIGNALS:
            if re.search(pattern, text_lower):
                return "ASSUMED"
        for pattern in INFERRED_SIGNALS:
            if re.search(pattern, text_lower):
                return "INFERRED"
        return "OBSERVED"  # default — assume direct unless signals found

    def annotate_body(self, body: str, claim_type: Optional[str] = None,
                      evidence: Optional[str] = None) -> str:
        """
        Annotate a mesh message body with verification status.
        Call before every mesh-send about external state.
        """
        if claim_type is None:
            claim_type = self.classify_text(body)

        if claim_type in ("OBSERVED", "VERIFIED"):
            prefix = f"[{claim_type}"
            if evidence:
                prefix += f": {evidence}"
            prefix += "] "
            return prefix + body
        elif claim_type == "ASSUMED":
            _log(f"BLOCKED ASSUMED CLAIM: {body[:80]}")
            return f"[UNVERIFIED — ASSUMED, not sent as fact] {body}"
        else:  # INFERRED
            _log(f"INFERRED CLAIM flagged: {body[:80]}")
            return f"[UNVERIFIED — INFERRED from external source, not confirmed this turn] {body}"

    def batch_verify_deployment(self, verifications: list[dict]) -> dict:
        """
        Run multiple verifications and return summary.
        Each verification: {type, path, pattern, expected, description}
        Used by mesh-send-verified.sh before sending deployment reports.
        """
        results = []
        all_pass = True
        for v in verifications:
            vtype = v.get("type", "file_exists")
            desc = v.get("description", "check")
            if vtype == "file_exists":
                r = self.verify_file_exists(v["path"])
            elif vtype == "grep_count":
                r = self.verify_grep_count(v["path"], v["pattern"],
                                           expected=v.get("expected", 0))
            elif vtype == "file_content":
                r = self.verify_file_content(v["path"],
                                             v.get("must_contain", []),
                                             v.get("must_not_contain", []))
            elif vtype == "cmd":
                r = self.verify_cmd(v["cmd"],
                                    expect_exit=v.get("expect_exit", 0),
                                    expect_in_output=v.get("expect_in_output"))
            else:
                r = ClaimResult(verified=False, claim_type="UNKNOWN",
                                evidence=f"Unknown type: {vtype}",
                                value=None, expected=None, error=f"Unknown type: {vtype}")
            if not r.verified:
                all_pass = False
            results.append({"description": desc, **r.to_dict()})

        return {
            "all_verified": all_pass,
            "passed": sum(1 for r in results if r["verified"]),
            "failed": sum(1 for r in results if not r["verified"]),
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ── CLI interface ──────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  claim_verifier.py verify-file /path/to/file")
        print("  claim_verifier.py verify-grep /path pattern [expected_count]")
        print("  claim_verifier.py verify-cmd 'shell command'")
        print("  claim_verifier.py classify 'claim text to classify'")
        print("  claim_verifier.py annotate 'body text' [INFERRED|VERIFIED]")
        sys.exit(1)

    cv = ClaimVerifier()
    cmd = sys.argv[1]

    if cmd == "verify-file":
        r = cv.verify_file_exists(sys.argv[2])
        print(json.dumps(r.to_dict(), indent=2))
        sys.exit(0 if r.verified else 1)

    elif cmd == "verify-grep":
        path = sys.argv[2]
        pattern = sys.argv[3]
        expected = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        r = cv.verify_grep_count(path, pattern, expected=expected)
        print(json.dumps(r.to_dict(), indent=2))
        sys.exit(0 if r.verified else 1)

    elif cmd == "verify-cmd":
        r = cv.verify_cmd(" ".join(sys.argv[2:]))
        print(json.dumps(r.to_dict(), indent=2))
        sys.exit(0 if r.verified else 1)

    elif cmd == "classify":
        text = " ".join(sys.argv[2:])
        claim_type = cv.classify_text(text)
        print(json.dumps({"text": text[:100], "claim_type": claim_type}, indent=2))

    elif cmd == "annotate":
        text = sys.argv[2]
        claim_type = sys.argv[3] if len(sys.argv) > 3 else None
        annotated = cv.annotate_body(text, claim_type=claim_type)
        print(annotated)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
