# Official Data Consistency Check

Use this reference when a China policy or macro-financial analysis relies on official statistics, regulator disclosures, local-government data, public-budget data, credit aggregates, property data, employment data, CPI/PPI, trade, FX reserves, capital-flow data, or market-support data.

The purpose is not to dismiss official data. The purpose is to avoid overreading top-line numbers, identify methodology and timing limitations, and build a more reliable range through component analysis and cross-checks.

## Core Principles

1. Do not rely on headline categories alone.
   - Always inspect sub-items, regional splits, ownership splits, price versus volume, nominal versus real, and stock versus flow.
   - In many policy questions, the sub-component is more decision-relevant than the aggregate.

2. Quantify possible statistical bias or "water" where possible.
   - Use ranges and confidence levels.
   - Separate normal measurement noise from reporting incentives, definition changes, delayed recognition, and sample limitations.

3. Cross-check with independent or adjacent evidence.
   - Compare official data with fiscal receipts, electricity, freight, property transactions, bank behavior, market prices, corporate reports, trade-partner mirror data, household behavior, and local implementation signals.
   - When data conflicts, explain why the conflict may exist.

## Data Reliability Score

Score each data point from 0 to 5 for the current question:

| Score | Meaning |
| ---: | --- |
| 5 | Transparent, granular, timely, and confirmed by cross-checks. |
| 4 | Mostly usable with component checks. |
| 3 | Directionally useful but affected by lag, sample, or definition limits. |
| 2 | Needs reconstruction from proxies before drawing strong conclusions. |
| 1 | Better treated as a policy communication signal than a direct activity measure. |
| 0 | Insufficient for inference without independent data. |

If a data point scores 0-2, avoid using it as the main basis for resident guidance or market probabilities.

## Bias Types

Classify possible limitations:

- Aggregation bias: national or provincial total hides sector, city, income, ownership, or household split.
- Definition bias: methodology changes make history less comparable.
- Sample bias: informal employment, small firms, distressed firms, private firms, or migrant groups may be underrepresented.
- Timing bias: losses, defaults, arrears, unemployment, and asset-quality deterioration may be recognized late.
- Price/volume bias: nominal value improves because of price changes while real volume remains weak.
- Base-effect bias: year-on-year comparison is distorted by a weak or strong base.
- Administrative smoothing: the reported path is steadier than underlying high-frequency conditions.
- Incentive bias: local or institutional reporting may be influenced by budget, financing, performance, or regulatory constraints.

Use this rough range:

| Bias level | Indicative treatment |
| --- | --- |
| Low | Use official data with normal caveats. |
| Medium | Give a reconstructed range and lower confidence one step. |
| High | Treat the headline as incomplete; rely on sub-items and cross-checks. |
| Very high | Do not infer true conditions from the headline direction alone. |

## Required Checks by Data Area

### GDP and Activity

Check:

- Nominal versus real growth.
- Deflator contribution.
- Consumption, investment, government spending, net exports.
- Industrial output by sector and ownership.
- Regional dispersion.

Cross-check:

- VAT and income-tax receipts, electricity, freight, port throughput, commodity imports, PMI subindexes, corporate earnings, household income, and credit demand.

### Employment and Income

Check:

- Headline unemployment, youth unemployment, labor-force participation, migrant employment, wage growth, working hours, wage arrears, recruitment demand, and household disposable income.

Cross-check:

- Social-security contributions, personal income tax, job postings, platform income, local wage arrears, consumption data, and household savings behavior.

### CPI, PPI, and Living Cost

Check:

- Food, energy, utilities, rent, medical, education, transportation, services, durable goods, and regional differences.
- CPI versus household "felt inflation" for non-discretionary items.

Cross-check:

- Utility tariffs, local fee changes, supermarket prices, rent listings, producer prices, import prices, wage growth, and household consumption substitution.

### Credit, Money, and Banking

Check:

- M1, M2, household deposits, corporate deposits, short-term versus long-term loans, household versus corporate loans, government bond financing, bill financing, off-balance-sheet financing, NPLs, special-mention loans, and net interest margins.

Cross-check:

- Property sales, corporate capex, bank equity performance, deposit-rate changes, wealth-management products, trust restructurings, local-bank mergers, and credit spreads.

### Fiscal and Local Debt

Check:

- General public budget, government fund budget, land-transfer revenue, tax versus non-tax revenue, transfer payments, special bonds, refinancing bonds, LGFV spreads, and arrears.

Cross-check:

- Local fee/utility increases, contractor payments, public-service changes, infrastructure starts, land auctions, local bank exposure, and city-level population/income trends.

### Property

Check:

- New-home prices, second-hand prices, transaction volume, inventory, land auctions, mortgage rates, prepayment, developer funding, delivery progress, and foreclosure/auction listings.

Cross-check:

- Broker listings, transaction taxes, household income, local fiscal data, bank mortgage growth, construction employment, and developer bond pricing.

### External Balance and Capital Flows

Check:

- Trade value versus volume, product mix, destination mix, services trade, FDI, portfolio flows, FX settlement/sales, FX reserves, and RMB fixing behavior.

Cross-check:

- Trade-partner mirror data, shipping rates, export-company earnings, commodity imports, offshore RMB, CNH-CNY spread, bank FX procedures, and gold/USD demand.

### Capital Markets

Check:

- Broad index versus median stock, ETF shares, turnover concentration, IPO/refinancing pace, margin financing, institutional fund flows, buyback/dividend data, and delisting/enforcement data.

Cross-check:

- Retail account behavior, sector breadth, fund-redemption pressure, company financing needs, policy-tool announcements, and market liquidity.

## Contradiction Diagnosis

When official and independent data disagree, classify the likely reason:

- Lag: official data has not yet reflected current conditions.
- Composition: one strong component offsets several weak components.
- Regional split: national data hides weak cities or sectors.
- Definition change: methodology or sample changed.
- Price/volume split: nominal improvement hides real-volume weakness.
- Recognition delay: defaults, losses, arrears, or unemployment are carried forward.
- Policy smoothing: administrative support temporarily stabilizes reported outcomes.
- Market extrapolation: market prices may be reacting to expectations rather than current data.

State which evidence matters more for the user's question and time horizon.

## Output Add-On

When official data is important, add:

```text
Official data used: ...
Headline read: ...
Most important sub-items: ...
Reliability score: 0-5
Possible bias/water: low / medium / high / very high
Reconstructed range: ...
Confirming cross-checks: ...
Contradicting cross-checks: ...
Likely reason for contradiction: ...
Policy/resident implication: ...
```

If component or cross-check data is missing, state the missing pieces and avoid high-confidence conclusions.
