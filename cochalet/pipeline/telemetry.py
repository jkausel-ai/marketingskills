#!/usr/bin/env python3
"""
telemetry.py -- Execution Telemetry for COS Pipeline
Phase 3 Intelligence. Queries SQLite ledger for aggregate analytics.

Usage:
  python3 telemetry.py summary     # Overall pipeline stats
  python3 telemetry.py by-model    # Per-model performance
  python3 telemetry.py by-skill    # Per-skill performance
  python3 telemetry.py cost-report  # Cost breakdown by model/dept/day
"""

import json
import sqlite3
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from statistics import mean

DB_PATH = Path('/var/lib/hermes/memory/orchestration_ledger.db')
TELEMETRY_EVENT = 'telemetry_execution'


@dataclass
class TelemetryRecord:
    task_id: str
    model: str
    skill: str
    department: str
    execution_time_ms: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    quality_score: int
    verify_passed: bool
    attempt: int
    timestamp: str


def _get_conn(read_only=True):
    if read_only:
        conn = sqlite3.connect(f'file:{DB_PATH}?mode=ro', uri=True, timeout=5)
    else:
        conn = sqlite3.connect(str(DB_PATH), timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


def record_execution(task_id, model, skill, department, execution_time_ms=0,
                     input_tokens=0, output_tokens=0, quality_score=0,
                     verify_passed=False, attempt=1):
    """Append a TelemetryRecord to the JSONL log."""
    rec = TelemetryRecord(
        task_id=task_id, model=model, skill=skill, department=department,
        execution_time_ms=execution_time_ms, input_tokens=input_tokens,
        output_tokens=output_tokens, estimated_cost_usd=0.0,
        quality_score=quality_score, verify_passed=verify_passed,
        attempt=attempt, timestamp=datetime.now(timezone.utc).isoformat(),
    )
    conn = _get_conn(read_only=False)
    try:
        conn.execute(
            """INSERT INTO task_events (task_id, timestamp, event_type,
                current_stage, model, attempt, delta_payload)
            VALUES (?, ?, ?, 'EXECUTE', ?, ?, ?)""",
            (task_id, rec.timestamp, TELEMETRY_EVENT, model, attempt,
             json.dumps(asdict(rec), ensure_ascii=False, sort_keys=True)),
        )
        conn.commit()
    finally:
        conn.close()


def aggregate_by_model(since_days=30):
    """Per-model: total_tasks, avg_quality, success_rate, avg_time_ms, total_tokens."""
    if not DB_PATH.exists():
        return {}
    conn = _get_conn()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=since_days)).isoformat()
        rows = conn.execute("""
            SELECT s.model, s.status,
                   COUNT(*) as cnt
            FROM task_state s
            WHERE s.created_at >= ?
            GROUP BY s.model, s.status
        """, (cutoff,)).fetchall()

        models = {}
        for r in rows:
            m = r['model'] or 'unknown'
            if m not in models:
                models[m] = {'total_tasks': 0, 'promoted': 0, 'blocked': 0}
            models[m]['total_tasks'] += r['cnt']
            if r['status'] == 'COMPLETED':
                models[m]['promoted'] += r['cnt']
            elif r['status'] == 'BLOCKED':
                models[m]['blocked'] += r['cnt']

        for m in models:
            t = models[m]['total_tasks']
            p = models[m]['promoted']
            models[m]['success_rate'] = round(p / t, 2) if t > 0 else 0.0

        return models
    finally:
        conn.close()


def aggregate_by_skill(since_days=30):
    """Per-skill: total_tasks, models_used, success_rate."""
    if not DB_PATH.exists():
        return {}
    conn = _get_conn()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=since_days)).isoformat()
        rows = conn.execute("""
            SELECT skill, model, status, COUNT(*) as cnt
            FROM task_state
            WHERE created_at >= ?
            GROUP BY skill, model, status
        """, (cutoff,)).fetchall()

        skills = {}
        for r in rows:
            sk = r['skill']
            if sk not in skills:
                skills[sk] = {'total_tasks': 0, 'promoted': 0, 'models_used': set()}
            skills[sk]['total_tasks'] += r['cnt']
            skills[sk]['models_used'].add(r['model'] or 'unknown')
            if r['status'] == 'COMPLETED':
                skills[sk]['promoted'] += r['cnt']

        for sk in skills:
            t = skills[sk]['total_tasks']
            p = skills[sk]['promoted']
            skills[sk]['success_rate'] = round(p / t, 2) if t > 0 else 0.0
            skills[sk]['models_used'] = list(skills[sk]['models_used'])

        return skills
    finally:
        conn.close()


def summary():
    """Overall pipeline stats."""
    if not DB_PATH.exists():
        return {'total_tasks': 0, 'promoted': 0, 'blocked': 0, 'active': 0,
                'total_events': 0, 'success_rate': 0.0}
    conn = _get_conn()
    try:
        total = conn.execute('SELECT COUNT(*) FROM task_state').fetchone()[0]
        promoted = conn.execute("SELECT COUNT(*) FROM task_state WHERE status='COMPLETED'").fetchone()[0]
        blocked = conn.execute("SELECT COUNT(*) FROM task_state WHERE status='BLOCKED'").fetchone()[0]
        active = conn.execute("SELECT COUNT(*) FROM task_state WHERE status='ACTIVE'").fetchone()[0]
        events = conn.execute('SELECT COUNT(*) FROM task_events').fetchone()[0]

        return {
            'total_tasks': total,
            'promoted': promoted,
            'blocked': blocked,
            'active': active,
            'total_events': events,
            'success_rate': round(promoted / total, 2) if total > 0 else 0.0,
        }
    finally:
        conn.close()



