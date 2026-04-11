#!/usr/bin/env python3
"""
envelope.py -- FSM-Enforced ExecutionEnvelope for COS Pipeline
Phase 1+2 Foundation. 4-way consensus (Opus+Gemini+Codex+Hermes).

The ExecutionEnvelope is the typed contract that wraps every pipeline task.
It enforces a strict Finite State Machine -- illegal transitions raise
StateViolationError. State is persisted to the SQLite TaskLedger.

Architecture:
  - FSM with ALLOWED_TRANSITIONS dict (Gemini requirement)
  - version field for CAS concurrency control (Codex requirement)
  - idempotency_key prevents duplicate execution (Codex requirement)
  - Persists via TaskLedger (SQLite), not JSON files (Gemini requirement)

Usage:
  envelope = ExecutionEnvelope.create('email-sequence', 'dept-content-copy', 'write DW email FR')
  envelope.advance_stage('DISPATCH')
  envelope.advance_stage('EXECUTE')
  # ... executor runs ...
  envelope.advance_stage('STAGING')
  envelope.advance_stage('VERIFY')
  envelope.advance_stage('PRODUCTION')  # or 'BLOCKED' if failed
"""

import hashlib
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Import ledger (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from task_ledger import TaskLedger, EventType, ConcurrencyError

# -- FSM Transition Map (Gemini Enhancement #1) --------------------------
ALLOWED_TRANSITIONS = {
    'GATE_CHECK':    ['DISPATCH', 'GATE_REJECTED'],
    'DISPATCH':      ['EXECUTE'],
    'EXECUTE':       ['STAGING', 'EXECUTE_FAILED'],
    'EXECUTE_FAILED':['BLOCKED'],
    'STAGING':       ['VERIFY'],
    'VERIFY':        ['PRODUCTION', 'STAGING', 'BLOCKED'],  # STAGING = retry
    'PRODUCTION':    ['PROMOTED'],
    'PROMOTED':      [],       # terminal
    'BLOCKED':       [],       # terminal
    'GATE_REJECTED': [],       # terminal
}

TERMINAL_STAGES = {stage for stage, targets in ALLOWED_TRANSITIONS.items() if not targets}


class StateViolationError(Exception):
    """Raised when an illegal FSM transition is attempted."""
    def __init__(self, current: str, target: str, task_id: str = ''):
        self.current = current
        self.target = target
        self.task_id = task_id
        super().__init__(
            f'Illegal transition: {current} -> {target} for task {task_id}. '
            f'Allowed from {current}: {ALLOWED_TRANSITIONS.get(current, [])}'
        )


@dataclass
class ExecutionEnvelope:
    """
    Typed, durable contract for a pipeline task.
    Enforces FSM transitions. Persists to SQLite ledger.
    """
    task_id: str
    task: str
    skill: str
    department: str
    model: str
    persona: str                      # DW | PC | Both
    language: str                     # FR | EN | Bilingual
    current_stage: str = 'GATE_CHECK'
    attempt: int = 1
    max_attempts: int = 3
    version: int = 1
    prior_failures: list = field(default_factory=list)
    gate_result: dict = field(default_factory=dict)
    dispatch_payload_path: str = ''
    output_path: str = ''
    engineered_prompt: str = ''
    execution_start: float = 0.0
    execution_end: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    created_at: str = ''

    # Internal: ledger reference (not serialized)
    _ledger: Optional[TaskLedger] = field(default=None, repr=False)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.task_id:
            ts = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
            task_hash = hashlib.md5(self.task.encode()).hexdigest()[:8]
            self.task_id = f'{self.skill}-{ts}-{task_hash}'
        if self._ledger is None:
            self._ledger = TaskLedger()

    @classmethod
    def create(cls, skill: str, department: str, task: str,
               model: str = '', persona: str = 'Both',
               language: str = 'Bilingual', max_attempts: int = 3) -> 'ExecutionEnvelope':
        """Create a new envelope and register it in the ledger."""
        envelope = cls(
            task_id='',  # auto-generated in __post_init__
            task=task,
            skill=skill,
            department=department,
            model=model,
            persona=persona,
            language=language,
            max_attempts=max_attempts,
        )
        # Register in ledger
        envelope._ledger.create_task(
            envelope.task_id,
            skill=skill,
            department=department,
            model=model,
            max_attempts=max_attempts,
        )
        return envelope

    @classmethod
    def from_gate_and_dispatch(cls, gate_result: dict, dispatch_result: dict,
                                task: str) -> 'ExecutionEnvelope':
        """Create envelope from existing gate check + dispatch results."""
        skill = gate_result.get('skill', 'unknown')
        dept = gate_result.get('department', 'dept-strategy')
        model = gate_result.get('model', 'google/gemini-2.5-flash')
        persona = dispatch_result.get('payload', {}).get('persona', 'Both')
        language = dispatch_result.get('payload', {}).get('language', 'Bilingual')
        output_path = dispatch_result.get('output_path', '')

        envelope = cls.create(
            skill=skill,
            department=dept,
            task=task,
            model=model,
            persona=persona,
            language=language,
        )
        envelope.gate_result = gate_result
        envelope.output_path = output_path
        envelope.dispatch_payload_path = dispatch_result.get('payload_file', '')
        if gate_result.get('engineered_prompt'):
            envelope.engineered_prompt = gate_result['engineered_prompt']
        return envelope


    @classmethod
    def from_ledger(cls, task_id: str, ledger: Optional[TaskLedger] = None) -> 'ExecutionEnvelope':
        """Reconstruct envelope from SQLite for crash recovery."""
        ledger = ledger or TaskLedger()
        state = ledger.current_state(task_id)
        if not state:
            raise ValueError(f'Unknown task_id: {task_id}')
        return cls(
            task_id=state['task_id'],
            task='',
            skill=state['skill'],
            department=state['department'],
            model=state.get('model') or '',
            persona='Both',
            language='Bilingual',
            current_stage=state['current_stage'],
            attempt=state['attempt'],
            max_attempts=state['max_attempts'],
            version=state['version'],
            created_at=state['created_at'],
            _ledger=ledger,
        )

    @property
    def idempotency_key(self) -> str:
        return f'{self.task_id}:{self.attempt}'

    @property
    def is_terminal(self) -> bool:
        return self.current_stage in TERMINAL_STAGES

    @property
    def is_exhausted(self) -> bool:
        return self.attempt >= self.max_attempts

    def advance_stage(self, new_stage: str, event_type: str = None,
                      data: dict = None) -> int:
        """
        Transition to a new pipeline stage. Validates FSM rules.
        Returns new version number from ledger CAS.
        Raises StateViolationError on illegal transition.
        """
        # FSM validation
        allowed = ALLOWED_TRANSITIONS.get(self.current_stage, [])
        if new_stage not in allowed:
            raise StateViolationError(self.current_stage, new_stage, self.task_id)

        # Determine event type
        if event_type is None:
            event_type = self._default_event_type(new_stage)

        # Determine status
        status = 'ACTIVE'
        if new_stage in TERMINAL_STAGES:
            status = 'COMPLETED' if new_stage == 'PROMOTED' else 'BLOCKED'

        # Persist to ledger with CAS
        new_version = self._ledger.emit(
            task_id=self.task_id,
            event_type=event_type,
            current_stage=new_stage,
            model=self.model,
            attempt=self.attempt,
            status=status,
            expected_version=self.version,
            data=data or {},
        )

        # Update local state
        self.current_stage = new_stage
        self.version = new_version
        return new_version

    def trigger_retry(self, failures: dict = None) -> int:
        """
        Retry: persist next attempt FIRST, then update in-memory state.
        CAS-safe: in-memory only changes after ledger accepts.
        """
        if self.is_exhausted:
            return self.advance_stage('BLOCKED', EventType.BLOCKED.value,
                                       data={'reason': 'max_attempts_exhausted',
                                             'failures': failures or {}})

        next_attempt = self.attempt + 1
        next_prior_failures = list(self.prior_failures)
        if failures:
            next_prior_failures.append(str(failures))

        new_version = self.advance_stage(
            'STAGING',
            EventType.PATCH_STARTED.value,
            data={
                'attempt': next_attempt,
                'failures': failures or {},
                'prior_failures_count': len(next_prior_failures),
            },
        )
        # Only update in-memory AFTER ledger accepts
        self.attempt = next_attempt
        self.prior_failures = next_prior_failures
        return new_version

    def record_execution_time(self) -> float:
        """Record execution duration. Returns duration in seconds."""
        if self.execution_start and self.execution_end:
            return self.execution_end - self.execution_start
        return 0.0

    def to_dict(self) -> dict:
        """Serialize envelope to dict (for JSON logging)."""
        return {
            'task_id': self.task_id,
            'task': self.task[:200],
            'skill': self.skill,
            'department': self.department,
            'model': self.model,
            'persona': self.persona,
            'language': self.language,
            'current_stage': self.current_stage,
            'attempt': self.attempt,
            'max_attempts': self.max_attempts,
            'version': self.version,
            'prior_failures': self.prior_failures,
            'output_path': self.output_path,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'estimated_cost_usd': self.estimated_cost_usd,
            'execution_duration_s': self.record_execution_time(),
            'idempotency_key': self.idempotency_key,
            'created_at': self.created_at,
        }

    def _default_event_type(self, stage: str) -> str:
        """Map stage to default event type."""
        mapping = {
            'DISPATCH': EventType.GATE_PASSED.value,
            'GATE_REJECTED': EventType.GATE_REJECTED.value,
            'EXECUTE': EventType.EXECUTE_STARTED.value,
            'STAGING': EventType.STAGING_READY.value,
            'EXECUTE_FAILED': EventType.EXECUTE_FAILED.value,
            'VERIFY': EventType.VERIFY_STARTED.value,
            'PRODUCTION': EventType.VERIFY_PASSED.value,
            'PROMOTED': EventType.PROMOTED.value,
            'BLOCKED': EventType.BLOCKED.value,
        }
        return mapping.get(stage, stage.lower())


# -- CLI ---------------------------------------------------------------
if __name__ == '__main__':
    import json
    # Quick test
    env = ExecutionEnvelope.create(
        skill='email-sequence',
        department='dept-content-copy',
        task='Write DW email sequence FR',
        model='local:/root/claude-delegate.sh',
    )
    print(f'Created: {env.task_id} at {env.current_stage} v{env.version}')
    env.advance_stage('DISPATCH')
    print(f'Advanced to {env.current_stage} v{env.version}')
    env.advance_stage('EXECUTE')
    print(f'Advanced to {env.current_stage} v{env.version}')

    # Test FSM violation
    try:
        env.advance_stage('PROMOTED')  # illegal from EXECUTE
    except StateViolationError as e:
        print(f'FSM correctly blocked: {e}')

    print(json.dumps(env.to_dict(), indent=2))
