---
name: agent-evaluation
description: Build and run evaluation frameworks for vertical-domain agents and task-specific agents. Use when Codex needs to define agent performance metrics, split exact quantitative metrics from threshold/gate checks and human preference scoring, design multi-run eval datasets, expose traces for manual scoring, compute weighted final scores, or create reusable scripts for LLM/agent evaluation.
---

# Agent Evaluation

## Core Rule

Evaluate agents in three layers:

1. Exact quantitative metrics: count or measure directly, then normalize and average across runs.
2. Gate and threshold metrics: judge with booleans, red/yellow/green rules, or fixed thresholds, then report pass rates across a task suite.
3. Human preference metrics: expose trace and result, ask a human to score, and record the score without pretending it is objective.

Use a weighted final score only after each layer's evidence is preserved. Never hide fatal failures behind a high average.

## Default Formula

Use this default unless the project has better domain weights:

```text
final_score =
  0.35 * quantitative_score
+ 0.45 * gate_pass_score
+ 0.20 * human_preference_score
```

Within the script config, all component weights and individual metric weights are customizable. For high-risk domains, increase gate weight and enable fatal gates. For consumer-facing assistants, increase human preference weight after objective safety and correctness gates pass.

## Workflow

1. Define the agent scope: vertical domain, target users, task types, allowed tools, non-goals, and unacceptable failures.
2. Read `references/metric-taxonomy.md` to classify metrics into exact, gate/threshold, and human-preference layers.
3. Read `references/task-suite-design.md` to build a representative multi-run eval set.
4. Instrument runs using the schema in `references/run-record-schema.md`.
5. Run automated scoring with `scripts/score_runs.py`.
6. For subjective dimensions, read `references/human-preference.md`, expose trace packets, and record human scores with `scripts/record_human_score.py`.
7. Report the weighted score, component scores, fatal failures, confidence limits, and the top failure modes.

## Scripts

Score a directory or file of JSON/JSONL run records:

```bash
python scripts/score_runs.py --runs path/to/runs --out summary.json
```

Print the default scoring config for customization:

```bash
python scripts/score_runs.py --print-default-config > agent_eval_config.json
```

Record a human score after reviewing a trace or result artifact:

```bash
python scripts/record_human_score.py --artifact path/to/trace.md --run-id run-001 --task-id task-001 --out human_scores.jsonl
```

Merge recorded human scores into automated scoring:

```bash
python scripts/score_runs.py --runs path/to/runs --human-scores human_scores.jsonl --config agent_eval_config.json
```

Validate this skill folder without external Python packages:

```bash
python scripts/validate_skill.py .
```

## Required Outputs

Every serious evaluation should produce:

- Task-suite description and sampling rationale.
- Raw run records.
- Automated score summary.
- Human preference records when subjective quality matters.
- Failure taxonomy with examples.
- Final weighted score plus component scores.
- Explicit statement of missing metrics and residual risk.

## References

- `references/metric-taxonomy.md`: metric layers, default weights, fatal gates, and normalization guidance.
- `references/task-suite-design.md`: vertical task-suite construction, repeated-run protocol, and release gates.
- `references/run-record-schema.md`: JSON/JSONL schema consumed by the scripts.
- `references/human-preference.md`: trace exposure, manual rating rubric, and score recording rules.
