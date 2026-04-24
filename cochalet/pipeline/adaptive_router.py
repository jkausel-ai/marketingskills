#!/usr/bin/env python3
"""
adaptive_router.py -- data-driven model suggestions for the pipeline.
"""

import argparse
import hashlib
import json
import sqlite3
import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path("/var/lib/hermes/memory/orchestration_ledger.db")
ADAPTIVE_STATE = Path("/mnt/hermes-output/telemetry/adaptive-state.json")
MIN_SAMPLES = 10
CONFIDENCE_THRESHOLD = 0.7


class TaskDNA:
    """Fingerprint a task for adaptive routing."""

    def __init__(self, task: str, skill: str, persona: str = "Both", language: str = "Bilingual"):
        self.task = task or ""
        self.skill = skill or "unknown"
        self.persona = persona or "Both"
        self.language = language or "Bilingual"
        self.complexity_tier = self._infer_complexity_tier(self.task)

    @staticmethod
    def _infer_complexity_tier(task: str) -> str:
        text = (task or "").lower()
        if any(term in text for term in ("strategy", "architecture", "roadmap", "multi-step", "orchestrate")):
            return "high"
        if any(term in text for term in ("email", "copy", "content", "campaign", "brief", "analysis")):
            return "medium"
        return "low"

    def fingerprint(self) -> str:
        """Return bucket key: {skill}:{persona}:{language}."""
        return f"{self.skill}:{self.persona}:{self.language}"


