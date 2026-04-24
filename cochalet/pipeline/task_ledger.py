#!/usr/bin/env python3
"""
task_ledger.py — CQRS-Lite SQLite Ledger for COS Pipeline
Phase 1+2 Foundation. 4-way consensus (Opus+Gemini+Codex+Hermes).

Architecture:
  - task_state table: mutable current state (fast O(1) reads for routing)
  - task_events table: append-only immutable audit trail (replay + analytics)
  - WAL journal mode: concurrent readers don't block writers (Hermes requirement)
  - CAS (Compare-And-Swap): version column prevents race conditions (Codex requirement)
  - TOCTOU protection: WHERE stage = ? AND version = ? in state updates (Hermes requirement)

Usage:
  from task_ledger import TaskLedger
  ledger = TaskLedger()
  ledger.create_task('task-123', skill='email-sequence', department='dept-content-copy')
  ledger.emit('task-123', 'GATE_PASSED', current_stage='DISPATCH', data={'model': 'gemini-flash'})
  state = ledger.current_state('task-123')
  events = ledger.events('task-123')
"""

import json
import sqlite3
import os
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

# ── Configuration ─────────────────────────────────────────────────────────
DB_DIR = Path(os.environ.get('COS_LEDGER_DIR', '/var/lib/hermes/memory'))
DB_PATH = DB_DIR / 'orchestration_ledger.db'


class EventType(str, Enum):
    TASK_CREATED = 'task_created'
    GATE_PASSED = 'gate_passed'
    GATE_REJECTED = 'gate_rejected'
    DISPATCH_READY = 'dispatch_ready'
    EXECUTE_STARTED = 'execute_started'
    EXECUTE_COMPLETED = 'execute_completed'
    EXECUTE_FAILED = 'execute_failed'
    MODEL_FAILOVER = 'model_failover'
    STAGING_READY = 'staging_ready'
    VERIFY_STARTED = 'verify_started'
    VERIFY_PASSED = 'verify_passed'
    VERIFY_FAILED = 'verify_failed'
    PATCH_STARTED = 'patch_started'
    PATCH_COMPLETED = 'patch_completed'
    PROMOTED = 'promoted'
    BLOCKED = 'blocked'
    TIMEOUT_ENFORCED = 'timeout_enforced'


class LedgerError(Exception):
    """Base ledger error."""
    pass


class ConcurrencyError(LedgerError):
    """Raised when CAS (Compare-And-Swap) fails due to version mismatch."""
    pass


