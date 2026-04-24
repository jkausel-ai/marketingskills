#!/usr/bin/env python3
"""
liveness_probe.py -- Zombie Task Watchdog for COS Pipeline
Phase 1+2 Foundation. Moved from Phase 6 per Gemini+Hermes consensus.

Scans SQLite task_state for tasks stuck in EXECUTE > TIMEOUT_SECONDS.
Forces BLOCKED + emits TIMEOUT_ENFORCED event to ledger.
Logs to shared-memory.jsonl for mesh visibility.

Run via cron: * * * * * python3 /mnt/hermes-output/cochalet-skills/cochalet/pipeline/liveness_probe.py
Or manually: python3 liveness_probe.py [--timeout 300] [--dry-run]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from task_ledger import TaskLedger, EventType, ConcurrencyError

STAGE_TIMEOUTS = {
    'GATE_CHECK': 120,
    'DISPATCH': 120,
    'EXECUTE': 300,
    'STAGING': 300,
    'VERIFY': 300,
    'PRODUCTION': 120,
}
SHARED_MEM = Path('/mnt/hermes-output/memory/shared-memory.jsonl')
DEFAULT_TIMEOUT = 300


def sweep_zombies(timeout: int = DEFAULT_TIMEOUT, dry_run: bool = False) -> dict:
    """Scan for stuck tasks and force them to BLOCKED."""
    ledger = TaskLedger()
    now = datetime.now(timezone.utc)
    zombies_found = 0
    zombies_slain = 0
    errors = []

    # Find all tasks in EXECUTE stage that are ACTIVE
    active_tasks_all = ledger.active_tasks()

    for task in active_tasks_all:
        task_id = task['task_id']
        last_updated = datetime.fromisoformat(
            task['last_updated'].replace('Z', '+00:00')
        )
        age_seconds = (now - last_updated).total_seconds()

        stage = task['current_stage']
        stage_timeout = STAGE_TIMEOUTS.get(stage)
        if stage_timeout is None:
            continue

        if age_seconds <= stage_timeout:
            continue

        zombies_found += 1
        print(f'[WATCHDOG] Zombie: {task_id} stuck {age_seconds:.0f}s '
              f'(threshold {timeout}s) v{task['version']}')

        if dry_run:
            print(f'  [DRY RUN] Would force BLOCKED')
            continue

        try:
            # Force EXECUTE -> EXECUTE_FAILED -> BLOCKED via FSM-valid path
            # First: EXECUTE -> EXECUTE_FAILED
            v = ledger.emit(
                task_id=task_id,
                event_type=EventType.EXECUTE_FAILED.value,
                current_stage='EXECUTE_FAILED',
                status='ACTIVE',
                expected_version=task['version'],
                data={
                    'error': f'Zombie timeout in {stage}: {age_seconds:.0f}s > {stage_timeout}s',
                    'watchdog': 'liveness_probe',
                },
            )
            # Then: EXECUTE_FAILED -> BLOCKED
            ledger.emit(
                task_id=task_id,
                event_type=EventType.TIMEOUT_ENFORCED.value,
                current_stage='BLOCKED',
                status='BLOCKED',
                expected_version=v,
                data={
                    'error': f'Forced BLOCKED by watchdog after {age_seconds:.0f}s in {stage}',
                    'timeout_threshold': stage_timeout,
                    'timed_out_stage': stage,
                },
            )

            # Broadcast to mesh
            mesh_entry = {
                'ts': now.isoformat(),
                'from': 'LivenessProbe',
                'type': 'blocked',
                'id': f'zombie-{task_id}',
                'content': f'ZOMBIE KILLED: {task_id} stuck in EXECUTE for '
                           f'{age_seconds:.0f}s. Forced BLOCKED.',
                'pipeline_stage': 'BLOCKED',
            }
            try:
                with open(SHARED_MEM, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(mesh_entry, ensure_ascii=False) + '\n')
            except Exception:
                pass  # Non-blocking

            zombies_slain += 1
            print(f'  [SLAIN] {task_id} -> BLOCKED')

        except ConcurrencyError as e:
            # Another process already updated this task -- skip
            print(f'  [SKIP] {task_id}: CAS conflict (another process handled it)')
            errors.append(f'{task_id}: {e}')
        except Exception as e:
            print(f'  [ERROR] {task_id}: {e}')
            errors.append(f'{task_id}: {e}')

    result = {
        'timestamp': now.isoformat(),
        'stage_timeouts': STAGE_TIMEOUTS,
        'active_tasks': len(active_tasks_all),
        'zombies_found': zombies_found,
        'zombies_slain': zombies_slain,
        'errors': errors,
        'dry_run': dry_run,
    }

    if zombies_found == 0:
        print(f'[WATCHDOG] Clean sweep. {len(active_tasks_all)} active in EXECUTE, none over {timeout}s.')
    else:
        print(f'[WATCHDOG] Sweep complete. Found {zombies_found}, slain {zombies_slain}.')

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='COS Pipeline Liveness Probe')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                        help=f'Zombie threshold in seconds (default {DEFAULT_TIMEOUT})')
    parser.add_argument('--dry-run', action='store_true',
                        help='Report zombies but do not kill them')
    args = parser.parse_args()

    result = sweep_zombies(timeout=args.timeout, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))
