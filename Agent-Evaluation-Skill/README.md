# Agent Evaluation Skill

`agent-evaluation` is a Codex skill for building repeatable evaluation frameworks for vertical-domain agents and task-specific agents.

It separates agent performance evaluation into three evidence layers:

1. Exact quantitative metrics that can be counted or measured directly.
2. Gate, threshold, boolean, and red/yellow/green metrics that can be judged by pass rate across repeated task runs.
3. Human preference metrics that should expose traces and artifacts for manual scoring instead of pretending to be fully objective.

The default final score is weighted but configurable:

```text
final_score =
  0.35 * quantitative_score
+ 0.45 * gate_pass_score
+ 0.20 * human_preference_score
```

## Repository Layout

```text
agent-evaluation/
  SKILL.md
  agents/
    openai.yaml
  references/
    human-preference.md
    metric-taxonomy.md
    run-record-schema.md
    task-suite-design.md
  scripts/
    record_human_score.py
    score_runs.py
    validate_skill.py
```

## Install

Install this skill into Codex from GitHub:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo 222222222l/Agent-Evaluation-Skill \
  --path agent-evaluation
```

On Windows, if `python` is not on `PATH`, use the Python runtime bundled with Codex:

```powershell
& "C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" `
  "C:\Users\Administrator\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo 222222222l/Agent-Evaluation-Skill `
  --path agent-evaluation
```

Restart Codex after installing new skills.

## Use

Ask Codex to use the skill:

```text
Use $agent-evaluation to design an evaluation framework for this coding agent.
```

Typical outputs include:

- task-suite design
- run-record schema
- exact metric definitions
- gate and threshold definitions
- human preference rubric
- weighted scoring formula
- validation and reporting plan

## Run Record Format

The scoring script accepts JSON or JSONL run records. A minimal record looks like:

```json
{
  "run_id": "run-001",
  "task_id": "task-001",
  "metrics": {
    "cost_usd": 0.42,
    "input_tokens": 12000,
    "output_tokens": 2400,
    "reasoning_tokens": 8000,
    "wall_time_s": 480,
    "tool_calls": 18,
    "retry_count": 1,
    "test_pass_rate": 1.0,
    "regression_count": 0
  },
  "checks": {
    "verified_completion": true,
    "tests_passed": true,
    "acceptance_passed": true,
    "context_grounded": true,
    "no_critical_risk": true
  },
  "human": {
    "preference_score": 4,
    "max_score": 5
  }
}
```

## Score Runs

Run the built-in smoke test:

```bash
python agent-evaluation/scripts/score_runs.py --self-test
```

Score real runs:

```bash
python agent-evaluation/scripts/score_runs.py --runs path/to/runs --out summary.json
```

Print the default scoring configuration:

```bash
python agent-evaluation/scripts/score_runs.py --print-default-config > agent_eval_config.json
```

Use a customized scoring configuration:

```bash
python agent-evaluation/scripts/score_runs.py \
  --runs path/to/runs \
  --config agent_eval_config.json \
  --out summary.json
```

## Record Human Scores

Interactive review:

```bash
python agent-evaluation/scripts/record_human_score.py \
  --artifact path/to/trace.md \
  --run-id run-001 \
  --task-id task-001 \
  --out human_scores.jsonl
```

Non-interactive score recording:

```bash
python agent-evaluation/scripts/record_human_score.py \
  --run-id run-001 \
  --task-id task-001 \
  --score 4 \
  --max-score 5 \
  --notes "Good result with minor verbosity." \
  --out human_scores.jsonl
```

Merge human scores into final scoring:

```bash
python agent-evaluation/scripts/score_runs.py \
  --runs path/to/runs \
  --human-scores human_scores.jsonl
```

## Validate

The skill includes a validation script that uses only the Python standard library:

```bash
python agent-evaluation/scripts/validate_skill.py agent-evaluation
```

The helper compiles bundled scripts, checks required skill metadata, verifies referenced files, and validates the UI metadata file.

## Design Notes

- Keep objective telemetry, threshold gates, and human preference scores separate until final aggregation.
- Use fatal gates for severe failures such as data loss, security leakage, fabricated verification, or unsafe irreversible actions.
- Aggregate by task before aggregating across the suite when tasks have repeated stochastic runs.
- Always report component scores next to the final weighted score.
