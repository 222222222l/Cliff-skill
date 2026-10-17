# Official Data Verification

Use this reference whenever market analysis relies on government or regulator data: CPI/PCE, GDP, employment, fiscal data, credit aggregates, money supply, FX reserves, trade, property, industrial output, PMI, official fund-flow data, official exchange statistics, and regulatory disclosures.

Core rule: never trade or infer macro regimes from a headline series alone. Decompose the headline, estimate measurement bias, cross-check with independent indicators, and state whether the official data is confirmed, noisy, stale, or contradicted.

## Three Principles

1. Do not stop at the top-line number.
   - Always inspect sub-components, weights, base effects, revisions, seasonal adjustment, real versus nominal split, and price versus volume contribution.
   - A stable headline can hide deterioration in the most important component.

2. Quantify possible data padding, understatement, or measurement bias.
   - Use a range, not a single correction, when the bias cannot be observed directly.
   - Separate benign measurement noise from incentive-driven bias, definition changes, delayed recognition, and sample distortion.

3. Cross-validate across independent channels.
   - Compare official data against market prices, corporate reports, tax/fiscal receipts, industry volumes, household surveys, platform data, trade-partner mirror data, electricity/freight/traffic data, and financial-market behavior.
   - When evidence conflicts, explain the likely reason rather than averaging the conflict away.

## Data Quality Score

Assign each official series a 0-5 reliability score for the current question:

| Score | Read |
| ---: | --- |
| 5 | High-frequency, transparent, revised openly, and confirmed by independent data. |
| 4 | Useful but needs component checks and revision awareness. |
| 3 | Directionally useful but subject to sampling, lag, or definitional issues. |
| 2 | Heavily managed, delayed, or contradicted by partial cross-checks. |
| 1 | Mostly a policy signal or confidence-management number for this use case. |
| 0 | Unusable for probability scoring without independent reconstruction. |

Use the score to adjust confidence:

```text
reported_signal = official value
bias_range = estimated upward/downward distortion
reconstructed_range = official value adjusted by bias_range and cross-checks
confidence = data quality score + cross-validation strength
```

Do not mechanically haircut every official data point. Apply a bias range only when the series has known definition changes, incentive pressure, stale recognition, sample distortion, or conflict with independent evidence.

## Bias and "Water" Taxonomy

Classify possible distortion before estimating it:

- Definition bias: categories are changed, excluded, or reweighted.
- Sampling bias: survey population misses informal, small, rural, private, or distressed entities.
- Timing bias: stress is delayed through forbearance, loan extensions, smoothing, or late recognition.
- Price-index bias: quality adjustment, imputed prices, rent equivalence, deflator choices, or substitution effects alter real purchasing-power interpretation.
- Base-effect bias: year-over-year looks good or bad because the comparison period was unusual.
- Local reporting incentive: local or sector data is shaped by budget, promotion, financing, or regulatory pressure.
- Survivorship bias: failed firms, delisted securities, closed stores, or unemployed workers exit the sample.
- Aggregation bias: national or top-line data hides regional, income, sector, or ownership splits.

Estimate the possible magnitude:

| Bias level | Indicative adjustment |
| --- | --- |
| Low | 0-10% of the reported move, or less than 0.1 percentage point for inflation/growth rates. |
| Medium | 10-30% of the reported move, or 0.1-0.5 percentage point. |
| High | 30-60% of the reported move, or 0.5-1.5 percentage points. |
| Very high | Reported direction itself may be unreliable; require reconstruction from proxies. |

State the adjustment as a scenario range, not as a definitive true number.

## Required Component Checks

### Inflation

Check:

- Headline versus core.
- Goods versus services.
- Shelter, rent, owners' equivalent rent, utilities, medical, insurance, food, energy, transportation, and electronics.
- Month-over-month, 3-month annualized, 6-month annualized, and year-over-year.
- Weight changes, quality adjustment, and substitution effects.

Cross-check:

- Commodity prices, rents, wage growth, corporate price guidance, utility tariffs, import prices, producer prices, and household inflation expectations.

### Labor and Income

Check:

- Headline unemployment, participation, employment-population ratio, payroll breadth, hours, wages, revisions, underemployment, youth unemployment, informal work, and labor-force exits.

Cross-check:

- Tax receipts, social-security contributions, job postings, platform income, corporate hiring freezes, wage arrears, claims data, and consumption data.

### GDP and Activity

Check:

- Nominal versus real GDP.
- Deflator contribution.
- Consumption, investment, government spending, net exports.
- Inventory contribution.
- Sector and regional split.

Cross-check:

- Electricity, freight, ports, tax revenue, corporate earnings, PMI subindexes, credit demand, commodity consumption, imports, and household income.

### Credit and Money

Check:

- M1, M2, loans, deposits, social financing, government bond financing, household versus corporate credit, short-term versus long-term credit, bill financing, and off-balance-sheet credit.

Cross-check:

- Bank margins, credit spreads, property transactions, corporate capex, deposit migration, wealth-management products, and market yields.

### Fiscal and Local Finance

Check:

- General public budget, government fund budget, land sales, tax versus non-tax revenue, transfer payments, special bonds, hidden debt rollover, and arrears.

Cross-check:

- Local fee increases, contractor payment delays, LGFV spreads, public-service cuts, infrastructure starts, and local bank exposure.

### Property

Check:

- New-home prices, second-hand prices, transaction volume, inventory, land auctions, mortgage rates, developer funding, completion, and resale liquidity.

Cross-check:

- Listings, auction discounts, broker data, mortgage prepayments, household income, local fiscal data, bank asset quality, and construction employment.

### Trade and External Balance

Check:

- Export and import value, volume, price, product mix, destination, re-export routing, services trade, direct investment, portfolio flows, and FX settlement.

Cross-check:

- Trade-partner mirror data, shipping rates, port throughput, commodity imports, corporate guidance, FX reserves, and currency basis.

## Contradiction Handling

When official data and independent evidence diverge, classify the contradiction:

- Lag: official data has not yet recognized current stress.
- Composition: headline is supported by one component while household or corporate reality worsens elsewhere.
- Definition: changed categories, exclusions, or methodology reduce comparability.
- Regional split: national average hides local stress.
- Price/volume split: nominal data rises because prices rise, not because real demand improves.
- Policy smoothing: credit, defaults, unemployment, or asset quality are delayed by forbearance or administrative tools.
- Market overreaction: market prices may extrapolate too far beyond the data.

Do not average contradictory data into a false neutral. Present both and state which one is more decision-relevant for the user's horizon.

## Output Add-On

When official data matters, add this compact block:

```text
Official data used: ...
Headline read: ...
Key sub-components: ...
Data quality score: 0-5
Estimated bias/water range: low / medium / high / very high, with numeric range when possible
Reconstructed range: ...
Cross-checks confirming: ...
Cross-checks contradicting: ...
Likely reason for contradiction: ...
Trading/policy implication: ...
```

If component data is unavailable, say so and reduce confidence. Never turn an official headline into a high-confidence market signal without component and cross-check evidence.
