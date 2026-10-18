# China Policy Analysis — Political-Economy Causal Engine

## Status and purpose

Supplementary reference for `china-policy-risk-analysis` (not a replacement for the existing Skill). Its purpose is to connect political objective constraints, bureaucratic incentives, macro-financial accounting, industry transmission, and ordinary residents' micro behavior. Invoke for reform-motivation, policy-enforcement, macro-to-micro, and apparently contradictory policy questions.

### Non-negotiable epistemic rules

1. Treat all claims about hidden motives as **hypotheses**, even if they are plausible. Public statements, legal texts, personnel changes, implementation actions, and outcomes have different evidentiary status.
2. The existing four-level hierarchy (`regime continuity > stability > core groups > residents`) is a **candidate explanatory model**, not a presumption that decides every case. Compete it against (at minimum) fiscal constraints, implementation capacity, national security, policy design mistakes, and real social-welfare objectives.
3. A policy that benefits a state-owned institution is not by itself proof that enriching that institution was the policy's objective. Likewise, a policy that benefits households is not by itself proof that household welfare was the sole objective.
4. Infer revealed preferences from **feasible, controlled, costly choices under comparable constraints**, not just stated objectives. Failure to act is weak evidence when authority, fiscal headroom, information, and institutional capability are unknown.
5. Use evidence tags: `FACT`, `INFERENCE`, `HYPOTHESIS`, `COUNTEREVIDENCE`, `UNKNOWN`. Every strong causal claim needs a plausible mechanism and a counterfactual.
6. A coherent narrative is not necessarily correct. Prefer hypotheses that generate risky, falsifiable predictions; update them when predictions fail. Do not present political forecasts or subjective numerical odds as calibrated facts.
7. Distinguish 'safe for the system', 'efficient for aggregate output', 'good for household welfare', and 'good for a particular household'. These are distinct dependent variables.

## End-to-end causal graph

```text
Exogenous conditions (global rates, sanctions, demographics, technology, shocks)
   + inherited commitments and constraints
            ↓
Central stated objectives and observed institutional priorities
            ↓
Negotiated allocation of authority, budget and liability
            ↓
Provincial / municipal / regulator / bank / SOE / private-firm incentives
            ↓
Implementing rules, budgets, liquidity, enforcement and actual transfers
            ↓
Sector-specific prices, cash flows, debt dynamics, employment and wages
            ↓
Household income, precautionary saving, leverage, portfolio choices and exit rights
            ↓
Aggregate demand, defaults, tax revenue, asset prices, trust and political feedback
            ↺ (feedback into future policy choice)
```

Always identify the **weakest measurable link** and a plausible route that bypasses the proposed cause.

## Stage A — Policy object and institutional feasibility

Document: issuer; date; legal rank; superior regulation; territorial scope; ministry and implementing agent; funded budget line; stakeholders with veto/implementation power; deadlines; pilots versus national rollout; whether the measure changes enforceable rights or merely announces an objective.

For the relevant decision-maker identify:
- **Authority**: What could they lawfully or practically decide?
- **Resources**: What appropriations, balance-sheet capacity, quota, staff and data were available?
- **Accountability**: What performance, compliance and risk indicators shape rewards and penalties?
- **Costs of reversal**: legal, contractual, political, financial and reputational costs.
- **Outside options**: can the agency delay, pass responsibility, roll debt, restrict exits or allow market adjustment?

Never collapse 'central government', 'local government', 'banks', 'SOEs', and 'party organs' into a single unified actor.

## Stage B — At least three distinct competing explanations

Use at least three distinct competing explanations with differentiating predictions when motive or reform willingness matters. The following four categories are candidates, not mandatory slots; select or adapt explanations to the policy and available evidence rather than mechanically filling all four:

- `H-S`: Political/institutional-security constraint dominates **this decision**.
- `H-F`: Fiscal or balance-sheet capacity binds the decision.
- `H-A`: Agency, information, coordination, or implementation capacity is the principal obstacle.
- `H-W`: Welfare, development, or long-horizon industrial-security trade-off explains the decision.

For each: prior supporting evidence, conflicting evidence, one *differentiating prediction*, earliest observable indicator, and what evidence would **weaken** the hypothesis. Additional hypotheses may include elite capture, external shock, or policy error, only where evidence justifies them.

Example for a social-benefit expansion delayed despite publicly stated support:
- H-S: delays cluster around clauses that create independent enforceable claim rights, even where pilots are financially funded.
- H-F: expansion tracks central transfers and subnational fiscal capacity; richer cities expand earlier.
- H-A: variation tracks administration, information systems and fraud-control readiness after controlling for finances.
- H-W: timing reflects targeted distributional design or concern about labor-supply incentives.

If all available explanations predict the observed event equally well, mark the motive as `UNIDENTIFIED`.

## Stage C — Observe choices, not merely words

Build a dated ledger with: announcement → issued rules → budget appropriated → cash allocated → cash actually disbursed → enforcement actions → first-order outcomes → longer-term behavioral responses. Mark implementation lags and funds redirected from other uses.

Revealed-preference claims require a **choice set**: identify what materially different and feasible alternative was rejected, what it would cost, and whether the actor controlled it. Hidden private intentions cannot be directly verified from public actions.

For political-language analysis: count exact tokens and semantic contexts; normalize by comparable character or word counts; compare **same document genre**, edit for annexes and quotations, store file versions; do not equate every 'security' mention with 'regime security'. Include co-occurrence, priority statements and institutional changes.

## Stage D — Stock-flow-consistent macro bridge

Use the budget and accounting identities as checks, **not as causal theories**:

