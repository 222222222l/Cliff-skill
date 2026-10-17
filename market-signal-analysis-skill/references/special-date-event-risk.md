# Special Date and Event-Calendar Risk

Use this reference when a market view could be distorted by futures delivery, options expiration, macro releases, central-bank decisions, Treasury issuance, index rebalancing, holiday liquidity, or month/quarter-end flows.

Core principle: special dates are usually a signal-quality and liquidity overlay, not a directional edge. They can create pinning, forced hedging, false breakouts, gap risk, volatility crush, and abrupt liquidity withdrawal. Do not turn an event date into a buy/sell call unless positioning, price/volume behavior, implied volatility, and post-event confirmation support it.

## Event Classes

| Class | Examples | Main mechanism | Usual warning window |
| --- | --- | --- | --- |
| Options expiration | U.S. monthly OpEx, weekly options, index/ETF options, SPX/NDX/QQQ/SPY options, A-share ETF options | Dealer gamma hedging, strike pinning, vol crush, post-expiry positioning reset | T-3 to T+2 trading days |
| Futures expiry and delivery | Equity-index futures, Treasury futures, commodity futures first-notice/last-trade/delivery, contract roll | Roll pressure, basis changes, margin/liquidity demand, physical-delivery squeeze | T-5 to T+3; longer for commodities |
| Quarterly witching | U.S. third Friday of Mar/Jun/Sep/Dec; index futures/options and stock options expire together | High notional settlement, gamma reset, index/ETF rebalance overlap | T-5 to T+2 |
| Fed and macro releases | FOMC rate decision, SEP/dot plot, Powell press conference, FOMC minutes, CPI, PCE, NFP, ECI, JOLTS, ISM, retail sales | Rate path repricing, real-yield shock, USD/liquidity reaction, factor rotation | T-2 to T+1 |
| Treasury and liquidity dates | QRA, refunding details, large coupon auctions, settlement dates, TGA rebuild/drawdown, tax dates, month-end/quarter-end | Reserve drain/addition, term-premium shock, repo/SOFR pressure, duration-supply shock | T-3 to T+3 |
| Index and ETF rebalancing | MSCI/FTSE/S&P/Russell rebalance, sector-index rebalance, ETF creation/redemption stress | Mechanical flows, close auction imbalance, temporary breadth distortion | T-5 to T+2 |
| Holiday and session effects | Pre-holiday thin liquidity, post-holiday gap, cross-market closures, northbound/southbound closure | Lower depth, wider spreads, stale cross-market hedges | T-2 to T+1 |

## Market-Specific Checks

- U.S. equities and ETFs: check weekly/monthly options expiry, quarterly triple/quad witching, FOMC, CPI/PCE/NFP/ECI/JOLTS/ISM/retail sales, QRA, Treasury auctions and settlement, month/quarter-end, Russell/MSCI/S&P rebalance, earnings clusters, and buyback blackout windows.
- U.S. bonds, gold, USD, and high-duration growth: raise weight on FOMC, CPI/PCE, NFP, ECI, QRA, coupon auctions, SOFR-IORB, TGA/reserve changes, and Treasury settlement dates.
- Futures and commodities: check first-notice day, last-trade day, delivery window, roll schedule, exchange margin changes, inventory reports, and whether price action is front-month-specific or spread-wide.
- A-shares and Hong Kong: check index futures/options delivery, ETF options expiry, MSCI/FTSE index rebalances, LPR/MLF/RRR windows, major policy meetings, exchange holidays, northbound/southbound closure, quarterly earnings and lock-up expiry.
- Crypto: check futures/options expiry on major venues, funding-rate reset, large unlocks, ETF creation/redemption windows, U.S. macro release times, and weekend liquidity gaps.

## Scoring

Compute a `special_date_risk_score` from 0 to 100 when data permits:

```text
proximity_score = max(0, 1 - abs(days_to_event) / (window_days + 1))
importance_score = high: 1.00, medium: 0.65, low: 0.35
positioning_score = 0 to 1 from gamma exposure, put/call, open interest, crowding, leverage, or fund-flow heat
liquidity_score = 0 to 1 from spread/depth, SOFR/repo stress, volume thinning, holiday effects, or exchange settlement pressure
technical_fragility = 0 to 1 from overextension, failed breakout risk, narrow breadth, or crowded leadership

special_date_risk_score =
100 * (0.30*proximity + 0.25*importance + 0.20*positioning + 0.15*liquidity + 0.10*technical_fragility)
```

If positioning, liquidity, or fragility data are unavailable, use proximity and importance only, reduce confidence, and state the missing evidence.

Interpretation:

- 0-24: low calendar risk; mention only if the user asks about timing.
- 25-49: moderate warning; avoid overreading intraday or one-day breakouts.
- 50-74: high warning; require post-event confirmation before upgrading trend probability.
- 75-100: severe warning; gap, vol crush, liquidation, or forced-flow risk can dominate normal technical signals.

## How To Adjust Market Analysis

- Do not add a directional bullish or bearish signal from the calendar alone.
- Lower confidence or widen the expected range when a high-impact event is within the warning window.
- Treat breakouts into an event as provisional unless volume, breadth, and relative strength remain intact after T+1 or T+2.
- Treat breakdowns into an event as provisional if they occur on thin liquidity and reverse quickly after settlement.
- Watch for post-event confirmation: close above/below the event-day range, volume follow-through, breadth confirmation, volatility reaction, and whether the original leadership still leads.
- For options expiry, distinguish gamma pinning before expiry from genuine trend continuation after the open-interest reset.
- For futures delivery, distinguish front-month roll noise from broad curve movement.
- For Fed/macro releases, separate first reaction from second-day confirmation; the second day often reveals whether the move is positioning cleanup or durable repricing.

## Output Warning Template

When relevant, add a compact special-date warning:

```text
特殊日期预警：高
事件：FOMC 利率决议 / CPI / 月度 OpEx / 季度三巫日 / 期货交割
日期与距离：2026-07-29，T-2
影响资产：QQQ、纳指期货、美元、黄金、长久期资产
主要机制：利率路径重定价 + 期权 gamma 仓位调整，可能放大假突破和盘中反转
对结论的影响：不单独改变方向判断，但将短线置信度下调一级；突破需等 T+1/T+2 收盘确认
缺失数据：期权最大痛点、gamma exposure、期货持仓、隐含波动率期限结构
```

For ordinary investors, translate the warning into execution discipline:

- avoid all-in entry immediately before high-impact events;
- use smaller tranches and wider invalidation levels;
- wait for post-event close confirmation when the existing trend is already extended;
- do not average down before delivery/expiry/macro release unless the thesis survives the event and liquidity has normalized.
