# Run Record Schema

## File Format

Use JSONL for repeated runs. Each line is one run record. A JSON file may contain either a single object or:

```json
{
  "runs": []
}
```

## Minimal Run Record

```json
{
  "run_id": "run-001",
  "task_id": "task-001",
  "metrics": {
    "cost_usd": 0.42,
    "input_tokens": 12000,
    "output_tokens": 2400,
    "reasoning_tokens": 8000,
    "total_tokens": 22400,
    "wall_time_s": 480,
    "tool_calls": 18,
    "retry_count": 1,
    "test_pass_rate": 1.0,
    "regression_count": 0,
    "schema_error_count": 0
  },
  "checks": {
    "verified_completion": true,
    "tests_passed": true,
    "acceptance_passed": true,
    "context_grounded": true,
    "no_critical_risk": true,
    "no_unverified_done_claim": true
  },
  "trace_ref": "traces/run-001.md",
  "result_ref": "outputs/task-001.md"
}
```

## Human Score Record

`scripts/record_human_score.py` appends JSONL records like:

```json
{
  "timestamp": "2026-07-08T12:00:00Z",
  "run_id": "run-001",
  "task_id": "task-001",
  "score": 4,
  "max_score": 5,
  "dimensions": {
    "usefulness": 4,
    "trust": 5
  },
  "artifact": "traces/run-001.md",
  "notes": "Clear answer with minor verbosity."
}
```

`scripts/score_runs.py --human-scores human_scores.jsonl` merges these records into matching run records.

## Metric Naming Rules

Prefer stable names:

- `metrics.cost_usd`
- `metrics.total_tokens`
- `metrics.wall_time_s`
- `metrics.tool_calls`
- `metrics.retry_count`
- `metrics.test_pass_rate`
- `metrics.regression_count`
- `checks.verified_completion`
- `checks.tests_passed`
- `checks.acceptance_passed`
- `checks.no_critical_risk`

If `metrics.total_tokens` is missing, the scoring script derives it from known token fields when possible.
