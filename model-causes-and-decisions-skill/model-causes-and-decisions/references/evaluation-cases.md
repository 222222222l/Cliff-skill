# Evaluation Cases

Use this file only to validate or revise the Skill. Keep authoring and evaluation
trajectories separate when possible.

## Candidate Contract

```yaml
candidate_id: model-causes-and-decisions@0.1.0
kind: skill
scope: cross-domain event, causal, attribution, judgment, and action analysis
applicability: a phenomenon must be modeled to support a judgment or action
incompatible_versions: []
source: repo-local candidate; record immutable revision and hash before promotion
inputs: [question, evidence, decision context]
expected_artifacts: [model, claim level, uncertainty, falsification, action rule]
validator: quick_validate.py plus representative behavior cases
known_failure_modes: [false causality, false precision, model-world attribution confusion]
permissions: []
fast_path: frame -> system map -> identification -> minimum method -> action
fallback: baseline reasoning with explicit uncertainty and no unsupported causal claim
stop_conditions: [missing decision-critical evidence, unidentifiable causal estimand]
evidence_state: internally-valid
```

After structural and behavior smoke checks, the candidate may be called
`internally-valid`. Do not call it `downstream-proven` without paired repeated trials
against the baseline on a representative dataset.

## Current Smoke Evidence

Tested on 2026-08-08 in the current Codex desktop harness. The exact deployment alias
was not exposed. Each case ran once in a fresh context with the candidate Skill and no
file-writing authority.

| Case | Result | Material evidence |
| --- | --- | --- |
| Confounded algorithm launch | Pass | Refused a causal percentage, declared `I1`, exposed the missing counterfactual and interactions, and proposed a reversible controlled rollout with guardrails |
| High-loss supplier decision | Pass | Calculated the replacement threshold and information-value ceiling, challenged the probability calibration, and recommended a staged action with explicit switch conditions |
| Explicit `数学建模` request | Pass | Activated the full requested scope, selected group-time DiD, defined the counterfactual and identification checks, and produced a conditional rollout rule |
| Implicit scenario fit | Pass | Recommended interrupted time series plus an optional DiD design, stated evidence and limits, and returned the proceed-or-not choice without completing causal attribution |

Fatal failures: `0`. Structural validation: pass. Trigger-boundary cases were rerun
after the 2026-08-08 invocation-policy change. This is internal smoke evidence only:
there was no no-Skill baseline, repeated trial, held-out suite, calibrated grader,
cost comparison, or transfer test.

## Behavior Constraints

The evaluator should mark each applicable rule `pass`, `fail`, or
`insufficient-evidence`.

1. Define decision, outcome, unit, horizon, and claim type before selecting a method.
2. Distinguish observation, model attribution, and causal effect.
3. State a counterfactual and identification limits for causal language.
4. Select the minimum method that fits event timing and data shape.
5. Preserve residuals, interactions, and rival explanations.
6. Label probability provenance and avoid arbitrary precision.
7. Convert the conclusion into a bounded action and observable update triggers.
8. Abstain from a causal point estimate when a material identification gate fails.
9. Execute the requested modeling scope after explicit Skill or keyword selection.
10. When selected only by scenario fit, recommend a concrete method and return the
    decision to the user without running the full workflow.

## Smoke Cases

### Case 1: Sparse One-Off Event

Prompt: "A competitor cut prices and our sales fell 12%. What percentage of the fall
did the price cut cause?"

Expected: define product, market, horizon, exposure, baseline, concurrent changes, and
comparison options; refuse a causal percentage from before-after data; propose a DAG,
comparison design, bounds or scenarios, and evidence that would discriminate causes.

Fatal failure: assigning causal shares that sum to 100% from the single observation.

### Case 2: Staggered Policy Rollout

Prompt: "A policy started in different cities in different months. Estimate its effect
on employment."

Expected: define `ATT(g,t)`, use group-time DiD, inspect anticipation and pre-trends,
declare comparison groups and aggregation weights, and test spillovers.

Fatal failure: treating one heterogeneous two-way fixed-effects coefficient as the
effect without qualification.

### Case 3: Prediction Explanation

Prompt: "Our churn model assigns 0.82 risk. Which features caused the customer to
churn?"

Expected: reframe SHAP or similar output as model attribution; disclose baseline,
background data, correlated features, and feature grouping; separate predictive
explanation from real-world intervention effects.

Fatal failure: calling feature attributions causal effects.

### Case 4: Unknown Break Time

Prompt: "Latency became unstable, but we do not know when or why. Find the event."

Expected: detect a change point first, report false-alarm and delay assumptions, then
test deployments, load, dependencies, and measurement changes as competing causes.

Fatal failure: equating the detected break date with a proven cause.

### Case 5: Market Announcement

Prompt: "Did an earnings announcement add 6% to the stock price?"

Expected: define estimation and event windows, expected-return baseline, abnormal
return and CAR, leakage, market or sector moves, and concurrent disclosures; label the
result abnormal deviation unless stronger identification exists.

Fatal failure: treating raw return or CAR as an identified causal effect.

### Case 6: High-Stakes Action

Prompt: "There is a 60% chance a supplier fails. Should we replace it now?"

Expected: label the probability source, model failure and non-failure payoffs,
transition and delay costs, correlated supplier risk, reversibility, expected utility,
regret, and value of additional information; recommend staged or hedged action when
appropriate.

Fatal failure: choosing solely because 60% exceeds 50%.

### Case 7: Weak Identification

Prompt: "The regression coefficient is significant after many controls, so the
program works. Confirm the causal effect."

Expected: identify treatment, outcome, estimand, selection and post-treatment control
risks; request a design argument; benchmark omitted-confounder sensitivity and report
bounds or an associational claim if identification fails.

Fatal failure: equating statistical significance or control count with causality.

### Case 8: Small Reversible Experiment

Prompt: "Evidence is weak but waiting is costly. What should we do next?"

Expected: state rival hypotheses and the decision threshold; choose a bounded,
reversible probe that produces discriminating evidence; define exposure, stop loss,
success threshold, and update time.

Fatal failure: recommending full irreversible commitment or endless research without
comparing information value and delay cost.

### Case 9: Explicit Keyword Selection

Prompt: "请使用数学建模分析门店错峰延长营业时间对销售额和利润的影响，并给出是否推广的判断。"

Expected: treat `数学建模` as explicit selection; define the decision, unit, horizon,
estimand, counterfactual, staggered design, uncertainty, and action threshold. Execute
the requested workflow rather than merely offering a generic method menu.

Fatal failure: failing to activate, or returning only an invitation to use the Skill.

### Case 10: Implicit Scenario Fit

Prompt: "Customer complaints doubled after a release, while traffic and staffing also
changed. Tell me what you think."

Selection context: the harness selected this Skill because the scenario appears
suitable; the user did not explicitly request modeling.

Expected: recommend a concrete primary method such as interrupted time series with a
causal DAG and comparison series; state why it fits, required evidence, and what it
cannot establish; ask whether to proceed. Do not execute the complete attribution or
make the final causal decision.

Fatal failure: silently running the full workflow or presenting a final causal share
or action without user confirmation.

## Review Record

Record the tested system, task version, trials, grader, budgets, behavior coverage,
unsupported claims, fatal failures, cost, and result. Keep `task success` separate
from `Skill behavior coverage`. A passing author review is smoke evidence only.
