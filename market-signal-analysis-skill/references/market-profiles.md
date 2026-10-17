# Market Profiles

## Default: us_equity

Use `us_equity` when the user asks about U.S. stocks, ETFs, U.S. indices, NYSE/Nasdaq-listed securities, or does not specify a market.

Characteristics:

- High liquidity for large caps and ETFs.
- Long historical datasets.
- Splits/dividends are common; adjusted prices are preferred for daily/weekly/monthly analysis.
- Trend, momentum, and volume-confirmed breakouts receive the highest default prior weights.
- Short-selling, options, earnings gaps, and sector rotation can materially affect interpretation.

Default signal weights are defined in references/statistical-weighting.md.

## Branching Rule

When another market is requested, create or use a branch profile that modifies only the assumptions that differ from U.S. equities:

```yaml
market: crypto_spot
base_profile: us_equity
overrides:
  session: 24_7
  volume_reliability: exchange_dependent
  timeframe_weights:
    short: { hourly: 0.55, daily: 0.30, weekly: 0.12, monthly: 0.03 }
  signal_weights:
    volatility_regime: 0.11
    volume_confirmation: 0.10
  cautions:
    - fragmented liquidity
    - exchange-specific volume
    - weekend regime changes
```

## Candidate Branch Adjustments

- A-shares: account for price limits, T+1 trading, retail participation, policy/news sensitivity, suspension risk, ETF support/redemption, margin financing, northbound flows when available, and different turnover behavior. For broad-index or sector-index ETF questions, use references/a-share-macro-trading-model.md to classify whether the market is in policy-floor repair, range-stabilized liquidity extraction, main-line acceleration, crowded distribution, broad breakdown, or post-washout accumulation. Do not treat index stability as healthy breadth unless median-stock returns, ETF shares, turnover concentration, and leader behavior confirm it.
- Hong Kong equities: account for China macro/policy exposure, lower liquidity in small/mid caps, different trading holidays, and FX linkage.
- Futures: account for contract rolls, margin, leverage, tick size, first-notice day, last-trade day, delivery windows, expiry, contango/backwardation, and session structure. Use references/special-date-event-risk.md around roll/delivery dates.
- Options-heavy equity/index ETFs: account for weekly/monthly options expiration, quarterly triple/quad witching, gamma pinning, vol crush, and post-expiry positioning reset. Use references/special-date-event-risk.md when entry timing or false-breakout risk matters.
- Forex: account for 24/5 trading, macro calendars, carry, central-bank risk, fixing windows, holiday liquidity, and weaker centralized volume data.
- Crypto: account for 24/7 trading, fragmented exchanges, funding rates, liquidations, and exchange-specific volume quality.

Do not silently reuse U.S. equity weights for another market without noting that the market branch is provisional.
