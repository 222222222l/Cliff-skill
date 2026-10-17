# Cycle Overlay Analysis

Use this reference when a request asks about macro cycles, Kondratieff cycles, dollar-liquidity tides, credit/inventory cycles, industry prosperity cycles, sector rotation cycles, multi-cycle resonance, cycle weighting, macro-financial regime, buffer cushions, black-swan risk, Fourier/FFT cycle confirmation, or Bayesian trend probabilities.

Cycle analysis should improve evidence discipline. It should not turn vague long-cycle stories into deterministic forecasts. Treat long cycles as priors; require current data to confirm them.

## Cycle Hierarchy

Analyze from slow to fast, then reconcile from fast back to slow:

| Layer | Typical Horizon | Main Evidence | Use |
| --- | ---: | --- | --- |
| Kondratieff / technology-capex background | 20-60 years | General-purpose technology, infrastructure waves, commodity supercycles, geopolitical supply chains | Low-frequency prior; not a timing signal by itself. |
| Global dollar tide / external liquidity | 1-7 years | Fed policy, real rates, DXY, U.S. reserves/RRP/TGA, global credit spreads, USD funding stress, capital flows | Affects valuation multiples, EM liquidity, commodities, and high-duration assets. |
| Domestic economic and credit cycle | 1-5 years | GDP/PMI, credit impulse, fiscal impulse, PPI/CPI, property, exports, industrial profits, employment | Sets aggregate demand, pricing power, and risk appetite. |
| Policy and institutional cycle | 3-36 months | fiscal subsidies, procurement, regulation, industrial policy, anti-corruption, supply-side controls, state-capital allocation | Can create or destroy industry demand and valuation support. |
| Industry supply-demand cycle | 3 months-5 years | capacity, utilization, inventory, order backlog, product prices, spreads, capex, import/export volume | Core profit-cycle signal for sectors and stocks. |
| Sector market cycle | 1 week-18 months | relative strength, breadth, turnover, fund flow, earnings revisions, valuation percentile, leadership | Confirms whether investors are pricing the cycle. |
| Single-security cycle | days-24 months | company fundamentals, events, technical stage, float supply, insider actions | Converts cycle view into actionable risk levels. |

Fourier/FFT frequency-domain evidence can be used inside the sector market cycle, global dollar tide, liquidity, commodity, or single-security layers when sufficient time-series data exists. Treat it as a cycle-stability and noise-quality overlay, not as an independent macro cause.

## Macro-Financial Five-Direction Checklist

Before assigning a macro or sector probability, reconcile five directions:

| Direction | What It Measures | Typical Evidence | Bayesian Role |
| --- | --- | --- | --- |
| Fundamentals and cycles | Real demand, profits, margins, credit, inventory, capex, employment | GDP/PMI, earnings, order backlog, spreads, utilization, credit impulse | Sets the base prior. |
| Market sentiment and bubble | Whether price has outrun fundamentals or fear has overshot reality | valuation percentile, turnover, leverage, fund flows, breadth, options/skew, media consensus | Adjusts timing and crash/rebound risk. |
| Official-data water | Whether headline data may overstate or understate true momentum | sub-components, revisions, alternative proxies, trade-partner data, market prices | Reduces reliability or reconstructs the prior. |
| Buffer cushions | Resources that absorb shocks before forced liquidation or policy panic | cash, deposits, reserves, bank capital, provisions, fiscal space, maturities, collateral, current account, hedges | Dampens or amplifies transmission speed. |
| Black-swan vulnerability | Low-probability high-impact jump risks | geopolitics, policy shock, funding freeze, fraud, cyber, commodity shock, sanctions, disaster | Adds scenario tails and position-size caution. |

Do not treat a buffer as the same thing as bullish momentum. A strong buffer may only delay deterioration or reduce forced selling; it does not prove new profit growth.

## Signal Scoring

For each layer, assign a direction score and reliability:

- Direction score `s`: `+2` strong upswing, `+1` improving, `0` neutral/mixed, `-1` deteriorating, `-2` contraction/stress.
- Reliability `r`: `0.3` weak/noisy, `0.5` partial evidence, `0.7` good evidence, `1.0` high-confidence multi-source confirmation.
- Time alignment: downgrade reliability when the cycle evidence is stale, lagging, or only narrative.

Use current, measurable data where possible:

- Growth: PMI, industrial production, retail sales, exports, fixed asset investment, credit impulse.
- Inflation/pricing: PPI, CPI, commodity prices, product price indices, industry spreads.
- Liquidity: rates, credit spreads, money/credit growth, dollar index, funding stress, equity turnover.
- Industry: capacity utilization, inventory days, backlog, order intake, utilization, revenue and margin revisions.
- Market: relative strength, breadth, volume, valuation, fund flows, earnings revisions.
- Frequency-domain rhythm: rolling FFT on log returns, detrended log price, realized volatility, turnover, relative strength, or breadth to test whether dominant cycle bands are stable and whether high-frequency noise is rising.

