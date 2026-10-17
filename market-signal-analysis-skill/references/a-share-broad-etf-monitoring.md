# A-Share Broad ETF Monitoring

Use this reference for whole-market broad-ETF flow monitoring, policy-capital support or withdrawal, state-backed-capital inference, ETF migration, and market-level up/range/down probabilities.

## Contents

1. Attribution boundary
2. Data and aggregation
3. Abnormal-flow thresholds
4. Price-flow states
5. Support-withdrawal dashboard
6. Bayesian scenarios
7. Decision rules
8. Monitoring cadence

## Attribution Boundary

ETF shares measure primary-market creation/redemption, not the identity of the buyer or seller.

- A holder can sell ETF units in the secondary market without changing total shares.
- Shares fall only when an authorized participant or holder completes redemption.
- In-kind redemption transfers a basket; it does not prove that every constituent was immediately sold.
- Falling shares in one product may reflect migration to another ETF tracking the same or a substitute index.

Use `broad-ETF support withdrawal risk`, not `national team selling`, unless dated holder disclosures or official statements identify the actor. Treat actor attribution as an inference grade below the verified flow observation.

## Data and Aggregation

Collect daily data after the final share field is available:

- date, symbol, tracked index, close, NAV/iNAV, total shares, turnover, premium/discount;
- index return and MA20/50/120/200 structure;
- median-stock 20/60-day return, percentage above MA20/50, new highs minus lows;
- futures basis/open interest and options skew when available;
- PBOC liquidity, margin balance, policy announcements, and price response;
- quarterly holder disclosures for delayed actor verification.

Aggregate all ETFs tracking the same exposure before inference:

```text
estimated_flow_i,t = (shares_i,t - shares_i,t-1) * NAV_i,t
group_flow_t = sum_i estimated_flow_i,t
group_flow_rate_t = group_flow_t / group_AUM_t-1
```

Maintain separate groups for SSE 50, CSI 300, CSI A500, CSI 500, CSI 1000/2000, STAR/ChiNext, and all-market products. Then create an all-broad dashboard. Do not sum raw shares across products with materially different NAVs; aggregate estimated money flow.

Check splits, share conversions, dividends, mergers, index changes, vendor backfills, and stale NAV before calling a flow abnormal. AUM change is price plus flow; it is not a flow measure.

## Abnormal-Flow Thresholds

Use each ETF or index group's rolling 252-day distribution first:

```text
share_change_z = (current 5-day change - rolling mean) / rolling standard deviation
```

Heuristic fallback when history is unavailable:

| Measure | Watch | Abnormal | Extreme |
| --- | ---: | ---: | ---: |
| Broad ETF 5-day share change | 3% | 5% | 8%-10% |
| Broad ETF 20-day share change | 5% | 10% | 15%-20% |
| Absolute Z-score | 1.5 | 2.0 | 3.0 |
| One-day estimated flow / 20-day average ETF turnover | 0.3 | 0.5 | 1.0 |
| Peer ETFs moving in the same direction | 50% | 70% | 85% |

Require at least two dimensions: relative change or Z-score, absolute money amount or turnover pressure, and peer consistency. A fixed percentage alone is unreliable across ETF sizes.

## Price-Flow States

| Price | Shares/flow | Primary read | Required cross-check |
| --- | --- | --- | --- |
| Up | Up | new demand; healthy early, crowded if accelerating late | breadth and valuation |
| Up | Down | secondary demand absorbs redemption, profit-taking, or migration | peer ETF flows and breadth |
| Down | Up | dip buying or policy support; not a bottom without price repair | stabilization and breadth |
| Down | Down | redemption-price negative feedback; strongest de-risking state | leaders, futures, liquidity |

The strongest early distribution warning is: index flat/up, broad-group flow negative, median stock weak, and turnover concentrated. The strongest breakdown confirmation is: price down, group flow down, breadth down, and policy action fails to repair price within one to two weeks.

## Support-Withdrawal Dashboard

Score 0-100 using available independent families; disclose coverage and do not renormalize fewer than three families into false confidence.

| Family | Weight | Withdrawal-risk evidence |
| --- | ---: | --- |
| Peer-aggregated ETF flow | 30 | negative 5/20-day flow, Z below -2, acceleration |
| Price and trend | 20 | index below MA50/120, failed reclaim |
| Breadth/median stock | 20 | index stable while median and MA breadth deteriorate |
| Turnover and derivatives | 10 | narrow turnover, futures discount, defensive open-interest shift |
| Policy/liquidity response | 10 | liquidity neutral/tight or support language without price confirmation |
| Cross-market confirmation | 10 | A/H/CNH and former leaders weaken together |

Interpretation: below 35 low, 35-54 watch, 55-69 high, 70+ extreme. This is a support-withdrawal score, not proof of a named actor.

## Bayesian Three-State Scenarios

Model `up`, `range`, and `down` for a fixed horizon. Use regime-conditional scenario priors when calibrated priors are unavailable:

| Regime | Up | Range | Down |
| --- | ---: | ---: | ---: |
| Policy-floor repair | 0.45 | 0.40 | 0.15 |
| Range-stabilized extraction | 0.25 | 0.50 | 0.25 |
| Crowded distribution | 0.20 | 0.35 | 0.45 |
| Broad breakdown | 0.10 | 0.25 | 0.65 |
| Post-washout accumulation | 0.35 | 0.50 | 0.15 |

These are heuristic scenario priors, not empirical frequencies. Update only once per independent family: trend, peer-aggregated flow, breadth, policy/liquidity, derivatives/turnover, and cross-market stress. ETF shares and estimated flow are one family, not two.

Use the Bayesian rules in `references/statistical-weighting.md`. Run sensitivity with a neutral prior and the selected regime prior. If the leading scenario changes, report low confidence and a probability range rather than one number.

## Decision Rules

- Yellow: 20-day broad-group flow below -5%, Z below -1.5, or flat index with weakening breadth. Stop adding themes and tighten exits.
- Orange: price and group flow fall together, Z below -2, and MA50 or breadth fails. Reduce high-beta exposure.
- Red: broad groups keep redeeming, index loses MA120, breadth collapses, and policy support fails. Treat as defensive de-risking.
- Re-entry: group flows stabilize, new lows contract, median returns improve, and price reclaims the relevant MA with peer confirmation.

Report current observations, actor inference, scenario posterior, sensitivity, and the exact evidence that would reverse the view.

## Monitoring Cadence

- After each close: refresh final shares/NAV, 1/5/20/60-day estimated flows, Z-score, peer agreement, price-flow quadrant, breadth, and alert state.
- Weekly: review migration across substitute exposures, turnover concentration, trend repair/failure, and whether policy action produced a durable price response.
- Monthly or quarterly: reconcile holder disclosures and fund reports; use them to revise actor attribution, never to backfill certainty into earlier real-time signals.
- Trigger an alert only when at least two independent dimensions agree. Preserve the raw snapshot so later revisions, splits, and vendor backfills can be audited.
