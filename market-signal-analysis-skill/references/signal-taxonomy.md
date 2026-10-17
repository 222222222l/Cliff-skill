# Signal Taxonomy

## Data Schema

Preferred input:

```text
timestamp, open, high, low, close, volume
```

Optional fields: adjusted close, vwap, turnover, market_cap, float, sector, index membership, split/dividend adjustment flag, borrow/shortability, options-implied volatility, benchmark returns.

## Trend And Breakout

- Bullish MA regime: close above rising MA20 and MA50; stronger when MA50 above rising MA200.
- Bearish MA regime: close below falling MA20 and MA50; stronger when MA50 below falling MA200.
- Bullish crossover: faster MA crosses above slower MA within the latest 1-3 bars.
- Bearish crossover: faster MA crosses below slower MA within the latest 1-3 bars.
- Breakout: close exceeds prior N-bar high with relative volume above 1.3. Use N=20 for short/mid-term and N=55 or 252 for longer-term context.
- Breakdown: close falls below prior N-bar low with relative volume above 1.3.

## Momentum And Relative Strength

- Bullish momentum: positive 3/6/12-month return with price above MA trend filter.
- Bearish momentum: negative 3/6/12-month return with price below trend filter.
- Relative strength: symbol outperforms benchmark over the horizon; if benchmark data is missing, report absolute momentum only.

## Volume

- Bullish confirmation: up day or breakout with volume above 1.3x 20-period average.
- Bearish confirmation: down day or breakdown with volume above 1.3x 20-period average.
- Accumulation: price forms higher lows while volume expands on up moves and contracts on pullbacks.
- Distribution: price forms lower highs while volume expands on down moves and contracts on rebounds.

## MACD

- Bullish cross: MACD line crosses above signal line.
- Bearish cross: MACD line crosses below signal line.
- Bullish zero-line regime: MACD above zero and rising.
- Bearish zero-line regime: MACD below zero and falling.
- Bullish histogram acceleration: histogram increases for at least 3 consecutive bars.
- Bearish histogram acceleration: histogram decreases for at least 3 consecutive bars.

## RSI

- Oversold rebound: RSI crosses up through 30 or 40 after oversold/weak conditions.
- Overbought reversal: RSI crosses down through 70 or 60 after overbought/strong conditions.
- Bullish regime: RSI mostly holds above 40 and retakes 50.
- Bearish regime: RSI mostly stays below 60 and loses 50.

## KDJ / Stochastic

- Bullish KDJ cross: K crosses above D while K/D are below 30, or J rebounds from extreme weakness.
- Bearish KDJ cross: K crosses below D while K/D are above 70, or J turns down from extreme strength.
- Treat KDJ as a timing/exhaustion signal. Do not let it dominate trend and momentum evidence.

## Divergence

Detect divergence from recent swing highs/lows:

- Bullish bottom divergence: price makes a lower low while MACD histogram/line, RSI, or KDJ makes a higher low.
- Bearish top divergence: price makes a higher high while MACD histogram/line, RSI, or KDJ makes a lower high.
- Require two visible swing points. Prefer divergence confirmed by a trendline break, MACD/RSI turn, or volume reversal.
- Penalize divergence that fights a strong weekly/monthly trend unless the user asks for short-term reversal timing.

## Bottom Reversal Structures

- Bottom bullish engulfing: after a visible downtrend, the latest daily candle is bullish, the prior candle is bearish or weak, and the latest real body effectively exceeds the prior day's real-body high. Use the higher of the prior open/close as the body-high reference; do not upgrade a mere intraday-shadow break.
- Effective volume expansion: latest volume or turnover is at least 1.3x the prior day, with 1.5x or higher treated as stronger evidence. Prefer volume that also exceeds the 20-period average; downgrade isolated abnormal volume that reverses into weakness.
- Support confirmation: latest price is near a key MA, recent 20/55-period low, prior base, gap support, or high-turnover support shelf. When chip-distribution data is unavailable, state that support is approximated from OHLCV structure.
- Reversal confidence: all three checks support a high-confidence early reversal candidate after follow-through; two checks create a lower-confidence watch; one check is not a reversal signal.
- Key-MA reclaim/retest: price reclaims a horizon-relevant MA, retests without an effective close below it, and resumes with sustained healthy volume. Use it as stronger reversal confirmation than a single-day candle.

## Evidence Object

Each matched signal should be reported with:

```json
{
  "timeframe": "daily",
  "family": "macd_combo",
  "signal": "bullish_macd_cross",
  "direction": "bullish",
  "strength": 0.62,
  "recency_bars": 1,
  "evidence": "MACD crossed above signal; histogram positive for 3 bars",
  "limitations": []
}
```
