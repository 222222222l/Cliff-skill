---
name: model-causes-and-decisions
description: >-
  Model ambiguous phenomena, events, causal claims, attribution questions,
  forecasts, and action choices with explicit system structure, estimands,
  counterfactuals, uncertainty, falsification, and decision rules. Run the
  requested workflow when the user invokes $model-causes-and-decisions or
  explicitly asks for "使用建模分析", "建模分析", "数学建模", "建模方法", or
  equivalent modeling analysis. When a task merely appears suitable and modeling
  was not explicitly requested, use recommendation-only mode: name a specific
  applicable methodology, why it fits, required evidence, and limits; do not
  execute the full workflow until the user confirms. Use across business, policy,
  operations, science, markets, and personal planning; distinguish prediction,
  model attribution, and causal effect.
---

# Model Causes and Decisions

## Purpose

Convert a visible phenomenon into the smallest falsifiable model that can improve a
decision. Seek the mechanism behind the observation, but do not force causal or
numeric certainty beyond the evidence.

## Invocation Boundary

Determine the mode before applying the methodology.

### Explicit Execution

Treat the Skill as explicitly selected when the user:

- invokes `$model-causes-and-decisions`;
- asks to use `使用建模分析`, `建模分析`, `数学建模`, `建模方法`, or an
  equivalent phrase in another language;
- directly requests a mathematical, causal, attribution, or decision model.

Apply the workflow to the scope the user requested. Explicit selection permits use of
the Skill; it does not permit inventing missing data or expanding the decision scope.
If the user asks only for method selection, recommend methods rather than performing
an unsolicited full analysis.

### Implicit Recommendation Only

When the situation appears suitable but the user did not explicitly request modeling,
do not execute the Core Workflow. Recommend one primary method and at most one
alternative, then return control to the user. State concisely:

```text
Recommended method:
Why it fits:
What it would estimate or clarify:
Minimum evidence required:
What it cannot establish:
Choice: proceed, compare methods, or stay qualitative
```

Do not calculate a complete attribution, build the full evidence ledger, or make a
final causal or action claim in this mode. Ask whether the user wants to proceed with
the recommendation. If another domain Skill owns the substantive request, let it
answer within its own scope and keep this recommendation optional.

## Non-Negotiable Rules

1. Start from the decision, not from an impressive method.
2. Separate `observed`, `estimated`, `assumed`, and `scenario` quantities.
3. Distinguish detection, description, prediction, model attribution, causal effect,
   counterfactual analysis, and decision. They answer different questions.
4. Define the counterfactual before claiming impact: what would have happened to
   the same target, over the same horizon, without the event or action?
5. Treat a formula as a claim made explicit, not as evidence that the claim is true.
6. Never call correlation, abnormal deviation, regression weight, SHAP value, or
   sensitivity index a causal contribution without an identification argument.
7. Do not force contributions to sum to 100% unless an accounting identity or a
   declared model decomposition justifies it. Preserve interactions and residuals.
8. Prefer ranges, bounds, and scenario weights to unsupported point estimates.
9. Keep at least one credible rival hypothesis and name evidence that would favor it.
10. Turn uncertainty into action design: smaller exposure, reversibility, staging,
    information gathering, stop conditions, and update triggers.

## Core Workflow

### 1. Frame the Decision

State:

- the decision and available actions;
- target outcome `Y`, unit of analysis, horizon, and decision deadline;
- event or intervention `E`, exposure, and event time if known;
- the minimum effect that would change the decision;
- constraints, loss asymmetry, reversibility, and cost of waiting.

Classify the request as one or more of:

```text
detect -> describe -> predict -> explain-model -> causal -> counterfactual -> decide
```

Do not silently answer a causal question with a predictive model.

### 2. Model the System Before the Statistic

Map actors, incentives, actions, state variables, flows, constraints, information,
and external shocks. Use the minimal dynamic skeleton:

```text
a[i,t] ~= argmax_a E[U_i(a, S_t) | information_i, constraints_i]
S[t+1] = F(S[t], a[1:n,t], Z[t]) + process_error[t]
Y[t]   = G(S[t]) + measurement_error[t]
```

