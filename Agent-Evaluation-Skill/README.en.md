# Agent Evaluation Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `Agent-Evaluation-Skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

`agent-evaluation` designs and aggregates repeatable evaluations for domain-specific and task-oriented agents. It separates direct measurements, acceptance gates, and human preferences, preserving task/run records before transparent aggregation.

This is an evaluation workflow and scoring toolkit, not a validated universal agent leaderboard. Task suites, weights, and human rubrics need calibration for their intended setting.

## Evidence layers

| Layer | Examples | Interpretation |
| --- | --- | --- |
| Quantitative telemetry | Cost, tokens, time, tool calls, retries | Consistent collection is required; missing values are not zero |
| Acceptance gates | Verified completion, tests, regressions, critical risks | Require reviewable evidence or independent checks |
| Human preference | Readability and practical suitability | Preserve artifacts and rubrics; not fully objective |

The default aggregate is `0.35 × quantitative + 0.45 × gates + 0.20 × human preference`. These are configurable defaults, not a validated universal utility function. Report components, sample counts, and critical failures alongside totals. An average must not hide a severe failure.

## Install and use

Install `agent-evaluation/` in the host's supported Skill directory, then invoke:

```text
Use $agent-evaluation to define a task suite, run records,
acceptance gates, a human rubric, and explicit aggregation rules.
```

Inputs are JSON/JSONL run records with `run_id`, `task_id`, `metrics`, `checks`, and `human`. See the [record contract](agent-evaluation/references/run-record-schema.md). Aggregate repeated runs by task before aggregating the suite.

## Commands

From the repository root:

```bash
python agent-evaluation/scripts/score_runs.py --self-test
python agent-evaluation/scripts/score_runs.py --print-default-config > agent_eval_config.json
python agent-evaluation/scripts/score_runs.py --runs path/to/runs --config agent_eval_config.json --out summary.json
python agent-evaluation/scripts/record_human_score.py --artifact path/to/trace.md --run-id run-001 --task-id task-001 --out human_scores.jsonl
python agent-evaluation/scripts/score_runs.py --runs path/to/runs --human-scores human_scores.jsonl
python agent-evaluation/scripts/validate_skill.py agent-evaluation
```

Human scores can also be recorded non-interactively with `--score`, `--max-score`, and `--notes`. Structural checks and self-tests do not establish cross-task validity.

## Method and evidence

- [SKILL.md](agent-evaluation/SKILL.md)
- [Task-suite design](agent-evaluation/references/task-suite-design.md)
- [Metric taxonomy](agent-evaluation/references/metric-taxonomy.md)
- [Human preference](agent-evaluation/references/human-preference.md)

Agent/Skill comparisons should fix tasks and resource conditions, repeat stochastic runs, retain failures, and use acceptance tasks withheld from development. A higher score without those controls does not establish general capability improvement.

No top-level `LICENSE` is currently supplied.