def cost_report(since_days=30):
    """Cost report: per-model spend from executor telemetry events."""
    if not DB_PATH.exists():
        return {'total_cost_usd': 0.0, 'by_model': {}, 'by_day': {}}
    conn = _get_conn()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=since_days)).isoformat()
        rows = conn.execute("""
            SELECT e.task_id, e.model, e.timestamp, e.delta_payload,
                   s.skill, s.department
            FROM task_events e
            LEFT JOIN task_state s ON e.task_id = s.task_id
            WHERE e.timestamp >= ?
              AND e.event_type IN ('execute_completed', 'telemetry_execution', 'staging_ready')
        """, (cutoff,)).fetchall()

        total_cost = 0.0
        total_in = 0
        total_out = 0
        by_model = {}
        by_day = {}
        by_dept = {}

        for r in rows:
            model = r['model'] or 'unknown'
            day = r['timestamp'][:10] if r['timestamp'] else 'unknown'
            dept = r['department'] or 'unknown'
            payload = {}
            if r['delta_payload']:
                try:
                    payload = json.loads(r['delta_payload'])
                except Exception:
                    pass

            in_tok = payload.get('input_tokens', 0)
            out_tok = payload.get('output_tokens', 0)
            cost = payload.get('estimated_cost_usd', 0.0)

            total_cost += cost
            total_in += in_tok
            total_out += out_tok

            if model not in by_model:
                by_model[model] = {'cost_usd': 0.0, 'input_tokens': 0, 'output_tokens': 0, 'tasks': 0}
            by_model[model]['cost_usd'] += cost
            by_model[model]['input_tokens'] += in_tok
            by_model[model]['output_tokens'] += out_tok
            by_model[model]['tasks'] += 1

            if day not in by_day:
                by_day[day] = {'cost_usd': 0.0, 'tasks': 0}
            by_day[day]['cost_usd'] += cost
            by_day[day]['tasks'] += 1

            if dept not in by_dept:
                by_dept[dept] = {'cost_usd': 0.0, 'tasks': 0}
            by_dept[dept]['cost_usd'] += cost
            by_dept[dept]['tasks'] += 1

        total_cost = round(total_cost, 4)
        for m in by_model:
            by_model[m]['cost_usd'] = round(by_model[m]['cost_usd'], 4)
        for d in by_day:
            by_day[d]['cost_usd'] = round(by_day[d]['cost_usd'], 4)
        for d in by_dept:
            by_dept[d]['cost_usd'] = round(by_dept[d]['cost_usd'], 4)

        return {
            'period_days': since_days,
            'total_cost_usd': total_cost,
            'total_input_tokens': total_in,
            'total_output_tokens': total_out,
            'by_model': dict(sorted(by_model.items(), key=lambda x: -x[1]['cost_usd'])),
            'by_day': dict(sorted(by_day.items())),
            'by_department': dict(sorted(by_dept.items(), key=lambda x: -x[1]['cost_usd'])),
        }
    finally:
        conn.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: telemetry.py [summary|by-model|by-skill]')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'summary':
        print('\nPIPELINE TELEMETRY SUMMARY')
        print('=' * 40)
        print(json.dumps(summary(), indent=2))
    elif cmd == 'by-model':
        print('\nPER-MODEL PERFORMANCE')
        print('=' * 50)
        data = aggregate_by_model()
        for model, stats in sorted(data.items()):
            print(f'\n  {model}:')
            for k, v in stats.items():
                print(f'    {k}: {v}')
    elif cmd == 'by-skill':
        print('\nPER-SKILL PERFORMANCE')
        print('=' * 50)
        data = aggregate_by_skill()
        for skill, stats in sorted(data.items()):
            print(f'\n  {skill}:')
            for k, v in stats.items():
                print(f'    {k}: {v}')
    elif cmd == 'cost-report':
        print('\nCOST REPORT')
        print('=' * 50)
        data = cost_report()
        print(f"  Period: last {data['period_days']} days")
        print(f"  Total cost: ${data['total_cost_usd']:.4f}")
        print(f"  Total tokens: {data['total_input_tokens']:,} in / {data['total_output_tokens']:,} out")
        if data['by_model']:
            print('\n  By Model:')
            for model, stats in data['by_model'].items():
                c = stats['cost_usd']
                t = stats['tasks']
                i = stats['input_tokens']
                o = stats['output_tokens']
                print(f"    {model}: ${c:.4f} ({t} tasks, {i:,}+{o:,} tokens)")
        if data.get('by_department'):
            print('\n  By Department:')
            for dept, stats in data['by_department'].items():
                print(f"    {dept}: ${stats['cost_usd']:.4f} ({stats['tasks']} tasks)")
        if data['by_day']:
            print('\n  By Day:')
            for day, stats in data['by_day'].items():
                print(f"    {day}: ${stats['cost_usd']:.4f} ({stats['tasks']} tasks)")
    else:
        print(f'Unknown: {cmd}')
        sys.exit(1)
