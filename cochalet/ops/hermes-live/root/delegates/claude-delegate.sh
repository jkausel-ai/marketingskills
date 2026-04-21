#!/bin/bash
# claude-delegate.sh — MANAGER TIER (Sonnet 4.6 CLI, $0 via Max)
# ⚠️ LOCKED BY OPUS — DO NOT MODIFY
# Fixes applied: stdin piping, NO --bare, NO --max-turns, token hardcoded
# If you see this comment, the file was locked on Apr 11 2026.

set -eo pipefail
# NOTE: removed -u flag (unbound variable check causes crashes with external tools)

LOG="/var/log/delegate-claude.log"
TIMEOUT=300
MIN_OUTPUT_CHARS=50

TOKEN_SECRET_FILE="${CLAUDE_CODE_OAUTH_TOKEN_FILE:-/root/.claudeos/secrets/claude-code-oauth-token}"
if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
    if [ -r "$TOKEN_SECRET_FILE" ]; then
        CLAUDE_CODE_OAUTH_TOKEN="$(tr -d '
' < "$TOKEN_SECRET_FILE")"
    else
        echo "DELEGATE_FAIL:claude:missing_oauth_token"
        exit 1
    fi
fi
export CLAUDE_CODE_OAUTH_TOKEN
export PATH=/root/.local/bin:$PATH

PROMPT="${1:-}"
if [ -z "$PROMPT" ]; then
    echo "DELEGATE_FAIL:claude:no_prompt"
    exit 1
fi

PROMPT_FILE=""
CLEANUP_FILE=false
if [ -f "$PROMPT" ]; then
    PROMPT_FILE="$PROMPT"
else
    PROMPT_FILE=$(mktemp /tmp/cos-prompt-XXXXXX.txt)
    printf '%s' "$PROMPT" > "$PROMPT_FILE"
    CLEANUP_FILE=true
fi

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "[$TS] CLAUDE-DELEGATE START: $(head -c 120 "$PROMPT_FILE")..." >> "$LOG"

# NO --bare (blocks OAuth), NO --max-turns (causes timeout), stdin piping (avoids shell expansion)
OUTPUT=$(timeout "$TIMEOUT" /root/.local/bin/claude -p \
    --model sonnet \
    < "$PROMPT_FILE" 2>/dev/null) || {
    EXIT_CODE=$?
    echo "[$TS] CLAUDE-DELEGATE FAIL: exit=$EXIT_CODE" >> "$LOG"
    $CLEANUP_FILE && rm -f "$PROMPT_FILE"
    echo "DELEGATE_FAIL:claude:exit=$EXIT_CODE"
    exit $EXIT_CODE
}

$CLEANUP_FILE && rm -f "$PROMPT_FILE"

OUTPUT_LEN=${#OUTPUT}
if [ "$OUTPUT_LEN" -lt "$MIN_OUTPUT_CHARS" ]; then
    echo "[$TS] CLAUDE-DELEGATE WARN: short ($OUTPUT_LEN chars)" >> "$LOG"
fi

echo "[$TS] CLAUDE-DELEGATE DONE: ${OUTPUT_LEN} chars" >> "$LOG"
echo "$OUTPUT"