## Buffer-Cushion Scoring

Score buffers separately from cycle direction:

- Buffer score `b`: `+2` ample and usable, `+1` moderate, `0` unclear/neutral, `-1` thin, `-2` already being consumed or unavailable.
- Reliability `br`: `0.3` weak/noisy, `0.5` partial evidence, `0.7` good evidence, `1.0` multi-source confirmation.
- Transmission effect: positive buffers slow stress propagation; negative buffers accelerate it.

Common buffer checks:

| Buffer | Positive Evidence | Negative Evidence |
| --- | --- | --- |
| Household | high liquid deposits, low short-term debt service, stable wages | falling income, rising delinquency, forced asset sales |
| Corporate | net cash, low refinancing need, high backlog, short cash-conversion cycle | receivables surge, inventory buildup, refinancing wall |
| Financial system | high capital/provisions, stable deposits, low wholesale funding reliance | rising NPL migration, deposit competition, capital injections under stress |
| Government/policy | fiscal room, credible facility, targeted support with funding source | hidden debt rollover pressure, unfunded mandates, delayed payments |
| External | current-account surplus, usable FX liquidity, stable capital flows | funding squeeze, reserve drain, currency mismatch |
| Market structure | low leverage, dispersed positioning, reasonable valuation | crowded ownership, margin financing, ETF/liquidity illusion |

When data is official or incomplete, estimate a buffer range instead of a point score and reduce `br`.

## Horizon Weights

Select weights by the user's horizon. Normalize weights to 1.0 after removing unavailable layers.

### Short-Term Trading: days to 4 weeks

| Layer | Weight |
| --- | ---: |
| Sector market cycle and technical structure | 0.30 |
| Single-security event/float/liquidity cycle | 0.20 |
| Industry price/inventory short-cycle | 0.20 |
| Domestic policy/liquidity impulse | 0.15 |
| Global dollar tide | 0.10 |
| Long-cycle/Kondratieff background | 0.05 |

### Medium-Term Allocation: 1 to 6 months

| Layer | Weight |
| --- | ---: |
| Industry supply-demand cycle | 0.30 |
| Sector market cycle and earnings revisions | 0.20 |
| Domestic economic/credit cycle | 0.18 |
| Policy/institutional cycle | 0.15 |
| Global dollar tide | 0.10 |
| Long-cycle/Kondratieff background | 0.07 |

### Long-Term Allocation: 6 to 24 months

| Layer | Weight |
| --- | ---: |
| Industry supply-demand and capex cycle | 0.28 |
| Domestic economic/credit cycle | 0.20 |
| Policy/institutional cycle | 0.17 |
| Long-cycle/Kondratieff or technology-capex background | 0.15 |
| Global dollar tide | 0.10 |
| Sector market cycle | 0.07 |
| Single-security cycle | 0.03 |

Do not over-weight a long cycle for a short-term decision. Do not over-weight technical momentum for a long-term industry prosperity call.

## Overlay Score

Calculate an effective cycle score:

```text
effective_weight_i = weight_i * reliability_i
cycle_score = sum(effective_weight_i * direction_score_i) / sum(effective_weight_i)
```

Interpretation:

| Cycle Score | State |
| ---: | --- |
| `>= +1.0` | Multi-cycle rising prosperity / strong resonance |
| `+0.4 to +1.0` | Improving or early-to-mid upswing |
| `-0.4 to +0.4` | Mixed, transition, or no durable cycle edge |
| `-1.0 to -0.4` | Deteriorating or late-cycle rollover |
| `<= -1.0` | Multi-cycle contraction / high decline risk |

Confidence is lower when the score is driven by one layer, when evidence is lagging, when policy can abruptly reverse incentives, or when market price strongly disagrees with fundamentals.

## Fourier Frequency-Domain Overlay

Use references/fourier-cycle-analysis.md when Fourier/FFT evidence is material. Integrate it conservatively:

| Fourier Evidence | Cycle Impact |
| --- | --- |
| Stable low-frequency trend agrees with the scored macro/industry/technical layer | Increase that layer's reliability by `+0.05` to `+0.15`, capped at `1.0`. |
| Stable medium-frequency rhythm agrees with major trend and breadth | Improve timing confidence; do not upgrade fundamental prosperity by itself. |
| High-frequency energy share rises sharply | Reduce position confidence, increase event/noise caution, or add a tail-risk warning. |
| Dominant period appears in only one window or after parameter fishing | Do not adjust the cycle score; mention as low-reliability observation only. |
| Frequency-domain correlation shows low-frequency co-movement across supposed hedges | Reduce diversification confidence and increase black-swan vulnerability. |

