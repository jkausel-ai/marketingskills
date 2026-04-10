#!/usr/bin/env python3
"""Aggregate CoChalet execution and review logs into a dashboard JSON file."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_type(expected: str, value: object) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema(schema: dict[str, object], value: object, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        allowed = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(is_type(kind, value) for kind in allowed):
            return [f"{path}: expected {allowed}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not in enum")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: {value!r} != const {schema['const']!r}")
    if isinstance(value, str) and schema.get("format") == "date-time":
        try:
            parse_datetime(value)
        except ValueError:
            errors.append(f"{path}: invalid date-time")
    if isinstance(value, str) and schema.get("format") == "date":
        try:
            datetime.fromisoformat(value)
        except ValueError:
            errors.append(f"{path}: invalid date")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and value < minimum:
            errors.append(f"{path}: {value} < minimum {minimum}")
        if maximum is not None and value > maximum:
            errors.append(f"{path}: {value} > maximum {maximum}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}: missing required key {key!r}")
        for key, child in properties.items():
            if key in value:
                errors.extend(validate_schema(child, value[key], f"{path}.{key}"))
        extra_schema = schema.get("additionalProperties")
        if isinstance(extra_schema, dict):
            for key, child_value in value.items():
                if key not in properties:
                    errors.extend(validate_schema(extra_schema, child_value, f"{path}.{key}"))

    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            errors.extend(validate_schema(schema["items"], item, f"{path}[{index}]"))

    return errors


def load_records(directory: Path, schema: dict[str, object]) -> list[tuple[Path, dict[str, object]]]:
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(directory.glob("*.json")):
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}: expected top-level object")
        errors = validate_schema(schema, payload)
        if errors:
            joined = "\n".join(errors[:10])
            raise ValueError(f"{path}: schema validation failed\n{joined}")
        records.append((path, payload))
    return records


def quality_percentage(review: dict[str, object]) -> float | None:
    percentage = review.get("percentage")
    if isinstance(percentage, (int, float)) and not isinstance(percentage, bool):
        return float(percentage)
    total = review.get("total_score")
    max_score = review.get("max_score", 40)
    if isinstance(total, int) and isinstance(max_score, int) and max_score > 0:
        return (total / max_score) * 100
    return None


def infer_trend(values: list[float]) -> str:
    if len(values) < 2:
        return "new"
    midpoint = max(1, len(values) // 2)
    early = mean(values[:midpoint])
    late = mean(values[midpoint:])
    diff = late - early
    if diff > 5:
        return "improving"
    if diff < -5:
        return "declining"
    return "stable"


def round_number(value: float) -> float:
    return round(value, 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", required=True, type=Path)
    parser.add_argument("--reviews", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    execution_schema = load_json(root / "schemas" / "execution-log.schema.json")
    review_schema = load_json(root / "schemas" / "quality-review.schema.json")
    dashboard_schema = load_json(root / "schemas" / "dashboard.schema.json")

    execution_records = load_records(args.iterations.expanduser(), execution_schema)
    review_records = load_records(args.reviews.expanduser(), review_schema)
    review_by_execution = {
        Path(str(review["reviews_execution"])).name: review for _, review in review_records
    }

    models_used: Counter[str] = Counter()
    four_nevers_flags: set[str] = set()
    period_points: list[datetime] = []
    total_cost = 0.0
    published_count = 0
    quality_values: list[float] = []

    skill_bucket: dict[str, list[dict[str, object]]] = defaultdict(list)
    model_bucket: dict[str, list[dict[str, object]]] = defaultdict(list)

    for path, execution in execution_records:
        skill = str(execution["skill"])
        model = str(execution["model"])
        review = review_by_execution.get(path.name)
        quality = quality_percentage(review) if review else None
        cost = float(execution.get("estimated_cost_usd", 0) or 0)
        record = {
            "execution": execution,
            "review": review,
            "quality": quality,
            "cost": cost,
            "timestamp": parse_datetime(str(execution["timestamp"])),
        }

        skill_bucket[skill].append(record)
        model_bucket[model].append(record)
        models_used[model] += 1
        total_cost += cost
        ts = record["timestamp"]
        if ts.tzinfo is None:
            from datetime import timezone as _tz
            ts = ts.replace(tzinfo=_tz.utc)
        period_points.append(ts)

        if execution.get("four_nevers_self_check") is False:
            four_nevers_flags.add(path.name)
        if review:
            if review.get("publish_status") == "published":
                published_count += 1
            if quality is not None:
                quality_values.append(quality)
            scores = review.get("scores", {})
            if isinstance(scores, dict) and scores.get("four_nevers_clean") is False:
                four_nevers_flags.add(path.name)

    per_skill: dict[str, dict[str, object]] = {}
    for skill, rows in sorted(skill_bucket.items()):
        reviewed = [row["quality"] for row in rows if isinstance(row["quality"], (int, float))]
        published = sum(1 for row in rows if row["review"] and row["review"].get("publish_status") == "published")
        cost_total = sum(float(row["cost"]) for row in rows)
        quality_by_model: dict[str, list[float]] = defaultdict(list)
        model_costs: dict[str, float] = defaultdict(float)
        for row in rows:
            model = str(row["execution"]["model"])
            model_costs[model] += float(row["cost"])
            if isinstance(row["quality"], (int, float)):
                quality_by_model[model].append(float(row["quality"]))

        if quality_by_model:
            ranked = sorted(
                quality_by_model.items(),
                key=lambda item: (
                    mean(item[1]),
                    len(item[1]),
                    -model_costs[item[0]],
                ),
                reverse=True,
            )
            best_model = ranked[0][0]
        else:
            counts = Counter(str(row["execution"]["model"]) for row in rows)
            best_model = counts.most_common(1)[0][0]

        per_skill[skill] = {
            "executions": len(rows),
            "avg_quality": round_number(mean(reviewed)) if reviewed else 0.0,
            "total_cost": round_number(cost_total),
            "best_model": best_model,
            "published": published,
            "trend": infer_trend([float(value) for value in reviewed]),
        }

    per_model: dict[str, dict[str, object]] = {}
    for model, rows in sorted(model_bucket.items()):
        reviewed = [row["quality"] for row in rows if isinstance(row["quality"], (int, float))]
        cost_total = sum(float(row["cost"]) for row in rows)
        score_total = sum(float(value) for value in reviewed)
        per_model[model] = {
            "executions": len(rows),
            "avg_quality": round_number(mean(reviewed)) if reviewed else 0.0,
            "total_cost": round_number(cost_total),
            "quality_per_dollar": round_number(score_total / cost_total) if cost_total > 0 else 0.0,
        }

    dashboard: dict[str, object] = {
        "generated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "summary": {
            "total_executions": len(execution_records),
            "total_cost_usd": round_number(total_cost),
            "avg_quality_score": round_number(mean(quality_values)) if quality_values else 0.0,
            "four_nevers_violations": len(four_nevers_flags),
            "skills_active": len(skill_bucket),
            "published_count": published_count,
            "models_used": dict(sorted(models_used.items())),
        },
        "per_skill": per_skill,
        "per_model": per_model,
    }
    if period_points:
        dashboard["period_start"] = min(period_points).date().isoformat()
        dashboard["period_end"] = max(period_points).date().isoformat()

    errors = validate_schema(dashboard_schema, dashboard)
    if errors:
        joined = "\n".join(errors[:10])
        raise ValueError(f"Dashboard schema validation failed\n{joined}")

    args.output.expanduser().parent.mkdir(parents=True, exist_ok=True)
    with args.output.expanduser().open("w", encoding="utf-8") as handle:
        json.dump(dashboard, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
