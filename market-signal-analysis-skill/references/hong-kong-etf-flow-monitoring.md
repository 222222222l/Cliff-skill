# Hong Kong ETF Flow and Crowding

Use this reference for Hong Kong-listed broad or sector ETFs, Southbound ETF Connect flows, multi-counter products, creation/redemption, market-maker inventory, and Hong Kong up/range/down scenario weights.

## Contents

1. Transferable core and non-transferable assumptions
2. Hong Kong-specific distortions
3. Data identity and normalization
4. Flow and crowding interpretation
5. Bayesian scenarios
6. Monitoring and alerts
7. Official sources

## Transferable Core

The A-share ETF framework remains valid for:

- separating secondary-market trading from primary-market creation/redemption;
- estimating money flow as `change in units * NAV`;
- aggregating peer funds by money flow rather than raw units;
- combining price, units, breadth, valuation, fundamentals, and policy/liquidity;
- treating crowding as fragility rather than an immediate sell signal;
- refusing to identify the beneficial buyer or seller from units alone.

Do not copy A-share thresholds, actor priors, or policy-support interpretation mechanically. Hong Kong has more cross-border investors, market-maker intermediation, multi-currency counters, overseas-underlying timing gaps, shorting/derivatives hedges, and small products with lumpy creation units.

## Hong Kong-Specific Distortions

### Multi-Counter and Fund Identity

One legal fund or share class may trade under multiple stock codes or currency counters. Counter turnover and quotes are separate secondary-market observations, while fund units may be one shared primary-market pool.

- Use `ISIN + legal fund + share class` as the canonical fund identity.
- Consolidate counter turnover after FX conversion; retain counter-level spread and premium/discount diagnostics.
- Use official fund-level units once. Never add repeated units from HKD, RMB, or other counters.
- Treat a counter transfer by a dual-counter market maker as inventory migration, not fund creation/redemption.

If identity cannot be reconciled, analyze counters only for liquidity and price discovery and withhold fund-flow totals.

### Southbound ETF Connect

Southbound trading is normally secondary-market demand. A rise in Southbound holdings or turnover can lift price without immediately changing fund units because market makers or other holders may supply inventory. Creation follows only when the premium, inventory cost, and creation economics justify primary-market activity.

Separate four observations:

1. Southbound net buying or holding change;
2. total fund units and estimated primary flow;
3. premium/discount and quote spread;
4. non-Southbound/global flow and price response.

ETF Connect inclusion, exclusion, sell-only changes, and regular-review effective dates can create discrete flows. Treat them as event risk rather than organic trend evidence. Do not infer mainland retail sentiment from omnibus/custodian positions without beneficial-owner evidence.

### Market Makers and Participating Dealers

HKEX-authorized market makers support liquidity and price efficiency. Participating dealers and market makers can warehouse inventory, hedge with futures or constituents, and create/redeem in blocks. Consequences:

- flat units during strong secondary buying can mean inventory absorption, not absent demand;
- one large creation/redemption can be operational or arbitrage-driven rather than a regime change;
- thin products require spread, depth, premium/discount persistence, and creation-unit multiples before flow inference;
- price down plus units down is strongest when spreads widen, discounts persist, and peers confirm.

### NAV Timing and Underlying-Market Mismatch

For ETFs holding Mainland, U.S., Japanese, commodity, bond, or other non-overlapping assets, the latest official NAV may be stale while Hong Kong trades. A large apparent premium/discount may be price discovery rather than arbitrage stress.

- Use contemporaneous iNAV or a fair-value proxy when the underlying market is closed.
- Mark holidays, half-days, FX moves, futures moves, and underlying-market overlap.
- Reduce flow-signal reliability when NAV is stale or the spread is abnormal.
- Do not use stale premium/discount as a directional Bayesian family.

### Product Structure

Classify physical, synthetic, futures-based, bond, commodity, active, and leveraged/inverse products before applying thresholds. Daily-reset leveraged/inverse products and futures roll effects require separate exposure and rebalance analysis. Synthetic or futures-based creations need not transmit immediately into constituent cash trading.

### Shared but Offset Liquidity Pools

Hong Kong prices can reflect Southbound demand, global active/passive funds, offshore China ETFs, H-share/A-share substitution, HKD funding, USD rates, CNH, derivatives, and issuer hedging. These pools interact but are not one directly additive flow series.

- Aggregate only legally identical or genuinely substitutable local ETF exposures.
- Use U.S./European-listed China ETF flows as a separate global-flow family.
- Use Southbound and CCASS evidence as one cross-border family.
- Use HKD liquidity, USD rates, CNH, and index futures as macro/discount-rate evidence, not ETF creation evidence.

## Data Identity and Normalization

Collect at least 60 daily observations; prefer 252:

- canonical fund ID, ISIN, share class, all counter codes, counter currency, and FX to HKD;
- close, official NAV/iNAV or fair value, total fund units, AUM, creation-unit size, turnover, spread, depth, and premium/discount;
- Southbound eligibility, review/effective dates, post-close holding or flow data with source/method label;
- index return, breadth, concentration, valuation, earnings revisions, futures basis, short interest, and options skew;
- HKD liquidity, HIBOR, USD rates, CNH, and offshore China ETF flows when material;
- physical/synthetic/futures/leveraged structure and underlying-market trading overlap.

Normalize one row per canonical fund/share class/day. Convert money fields to HKD or one disclosed common currency. If multiple counter rows repeat the same fund units, reject the aggregate rather than silently double count.

