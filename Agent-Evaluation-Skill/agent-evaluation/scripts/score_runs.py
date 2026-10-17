#!/usr/bin/env python3
"""Score agent evaluation run records.

The script intentionally uses only the Python standard library so it can travel
with the skill folder.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
import math
import pathlib
import statistics
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_CONFIG: Dict[str, Any] = {
    "component_weights": {
        "quantitative": 0.35,
        "gates": 0.45,
        "human": 0.20,
    },
    "fatal_zero": True,
    "quantitative_metrics": [
        {
            "path": "metrics.cost_usd",
            "weight": 0.25,
            "direction": "lower",
            "target": 0.50,
            "limit": 2.00,
            "required": False,
        },
        {
            "path": "metrics.total_tokens",
            "weight": 0.25,
            "direction": "lower",
            "target": 50000,
            "limit": 200000,
            "required": False,
        },
        {
            "path": "metrics.wall_time_s",
            "weight": 0.20,
            "direction": "lower",
            "target": 600,
            "limit": 3600,
            "required": False,
        },
        {
            "path": "metrics.tool_calls",
            "weight": 0.15,
            "direction": "lower",
            "target": 20,
            "limit": 80,
            "required": False,
        },
        {
            "path": "metrics.retry_count",
            "weight": 0.15,
            "direction": "lower",
            "target": 1,
            "limit": 8,
            "required": False,
        },
    ],
    "gates": [
        {
            "path": "checks.verified_completion",
            "weight": 0.30,
            "type": "boolean",
            "required": True,
            "fatal": False,
        },
        {
            "path": "checks.tests_passed",
            "weight": 0.20,
            "type": "boolean",
            "required": False,
            "fatal": False,
        },
        {
            "path": "checks.acceptance_passed",
            "weight": 0.20,
            "type": "boolean",
            "required": False,
            "fatal": False,
        },
        {
            "path": "checks.no_critical_risk",
            "weight": 0.20,
            "type": "boolean",
            "required": True,
            "fatal": True,
        },
        {
            "path": "checks.context_grounded",
            "weight": 0.10,
            "type": "boolean",
            "required": False,
            "fatal": False,
        },
    ],
    "thresholds": [
        {
            "path": "metrics.test_pass_rate",
            "weight": 0.35,
            "min": 0.95,
            "required": False,
            "fatal": False,
        },
        {
            "path": "metrics.regression_count",
            "weight": 0.35,
            "max": 0,
            "required": False,
            "fatal": False,
        },
        {
            "path": "metrics.schema_error_count",
            "weight": 0.15,
            "max": 0,
            "required": False,
            "fatal": False,
        },
        {
            "path": "metrics.critical_lint_count",
            "weight": 0.15,
            "max": 0,
            "required": False,
            "fatal": False,
        },
    ],
    "human": {
        "score_path": "human.preference_score",
        "max_path": "human.max_score",
        "default_max_score": 5,
    },
}


def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json_file(path: pathlib.Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        return []
    if path.suffix.lower() == ".jsonl":
        records = []
        for line_no, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
        return records
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("runs"), list):
        return data["runs"]
    if isinstance(data, dict):
        return [data]
    raise SystemExit(f"{path}: expected object, list, or object with runs[]")


def load_records(paths: List[str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for raw in paths:
        path = pathlib.Path(raw)
        if path.is_dir():
            files = sorted(
                [*path.rglob("*.jsonl"), *path.rglob("*.json")]
            )
        else:
            files = [path]
        for file_path in files:
            if file_path.exists():
                records.extend(load_json_file(file_path))
            else:
                raise SystemExit(f"missing input path: {file_path}")
    return records


def get_path(record: Dict[str, Any], path: str) -> Any:
    node: Any = record
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def set_path(record: Dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    node: Dict[str, Any] = record
    for part in parts[:-1]:
        child = node.get(part)
        if not isinstance(child, dict):
            child = {}
            node[part] = child
        node = child
    node[parts[-1]] = value


def numeric(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if math.isfinite(float(value)):
            return float(value)
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        return parsed if math.isfinite(parsed) else None
    return None


def derive_metrics(record: Dict[str, Any]) -> Dict[str, Any]:
    record = copy.deepcopy(record)
    metrics = record.setdefault("metrics", {})
    if not isinstance(metrics, dict):
        record["metrics"] = {}
        metrics = record["metrics"]

    if numeric(metrics.get("total_tokens")) is None:
        token_keys = [
            "input_tokens",
            "output_tokens",
            "reasoning_tokens",
            "cache_write_tokens",
            "cache_read_tokens",
            "cached_tokens",
        ]
        total = 0.0
        found = False
        for key in token_keys:
            value = numeric(metrics.get(key))
            if value is not None:
                total += value
                found = True
        if found:
            metrics["total_tokens"] = total

    if numeric(metrics.get("tool_calls")) is None and isinstance(record.get("tool_calls"), list):
        metrics["tool_calls"] = len(record["tool_calls"])

    if numeric(metrics.get("retry_count")) is None and isinstance(record.get("retries"), list):
        metrics["retry_count"] = len(record["retries"])

    if numeric(metrics.get("cost_usd")) is None and numeric(record.get("cost_usd")) is not None:
        metrics["cost_usd"] = numeric(record.get("cost_usd"))

    return record


def weighted_average(items: Iterable[Tuple[Optional[float], float]]) -> Optional[float]:
    total = 0.0
    weight_total = 0.0
    for score, weight in items:
        if score is None or weight <= 0:
            continue
        total += max(0.0, min(1.0, score)) * weight
        weight_total += weight
    if weight_total <= 0:
        return None
    return total / weight_total


def normalize_metric(value: float, spec: Dict[str, Any]) -> float:
    direction = spec.get("direction", "lower")
    if direction == "lower":
        target = float(spec.get("target", 0))
        limit = float(spec.get("limit", target))
        if value <= target:
            return 1.0
        if value >= limit or limit <= target:
            return 0.0
        return (limit - value) / (limit - target)
    if direction == "higher":
        target = float(spec.get("target", 1))
        floor = float(spec.get("floor", 0))
        if value >= target:
            return 1.0
        if value <= floor or target <= floor:
            return 0.0
        return (value - floor) / (target - floor)
    if direction == "exact":
        target = float(spec.get("target", value))
        return 1.0 if value == target else 0.0
    raise SystemExit(f"unsupported metric direction: {direction}")


def score_quantitative(record: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Optional[float], List[str], Dict[str, Any]]:
    missing: List[str] = []
    details: Dict[str, Any] = {}
    items: List[Tuple[Optional[float], float]] = []
    for spec in config.get("quantitative_metrics", []):
        path = spec["path"]
        raw_value = get_path(record, path)
        value = numeric(raw_value)
        if value is None:
            missing.append(path)
            if spec.get("required", False):
                items.append((0.0, float(spec.get("weight", 1))))
            continue
        score = normalize_metric(value, spec)
        details[path] = {
            "value": value,
            "score": score,
            "weight": spec.get("weight", 1),
        }
        items.append((score, float(spec.get("weight", 1))))
    return weighted_average(items), missing, details


def eval_boolean(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "pass", "passed", "green", "yes", "y", "1"}:
            return True
        if lowered in {"false", "fail", "failed", "red", "no", "n", "0"}:
            return False
    return None


def score_gate_specs(
    record: Dict[str, Any],
    specs: List[Dict[str, Any]],
    threshold: bool,
) -> Tuple[List[Tuple[Optional[float], float]], List[str], List[str], Dict[str, Any]]:
    items: List[Tuple[Optional[float], float]] = []
    missing: List[str] = []
    fatal_failed: List[str] = []
    details: Dict[str, Any] = {}
    for spec in specs:
        path = spec["path"]
        raw_value = get_path(record, path)
        passed: Optional[bool]
        if raw_value is None:
            missing.append(path)
            if spec.get("required", False):
                passed = False
            else:
                continue
        elif threshold:
            value = numeric(raw_value)
            if value is None:
                passed = False
            else:
                passed = True
                if "min" in spec and value < float(spec["min"]):
                    passed = False
                if "max" in spec and value > float(spec["max"]):
                    passed = False
        else:
            passed = eval_boolean(raw_value)
            if passed is None:
                passed = False

        score = 1.0 if passed else 0.0
        details[path] = {
            "value": raw_value,
            "passed": bool(passed),
            "weight": spec.get("weight", 1),
        }
        if spec.get("fatal", False) and not passed:
            fatal_failed.append(path)
        items.append((score, float(spec.get("weight", 1))))
    return items, missing, fatal_failed, details


def score_gates(record: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Optional[float], List[str], List[str], Dict[str, Any]]:
    gate_items, gate_missing, gate_fatal, gate_details = score_gate_specs(
        record, config.get("gates", []), threshold=False
    )
    threshold_items, threshold_missing, threshold_fatal, threshold_details = score_gate_specs(
        record, config.get("thresholds", []), threshold=True
    )
    details = {}
    details.update(gate_details)
    details.update(threshold_details)
    return (
        weighted_average([*gate_items, *threshold_items]),
        [*gate_missing, *threshold_missing],
        [*gate_fatal, *threshold_fatal],
        details,
    )


def score_human(record: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Optional[float], List[str], Dict[str, Any]]:
    human_config = config.get("human", {})
    score_path = human_config.get("score_path", "human.preference_score")
    max_path = human_config.get("max_path", "human.max_score")
    raw_score = get_path(record, score_path)
    score = numeric(raw_score)
    if score is None:
        return None, [score_path], {}
    max_score = numeric(get_path(record, max_path))
    if max_score is None:
        max_score = float(human_config.get("default_max_score", 5))
    if max_score <= 0:
        return None, [max_path], {}
    normalized = max(0.0, min(1.0, score / max_score))
    return normalized, [], {
        score_path: {
            "value": score,
            "max_score": max_score,
            "score": normalized,
        }
    }


def score_record(record: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    record = derive_metrics(record)
    quant_score, quant_missing, quant_details = score_quantitative(record, config)
    gate_score, gate_missing, fatal_failed, gate_details = score_gates(record, config)
    human_score, human_missing, human_details = score_human(record, config)

    weights = config.get("component_weights", {})
    final = weighted_average(
        [
            (quant_score, float(weights.get("quantitative", 0))),
            (gate_score, float(weights.get("gates", 0))),
            (human_score, float(weights.get("human", 0))),
        ]
    )
    if config.get("fatal_zero", True) and fatal_failed:
        final = 0.0

    return {
        "run_id": record.get("run_id"),
        "task_id": record.get("task_id"),
        "final_score": final,
        "final_score_pct": None if final is None else round(final * 100, 2),
        "component_scores": {
            "quantitative": quant_score,
            "gates": gate_score,
            "human": human_score,
        },
        "component_scores_pct": {
            "quantitative": None if quant_score is None else round(quant_score * 100, 2),
            "gates": None if gate_score is None else round(gate_score * 100, 2),
            "human": None if human_score is None else round(human_score * 100, 2),
        },
        "fatal_failed": fatal_failed,
        "missing": {
            "quantitative": quant_missing,
            "gates": gate_missing,
            "human": human_missing,
        },
        "details": {
            "quantitative": quant_details,
            "gates": gate_details,
            "human": human_details,
        },
    }


def load_config(path: Optional[str]) -> Dict[str, Any]:
    config = copy.deepcopy(DEFAULT_CONFIG)
    if not path:
        return config
    custom = json.loads(pathlib.Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(custom, dict):
        raise SystemExit("config must be a JSON object")
    return deep_merge(config, custom)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def human_key(record: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    return record.get("run_id"), record.get("task_id")


def merge_human_scores(records: List[Dict[str, Any]], human_records: List[Dict[str, Any]]) -> None:
    by_key: Dict[Tuple[Optional[str], Optional[str]], Dict[str, Any]] = {}
    by_run: Dict[Optional[str], Dict[str, Any]] = {}
    for human in human_records:
        if not isinstance(human, dict):
            continue
        run_id = human.get("run_id")
        task_id = human.get("task_id")
        if run_id:
            by_run[run_id] = human
        if run_id or task_id:
            by_key[(run_id, task_id)] = human

    for record in records:
        match = by_key.get(human_key(record))
        if match is None and record.get("run_id"):
            match = by_run.get(record.get("run_id"))
        if match is None:
            continue
        human = record.setdefault("human", {})
        human["preference_score"] = match.get("score", match.get("preference_score"))
        human["max_score"] = match.get("max_score", match.get("max", 5))
        if "dimensions" in match:
            human["dimensions"] = match["dimensions"]
        if "notes" in match:
            human["notes"] = match["notes"]


def mean_or_none(values: List[Optional[float]]) -> Optional[float]:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return statistics.mean(cleaned)


def pct(value: Optional[float]) -> Optional[float]:
    return None if value is None else round(value * 100, 2)


def summarize(scored: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    final_scores = [item["final_score"] for item in scored if item["final_score"] is not None]
    component_names = ["quantitative", "gates", "human"]
    component_means = {
        name: mean_or_none([item["component_scores"][name] for item in scored])
        for name in component_names
    }
    fatal_count = sum(1 for item in scored if item["fatal_failed"])
    task_ids = sorted({str(item.get("task_id")) for item in scored if item.get("task_id") is not None})
    missing_counts: Dict[str, int] = {}
    for item in scored:
        for group, fields in item["missing"].items():
            for field in fields:
                key = f"{group}:{field}"
                missing_counts[key] = missing_counts.get(key, 0) + 1

    return {
        "generated_at": utc_now_iso(),
        "run_count": len(scored),
        "task_count": len(task_ids),
        "mean_final_score": mean_or_none(final_scores),
        "mean_final_score_pct": pct(mean_or_none(final_scores)),
        "stdev_final_score": statistics.pstdev(final_scores) if len(final_scores) > 1 else 0.0,
        "min_final_score": min(final_scores) if final_scores else None,
        "max_final_score": max(final_scores) if final_scores else None,
        "component_means": component_means,
        "component_means_pct": {name: pct(value) for name, value in component_means.items()},
        "fatal_failure_count": fatal_count,
        "fatal_failure_rate": fatal_count / len(scored) if scored else None,
        "missing_counts": dict(sorted(missing_counts.items())),
        "config": config,
        "runs": scored,
    }


def print_summary(summary: Dict[str, Any]) -> None:
    print("Agent evaluation summary")
    print(f"runs: {summary['run_count']}")
    print(f"tasks: {summary['task_count']}")
    print(f"mean_final_score: {summary['mean_final_score_pct']}")
    print(f"component_means_pct: {json.dumps(summary['component_means_pct'], sort_keys=True)}")
    print(f"fatal_failure_rate: {summary['fatal_failure_rate']}")
    if summary["missing_counts"]:
        print("missing_counts:")
        for key, count in summary["missing_counts"].items():
            print(f"  {key}: {count}")


def self_test() -> None:
    records = [
        {
            "run_id": "run-001",
            "task_id": "task-001",
            "metrics": {
                "cost_usd": 0.3,
                "input_tokens": 10000,
                "output_tokens": 2000,
                "reasoning_tokens": 3000,
                "wall_time_s": 500,
                "tool_calls": 12,
                "retry_count": 0,
                "test_pass_rate": 1.0,
                "regression_count": 0,
                "schema_error_count": 0,
            },
            "checks": {
                "verified_completion": True,
                "tests_passed": True,
                "acceptance_passed": True,
                "context_grounded": True,
                "no_critical_risk": True,
            },
            "human": {"preference_score": 4, "max_score": 5},
        },
        {
            "run_id": "run-002",
            "task_id": "task-002",
            "metrics": {
                "cost_usd": 1.5,
                "total_tokens": 180000,
                "wall_time_s": 2400,
                "tool_calls": 60,
                "retry_count": 4,
                "test_pass_rate": 0.8,
                "regression_count": 2,
            },
            "checks": {
                "verified_completion": False,
                "tests_passed": False,
                "acceptance_passed": False,
                "context_grounded": False,
                "no_critical_risk": True,
            },
            "human": {"preference_score": 2, "max_score": 5},
        },
    ]
    config = load_config(None)
    scored = [score_record(record, config) for record in records]
    summary = summarize(scored, config)
    assert summary["run_count"] == 2
    assert scored[0]["final_score"] and scored[0]["final_score"] > scored[1]["final_score"]
    print_summary(summary)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Score agent evaluation run records.")
    parser.add_argument("--runs", nargs="*", help="JSON/JSONL run file(s) or directories.")
    parser.add_argument("--human-scores", nargs="*", help="Optional human score JSON/JSONL files.")
    parser.add_argument("--config", help="Optional JSON config overriding default weights and metric specs.")
    parser.add_argument("--out", help="Optional path to write full JSON summary.")
    parser.add_argument("--print-default-config", action="store_true", help="Print default config JSON and exit.")
    parser.add_argument("--self-test", action="store_true", help="Run a built-in smoke test.")
    args = parser.parse_args(argv)

    if args.print_default_config:
        print(json.dumps(DEFAULT_CONFIG, indent=2, sort_keys=True))
        return 0

    if args.self_test:
        self_test()
        return 0

    if not args.runs:
        parser.error("--runs is required unless --print-default-config or --self-test is used")

    config = load_config(args.config)
    records = load_records(args.runs)
    if args.human_scores:
        merge_human_scores(records, load_records(args.human_scores))
    scored = [score_record(record, config) for record in records]
    summary = summarize(scored, config)
    print_summary(summary)
    if args.out:
        out_path = pathlib.Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
