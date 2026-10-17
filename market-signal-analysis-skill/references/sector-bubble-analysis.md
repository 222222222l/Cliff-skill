# Sector and Bubble Momentum Analysis

Use this reference when analyzing sectors, boards, themes, main-line markets, policy-driven rallies, or bubble-like momentum. Examples include AI hardware, semiconductors, CPO, storage, gold, rare earths, brokerages, biotech themes, and any "can it keep rising / can it double / is it time to be bold or cautious" question.

## Data Requirements

Prefer structured data over impressions:

- Sector/index OHLCV and amount for at least 60 daily bars; 120-252 bars is better.
- Constituent returns, market caps, turnover, and price positions when available.
- Benchmark index and peer-sector returns for relative strength.
- Northbound, ETF/fund flow, margin financing, and turnover heat when available.
- Fundamental catalysts such as orders, price hikes, earnings guidance, capacity, inventory, policy, and liquidity conditions.
- Insider sell-down, block transfer, inquiry transfer, private placement, or large shareholder reduction announcements when relevant.

If breadth, flows, or constituent data are missing, disclose the limitation and reduce confidence. Do not infer broad sector strength from one or two leaders alone.

## Trend/Momentum Score T

Compute a 0-100 score. Use it to judge whether the market still rewards risk-taking.

| Factor | Weight | Evidence |
| --- | ---: | --- |
| Price trend | 25 | Price above MA20/MA50/MA120; moving averages rising; 20-day or 55-day breakout; pullbacks hold MA10/MA20. |
| Relative strength | 20 | Sector outperforms benchmark and peer sectors over 5/10/20/60 days; relative strength line makes new highs. |
| Breadth and rotation | 15 | Many constituents rise; share above MA20/MA50 improves; new highs broaden; gains are not only one or two leaders; laggards rotate without leaders breaking. |
| Volume and turnover | 15 | Breakouts expand amount/turnover; pullbacks shrink volume; failed rallies are not repeatedly high-volume. |
| Fundamental validation | 15 | Orders, price hikes, earnings previews, margins, utilization, or industry data continue to exceed expectations. |
| Policy and liquidity | 10 | Policy narrative, liquidity, fund flows, or institutional positioning still support the theme. |

Interpretation:

| T range | Read |
| ---: | --- |
| 75-100 | Strong trend; do not fight solely on valuation. |
| 60-74 | Positive trend but monitor breadth and volume. |
| 45-59 | Mixed; use smaller exposure or wait for confirmation. |
| below 45 | Trend support is weak or broken. |

## Bubble-Risk Score R

Compute a 0-100 score. Use it to judge fragility, not immediate downside.

| Factor | Weight | Evidence |
| --- | ---: | --- |
| Valuation percentile | 20 | Sector or leaders enter high historical valuation percentiles; current valuation needs unrealistic multi-year profit growth. |
| Price overextension | 15 | 1-3 month rise far exceeds fundamental change; price sits far above MA20/MA50; consecutive gaps or limit-up style acceleration. |
| Turnover and inflow heat | 15 | Turnover, financing, ETF/fund subscriptions, or social attention are overheated; late-stage retail FOMO appears. |
| Breadth deterioration | 15 | Leaders make highs while the number of rising constituents falls; new highs narrow; laggards fail to follow; index rise depends on a few heavyweights. |
| Failed-breakout behavior | 15 | Double top fails, second breakout reverses below prior high, long upper shadows increase, good news stops moving prices, or high-volume stagnation appears. |
| Supply pressure | 10 | Large shareholder reductions, inquiry transfers, private placements, sell-down plans/results, or unlock pressure increase. |
| Consensus euphoria | 10 | Media/social narrative shifts to "cannot lose", "not buying means falling behind", or extreme extrapolation of the theme. |

Interpretation:

| R range | Read |
| ---: | --- |
| 0-39 | Bubble pressure is low to moderate. |
| 40-59 | Trend can continue, but risk controls matter. |
| 60-74 | Fragile bubble momentum; avoid adding without strong confirmation. |
| 75-100 | Late-stage risk; require strict exit rules or reduce exposure. |

## Bold/Cautious Matrix

Use T and R together. Do not make decisions from either score alone.

| State | Read | Action language |
| --- | --- | --- |
| T >= 70 and R < 50 | Strong trend, risk not extreme | Be bold on pullbacks; trend-following exposure is justified. |
| T >= 70 and R 50-75 | Bubble-like main uptrend | Participate only as trend exposure; avoid leverage; use mechanical exits. |
| T 50-70 and R >= 70 | High-level fatigue | Become cautious; reduce or avoid chasing. |
| T < 50 and R >= 60 | Expensive and weakening | Treat as trend break or distribution unless quickly repaired. |
| T < 50 and R < 50 | No strong trend | Wait for a new signal. |

## Breakout, Double Top, and Second Breakout

Do not label every double top as bearish. Require invalidation evidence.

Bullish second breakout:

- Breaks prior high with expanded amount.
- Pullback stays above the old high or MA10/MA20.
- Volume contracts on pullback.
- Leaders continue to make highs and breadth does not collapse.

Failed breakout:

- Breaks prior high intraday but closes with a long upper shadow.
- Falls back below the prior high within 1-3 sessions.
- Retest fails on lower highs or high-volume stagnation.
- Sector index rises while most constituents weaken.

For bubble-like sectors, use MA5 as sentiment line, MA10 as strong-trend line, and MA20 as main trend line. A close below MA20 is a warning; failure to recover within about three sessions materially reduces T and raises R.

## Sector Breadth Checklist

Measure breadth whenever constituent data are available:

- Advance/decline ratio for the session and rolling 5/10/20 sessions.
- Share of constituents above MA20/MA50/MA120.
- New 20-day/60-day highs minus lows.
- Equal-weight sector return versus cap-weighted sector return.
- Top 5 constituent contribution to sector return and amount.
- Leader basket versus laggard basket returns.
- Whether rotation occurs within the theme without leaders breaking down.

If cap-weighted sector indices rise while equal-weight or median constituent returns weaken, state that the rally is narrowing.

## A-Share Main-Line and Policy Caveats

For A-shares, adjust interpretation for price limits, T+1 trading, retail participation, policy narratives, financing balance, ETF/fund subscriptions, and sell-down announcements.

When the user asks whether ordinary investors can follow a sector ETF, whether broad ETFs are safe to hold, or whether index stability is masking retail losses, also use references/a-share-macro-trading-model.md. A strong A-share theme is lower quality if the broad market is in range-stabilized liquidity extraction, ETF shares are contracting, median-stock returns are deeply negative, and the theme's turnover share greatly exceeds its market-cap share.

Policy support can extend trends and valuation expansion, but it is not a substitute for breadth and liquidity. Distinguish:

- Real industry cycle: orders, prices, capacity, margins, and earnings improve.
- Policy narrative: valuation tolerance and fund willingness rise.
- Liquidity concentration: money exits weaker sectors and crowds into the strongest theme.

When a theme rises during broad market weakness, do not automatically call it new money. Consider whether it is sector rotation or liquidity extraction from other sectors.

## Probability Framing

When data are sufficient, present scenario probabilities instead of a single target:

- Continued trend or final acceleration.
- High-level consolidation while fundamentals catch up.
- Rotation from leaders to laggards.
- 20-35% correction after failed breakout or earnings disappointment.
- Full trend break when leaders, breadth, and volume all deteriorate.

Avoid precise "can double" claims unless the analysis includes valuation capacity, earnings growth needed to support the move, liquidity capacity, and historical analogs.
