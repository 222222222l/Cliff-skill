# Mathematical Method Router

## Contents

- Universal model skeleton
- Claim and method router
- Causal identification
- Event and time-series analysis
- Attribution and sensitivity
- Bayesian judgment
- Decision and action
- Failure modes
- Research basis

## Universal Model Skeleton

Start with a decision-relevant target, not a free-floating equation.

```text
Observed phenomenon: O
Latent system state: S
Actors and actions: a_i
Constraints: C
External drivers: Z
Outcome: Y
Decision: d
```

Represent the system as:

```text
a[i,t] ~= argmax_a E[U_i(a, S_t) | I_i, C_i]
S[t+1] = F(S[t], a[1:n,t], Z[t]) + epsilon[t]
Y[t]   = G(S[t]) + nu[t]
```

This is a thinking scaffold, not an estimable model until variables, data, and
assumptions are specified. Its purpose is to expose incentives, constraints,
transmission, feedback, and measurement error.

For an observed change, keep the decomposition honest:

```text
Delta Y_observed
  = Delta Y_baseline
  + event_effect
  + concurrent_shocks
  + interactions
  + measurement_or_model_error
```

Only an identification design can separate these terms. If the design cannot, keep
them as competing explanations or bounds.

## Claim and Method Router

| Question | Preferred first method | Valid output | Main boundary |
| --- | --- | --- | --- |
| Did the generating process change? | Change-point detection | Break probability or date | A break does not identify its cause |
| Was an outcome abnormal around a known date? | Event study | Abnormal deviation over a window | Confounding and anticipation remain |
| Did staggered exposure cause an effect? | Group-time DiD | `ATT(g,t)` and aggregation | Needs defensible parallel trends and overlap |
| What would happen under an intervention? | DAG/SCM or potential outcomes | Intervention estimand or bound | Needs an identification argument |
| Why did a model produce this value? | Shapley attribution | Contribution to model output | Not automatically a real-world cause |
| Which uncertain inputs drive model variance? | Sobol/global sensitivity | Main and total sensitivity | Depends on input ranges and distributions |
| How should belief change with evidence? | Bayesian update | Posterior or odds | Prior and likelihood must be declared |
| What should be done? | Expected utility and regret | Action under loss and constraints | Preferences are not learned from facts alone |

When the question mixes rows, execute them in dependency order. For example:
detect a break, identify a plausible cause, estimate an effect, then choose an action.

## Causal Identification

### Potential Outcomes

Define treatment `D`, potential outcomes `Y(1)` and `Y(0)`, and an estimand before
choosing an estimator:

```text
Y = D * Y(1) + (1 - D) * Y(0)
ATE = E[Y(1) - Y(0)]
ATT = E[Y(1) - Y(0) | D = 1]
```

Audit consistency, no material interference, exchangeability or a substitute design,
and positivity. The missing counterfactual is the central problem; regression does
not make it disappear.

### Structural Causal Models

Use a time-directed DAG to separate causes, mediators, confounders, colliders, and
outcomes. Observational and interventional quantities differ:

```text
P(Y | X = x) != P(Y | do(X = x))
```

When `Z` is a valid backdoor adjustment set:

```text
P(y | do(x)) = sum_z P(y | x, z) P(z)
```

Name the adjustment set and explain why it blocks non-causal paths without blocking
the effect of interest. If no defensible adjustment or design exists, report bounds,
sensitivity, or scenario direction instead of a causal point estimate.

### Identification Gate

Require evidence for the material items:

1. treatment or event precedes the outcome;
2. treatment, outcome, exposure, and unit are measured consistently;
3. comparison units or histories support the relevant counterfactual;
4. no unaddressed confounder, anticipation, spillover, or concurrent event dominates;
5. model specification and sample selection do not use future information;
6. the estimand matches the user's decision.

Failing a gate changes the permitted claim, not merely the confidence adjective.

## Event and Time-Series Analysis

### Known Event Time

For a financial or analogous event study:

```text
AR[i,t] = Y[i,t] - E[Y[i,t] | baseline_information]
CAR[i,t1,t2] = sum(t=t1..t2) AR[i,t]
```

Declare the estimation window, event window, baseline model, leakage or anticipation,
concurrent events, cross-sectional dependence, and placebo windows. Call the result
an abnormal deviation unless a causal design supports a stronger label.

For a single treated time series, interrupted time series, synthetic controls, or a
Bayesian structural time-series counterfactual may estimate `Y_hat(0)`. Controls must
predict the untreated path and must not themselves be affected by the event.

### Staggered Events

For cohort `g` at time `t`, target:

```text
ATT(g,t) = E[Y_t(1) - Y_t(0) | first_treated_time = g]
```

Estimate cohort-time effects and aggregate with declared weights. Inspect pre-event
effects and anticipation. Do not rely on one two-way fixed-effects coefficient when
treatment timing and effects are heterogeneous.