- Output (expenditure): `Y = C + I + G + (X − M)` using consistent national-accounting definitions.
- Financial-sector balances: `(private saving − private investment) + (taxes − government spending) + (imports − exports) ≈ 0` under a simplified closed capital-account/income-transfer treatment. For precision use national-accounting sectoral net lending and the full current account.
- An agent's debt stock evolves with net financing, amortization, valuation, write-down and off-balance-sheet recognition; do not confuse refinancing flows with debt extinguishment.
- A gain for one **financial claim** often corresponds to another party's liability; that does **not** mean all real-sector growth is zero-sum.

Classify every measure by mechanism:
1. Net new income or real productivity;
2. Timing shift (spend now, less later);
3. Transfer across groups (fiscal or regulatory);
4. Liquidity repair without solvency change;
5. Solvency transfer / debt reduction;
6. Relative-price / regulation / property-right change;
7. Information / expectations / credibility.

Specify quantities and units, stocks versus flows, nominal versus real, and time horizons. Trace at least one plausible **positive** and one plausible **negative** spillover.

## Stage E — Industry and micro behavior bridge

Industry: identify production input-output linkages, market power, subsidies, competition, import/export substitution, inventory, prices, capacity utilization, margins, private capex and employment.

Households: segment by income, employment security, homeownership, debt, household size, age, region and access to public services. For each group distinguish:
- Change in **cash income**;
- Change in **real purchasing power**;
- Change in **asset value and liability burden**;
- Change in **risk distribution** (income volatility, tail losses and insurance);
- Change in **optionality** (mobility, withdrawal rights, legal recourse, ability to exit);
- Change in **expectations** and desired precautionary buffers.

A consumer voucher may affect short-run spending without permanently changing permanent income. A pension or healthcare entitlement may affect risk-bearing even before transfers are paid. An industrial subsidy may benefit employment but reduce prices and profits in competing firms. Model the competing channels.

## Stage F — Adversarial data audit

Use the existing `official-data-consistency-check.md`, plus a data-vintage record for each sensitive series:

`publisher | dataset ID | metric and unit | geography/population | period | source URL | download time | publication date | methodology version | base year/denominator/sample | preliminary/final | back-revision | revised older observations | old-series retained? | known breaks | independently cross-checked?`

Escalation triggers:
- Suspended, delayed, withdrawn or silently replaced releases.
- A methodology change shortly after a persistently worsening series.
- A denominator, sample, threshold, adjustment method or base-year change without a bridge series.
- Historical back-revisions in one direction that materially alter previously visible trend.

A change is a **flag for verification**, never automatic proof of fabrication. Look for equally plausible administrative, legal, definitional or quality-control explanations. Archive official originals and independent contemporaneous copies where lawful.

For quantitative diagnostics: use harmonized-frequency measurements; avoid naive second differences when the series has seasonal changes, autocorrelation, inconsistent denominators or one-off base effects. Where possible show seasonally adjusted trend, uncertainty and sensitivity to smoothing. Scores (0–5) are **heuristic**, not measured probabilities, and must not add unrelated dimensions without validation.

## Stage G — Precommitted, falsifiable scenario outputs

Produce a dated hypothesis register:

| Field | Meaning |
|---|---|
| Hypothesis | Mechanism with actor and policy object |
| Current evidence | Sources with dates and evidence tag |
| Alternative | Strongest competing mechanism |
| Distinguishing test | Observation predicted differently by alternatives |
| Time horizon | Earliest and latest reasonable date |
| Update trigger | What result raises/lowers confidence |
| Failure criterion | What would cause model revision |
| Household consequence | Impact by household archetype |

Use `low / medium / high confidence` only if anchored in evidence quantity, independence, and identification quality; do not convert confidence labels to numerical event probabilities. Calibrate optional probability predictions with historical out-of-sample results before publishing.

## Stage H — Policy-to-resident decision rules

Separate **diagnosis** (what is happening), **forecast** (what could happen), and **decision** (what a person should do). For household decisions consider liquidity floor, income/job concentration, debt duration, jurisdictional access, legal exit and regret under at least three scenarios. Explicitly include opportunity cost of excessive defensiveness; risk avoidance is not identical to never investing.

Not every macro risk justifies immediate asset trading. Suggest action only when observation changes the household's exposure, liquidity, rights or expected costs, and distinguish reversible actions from irreversible choices.

## Required compact response schema

1. **Question and dependent variable** — whose welfare, risk or returns, over what time horizon?
2. **Verified facts and data quality** — current sources, vintages and contradictions.
3. **Institutional choice set** — authority, budget, constraints, feasible alternatives.
4. **Competing causal explanations** — including counterevidence and distinguishing tests.
5. **Macro → institution → industry → household chain** — cash, balance sheet, incentives, externalities.
6. **Policy announced versus implemented** — dated execution ledger.
7. **Scenarios with falsification triggers** — not false-precision probabilities.
8. **Resident implication** — segmented, proportionate, legal, reversible where possible.
9. **What would change my mind?** — explicit disconfirming evidence.

## Quality-gate checklist

Reject/rewrite an analysis if any of these apply:
- Hidden motive is declared as fact without direct evidence.
- Benefit incidence is equated to policymaker intent.
- A government is modeled as one actor when levels/agencies have conflicting incentives.
- Liquidity assistance is labeled insolvency resolution without accounting for losses.
- Gross index values are mistaken for typical household experience.
- Qualitative stress score is read as event probability.
- A methodological change is claimed as manipulation without bridge-series and cross-check attempts.
- A confident recommendation relies entirely on a low-reliability data series.
- At least one nontrivial alternative explanation and a falsification condition are missing.
