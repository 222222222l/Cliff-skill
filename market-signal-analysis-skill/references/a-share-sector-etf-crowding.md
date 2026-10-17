# A-Share Sector ETF Share Trend and Crowding

Use this reference for one sector/theme ETF or a peer group when the question concerns share expansion, redemptions, crowding, apparently irrational oversold conditions, or the probability of a rebound, range, or further decline.

## Contents

1. Data gate
2. Share-flow trend
3. Crowding and unwind scores
4. Fundamental overlay
5. Bayesian scenarios
6. Trading interpretation
7. Monitoring cadence

## Data Gate

Collect at least 60 daily observations; 252 is preferred:

- close, NAV/iNAV, total shares, turnover, premium/discount;
- tracked-index and peer-sector returns;
- constituent weights, free-float market cap, breadth, and top-five return contribution;
- valuation percentile and earnings/order revisions;
- margin, insider supply, policy catalysts, and ETF peer flows when material.

For peer aggregation, `free_float_mcap` should describe the underlying exposure's investable capacity and may be repeated on each peer row. Do not sum repeated capacity denominators across ETFs.

Verify share splits, fund mergers, index rebalances, stale NAV, and whether the vendor reports daily final shares. For a new or small ETF, require absolute flow and turnover pressure because percentages can be misleading.

## Share-Flow Trend

Compute:

```text
estimated_flow_t = (shares_t - shares_t-1) * NAV_t
flow_to_AUM_t = estimated_flow_t / AUM_t-1
flow_pressure_t = abs(estimated_flow_t) / average_turnover_20
share_z_5 = Z-score of rolling 5-day share change
```

Heuristic fallback thresholds:

| Measure | Watch | Abnormal | Extreme |
| --- | ---: | ---: | ---: |
| Sector ETF 5-day share change | 5% | 10% | 15%-20% |
| Sector ETF 20-day share change | 10% | 20% | 35% |
| Absolute Z-score | 1.5 | 2.0 | 3.0 |
| Flow pressure | 0.3 | 0.5 | 1.0 |

Use the price/share quadrant from the broad-ETF reference. `Price down + shares down + relative strength down` is redemption confirmation. `Price down + shares up` is dip-buying pressure, not automatic accumulation.

## Crowding Score

Score 0-100 and report input coverage:

| Factor | Weight | High-crowding evidence |
| --- | ---: | --- |
| Positive share-flow acceleration | 25 | share Z above 2, 20-day growth above 20% |
| Turnover heat | 20 | turnover/MA20 above 1.5, turnover share far above market-cap share |
| Constituent concentration | 15 | top 10 above 50%, top-five return contribution above 50% |
| ETF AUM/free-float capacity | 15 | above 3% watch, above 5% high, above 10% structural |
| Price extension | 15 | more than 12% above MA20 or parabolic weekly structure |
| Valuation/consensus | 10 | valuation percentile above 80%, euphoric narrative |

Interpretation: below 40 normal, 40-59 elevated, 60-74 crowded, 75+ extreme. Crowding measures fragility, not immediate downside.

## Unwind Score

Score negative-feedback risk separately:

| Factor | Weight | High-unwind evidence |
| --- | ---: | --- |
| Negative share-flow acceleration | 30 | share Z below -2, 20-day contraction above 20% |
| Trend break | 25 | below MA20/50, failed reclaim, new 55-day low |
| Price-flow confirmation | 20 | price and shares fall together |
| Constituent breadth | 15 | leaders and laggards break together; few above MA20 |
| Fundamental/policy non-confirmation | 10 | good news no longer lifts price or revisions roll over |

Below 35 low, 35-54 watch, 55-69 high, 70+ extreme. Extreme oversold RSI can coexist with a high unwind score; oscillator exhaustion is not flow stabilization.

## Fundamental Overlay

Separate `good fundamentals` from `positive revisions`:

- stable orders and reasonable PE limit long-run valuation compression;
- accelerating earnings revisions can reverse flow pressure;
- good but non-accelerating earnings may underperform faster-growth sectors;
- policy totals spread across years are expectations until orders, revenue, margins, and cash flow confirm;
- a low weighted PE can hide expensive high-beta constituents.

Do not reduce the unwind score merely because valuation is reasonable. Use valuation to narrow the downside scenario and fundamentals/revisions to update medium-horizon probabilities.

## Bayesian Three-State Scenarios

Select a fixed horizon and one prior:

| Sector state | Up | Range | Down |
| --- | ---: | ---: | ---: |
| Main-line acceleration | 0.55 | 0.30 | 0.15 |
| Healthy pullback | 0.40 | 0.45 | 0.15 |
| Crowded distribution | 0.25 | 0.35 | 0.40 |
| Broken trend/unwind | 0.15 | 0.30 | 0.55 |
| Washout/accumulation attempt | 0.25 | 0.50 | 0.25 |

Update once per independent family: price trend, relative strength/breadth, share flow, fundamentals/revisions, valuation, and policy/catalyst response. Treat crowding as a state prior or interaction term; do not count its component inputs again as independent evidence.

If price and shares keep falling, down likelihood rises. If shares stabilize before price, raise range first. Raise up materially only after price reclaims trend, breadth improves, and flow or revisions confirm.

Label uncalibrated output `model-implied scenario weights`. With fewer than 60 observations, missing share history, or no constituent breadth, reduce confidence and widen results by at least 5-10 percentage points.

## Trading Interpretation

- Strong trend + rising shares + moderate crowding: hold with trailing exits.
- Strong trend + extreme crowding + narrowing breadth: stop adding and protect profits.
- Broken trend + falling shares: reduce; reasonable valuation alone is not a timing signal.
- Extreme oversold + shrinking downside volume + stable shares: rebound candidate, not yet a right-side reversal.
- Reclaim MA10/20 + stable/growing shares + breadth repair: right-side re-entry evidence.

Report support/resistance, share-flow state, crowding score, unwind score, posterior probabilities, evidence coverage, and explicit reversal conditions.

## Monitoring Cadence

- Daily: track 1/5/20/60-day estimated flows, share Z-score, flow pressure, premium/discount, relative strength, breadth, and price-flow quadrant.
- Weekly: update concentration, top-five contribution, AUM/free-float capacity, earnings revisions, valuation percentile, and crowding/unwind states.
- Around rebalances, dividends, splits, mergers, and large announcements: suspend mechanical alerts until share-field discontinuities are reconciled.
- Escalate from watch to action only when flow, price structure, and at least one independent family such as breadth or revisions agree.
