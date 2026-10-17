# Task Suite Design

## Goal

Build an evaluation set that represents the vertical agent's real work, not a generic reasoning benchmark.

## Task Contract

For each task, define:

- task_id
- domain and task type
- user request
- available context and tools
- expected deliverable
- acceptance criteria
- unacceptable failures
- required evidence
- scoring gates
- human-review dimensions, if any

## Sampling Mix

Use this default distribution:

- 60% common path: normal work the agent should perform every day.
- 25% edge path: ambiguous, incomplete, noisy, multi-file, long-context, or tool-heavy work.
- 15% risk path: adversarial-ish, irreversible, expensive, security-sensitive, or hallucination-prone work.

For small pilots, start with 20 to 30 tasks. For production release gates, prefer 100+ tasks or a smaller set run repeatedly with strong coverage of failure modes.

## Repeated-Run Protocol

Run each task multiple times when the agent is stochastic or tool state changes.

Suggested defaults:

- deterministic code task: 1 to 3 runs
- LLM-heavy semantic task: 3 to 5 runs
- high-risk agent workflow: 5+ runs with fixed seeds or fixed input snapshots when possible

Aggregate by task first, then across the suite. This prevents one task with many retries from dominating the score.

## Evaluation Modes

Use exact automation when:

- logs contain the metric
- tests or validators can run
- schema or output format is deterministic
- the expected answer can be checked mechanically

Use gate/threshold checks when:

- a common pass/fail standard exists
- a threshold can be defended before the run
- red/yellow/green status is more meaningful than a continuous score

Use human review when:

- quality depends on taste, judgment, trust, or communication
- there are multiple acceptable answers
- the artifact is product, design, strategy, or narrative-heavy

## Release Gate Template

Example for a coding agent:

```text
verified_completion >= 0.85
fatal_failure_rate == 0
regression_count == 0 on release candidates
tests_passed >= 0.95 where tests exist
cost_per_verified_task <= 1.25x baseline
human_preference_score >= 0.70 for reviewed tasks
```

Example for a research agent:

```text
answer_grounded >= 0.90
citation_accuracy >= 0.95
unsupported_claim_rate <= 0.05
fatal_failure_rate == 0
human_usefulness_score >= 0.75
```

## Reporting

Always report:

- task count and run count
- sampling mix
- component scores
- final weighted score
- fatal failures
- top recurring failure modes
- cost per verified task
- confidence notes and missing evidence