Do not double-count the same price trend. If trend-stage analysis already scored a strong moving-average or relative-strength trend, Fourier low-frequency confirmation should adjust reliability rather than add a separate large bullish direction score.

## Bayesian Trend Probability

Use Bayesian updating to turn a prior trend probability into a posterior probability.

1. Set a prior probability:
   - `0.50` when no reliable trend/fundamental prior exists.
   - Technical-only prior from trend analysis when price data is strong.
   - Fundamental prior from earnings, margin, and cash-flow quality when available.
2. Convert prior to log odds:
   - `logit(p) = ln(p / (1 - p))`
3. Add cycle evidence:
   - `posterior_logit = logit(prior) + beta * cycle_score`
   - Default `beta = 0.75` for medium-term sector calls.
   - Use `beta = 0.45` for short-term trades and `beta = 0.90` for long-term industry calls with strong data.
   - If FFT evidence is strong and non-overlapping, apply it through reliability changes first. Use only a small extra logit adjustment (`+/-0.05` to `+/-0.25`) for timing/noise when it is not already captured by trend, breadth, or special-date risk.
4. Add buffer-cushion evidence:
   - `buffer_score = sum(buffer_weight_i * br_i * b_i) / sum(buffer_weight_i * br_i)`
   - `posterior_logit += gamma * buffer_score`
   - Default `gamma = 0.25` for ordinary sector calls, `0.40` for macro-financial stress calls, and `0.15` for short-term technical trades.
   - Cap the positive buffer contribution at `+0.25` logit unless buffers directly create demand or earnings.
   - Allow negative buffer contribution down to `-0.50` logit when buffers are already being consumed.
5. Add or subtract only non-overlapping hard evidence:
   - `+0.15 to +0.35` for confirmed price increases, backlog, earnings revisions, and breadth confirmation.
   - `-0.15 to -0.35` for margin compression, inventory buildup, financing stress, or failed price breakout.
   - Cap total manual adjustment to `+/-0.50` unless a major shock occurs.
6. Add black-swan scenario overlay:
   - Do not predict an exact black-swan event as a base case.
   - Assign tail vulnerability: low, medium, high.
   - For high vulnerability, report a downside scenario probability and reduce position confidence even if the base posterior is favorable.
   - For realized shocks, bypass ordinary caps and rebuild scenarios from liquidity, solvency, policy response, and price gaps.
7. Convert back:
   - `posterior_probability = 1 / (1 + exp(-posterior_logit))`

Report probabilities as scenario-weighted evidence, not certainty. If the posterior exceeds 70% only because of narrative, low-reliability long-cycle assumptions, or buffers that only delay stress, reduce it.

## Cross-Validation

Require at least three of five evidence families before calling a sector a rising prosperity cycle:

1. Macro/policy support: credit, fiscal, regulation, procurement, or external demand helps the sector.
2. Industry hard data: prices, spreads, utilization, inventory, orders, exports, or backlog improve.
3. Financial statements: revenue, gross margin, deducted profit, cash flow, or earnings revisions improve.
4. Market confirmation: relative strength, breadth, volume, leadership, or valuation rerating confirms.
5. Micro confirmation: leading companies disclose orders, capacity utilization, delivery, or customer adoption.
6. Buffer confirmation: balance-sheet, liquidity, fiscal, external, or market-structure cushions are not being rapidly consumed.
7. Frequency-domain confirmation: rolling FFT shows stable cycle bands or a stable low-frequency trend that agrees with current market/fundamental evidence, without high-frequency noise overwhelming the signal.

For declining cycles, require at least three of:

- Demand weakening.
- Price/spread decline.
- Inventory or receivables stress.
- Margin/profit deterioration.
- Policy/regulatory headwind.
- Market relative weakness and failed rebounds.

## Output Template

When using cycle overlay, include:

1. Data date, sources, horizon, and confidence.
2. Cycle-state table by layer with direction score, reliability, and evidence.
3. Weighted cycle score and Bayesian posterior probability.
4. Five-direction macro check: fundamentals/cycles, sentiment/bubble, official-data water, buffers, black-swan vulnerability.
5. Cross-validation: macro/policy, industry data, financial statements, market confirmation, micro evidence, buffer confirmation, and optional frequency-domain confirmation.
6. Upside industries: why multiple cycles align, what could invalidate the view.
7. Downside/declining industries: what pressures overlap, what could reverse the view.
8. Ordinary-investor caution: distinguish prosperity trend from chaseable price, and name the level or evidence that would force reassessment.
