# Model Causes and Decisions Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `model-causes-and-decisions-skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

`model-causes-and-decisions` turns phenomena, attribution, forecasts, and action choices into explicit system models: targets, counterfactuals, competing hypotheses, identification conditions, uncertainty, and decision rules.

This repository provides methodological instructions and evaluation cases. It is not software that automatically discovers causality or a validated forecasting model.

## Workflow

1. Fix the decision, outcome, unit, horizon, losses, and action constraints.
2. Map actors, incentives, actions, stocks/flows, and feedback.
3. Specify a baseline, preferred explanation, and at least one rival, with discriminating evidence.
4. Check timing, measurement, confounding, common support, anticipation, spillovers, and selection.
5. Select the minimum sufficient method, stress-test it, and define actions and stop conditions.

References cover change points, event studies/interrupted time series, difference-in-differences, DAGs/structural causal models, model attribution, global sensitivity, partial identification, Bayesian updating, and value of information. Complexity follows the question and data.

## Claim boundaries

| Level | Supported claim |
| --- | --- |
| I0 | Narrative or scenario |
| I1 | Descriptive/accounting difference |
| I2 | Association, prediction, or model attribution |
| I3 | Causal estimate under explicit identification assumptions |
| I4 | Causal estimate corroborated by robustness, mechanism, or replication |

An equation makes assumptions explicit; it does not establish them. SHAP values, regression coefficients, abnormal differences, and correlations are not causal contributions by themselves. Contributions need not sum to 100% without an accounting identity or declared decomposition.

## Install and invoke

Install `model-causes-and-decisions/` in the host's supported Skill directory.

```text
Use $model-causes-and-decisions to model this phenomenon, separating
observations, assumptions, and scenarios, and state identification
conditions, rival explanations, and decision rules.
```

The current Skill distinguishes invocation modes: an explicit modeling request runs the requested scope; apparent suitability without that request produces one recommended method and at most one alternative, not a full unsolicited attribution. A method-selection request does not automatically become a full study.

## Files and evaluation

- [SKILL.md](model-causes-and-decisions/SKILL.md): invocation boundary, workflow, and output contract.
- [methods.md](model-causes-and-decisions/references/methods.md): method selection.
- [evaluation-cases.md](model-causes-and-decisions/references/evaluation-cases.md): evaluation cases.

Downstream benefit still requires paired representative tasks against a no-Skill or current-Skill baseline. A method inventory and author-written cases do not establish an improvement. No top-level `LICENSE` is currently supplied.
