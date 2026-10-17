# Trend Stage Analysis

Use this reference when the user asks whether a trend is ending, where an uptrend/downtrend would be invalidated, how to judge a stage trend, whether to hold a main-trend position, or how to combine Vegas channel, Granville moving-average rules, ordinary moving averages, ATR stops, Donchian levels, momentum, volume, and relative strength.

Do not claim that any indicator has a permanently highest win rate. Treat "best" indicators as regime-dependent evidence. Use historically robust priors, then adjust by asset type, liquidity, volatility, market structure, and available backtest samples.

## Data Requirements

- Minimum: 252 daily OHLCV bars for ordinary daily trend analysis.
- Preferred: 676+ daily bars for full Vegas long-cycle channels; 104+ weekly bars for long-horizon confirmation.
- For ETFs, indices, and liquid stocks, require adjusted prices when dividends/splits matter.
- For A-shares, disclose price-limit, T+1, suspension, policy-theme, and northbound/fund-flow caveats when relevant.
- For low-liquidity or frequently suspended assets, reduce confidence before scoring trend evidence.

## Trend Stage Taxonomy

Classify the asset into one primary stage and one transition risk:

| Stage | Typical Evidence | Practical Read |
| --- | --- | --- |
| Base / accumulation | Price oscillates around flat MA50/MA120; Vegas channel flat; volatility compresses; volume does not confirm breakdowns. | Direction is not proven. Wait for reclaim/breakout or use range rules. |
| Early trend reversal | Price reclaims MA50/MA120; MA20 and MA50 turn up; MACD repairs toward/above zero; relative strength improves. | Trend is improving, but failure risk remains high until pullbacks hold. |
| Healthy uptrend | Price above rising MA20/MA50/MA120 and daily Vegas channel; pullbacks hold MA20/MA50; RSI often holds 40-50 zone; volume expands on advances and contracts on pullbacks. | Main trend is intact. Prefer staged holding and pullback adds over chasing exhaustion. |
| Main acceleration / parabolic | Price far above MA20/MA50/Vegas; ATR expands; RSI stays elevated; breadth and leadership must confirm. | Vegas becomes too slow for risk control. Use MA20, MA50, ATR, and failed-breakout rules first. |
| Distribution / fatigue | New highs narrow; MACD/RSI divergence; high-volume stagnation; repeated failed breakouts; MA20 is lost and not quickly reclaimed. | Uptrend may still exist, but payoff becomes asymmetric. Reduce reliance on old momentum. |
| Trend break | Close below MA50/MA120 or Vegas channel with failed recovery; weekly confirmation strengthens the signal. | Treat as trend damage, not just noise, especially if relative strength and volume also deteriorate. |
| Downtrend | Price below falling MA20/MA50/MA120; Vegas turns down; rallies fail at MA20/MA50; relative strength remains weak. | Do not use oversold alone as a buy signal. Require reversal structure. |

## Indicator Families and Default Weights

Use this trend-stage weighting when the user's primary question is trend direction, trend ending, stage classification, or position-level invalidation. Keep the general probability framework in statistical-weighting.md for ordinary buy/sell/hold calls.

| Family | Default Weight | What To Check |
| --- | ---: | --- |
| Trend structure and MA stack | 0.25 | Price vs MA20/50/120/200, Granville rule state, MA slopes, higher highs/lows, pullback behavior. |
| Vegas channel | 0.20 | Daily EMA144/169 main channel, EMA576/676 long-cycle background, channel slope, recover/fail behavior. |
| Momentum and relative strength | 0.15 | 3/6/12-month momentum, benchmark/sector/peer relative strength, persistence during market pullbacks. |
| Breakout and support structure | 0.12 | Donchian 20/55 highs/lows, failed breakouts, prior pivot support/resistance, gap/limit zones. |
| Volume and turnover confirmation | 0.10 | Breakout volume, pullback volume contraction, distribution volume, turnover heat and fund-flow stress. |
| MACD/RSI/KDJ confirmation | 0.10 | MACD zero-line regime, histogram acceleration, RSI regime, divergence, oscillator failure swings. |
| Volatility and ATR trailing risk | 0.08 | ATR expansion, Chandelier exits, Bollinger expansion/squeeze, gap risk, stop distance. |