Use:

```text
primary_flow_t = (fund_units_t - fund_units_t-1) * official_NAV_t
southbound_holding_change_t = southbound_units_t - southbound_units_t-1
counter_turnover_HKD_t = sum(counter_turnover_t * FX_to_HKD_t)
```

Do not derive flow from AUM change. AUM also contains performance and FX effects.

## Flow and Crowding Interpretation

Use rolling fund-specific quantiles first. Heuristic fallbacks require stricter confirmation than large A-share ETFs:

| Measure | Large/liquid fund watch | Small/thin fund watch | Abnormal confirmation |
| --- | ---: | ---: | ---: |
| 5-day unit change | 3%-5% | 8%-10% | absolute Z-score above 2 plus flow pressure |
| 20-day unit change | 8%-12% | 20% | peer or premium/spread confirmation |
| Flow / 20-day average turnover | 0.5 | 1.0 | persistent for at least 2 observations |
| Absolute premium/discount | 0.5%-1.0% | product-specific | confirm NAV freshness and spread |
| Spread | rolling 90th percentile | rolling 95th percentile | confirm quote depth and market overlap |

Prefer creation-unit counts and absolute HKD flow for small funds. A 20% unit change from a tiny base can be one creation block.

### Price, Primary Flow, and Southbound States

| Price and units | Southbound | Primary interpretation |
| --- | --- | --- |
| Price up, units up | buying/holdings up | strongest demand confirmation if premium and spread are orderly |
| Price up, units flat/down | buying up | inventory transfer or delayed creation; check premium persistence |
| Price down, units up | buying up | dip buying against global/foreign selling; raise range before up |
| Price down, units down | buying up | Southbound is absorbing but not dominating; do not call a bottom |
| Price down, units down | selling/holdings down | strongest cross-border de-risking state |

For crowding, add Southbound concentration and inclusion-event demand, but do not count Southbound holding growth and vendor net-buy estimates twice. For unwind risk, distinguish global outflow offset by Southbound buying from synchronized global and Southbound selling.

## Bayesian Three-State Scenarios

Model `up`, `range`, and `down` for a fixed horizon. Suggested uncalibrated Hong Kong priors:

| Regime | Up | Range | Down |
| --- | ---: | ---: | ---: |
| Neutral cross-border balance | 0.32 | 0.40 | 0.28 |
| Southbound-supported repair | 0.40 | 0.42 | 0.18 |
| Southbound offsets global selling | 0.25 | 0.48 | 0.27 |
| Cross-border distribution | 0.18 | 0.37 | 0.45 |
| Broad breakdown | 0.10 | 0.25 | 0.65 |
| Post-washout stabilization | 0.30 | 0.50 | 0.20 |

These are scenario priors, not empirical frequencies. Update once per independent family:

- trend and relative strength;
- canonical fund-level primary flow;
- Southbound/CCASS cross-border demand;
- breadth and leadership;
- fundamentals and revisions;
- valuation;
- HKD/USD/CNH/global-flow conditions;
- policy, eligibility-review, and event response.

Reduce primary-flow reliability when peer-date coverage is poor, NAV is stale, spreads are above the 90th percentile, the fund is small relative to one creation unit, or the structure is synthetic/futures/leveraged. Run neutral-prior sensitivity. If Southbound and global flows conflict, raise `range`, widen return bands, and lower confidence rather than averaging them into a weak directional signal.

## Monitoring and Alerts

- Daily after close: reconcile canonical fund units, all-counter HKD turnover, premium/discount, spread, Southbound evidence, price-flow state, and NAV freshness.
- Weekly: update peer flows, breadth, concentration, global China ETF flows, HKD/USD/CNH conditions, and crowding/unwind scores.
- Before review dates: mark ETF Connect eligibility cutoffs, announcements, sell-only transitions, index rebalances, holidays, and underlying-market closures.
- Alert only after two independent families confirm for large/liquid funds and three for small/thin or stale-NAV funds.
- Re-entry requires unit-flow stabilization or orderly creation, narrowing discounts/spreads, breadth repair, and a price reclaim. Southbound buying alone is not right-side confirmation.

Report fund identity, counter consolidation, fund structure, NAV freshness, primary flow, Southbound state, global-flow offset, crowding/unwind, posterior sensitivity, and invalidation conditions.

## Official Sources

- HKEX ETP overview: https://www.hkex.com.hk/Products/Securities/Exchange-Traded-Products/Overview?sc_lang=en
- HKEX market makers: https://www.hkex.com.hk/Products/Securities/Exchange-Traded-Products/Market-Makers?sc_lang=en
- HKEX inclusion of ETFs in Stock Connect: https://www.hkex.com.hk/Mutual-Market/Stock-Connect/Reference-Materials/Inclusion-of-ETFs-in-Stock-Connect?sc_lang=en
- HKEX launch circular, effective 4 July 2022: https://www.hkex.com.hk/-/media/HKEX-Market/Services/Circulars-and-Notices/Participant-and-Members-Circulars/SEHK/2022/CT09122E.pdf
- HKEX Southbound regular-review criteria and dates: https://www.hkex.com.hk/-/media/HKEX-Market/Mutual-Market/Stock-Connect/Reference-Materials/Inclusion-of-ETFs-in-Stock-Connect/Inclusion_of_ETFs_in_Stock_Connect_SB_Regular_Review_Eng.pdf

Recheck current rules and effective dates before live use; eligibility thresholds and disclosure arrangements can change.