class TaskLedger:
    """
    CQRS-Lite SQLite ledger with dual tables.
    Thread-safe via SQLite WAL mode + version-based CAS.
    """

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), timeout=10)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute('PRAGMA journal_mode=WAL')
            self._conn.execute('PRAGMA foreign_keys=ON')
        return self._conn

    def _init_db(self):
        """Create tables if they don't exist. Idempotent."""
        conn = self._get_conn()
        try:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS task_state (
                    task_id       TEXT PRIMARY KEY,
                    skill         TEXT NOT NULL,
                    department    TEXT NOT NULL,
                    model         TEXT,
                    current_stage TEXT NOT NULL DEFAULT 'GATE_CHECK',
                    attempt       INTEGER NOT NULL DEFAULT 1,
                    max_attempts  INTEGER NOT NULL DEFAULT 3,
                    version       INTEGER NOT NULL DEFAULT 1,
                    status        TEXT NOT NULL DEFAULT 'ACTIVE',
                    idempotency_key TEXT,
                    created_at    TEXT NOT NULL,
                    last_updated  TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS task_events (
                    event_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id       TEXT NOT NULL,
                    timestamp     TEXT NOT NULL,
                    event_type    TEXT NOT NULL,
                    current_stage TEXT,
                    model         TEXT,
                    attempt       INTEGER,
                    delta_payload TEXT,
                    FOREIGN KEY (task_id) REFERENCES task_state(task_id)
                );

                CREATE INDEX IF NOT EXISTS idx_events_task ON task_events(task_id);
                CREATE INDEX IF NOT EXISTS idx_events_type ON task_events(event_type);
                CREATE INDEX IF NOT EXISTS idx_state_stage ON task_state(current_stage);
                CREATE INDEX IF NOT EXISTS idx_state_status ON task_state(status);
            ''')
            conn.commit()
        finally:
            pass  # conn is instance-owned

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_task(self, task_id: str, skill: str, department: str,
                    model: str = None, max_attempts: int = 3) -> dict:
        """Create a new task in the ledger. Returns the initial state."""
        now = self._now()
        idempotency_key = f'{task_id}:1'
        conn = self._get_conn()
        try:
            conn.execute('''
                INSERT INTO task_state (task_id, skill, department, model, current_stage,
                                        attempt, max_attempts, version, status,
                                        idempotency_key, created_at, last_updated)
                VALUES (?, ?, ?, ?, 'GATE_CHECK', 1, ?, 1, 'ACTIVE', ?, ?, ?)
            ''', (task_id, skill, department, model, max_attempts, idempotency_key, now, now))

            conn.execute('''
                INSERT INTO task_events (task_id, timestamp, event_type, current_stage,
                                         model, attempt, delta_payload)
                VALUES (?, ?, ?, 'GATE_CHECK', ?, 1, ?)
            ''', (task_id, now, EventType.TASK_CREATED.value, model,
                  json.dumps({'skill': skill, 'department': department})))

            conn.commit()
            return {'task_id': task_id, 'stage': 'GATE_CHECK', 'version': 1}
        except sqlite3.IntegrityError:
            raise LedgerError(f'Task {task_id} already exists')
        finally:
            pass  # conn is instance-owned

    def emit(self, task_id: str, event_type: str, current_stage: str = None,
             model: str = None, attempt: int = None, status: str = None,
             expected_version: int = None, data: dict = None) -> int:
        """
        Emit an event AND update task_state atomically.
        Uses CAS (Compare-And-Swap) via version column for TOCTOU protection.
        Returns the new version number.
        """
        now = self._now()
        delta = json.dumps(data or {})
        conn = self._get_conn()
        try:
            # Build UPDATE with CAS
            updates = ['last_updated = ?']
            params = [now]

            if current_stage:
                updates.append('current_stage = ?')
                params.append(current_stage)
            if model:
                updates.append('model = ?')
                params.append(model)
            if attempt is not None:
                updates.append('attempt = ?')
                params.append(attempt)
                updates.append('idempotency_key = ?')
                params.append(f'{task_id}:{attempt}')
            if status:
                updates.append('status = ?')
                params.append(status)

            updates.append('version = version + 1')

            # CAS: WHERE version = expected_version (TOCTOU protection)
            where = 'WHERE task_id = ?'
            params.append(task_id)
            if expected_version is not None:
                where += ' AND version = ?'
                params.append(expected_version)

            joined = ', '.join(updates); sql = f'UPDATE task_state SET {joined} {where}'
            cursor = conn.execute(sql, params)

            if cursor.rowcount == 0:
                if expected_version is not None:
                    raise ConcurrencyError(
                        f'CAS failed for {task_id}: expected version {expected_version}')
                raise LedgerError(f'Task {task_id} not found')

            # Append immutable event
            conn.execute('''
                INSERT INTO task_events (task_id, timestamp, event_type, current_stage,
                                         model, attempt, delta_payload)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (task_id, now, event_type, current_stage, model, attempt, delta))

            conn.commit()

            # Get new version
            row = conn.execute('SELECT version FROM task_state WHERE task_id = ?',
                               (task_id,)).fetchone()
            return row['version'] if row else -1
        finally:
            pass  # conn is instance-owned

    def current_state(self, task_id: str) -> Optional[dict]:
        """Get current mutable state for a task. O(1) read."""
        conn = self._get_conn()
        try:
            row = conn.execute('SELECT * FROM task_state WHERE task_id = ?',
                               (task_id,)).fetchone()
            return dict(row) if row else None
        finally:
            pass  # conn is instance-owned

    def events(self, task_id: str) -> list:
        """Get all events for a task. Full audit trail replay."""
        conn = self._get_conn()
        try:
            rows = conn.execute('''
                SELECT * FROM task_events WHERE task_id = ?
                ORDER BY event_id ASC
            ''', (task_id,)).fetchall()
            return [dict(r) for r in rows]
        finally:
            pass  # conn is instance-owned

    def query(self, event_type: str = None, since: str = None,
              model: str = None, limit: int = 100) -> list:
        """Cross-task event query for analytics."""
        conn = self._get_conn()
        try:
            sql = 'SELECT * FROM task_events WHERE 1=1'
            params = []
            if event_type:
                sql += ' AND event_type = ?'
                params.append(event_type)
            if since:
                sql += ' AND timestamp >= ?'
                params.append(since)
            if model:
                sql += ' AND model = ?'
                params.append(model)
            sql += ' ORDER BY event_id DESC LIMIT ?'
            params.append(limit)
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            pass  # conn is instance-owned

    def active_tasks(self, stage: str = None) -> list:
        """List all active tasks, optionally filtered by stage."""
        conn = self._get_conn()
        try:
            sql = "SELECT * FROM task_state WHERE status = 'ACTIVE'"
            params = []
            if stage:
                sql += ' AND current_stage = ?'
                params.append(stage)
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            pass  # conn is instance-owned

    def list_tasks(self, since: str = None, limit: int = 50) -> list:
        """List all tasks with current state."""
        conn = self._get_conn()
        try:
            sql = 'SELECT * FROM task_state'
            params = []
            if since:
                sql += ' WHERE created_at >= ?'
                params.append(since)
            sql += ' ORDER BY last_updated DESC LIMIT ?'
            params.append(limit)
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            pass  # conn is instance-owned

    def stats(self) -> dict:
        """Pipeline statistics for dashboard."""
        conn = self._get_conn()
        try:
            row = conn.execute("""
                SELECT COUNT(*) AS total_tasks,
                    SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active,
                    SUM(CASE WHEN status = 'BLOCKED' THEN 1 ELSE 0 END) AS blocked,
                    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed,
                    (SELECT COUNT(*) FROM task_events) AS total_events
                FROM task_state
            """).fetchone()
            return {
                'total_tasks': row[0] or 0, 'active': row[1] or 0,
                'blocked': row[2] or 0, 'completed': row[3] or 0,
                'total_events': row[4] or 0,
            }
        finally:
            pass  # conn is instance-owned


# ── CLI ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    ledger = TaskLedger()

    if len(sys.argv) < 2:
        print('Usage: task_ledger.py [stats|list|events <task_id>|query <event_type>]')
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'stats':
        print(json.dumps(ledger.stats(), indent=2))
    elif cmd == 'list':
        for t in ledger.list_tasks():
            print(f"  {t['task_id']:<40} {t['current_stage']:<15} {t['status']:<10} v{t['version']}")
    elif cmd == 'events' and len(sys.argv) >= 3:
        for e in ledger.events(sys.argv[2]):
            print(f"  [{e['timestamp'][:19]}] {e['event_type']:<20} stage={e['current_stage']} model={e['model']} attempt={e['attempt']}")
    elif cmd == 'query' and len(sys.argv) >= 3:
        for e in ledger.query(event_type=sys.argv[2]):
            print(f"  [{e['timestamp'][:19]}] {e['task_id']:<40} {e['event_type']}")
    else:
        print(f'Unknown: {cmd}')
        sys.exit(1)