Weights must sum to 1.0 after asset-specific adjustment. Penalize duplicate evidence: MA20 loss, 20-day low, and 2ATR Chandelier can point to the same short-term damage and should not all receive full independent credit.

## Asset-Specific Adjustments

For broad indices and index ETFs:
- Raise MA/Vegas/multi-timeframe structure weight.
- Raise breadth and constituent participation when available.
- Lower single-instrument volume weight because ETF volume can reflect creation/redemption and hedging.

For liquid single stocks:
- Keep MA/Vegas/RS as core evidence.
- Raise volume/turnover and event-risk penalties around earnings, guidance, lock-up expiry, major policy/news catalysts, or insider selling.

For A-share themes, sectors, and high-beta growth boards:
- Raise MA20/MA50, ATR trailing, breadth, turnover heat, and failed-breakout evidence.
- Reduce reliance on Vegas for timing in fast policy/theme bubbles; use Vegas mainly for formal main-trend invalidation.
- Treat limit-up/limit-down clustering, financing balance, northbound/fund flows, sector breadth, and policy narrative decay as important context.

For commodities, futures, and crypto:
- Raise volatility, ATR, liquidation/funding, term structure, inventory, and macro-liquidity evidence.
- Use Vegas mainly on daily/weekly trend context, not as the only stop mechanism.
- Require wider noise bands because 24/7 trading and leverage liquidations can create false breaks.

For low-liquidity small caps:
- Reduce overall confidence.
- Discount volume spikes that may be one-off or manipulation-prone.
- Require more confirmation from weekly structure and recover/fail behavior.

## Vegas Channel Rules

Use daily EMA144 and EMA169 as the main Vegas trend channel. Use EMA576 and EMA676 as long-cycle bull/bear background when enough data exists.

Bullish main-trend conditions:
- Price is above EMA144/169.
- EMA144/169 channel is rising or flattening upward.
- Pullbacks into the channel recover quickly.
- MA50/MA120 are rising or not yet damaged.

Warning conditions:
- Price approaches the EMA144/169 channel after a large extension above MA20/MA50.
- Price loses MA50 before testing Vegas.
- Relative strength turns down before price breaks Vegas.
- A pullback into the channel is accompanied by expanding down-volume or broad sector deterioration.

Formal daily trend-end rule:
- A close below the lower side of EMA144/169, followed by failure to recover within 2-3 sessions, is a daily main-trend break.
- A weekly close below the daily Vegas channel or below the corresponding weekly trend structure gives stronger confirmation.
- If price breaks below Vegas but immediately reclaims it on strong volume and relative strength, classify it as a bear trap / false break candidate rather than a confirmed trend end.

Do not wait for Vegas in parabolic or high-beta trends. By the time price reaches EMA144/169, a large drawdown may already have occurred.

## Granville Moving-Average Rules (葛兰碧八大法则)

Use Granville rules as a price-behavior checklist around an important moving average, not as a standalone trading system. Select the reference average by horizon:

- Tactical trading: MA20 or MA30.
- Swing trend: MA50 or MA60.
- Long trend: MA120, MA200, or MA250.
- Full trend view: compare the Granville state across short, swing, and long averages.

Bullish rules:

1. Price breaks above a flattening or rising MA after a base, while the MA turns up: early reversal candidate.
2. Price pulls back toward a rising MA and holds above it: healthy continuation or staged-add candidate.
3. Price briefly dips below a rising MA but quickly reclaims it with volume or relative-strength repair: false-break / bear-trap candidate.
4. Price is far below a falling MA after capitulation and starts reverting: oversold rebound only unless the MA later flattens and price builds a base.

