#!/bin/bash
# HERMES heartbeat writer v1.2 — 2026-04-21
OUT_DIR="/root/Hermes/comms-out"
mkdir -p "$OUT_DIR"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
UPTIME=$(uptime | sed "s/^ *//")
LOAD=$(uptime | awk -F"load average:" "{print \$2}" | tr -d " ")

# Cron health — thresholds tuned per cadence
# liveness-probe runs every minute (stale > 3 min = unhealthy)
# gemini-enforcer runs every minute (stale > 3 min = unhealthy)
# dashboard-refresh runs every hour at :15 (stale > 75 min = unhealthy)
CRON_HEALTHY=true
check_age() {
  local log="$1"; local max_min="$2"
  if [ -f "$log" ]; then
    local age=$(( ($(date +%s) - $(stat -c %Y "$log")) / 60 ))
    [ "$age" -gt "$max_min" ] && return 1
  fi
  return 0
}
check_age /var/log/liveness-probe.log 3 || CRON_HEALTHY=false
check_age /var/log/gemini-enforcer.log 3 || CRON_HEALTHY=false
check_age /var/log/dashboard-refresh.log 75 || CRON_HEALTHY=false

# Pipeline stats via task_ledger (robust parse to single-line JSON)
PIPELINE_STATS=$(python3 /mnt/hermes-output/cochalet-skills/cochalet/pipeline/task_ledger.py stats 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in (\"total\",\"by_stage\",\"execution_logs\") if k in d}))" 2>/dev/null || echo "{}")

# Deliverables today. Count live deliverables only; CMO rescue archives and
# backups are operational files and would otherwise spike dashboard metrics.
DELIVERABLES_TODAY=$(find /mnt/hermes-output/deliverables -type f -newermt "$(date +%Y-%m-%d)" \
  -not -path "*__pycache__*" \
  -not -path "*/.git/*" \
  -not -path "*/cmo-blocked-rescue-backups/*" \
  -not -path "*/cmo-resolved/*" \
  -not -path "*/cmo-rejected/*" \
  2>/dev/null | wc -l | tr -d " ")

# V2 iterations lifetime + today (from v2_alignment_tracking.jsonl)
V2_LIFETIME=0
V2_TODAY=0
if [ -f /mnt/hermes-output/v2_alignment_tracking.jsonl ]; then
  V2_LIFETIME=$(grep -c "thesis_version.*v2" /mnt/hermes-output/v2_alignment_tracking.jsonl 2>/dev/null || true)
  V2_TODAY=$(grep "$(date +%Y-%m-%d)" /mnt/hermes-output/v2_alignment_tracking.jsonl 2>/dev/null | grep -c "thesis_version.*v2" || true)
  V2_LIFETIME=${V2_LIFETIME:-0}
  V2_TODAY=${V2_TODAY:-0}
fi

# Cost today from cost_tracking.jsonl
COST_TODAY=$(python3 -c "
import json
try:
    total=0.0
    with open(\"/mnt/hermes-output/cost_tracking.jsonl\") as f:
        today=\"$(date +%Y-%m-%d)\"
        for line in f:
            try:
                e=json.loads(line)
                if e.get(\"ts\",\"\").startswith(today):
                    total += float(e.get(\"cost_usd\",0))
            except: pass
    print(round(total,6))
except: print(0)
")

# Write HB JSONL (single-line)
cat > "$OUT_DIR/HERMES.jsonl.new" << JSONL_EOF
{"terminal":"HERMES","event":"heartbeat","ts":"$TS","node":"vps","load":"$LOAD","crons_healthy":$CRON_HEALTHY,"deliverables_today":$DELIVERABLES_TODAY,"v2_iterations_today":$V2_TODAY,"v2_iterations_lifetime":$V2_LIFETIME,"cost_today_usd":$COST_TODAY,"pipeline":$PIPELINE_STATS}
JSONL_EOF
cat "$OUT_DIR/HERMES.jsonl.new" >> "$OUT_DIR/HERMES.jsonl"
rm -f "$OUT_DIR/HERMES.jsonl.new"

# Write status snapshot JSON
cat > "$OUT_DIR/HERMES.json" << JSON_EOF
{
  "ts": "$TS",
  "uptime": "$UPTIME",
  "load": "$LOAD",
  "crons_healthy": $CRON_HEALTHY,
  "deliverables_today": $DELIVERABLES_TODAY,
  "v2_iterations_today": $V2_TODAY,
  "v2_iterations_lifetime": $V2_LIFETIME,
  "cost_today_usd": $COST_TODAY,
  "pipeline": $PIPELINE_STATS,
  "callsign": "HERMES-VPS-CRUISE-$(date +%d)"
}
JSON_EOF

# Bound JSONL to last 2000 lines
if [ "$(wc -l < "$OUT_DIR/HERMES.jsonl")" -gt 2000 ]; then
  tail -2000 "$OUT_DIR/HERMES.jsonl" > "$OUT_DIR/HERMES.jsonl.tmp"
  mv "$OUT_DIR/HERMES.jsonl.tmp" "$OUT_DIR/HERMES.jsonl"
fi