### Unknown Event Time

Use change-point detection when `t0` is unknown. Bayesian online change-point
detection updates the posterior over the current run length using a hazard function
and a predictive model. Report the assumed hazard, false-alarm tradeoff, detection
delay, and predictive distribution. A detected break starts causal investigation; it
does not complete it.

## Attribution and Sensitivity

### Accounting Attribution

Use exact shares only when an identity defines them. Report a residual and interaction
term when the components do not add exactly. Do not replace a causal question with an
accounting decomposition.

### Predictive Attribution

For a model `f` and declared baseline:

```text
f(x) - baseline = sum_j phi_j
```

Shapley values `phi_j` distribute a model-output difference across features under a
specified coalition value. Always disclose:

- the model and output being explained;
- baseline and background distribution;
- feature grouping and dependence treatment;
- whether the value function is marginal, conditional, interventional, or causal.

Default to the label `predictive/model attribution`. Correlated features can move
credit between features without changing the prediction. A causal interpretation
requires a structural causal model and intervention semantics.

### Global Sensitivity

For model output `Y` and uncertain input `X_i`:

```text
S_i  = Var(E[Y | X_i]) / Var(Y)
ST_i = E[Var(Y | X_-i)] / Var(Y)
```

Report input ranges and distributions, main effects, total effects, and interactions.
Sensitivity describes the model over the chosen uncertainty distribution, not the
causal contribution of the input in the world.

### Weak Identification

For an observational estimate, ask how strong an omitted variable would need to be
to overturn the conclusion. Benchmark that strength against observed covariates.
When assumptions support only an identified set, report lower and upper bounds:

```text
theta in [theta_lower, theta_upper]
```

A wide honest interval is more informative than a precise unsupported estimate.

## Bayesian Judgment

For rival hypotheses `H_k` and evidence `D`:

```text
P(H_k | D) = P(D | H_k) P(H_k) / sum_j P(D | H_j) P(H_j)
posterior_odds = prior_odds * Bayes_factor
```

Use likelihood ratios only for evidence that discriminates among hypotheses. Group
dependent observations before updating; ten correlated indicators are not ten
independent confirmations. Run alternative-prior sensitivity. Label a posterior as
empirical or calibrated only when the inputs support that claim; otherwise use
`model-implied` or `judgmental scenario weight`.

## Decision and Action

Separate belief from preference. Given state `s`, action `a`, and utility or negative
loss `U`:

```text
a_star = argmax_a sum_s P(s | D) * U(a, s)
```

Include transaction or implementation cost, delay, exit failure, irreversibility, and
ruin paths in `U`. Compare expected value with worst-case loss and regret when
probabilities are fragile.

The expected value of perfect information is:

```text
EVPI = E_s[max_a U(a,s)] - max_a E_s[U(a,s)]
```

Gather more information only when expected information value exceeds research cost,
delay, and opportunity loss. Under high uncertainty, choose reversible probes whose
results discriminate among hypotheses and preserve future choices.

## Failure Modes

- **Formula laundering**: adding notation to an unsupported narrative.
- **Counterfactual omission**: calling before-after difference an event effect.
- **Attribution confusion**: calling SHAP or sensitivity a causal share.
- **Weight invention**: assigning arbitrary scores and renaming them probabilities.
- **Duplicate evidence**: multiplying confidence with correlated indicators.
- **Post-treatment control**: controlling away part of the effect or opening bias.
- **Window mining**: selecting event windows after seeing the desired result.
- **Average concealment**: hiding heterogeneous or ruin outcomes in one mean.
- **Action-free analysis**: producing a model with no decision threshold or update rule.

## Research Basis

Use these primary sources for the method boundaries, not as permission to skip
task-specific validation:

- Rubin, potential outcomes and causal effects: https://doi.org/10.1037/h0037350
- Pearl, structural causal models and intervention: https://doi.org/10.1214/09-SS057
- MacKinlay, event studies: https://www.jstor.org/stable/2729691
- Callaway and Sant'Anna, group-time DiD: https://arxiv.org/abs/1803.09015
- Lundberg and Lee, SHAP: https://arxiv.org/abs/1705.07874
- Janzing, Minorics, and Blobaum, causal semantics of feature relevance:
  https://arxiv.org/abs/1910.13413
- Adams and MacKay, Bayesian online change-point detection:
  https://arxiv.org/abs/0710.3742
- Heckerman, Bayesian networks: https://arxiv.org/abs/2002.00269
- Howard, decision analysis: https://doi.org/10.1109/PROC.1966.4758
- Sobol, global sensitivity indices: https://doi.org/10.1016/S0378-4754(00)00270-6
- Cinelli and Hazlett, omitted-variable sensitivity:
  https://doi.org/10.1111/rssb.12348
- Manski, nonparametric treatment-effect bounds:
  https://www.jstor.org/stable/2006592
