#!/bin/bash
# hermes-sonnet-swarm.sh -- direct Sonnet OAuth review swarm for Hermes.
# Runs outside the Gemini agent loop so quota/throttle on the driver cannot
# block review/optimization work.

set -euo pipefail

DELEGATE="${HERMES_SWARM_DELEGATE:-/root/claude-delegate.sh}"
OUT_DIR="${HERMES_SWARM_OUT_DIR:-/mnt/hermes-output/cmo-inbox/sonnet-swarm}"
SHARED_MEM="${HERMES_SHARED_MEM:-/mnt/hermes-output/memory/shared-memory.jsonl}"
TIMEOUT="${HERMES_SWARM_TIMEOUT:-900}"
MAX_FILE_CHARS="${HERMES_SWARM_MAX_FILE_CHARS:-50000}"

usage() {
  cat <<'USAGE'
Usage:
  hermes-sonnet-swarm.sh <task or file path>

Examples:
  hermes-sonnet-swarm.sh mobile-v2-wireframe.html
  hermes-sonnet-swarm.sh "Review /path/to/mobile-v2-wireframe.html for CMO/CRO/SEO/GTM feedback"
USAGE
}

if [ "$#" -lt 1 ]; then
  usage
  exit 2
fi

if [ ! -x "$DELEGATE" ]; then
  echo "DELEGATE_FAIL: missing executable delegate: $DELEGATE" >&2
  exit 1
fi

RAW_TASK="$*"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT_DIR"

slug="$(printf '%s' "$RAW_TASK" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9._-' '-' | sed 's/^-//; s/-$//' | cut -c1-64)"
[ -n "$slug" ] || slug="sonnet-swarm"
OUT_FILE="$OUT_DIR/${STAMP}-${slug}.md"
PROMPT_FILE="$(mktemp /tmp/hermes-sonnet-swarm-prompt-XXXXXX.md)"
RESULT_TMP="$(mktemp /tmp/hermes-sonnet-swarm-result-XXXXXX.md)"
trap 'rm -f "$PROMPT_FILE" "$RESULT_TMP"' EXIT

resolve_file() {
  local token="$1"
  if [ -f "$token" ]; then
    printf '%s\n' "$token"
    return 0
  fi
  if [[ "$token" != */* ]]; then
    find /mnt/hermes-output /root -maxdepth 8 -type f -name "$token" 2>/dev/null | head -1
  fi
}

{
  cat <<PROMPT
# SONNET OAUTH SWARM REVIEW

Gemini is only the driver/router. You are the Sonnet OAuth executor doing the real work.

Task/request:
$RAW_TASK

Run a practical org-marketing swarm review with these voices:

1. CMO / offer strategy
2. Product marketing / positioning
3. UX / mobile conversion flow
4. CRO / form and CTA optimization
5. SEO / discoverability and metadata
6. Paid acquisition / ad-message congruence
7. Growth-retention / onboarding and lifecycle
8. Sales-GTM / discovery-call and qualification handoff
9. Brand voice and compliance / Four Nevers

Output format:

## Executive Verdict
Short decision, top 3 leverage points, and risk level.

## Team Feedback
One section per role. Be specific, terse, and operational.

## Optimization Backlog
Prioritized table: P0/P1/P2, area, issue, recommendation, expected impact, owner.

## Copy / UX Patch Notes
Concrete proposed copy and interaction changes.

## Compliance Check
Call out Four Nevers, claims risk, securities/returns language, and any missing disclaimers.

## Final Next Actions
The 5 most useful next moves.

PROMPT

  printf '\n## Referenced Files\n\n'
  for token in "$@"; do
    file="$(resolve_file "$token" || true)"
    if [ -n "${file:-}" ] && [ -f "$file" ]; then
      printf '\n### %s\n\n```text\n' "$file"
      python3 - "$file" "$MAX_FILE_CHARS" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
limit = int(sys.argv[2])
text = path.read_text(encoding="utf-8", errors="ignore")
print(text[:limit])
if len(text) > limit:
    print(f"\n[TRUNCATED: {len(text) - limit} chars omitted]")
PY
      printf '\n```\n'
    fi
  done
} > "$PROMPT_FILE"

if ! timeout "$TIMEOUT" "$DELEGATE" "$PROMPT_FILE" > "$RESULT_TMP"; then
  code=$?
  {
    printf '# Sonnet Swarm Failed\n\n'
    printf '%s\n' "- Timestamp: \`$STAMP\`"
    printf '%s\n' "- Exit code: \`$code\`"
    printf '%s\n\n' "- Delegate: \`$DELEGATE\`"
    printf '## Task\n\n%s\n' "$RAW_TASK"
  } > "$OUT_FILE"
  echo "SONNET_SWARM_FAILED: $OUT_FILE" >&2
  exit "$code"
fi

{
  printf '# Sonnet OAuth Swarm Review\n\n'
  printf '%s\n' "- Timestamp: \`$STAMP\`"
  printf '%s\n' "- Delegate: \`$DELEGATE\`"
  printf '%s\n\n' "- Task: \`$RAW_TASK\`"
  cat "$RESULT_TMP"
} > "$OUT_FILE"

python3 - "$OUT_FILE" "$SHARED_MEM" "$RAW_TASK" <<'PY'
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

out_file = Path(sys.argv[1])
shared_mem = Path(sys.argv[2])
task = sys.argv[3]
entry = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "from": "Hermes",
    "type": "sonnet_swarm",
    "id": f"sonnet-swarm-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
    "content": f"SONNET_SWARM_COMPLETE: {task[:160]}",
    "file": str(out_file),
    "pipeline_stage": "SONNET_SWARM",
}
shared_mem.parent.mkdir(parents=True, exist_ok=True)
with shared_mem.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
PY

echo "SONNET_SWARM_COMPLETE: $OUT_FILE"
sed -n '1,90p' "$OUT_FILE"