Bearish rules:

1. Price breaks below a flattening or falling MA after a mature advance, while the MA turns down: trend-damage candidate.
2. Price rallies toward a falling MA and fails: reduce-on-rebound or avoid-bottom-fishing signal.
3. Price briefly rises above a falling MA but cannot hold it: bull-trap / failed-repair candidate.
4. Price is far above a rising MA after a parabolic move and then loses MA20 or forms exhaustion volume: risk-reduction signal, even before long-term trend breaks.

Confirmation rules:

- Upgrade a Granville signal only when volume, relative strength, breadth, and higher-timeframe structure confirm it.
- Downgrade it when the MA is flat and price is range-bound; many Granville signals whipsaw inside sideways markets.
- In A-shares, limit-up/limit-down, suspensions, theme hype, and T+1 constraints can delay execution; use wider confirmation bands.
- In low-liquidity stocks, do not treat one-day volume spikes as reliable confirmation.
- For losing positions, a bearish Granville state should prevent averaging down unless fundamental evidence improves and price reclaims the relevant MA.

## Bottom Reversal Confirmation

Use these rules for individual stocks, index ETFs, and indices that are already in a visible downtrend or post-crash decline. Do not apply them to ordinary pullbacks inside a healthy uptrend, and do not treat one candlestick as a durable long-term reversal without follow-through.

### Bullish Engulfing Bottom Signal

On the daily chart, classify a bottom bullish-engulfing reversal only when the setup is in a downtrend and these three checks are evaluated together:

1. Candlestick structure: the latest candle is bullish, the prior candle is bearish or weak, and the latest real body effectively exceeds the prior day's real-body high, preferably closing above the higher of the prior open/close rather than only piercing an intraday shadow.
2. Volume confirmation: latest volume or turnover expands materially versus the prior day. Treat 1.3x as a minimum effective expansion, 1.5x or more as stronger confirmation, and downgrade abnormal one-off volume that looks like distribution or a failed limit-up.
3. Support context: price appears near an important moving-average support, prior base, recent swing low, gap support, or high-turnover/volume-by-price shelf. If chip-distribution data is unavailable, approximate with MA20/50/120/200, recent 20/55-day lows, prior consolidation ranges, and high-volume bars.

Interpretation:

- All three checks present: high-confidence early reversal candidate; if the next 1-3 sessions hold the engulfing midpoint/low or reclaim the nearest MA, treat the bottom reversal as likely established for the user's short/mid horizon.
- Two checks present: lower-confidence reversal watch. Raise confidence only when volume expansion is strong, the bullish body is large and closes near the high, and follow-through holds support; otherwise classify it as an oversold bounce.
- One check present: do not call a reversal signal. Use it only as background evidence.

Invalidate the signal when price quickly closes back below the engulfing candle midpoint or low, loses the support zone on expanding volume, or fails to follow through while the relevant MA remains falling.

### Key-MA Reclaim And Retest Signal

Also treat reversal as confirmed when price stands above a key MA for the horizon, pulls back without an effective break, and then resumes with sustained healthy volume expansion.

- Tactical reversal: reclaim MA20/MA30, retest without closing materially below it, and show 3-5 sessions of constructive volume.
- Swing reversal: reclaim MA50/MA60, hold the retest, and show improving relative strength and MACD repair toward/above zero.
- Long reversal: reclaim MA120/MA200 or the Vegas EMA144/169 area, hold on weekly structure, and show fundamental/sector confirmation when available.

Healthy volume means rising volume on advances, contracting volume on pullbacks, and no repeated high-volume rejection at the same resistance. For broad indices, rely more on breadth, constituent participation, and ETF/futures flow because index volume alone can be distorted.

## Fast-Trend Risk Stack

When price is far above Vegas, stage risk controls from fast to slow:

