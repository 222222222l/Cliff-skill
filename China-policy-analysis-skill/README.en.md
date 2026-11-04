# China Policy Risk Analysis Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `China-policy-analysis-skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

A structured method for analyzing Chinese policy and macro-financial questions. It organizes public policy text, funding constraints, implementation incentives, and statistical evidence into testable transmission chains, then examines implications for household employment, cash flow, debt, and assets.

The deliverable is an Agent instruction package with methodological references, not a calibrated policy forecasting model. Results depend on data, identification assumptions, and the host model. Missing evidence should remain unknown or be represented by competing explanations.

## Method and scope

| Question | Verification focus |
| --- | --- |
| Policy objectives and implementation | Funding, rules, responsible actors, local capacity, complementary measures |
| Cost and risk transfers | Constraints and exit options of central/local government, finance, firms, and households |
| Macro-financial pressure | Transmission across FX, property, local debt, banks, employment, and capital flows |
| Official-data consistency | Comparable components, prices/quantities, regions, ownership, vintages, release lags |
| Household decisions | Applicability, irreversible downside, staged actions, follow-up evidence |

Record policy statements separately from realized outcomes. When statistics conflict, first inspect definitions, revisions, bases, lags, composition, and sampling; cross-check fiscal receipts, electricity, freight, company cash flows, and partner-country trade. A discrepancy alone does not establish falsification. Correlation or inferred incentives do not establish causality without an identification argument.

## Use

Install the directory containing `SKILL.md`, `references/`, and `agents/` into the host's supported Skill location, then invoke:

```text
Use $china-policy-risk-analysis to assess this policy's implementation
conditions, funding and risk transmission, official-data consistency,
and action boundaries for ordinary residents.
```

Lead with the conclusion and evidence strength, followed by mechanisms, supporting and opposing evidence, action conditions, and the next verification point. Load only the topics material to the question.

## Files and evidence

- [SKILL.md](SKILL.md): workflow and evidence discipline.
- [Macro-financial transmission](references/china-macro-financial-pressure-valves.md): cross-sector constraints and channels.
- [Official-data consistency](references/official-data-consistency-check.md): decomposition, definitions, and cross-checking.

Policy rules and figures require current primary sources. Quantified bias ranges require explicit evidence and assumptions. The repository does not supply independently validated out-of-sample forecasting accuracy. The method does not guarantee investment returns or replace case-specific professional judgment.

No top-level `LICENSE` is currently supplied. This document describes the current branch and does not imply that another branch or pull request has been merged.

## Collection-specific causal extension

This copy adds counterfactual/identification constraints, political-economy mechanisms, and macro–micro consistency checks. See the [integration note](docs/causal-extension-integration.md), [causal method](references/political-economy-causal-engine.md), and [cases](evals/cases.md). Cases are evaluation material, not forecasting-accuracy evidence. This collection's extension does not mean a pull request in the standalone repository has been merged.
