#!/usr/bin/env python3
"""
executor.py -- Stage 3 EXECUTE Engine for COS Pipeline
Phase 1+2 Foundation. 4-way consensus (Opus+Gemini+Codex+Hermes).

Two executor types:
  - LocalDelegateExecutor: calls hardened bash delegates via subprocess
  - OpenRouterExecutor: calls OpenRouter API via urllib (stdlib only)

Security:
  - NO shell=True anywhere (Codex security requirement)
  - load_secret() replaces all bash grep pipelines (Codex security requirement)
  - subprocess array format only (no shell injection)

Architecture:
  - Delegates write to STDOUT -- executor captures and writes to output_path
  - Delegates accept ONE argument (prompt string or prompt file path)
  - Output validation: min 50 chars, file must exist after write
  - Timeout: 300s Opus, 180s Sonnet/Codex, configurable per call

Usage:
  from executor import ExecutorFactory
  executor = ExecutorFactory.get_executor('local:/root/claude-delegate.sh')
  result = executor.execute(prompt='Write DW email FR', output_path='/tmp/test.md')
"""

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from subprocess import run as sp_run, TimeoutExpired, PIPE
from typing import Optional

# -- Configuration ------------------------------------------------------
DEFAULT_TIMEOUT = 180  # seconds
MIN_OUTPUT_CHARS = 50

# -- Cost Model (USD per 1M tokens) ------------------------------------
COST_PER_MILLION = {
    'google/gemini-2.5-flash': {'input': 0.15, 'output': 0.60},
    'google/gemini-2.5-flash:free': {'input': 0.0, 'output': 0.0},
    'deepseek/deepseek-chat': {'input': 0.14, 'output': 0.28},
    'deepseek/deepseek-chat:free': {'input': 0.0, 'output': 0.0},
    'local:/root/opus-delegate.sh': {'input': 0.0, 'output': 0.0},
    'local:/root/claude-delegate.sh': {'input': 0.0, 'output': 0.0},
    'local:/root/codex-delegate.sh': {'input': 0.0, 'output': 0.0},
}


def estimate_cost(model_id: str, input_tokens: int, output_tokens: int) -> float:
    rates = COST_PER_MILLION.get(model_id, {'input': 0.0, 'output': 0.0})
    cost = (input_tokens * rates['input'] + output_tokens * rates['output']) / 1_000_000
    return round(cost, 6)


def estimate_tokens_from_chars(char_count: int) -> int:
    return max(1, char_count // 4)

ENV_PATH = Path('/root/.hermes/.env')


# -- Safe Secret Loader (replaces bash grep pipeline) -------------------
def load_secret(name: str, env_path: Path = None) -> Optional[str]:
    """
    Load a secret from .env file safely.
    Replaces: sp.run(['bash', '-c', "grep 'KEY' .env | cut -d= -f2"])
    Handles: KEY=value, KEY="value", KEY='value'
    """
    path = env_path or ENV_PATH
    if not path.is_file():
        return os.environ.get(name)
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith(f'{name}='):
            val = line.split('=', 1)[1].strip()
            # Strip surrounding quotes
            if (val.startswith('"') and val.endswith('"')) or                (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            return val
    return os.environ.get(name)


# -- Result Dataclass ---------------------------------------------------
@dataclass
class ExecutorResult:
    success: bool
    output_path: Optional[str]
    output_size_bytes: int
    duration_ms: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    error: Optional[str]

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'output_path': self.output_path,
            'output_size_bytes': self.output_size_bytes,
            'duration_ms': self.duration_ms,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'estimated_cost_usd': self.estimated_cost_usd,
            'error': self.error,
        }


# -- Local Delegate Executor --------------------------------------------
class LocalDelegateExecutor:
    """
    Executes via hardened bash delegates (/root/{opus,claude,codex}-delegate.sh).
    Delegates accept ONE argument (prompt text) and write output to STDOUT.
    We capture stdout and write it to output_path.
    """

    def __init__(self, script_path: str, timeout: int = DEFAULT_TIMEOUT):
        self.script_path = script_path
        self.timeout = timeout

    def execute(self, prompt: str, output_path: str, **kwargs) -> ExecutorResult:
        start = time.monotonic()

        # Validate delegate exists and is executable
        if not os.path.isfile(self.script_path):
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=0, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=f'Delegate not found: {self.script_path}',
            )
        if not os.access(self.script_path, os.X_OK):
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=0, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=f'Delegate not executable: {self.script_path}',
            )

        prompt_file = None
        try:
            # Write prompt to temp file for long prompts (bash arg length limit)
            import tempfile
            if len(prompt) > 4000:
                fd, prompt_file = tempfile.mkstemp(suffix='.txt', prefix='cos-prompt-')
                with os.fdopen(fd, 'w', encoding='utf-8') as pf:
                    pf.write(prompt)
                arg = prompt_file
            else:
                arg = prompt

            # NO shell=True. Array format only.
            proc = sp_run(
                [self.script_path, arg],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            duration_ms = int((time.monotonic() - start) * 1000)

            if proc.returncode != 0:
                return ExecutorResult(
                    success=False, output_path=None, output_size_bytes=0,
                    duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                    estimated_cost_usd=0.0,
                    error=f'Delegate exit {proc.returncode}: {proc.stderr[:200]}',
                )

            output = proc.stdout
            if len(output) < MIN_OUTPUT_CHARS:
                return ExecutorResult(
                    success=False, output_path=None,
                    output_size_bytes=len(output.encode()),
                    duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                    estimated_cost_usd=0.0,
                    error=f'Output too short: {len(output)} chars < {MIN_OUTPUT_CHARS}',
                )

            # Write output to file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(output, encoding='utf-8')

            est_in = estimate_tokens_from_chars(len(prompt))
            est_out = estimate_tokens_from_chars(len(output))
            return ExecutorResult(
                success=True,
                output_path=output_path,
                output_size_bytes=len(output.encode()),
                duration_ms=duration_ms,
                input_tokens=est_in,
                output_tokens=est_out,
                estimated_cost_usd=0.0,  # CLI is free ($0 subscription)
                error=None,
            )

        except TimeoutExpired:
            duration_ms = int((time.monotonic() - start) * 1000)
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=f'Timeout after {self.timeout}s',
            )
        except Exception as e:
            duration_ms = int((time.monotonic() - start) * 1000)
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=str(e),
            )
        finally:
            if prompt_file:
                try:
                    os.unlink(prompt_file)
                except FileNotFoundError:
                    pass