| Layer | Typical Rule | Interpretation |
| --- | --- | --- |
| First warning | Lose MA20, close below 2ATR Chandelier, or fail to reclaim a short breakout level. | Momentum cooling; not necessarily trend end. |
| Strong warning | Lose 3ATR Chandelier, 20-day low, or repeated MA20 reclaim failures. | Acceleration phase likely ending. Reduce chase behavior. |
| Mid-trend break | Lose MA50, 55-day low, or key pivot with expanding down-volume. | Swing/intermediate trend is damaged. |
| Formal main-trend end | Lose EMA144/169, MA120/MA200, or weekly structure with failed recovery. | Main trend likely ended or entered a larger correction. |

For long-term holders, separate "take-profit/risk reduction" from "formal trend end." Fast-layer breaks can justify reducing exposure even while the main Vegas trend is technically intact.

## Auxiliary Indicator Rules

- MA stack: healthy uptrends usually have price > MA20 > MA50 > MA120 > MA200 with upward slopes. Slope matters more than the mere cross.
- Granville: classify whether price is breaking, pulling back, reclaiming, failing, or overextending around the relevant MA; treat the rule as stronger when it agrees with MA slope and volume.
- Donchian: 20-day lows are short-term risk markers; 55-day lows are stronger trend-damage markers. Breakouts that fail within 3-5 sessions are bearish evidence.
- Chandelier Exit: use highest high over 20 or 60 sessions minus 2ATR/3ATR. The 2ATR level is earlier but noisier; 3ATR is slower but more robust.
- MACD: above-zero MACD supports trend continuation; below-zero crosses after extended runs are more serious than isolated signal-line crosses.
- RSI: overbought is not a sell signal in strong trends. In healthy uptrends RSI often holds above 40-50; repeated breaks below 40 are trend-damage evidence.
- Volume: bullish breakouts should expand volume; pullbacks should contract volume. Heavy down-volume after failed highs is distribution evidence.
- Relative strength: a market leader should resist benchmark drawdowns and recover faster. If absolute price is rising but relative strength is falling, downgrade trend quality.
- Breadth: for sectors/themes, track the share of constituents above MA20/50/120, equal-weight versus cap-weighted performance, and whether gains rely on one or two leaders.

## Weighted Trend Dashboard

Use a dashboard instead of a single indicator verdict:

```text
趋势阶段：健康上升 / 加速主升 / 分歧派发 / 趋势破位 ...
综合趋势分：0-100
短线动能分：0-100
中期趋势分：0-100
长期背景分：0-100
趋势结束置信度：低 / 中 / 高
```

Suggested score interpretation:

| Score | Read |
| ---: | --- |
| 75-100 | Strong trend; only fast-layer risk controls may be active. |
| 60-74 | Uptrend intact but needs confirmation; avoid aggressive chasing if extended. |
| 45-59 | Mixed / transition zone; wait for reclaim or breakdown confirmation. |
| 30-44 | Trend damaged; rallies need proof. |
| 0-29 | Downtrend or failed trend; reversal requires new evidence. |

## Output Format for Trend Questions

When the user asks a trend-stage or trend-end question, include:

1. Data, horizon, and confidence.
2. Trend stage classification.
3. Key levels table:
   - short warning level
   - strong warning level
   - mid-trend break level
   - formal main-trend end level
4. Weighted indicator dashboard.
5. Bullish evidence and bearish/risk evidence.
6. What would upgrade the trend and what would downgrade it.
7. Risk-control language for the user's horizon.

Use cautious phrasing:

```text
当前更像是“加速后的回撤风险上升”，还不是“主趋势已经结束”。
若连续 2-3 个交易日无法收回 Vegas 下沿，才更接近日线主趋势结束。
若跌破 MA20/2ATR，只说明短线动能退潮；若再跌破 MA50/55日低点，中期趋势才明显受损。
```

Avoid:

```text
必然见顶
这个指标胜率最高所以一定有效
跌破某一条均线就无条件清仓
```