class AdaptiveRouter:
    """Self-tuning model selection from historical performance."""

    def __init__(self, db_path: Path = DB_PATH, state_path: Path = ADAPTIVE_STATE):
        self.db_path = Path(db_path)
        self.state_path = Path(state_path)

    def _connect(self, read_only: bool = False) -> sqlite3.Connection:
        if read_only:
            uri = f"file:{self.db_path}?mode=ro"
            conn = sqlite3.connect(uri, uri=True, timeout=10)
        else:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _load_payload(row: sqlite3.Row) -> dict:
        payload = row["delta_payload"] or "{}"
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _adaptive_task_id(fingerprint: str, model: str) -> str:
        digest = hashlib.sha1(f"{fingerprint}|{model}".encode("utf-8")).hexdigest()[:16]
        return f"adaptive-{digest}"

    def _ensure_task_state(self, conn: sqlite3.Connection, task_id: str, model: str) -> None:
        row = conn.execute("SELECT task_id FROM task_state WHERE task_id = ?", (task_id,)).fetchone()
        if row:
            return
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """
            INSERT INTO task_state (
                task_id, skill, department, model, current_stage, attempt, max_attempts,
                version, status, idempotency_key, created_at, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                "adaptive-routing",
                "dept-telemetry",
                model,
                "VERIFY",
                1,
                1,
                1,
                "ACTIVE",
                f"{task_id}:1",
                now,
                now,
            ),
        )

    def _read_observations(self) -> dict:
        if not self.db_path.exists():
            return {}
        conn = self._connect(read_only=True)
        try:
            rows = conn.execute(
                """
                SELECT model, delta_payload
                FROM task_events
                WHERE event_type = 'adaptive_observation'
                ORDER BY event_id ASC
                """
            ).fetchall()
        except sqlite3.OperationalError:
            return {}
        finally:
            conn.close()

        grouped = {}
        for row in rows:
            payload = self._load_payload(row)
            fingerprint = payload.get("fingerprint")
            model = payload.get("model") or row["model"]
            if not fingerprint or not model:
                continue
            bucket = grouped.setdefault(fingerprint, {}).setdefault(model, [])
            bucket.append(
                {
                    "quality": float(payload.get("quality", 0) or 0),
                    "passed": bool(payload.get("passed", False)),
                    "time_ms": int(payload.get("time_ms", 0) or 0),
                }
            )
        return grouped

    def _matrix_from_observations(self, grouped: dict) -> dict:
        matrix = {}
        for fingerprint, models in grouped.items():
            model_stats = {}
            for model, observations in models.items():
                qualities = [entry["quality"] for entry in observations]
                passes = [1 if entry["passed"] else 0 for entry in observations]
                model_stats[model] = {
                    "avg_quality": statistics.mean(qualities),
                    "count": len(observations),
                    "success_rate": statistics.mean(passes) if passes else 0.0,
                }
            matrix[fingerprint] = model_stats
        return matrix

    def suggest_model(self, task_dna: TaskDNA):
        """
        Return (model_id, avg_quality) if the best model has enough data and
        a quality advantage over the second-best model.
        """
        if not task_id:
            return
        fingerprint = task_dna.fingerprint()
        stats = self.performance_matrix().get(fingerprint, {})
        eligible = [
            (model, values)
            for model, values in stats.items()
            if values.get("count", 0) >= MIN_SAMPLES
        ]
        if not eligible:
            return None

        ranked = sorted(eligible, key=lambda item: item[1]["avg_quality"], reverse=True)
        best_model, best_stats = ranked[0]
        second_quality = ranked[1][1]["avg_quality"] if len(ranked) > 1 else 0.0
        if (best_stats["avg_quality"] - second_quality) < CONFIDENCE_THRESHOLD:
            return None
        return best_model, best_stats["avg_quality"]

    def record_outcome(self, task_dna: TaskDNA, model: str, quality_score: float,
                       execution_time_ms: int, verify_passed: bool,
                       task_id: str = '', attempt: int = 1) -> None:
        """Record an execution outcome into task_events."""
        if not task_id:
            return
        fingerprint = task_dna.fingerprint()
        # task_id comes from caller (real envelope.task_id)
        payload = {
            "fingerprint": fingerprint,
            "model": model,
            "quality": float(quality_score),
            "time_ms": int(execution_time_ms),
            "passed": bool(verify_passed),
            "complexity_tier": task_dna.complexity_tier,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        now = datetime.now(timezone.utc).isoformat()

        conn = self._connect(read_only=False)
        try:
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute(
                """
                INSERT INTO task_events (
                    task_id, timestamp, event_type, current_stage, model, attempt, delta_payload
                ) VALUES (?, ?, 'adaptive_observation', 'VERIFY', ?, 1, ?)
                """,
                (task_id, now, model, json.dumps(payload, ensure_ascii=True, sort_keys=True)),
            )
            conn.execute(
                "UPDATE task_state SET model = ?, last_updated = ? WHERE task_id = ?",
                (model, now, task_id),
            )
            conn.commit()
        finally:
            conn.close()

        self._write_state_snapshot()

    def performance_matrix(self) -> dict:
        """Return {fingerprint: {model: {avg_quality, count, success_rate}}}."""
        return self._matrix_from_observations(self._read_observations())

    def _write_state_snapshot(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "min_samples": MIN_SAMPLES,
            "confidence_threshold": CONFIDENCE_THRESHOLD,
            "matrix": self.performance_matrix(),
        }
        self.state_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True), encoding="utf-8")

    def decay_old_data(self, max_age_days: int = 90) -> int:
        """Delete adaptive observations older than max_age_days and return count deleted."""
        if not self.db_path.exists():
            return 0
        cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
        conn = self._connect(read_only=False)
        try:
            conn.execute("PRAGMA foreign_keys=ON")
            cursor = conn.execute(
                """
                DELETE FROM task_events
                WHERE event_type = 'adaptive_observation' AND timestamp < ?
                """,
                (cutoff.isoformat(),),
            )
            deleted = cursor.rowcount
            conn.commit()
        finally:
            conn.close()
        self._write_state_snapshot()
        return deleted


def _cmd_status(router: AdaptiveRouter) -> int:
    print(json.dumps(router.performance_matrix(), indent=2, sort_keys=True))
    return 0


def _cmd_suggest(router: AdaptiveRouter, skill: str) -> int:
    suggestion = router.suggest_model(TaskDNA(task="", skill=skill))
    if suggestion is None:
        print(json.dumps({"skill": skill, "suggestion": None}, indent=2, sort_keys=True))
    else:
        model_id, avg_quality = suggestion
        print(json.dumps(
            {"skill": skill, "suggestion": {"model": model_id, "avg_quality": avg_quality}},
            indent=2,
            sort_keys=True,
        ))
    return 0


def _cmd_decay(router: AdaptiveRouter, days: int) -> int:
    deleted = router.decay_old_data(max_age_days=days)
    print(json.dumps({"days": days, "deleted": deleted}, indent=2, sort_keys=True))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Adaptive model router")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show adaptive performance matrix")

    suggest_parser = subparsers.add_parser("suggest", help="Suggest a model for a skill")
    suggest_parser.add_argument("skill")

    decay_parser = subparsers.add_parser("decay", help="Delete old adaptive observations")
    decay_parser.add_argument("--days", type=int, default=90)

    args = parser.parse_args(argv)
    router = AdaptiveRouter()

    if args.command == "status":
        return _cmd_status(router)
    if args.command == "suggest":
        return _cmd_suggest(router, args.skill)
    if args.command == "decay":
        return _cmd_decay(router, args.days)
    return 1


if __name__ == "__main__":
    sys.exit(main())