# -- OpenRouter API Executor --------------------------------------------
class OpenRouterExecutor:
    """
    Calls OpenRouter API via urllib (stdlib only, no requests dependency).
    Parses token counts and cost from response.
    """

    API_URL = 'https://openrouter.ai/api/v1/chat/completions'

    def __init__(self, model_id: str, timeout: int = DEFAULT_TIMEOUT):
        self.model_id = model_id
        self.timeout = timeout
        self.api_key = load_secret('OPENROUTER_API_KEY')

    def execute(self, prompt: str, output_path: str, **kwargs) -> ExecutorResult:
        if not self.api_key:
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=0, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error='OPENROUTER_API_KEY not found',
            )

        start = time.monotonic()
        payload = json.dumps({
            'model': self.model_id,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 4000,
            'temperature': 0.4,
        }).encode('utf-8')

        req = urllib.request.Request(self.API_URL, data=payload)
        req.add_header('Authorization', f'Bearer {self.api_key}')
        req.add_header('Content-Type', 'application/json')
        req.add_header('HTTP-Referer', 'https://cochalet.co')

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                duration_ms = int((time.monotonic() - start) * 1000)
                body = json.loads(resp.read().decode('utf-8'))

            content = body.get('choices', [{}])[0].get('message', {}).get('content', '')
            usage = body.get('usage', {})
            input_tokens = usage.get('prompt_tokens', 0)
            output_tokens = usage.get('completion_tokens', 0)

            if len(content) < MIN_OUTPUT_CHARS:
                return ExecutorResult(
                    success=False, output_path=None,
                    output_size_bytes=len(content.encode()),
                    duration_ms=duration_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost_usd=0.0,
                    error=f'API output too short: {len(content)} chars',
                )

            # Write to file
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(content, encoding='utf-8')

            return ExecutorResult(
                success=True,
                output_path=output_path,
                output_size_bytes=len(content.encode()),
                duration_ms=duration_ms,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                estimated_cost_usd=estimate_cost(self.model_id, input_tokens, output_tokens),
                error=None,
            )

        except urllib.error.URLError as e:
            duration_ms = int((time.monotonic() - start) * 1000)
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=f'API error: {e}',
            )
        except Exception as e:
            duration_ms = int((time.monotonic() - start) * 1000)
            return ExecutorResult(
                success=False, output_path=None, output_size_bytes=0,
                duration_ms=duration_ms, input_tokens=0, output_tokens=0,
                estimated_cost_usd=0.0,
                error=str(e),
            )


# -- Factory ------------------------------------------------------------
class ExecutorFactory:
    """Select executor based on model string."""

    # Per-model timeout optimization (A2)
    MODEL_TIMEOUTS = {
        "opus": 300,      # Opus is thorough, needs time
        "sonnet": 300,    # Sonnet also thorough for quality tasks
        "claude": 300,    # Claude delegate = Sonnet
        "codex": 180,     # Codex is faster
        "gemini": 120,    # Gemini Flash is fast
        "deepseek": 180,  # DeepSeek moderate
    }

    @staticmethod
    def get_executor(model_id: str, timeout: int = DEFAULT_TIMEOUT):
        """
        local:/root/opus-delegate.sh   -> LocalDelegateExecutor
        local:/root/claude-delegate.sh -> LocalDelegateExecutor
        local:/root/codex-delegate.sh  -> LocalDelegateExecutor
        google/gemini-2.5-flash        -> OpenRouterExecutor
        deepseek/deepseek-chat         -> OpenRouterExecutor
        """
        # Per-model timeout (A2 optimization)
        if 'opus' in model_id.lower() or 'claude' in model_id.lower() or 'sonnet' in model_id.lower():
            timeout = max(timeout, 300)  # CLI models need time for quality
        if model_id.startswith('local:'):
            script = model_id[len('local:'):]
            # Detect timeout by delegate type
            if 'opus' in script:
                timeout = max(timeout, 300)  # Opus gets more time
            return LocalDelegateExecutor(script, timeout=timeout)
        return OpenRouterExecutor(model_id, timeout=timeout)


# -- CLI Test -----------------------------------------------------------
if __name__ == '__main__':
    print('Executor module loaded. Testing factory...')
    for model in ['local:/root/claude-delegate.sh', 'google/gemini-2.5-flash']:
        ex = ExecutorFactory.get_executor(model)
        print(f'  {model} -> {type(ex).__name__}')
    print('load_secret test:', 'OK' if load_secret('OPENROUTER_API_KEY') else 'NOT FOUND')
    print('EXECUTOR MODULE READY')