Then write the shortest plausible transmission chain:

```text
driver -> actor response -> mechanism -> state or flow -> outcome -> feedback
```

Separate stock from flow, expectation from realized action, first-round effects from
feedback, and binding constraints from background conditions.

### 3. Build Competing Hypotheses

Include a baseline or noise hypothesis, the preferred mechanism, and at least one
credible alternative. For each hypothesis, record:

- mechanism and required assumptions;
- observations it predicts before seeing the result;
- evidence that discriminates it from rivals;
- evidence that would invalidate or materially weaken it.

Use Bayesian updating for beliefs when calibrated frequencies are unavailable, but
label probabilities as empirical, model-implied, or judgmental scenario weights.

### 4. Pass the Identification Gate

Check temporal order, measurement validity, consistency, comparable support,
confounding or parallel trends, anticipation, spillovers, concurrent events, and
selection into exposure. Assign the strongest defensible claim level:

| Level | Permitted claim |
| --- | --- |
| `I0` | Narrative or scenario only; direction may be unknown |
| `I1` | Descriptive or accounting difference |
| `I2` | Associational, predictive, or model attribution |
| `I3` | Design-supported causal estimate under explicit assumptions |
| `I4` | Causal estimate corroborated by robustness, mechanism, or replication |

If a material gate fails, downgrade the claim. Use sensitivity analysis, partial
identification, or scenarios instead of manufacturing a point estimate.

### 5. Select the Minimum Sufficient Method

Read [methods.md](references/methods.md) when choosing a mathematical method or
making a quantitative attribution or causal claim. Route by question and data shape,
not by familiarity:

- unknown event time -> change-point detection;
- known event time and expected baseline -> event study or interrupted time series;
- staggered treatment with comparison units -> group-time difference-in-differences;
- multi-factor causal mechanism -> DAG/structural causal model plus an estimand;
- predictive model explanation -> Shapley attribution;
- nonlinear parameter influence -> global sensitivity analysis;
- weak identification -> sensitivity analysis or identified bounds;
- belief revision -> Bayesian update;
- action choice -> expected utility, regret, and value of information.

Use a more complex method only if it can change the decision or reduce a material
failure risk.

### 6. Quantify and Stress-Test

Define variables, units, equations, data lineage, estimator, and assumptions. Report
sampling, measurement, model, identification, and scenario uncertainty separately.

Run the checks applicable to the design: placebo dates or groups, pre-trends,
negative controls, alternative baselines, lag and window changes, holdout or
walk-forward tests, parameter ranges, omitted-confounder sensitivity, and rival
mechanisms. Do not average genuine contradictions into false neutrality.

### 7. Convert the Model Into Action

Choose actions by expected utility under constraints, not by the most likely story
alone. Compare base, upside, downside, and ruin or irreversibility paths. Seek more
information only when its expected value exceeds its cost and delay.

For every recommendation, state:

- action, size or intensity, timing, and reversibility;
- expected benefit, cost, downside, and confidence source;
- assumptions that the action depends on;
- leading indicators, invalidation conditions, and switch or stop triggers.

When uncertainty is high, favor staged experiments and options that preserve future
choices.

## Output Contract

Lead with the decision-relevant conclusion, then provide:

1. **Question and claim type**: outcome, unit, horizon, estimand, and claim level.
2. **Essence**: one sentence naming the binding constraint, incentive, mechanism,
   and feedback that best explains the phenomenon.
3. **Model**: variables, causal or system structure, counterfactual, and equations.
4. **Evidence ledger**: observations, estimates, assumptions, and scenarios.
5. **Result**: effect, attribution, range or posterior, with correct interpretation.
6. **Challenge**: strongest rival explanation, failed gates, and falsification tests.
7. **Action**: decision rule, exposure, update signals, invalidation, and next review.

Match depth to the decision. A short qualitative analysis may need only one equation;
a high-stakes causal claim requires the full identification and sensitivity record.

## Validation

Use [evaluation-cases.md](references/evaluation-cases.md) only when testing or
revising this Skill. Do not claim that this candidate improves downstream task
performance until it passes paired representative evaluations against a no-Skill or
current-Skill baseline.
