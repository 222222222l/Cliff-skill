# Metric Taxonomy

## Purpose

Use this reference to decide which parts of an agent evaluation can be scored automatically, which should be judged by pass-rate gates, and which must be left to human preference.

## Layer 1: Exact Quantitative Metrics

Use exact metrics when the value comes from logs, bills, telemetry, test output, or execution traces.

Common metrics:

- Cost: token cost, tool/API cost, code execution cost, platform markup, cache read/write cost.
- Usage: input tokens, output tokens, reasoning tokens, cached tokens, context length used.
- Process counts: tool calls, edit attempts, patch attempts, failed commands, retries, user interventions.
- Time: wall-clock duration, tool latency, test duration, time to first valid answer, time to verified completion.
- Code/test artifacts: files changed, diff lines, tests run, tests passed, coverage percentage, regression count.

Default exact-metric subweights:

```text
quantitative_score =
  0.25 * cost_efficiency
+ 0.25 * token_efficiency
+ 0.20 * time_efficiency
+ 0.15 * tool_efficiency
+ 0.15 * retry_efficiency
```

Normalize lower-is-better metrics with a target and a limit:

```text
score = 1.0                         when value <= target
score = 0.0                         when value >= limit
score = (limit - value)/(limit-target) otherwise
```

Use multiple runs when outputs are stochastic. Report mean, standard deviation, min, max, and outliers.

## Layer 2: Gates, Thresholds, and Red-Light Metrics

Use gates when a metric is not meaningfully continuous but has a common pass/fail standard.

Common boolean gates:

- verified_completion: the task was actually completed.
- tests_passed: relevant automated tests passed.
- acceptance_passed: written acceptance criteria passed.
- context_grounded: the answer or edit cites/uses the right source context.
- no_critical_risk: no data loss, security issue, policy violation, or destructive action.
- no_unverified_done_claim: the agent did not claim completion without evidence.

Common threshold gates:

- unit_test_pass_rate >= 0.95
- regression_count == 0
- schema_error_count == 0
- critical_lint_count == 0
- citation_coverage >= required project threshold
- retrieval_precision_at_k >= required domain threshold

Default gate score:

```text
gate_pass_score = weighted_passed_gates / weighted_applicable_gates
```

Use fatal gates for failures that should zero the run regardless of averages:

- data loss
- security leakage
- unsafe external action
- fabricated verification
- wrong irreversible transaction
- severe domain harm in medical, legal, financial, or infrastructure tasks

## Layer 3: Human Preference Metrics

Use human scoring when the evaluation is about taste, communication style, helpfulness, trust, perceived seniority, product sense, or aesthetics.

Do not convert these into fake objective measures. Instead:

1. Expose the trace and final artifact.
2. Ask the human to score with a fixed rubric.
3. Store the score and reviewer notes.
4. Keep it separate from exact and gate layers until final weighted aggregation.

Default subjective dimensions:

- usefulness
- trustworthiness
- clarity
- interaction burden
- domain taste or product judgment

## Default Final Score

Use this starting point:

```text
final_score =
  0.35 * quantitative_score
+ 0.45 * gate_pass_score
+ 0.20 * human_preference_score
```

Adjust weights by domain:

- Coding agents: 0.30 quantitative, 0.55 gates, 0.15 human.
- Research agents: 0.25 quantitative, 0.45 gates, 0.30 human.
- High-risk operational agents: 0.20 quantitative, 0.70 gates, 0.10 human.
- Creative agents: 0.20 quantitative, 0.25 gates, 0.55 human.

Always report component scores next to the final score.
