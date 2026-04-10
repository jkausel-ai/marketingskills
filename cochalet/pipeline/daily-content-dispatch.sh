#!/bin/bash
# daily-content-dispatch.sh — CoChalet cron task dispatcher
# Runs at 6AM UTC daily via cron
# Reads today's task from 30-day calendar and runs full pipeline
# Cron entry: 0 6 * * * /mnt/hermes-output/cochalet-skills/cochalet/pipeline/daily-content-dispatch.sh >> /tmp/cochalet-cron.log 2>&1

set -euo pipefail

PIPELINE=/mnt/hermes-output/cochalet-skills/cochalet/pipeline
CALENDAR=/mnt/hermes-output/deliverables/2026-04-09-30day-calendar-SONNET.md
SHARED_MEM=/mnt/hermes-output/memory/shared-memory.jsonl
LOG=/tmp/cochalet-cron-$(date +%Y%m%d).log

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] CRON DISPATCH STARTING" | tee -a "$LOG"

# Get today's day number since calendar start (April 9 = day 1)
CALENDAR_START="2026-04-09"
TODAY=$(date -u +%Y-%m-%d)
START_EPOCH=$(date -d "$CALENDAR_START" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$CALENDAR_START" +%s)
TODAY_EPOCH=$(date -d "$TODAY" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$TODAY" +%s)
DAY_NUMBER=$(( (TODAY_EPOCH - START_EPOCH) / 86400 + 1 ))

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Calendar day: $DAY_NUMBER" | tee -a "$LOG"

# Extract today's task from calendar (social-content is the default cron skill)
TASK="run social-content skill for CoChalet, DW persona, bilingual FR/EN, calendar day $DAY_NUMBER"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Task: $TASK" | tee -a "$LOG"

# Run pipeline (gate check + dispatch)
python3 "$PIPELINE/pipeline_runner.py" run "$TASK" | tee -a "$LOG"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] CRON DISPATCH COMPLETE" | tee -a "$LOG"
