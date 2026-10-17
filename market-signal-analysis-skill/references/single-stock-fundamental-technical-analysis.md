# Single-Stock Fundamental and Technical Analysis

Use this reference when the user asks whether an individual stock should be bought, held, reduced, or cut; whether a company announcement is real catalyst or noise; how fundamentals and technicals interact; or where short-term and long-term price zones may be.

Do not treat this as personalized financial advice. Produce a scenario-based risk-control view. Be especially strict when the user is an ordinary retail investor, the position is already losing money, or the stock is driven by concept narratives.

## Core Principle

Separate four questions:

1. Is the company real and improving?
2. Is the improvement large enough to matter for earnings, cash flow, or valuation?
3. Is the improvement already priced into the stock?
4. Does the price structure confirm or reject the story?

A company can be real but overpriced. A company can have good news but no material profit impact. A stock can bounce while the medium trend is still broken. Never merge these into one vague bullish or bearish label.

## Required Data

Prefer primary or structured sources:

- Latest quote, market cap, free-float market cap, turnover, and trading date.
- Adjusted daily OHLCV for at least 252 bars; prefer 676+ bars for full Vegas/long-cycle context.
- Latest annual report, quarterly report, and TTM reconstruction.
- Revenue, parent net profit, deducted net profit, gross margin, net margin, operating cash flow / revenue, ROE/ROIC, debt ratio, current ratio, quick ratio, inventory and receivables turnover.
- Segment revenue, segment profit, customer exposure, product mix, and whether the promoted business is already material.
- Recent announcements: performance forecast, contracts/orders, investment, M&A, pledge, reduction, buyback sale, convertible/exchangeable bonds, guarantees, litigation, inquiry letters, lockup expiry.
- Sector and index context: sector trend, breadth, valuation regime, and whether the stock is leader, laggard, or concept follower.

If key data is missing, state the gap and reduce confidence before giving price expectations.

## News and Announcement Noise Filter

Classify every piece of information before using it:

| Level | Signal Type | Practical Treatment |
| --- | --- | --- |
| 0 | Rumors, forums, short videos, target prices, unnamed channels, repeated concept labels | Ignore for valuation; use only as sentiment/noise context. |
| 1 | Strategic cooperation, layout, empowerment, ecosystem, intent, framework agreement, non-binding MOU | Watch only; no thesis upgrade unless later converted into orders/revenue. |
| 2 | Named customer/order/contract with amount, delivery period, product, obligations, and cancellation terms | Potential catalyst; estimate revenue and margin contribution. |
| 3 | Confirmed financial impact in revenue, gross margin, deducted profit, operating cash flow, backlog, or guidance | Core signal; compare with valuation and consensus expectations. |
| 4 | Two or more reporting periods of improved deducted profit and cash flow, plus price/volume confirmation | Durable thesis upgrade candidate. |

Use this hard rule: no amount, no delivery timeline, no accounting path, no profit/cash-flow impact, and no price confirmation means the information is not a core bullish signal.

For A-shares, assume announcements can be legally true but economically weak. Phrases such as "does not materially affect current earnings", "uncertainty remains", "subject to future negotiation", or "no undisclosed material matters" usually cap the immediate fundamental value of the news.

## Fundamental Scorecard

Score fundamentals as strong, acceptable, weak, or deteriorating. Do not average everything mechanically; identify the bottleneck that market pricing will care about most.

### Profit Quality

Prefer:

- Revenue growth with deducted profit growth.
- Gross margin stable or improving for business reasons, not one-off accounting.
- Operating cash flow positive and not persistently below net profit.
- Non-recurring gains small relative to profit.

Warn when:

- Parent net profit is positive but deducted profit is weak or negative.
- Operating cash flow / revenue is negative in a business that should collect cash.
- Profit relies on asset disposal, subsidies, fair-value gains, debt restructuring, or inventory capitalization.

### Growth Durability

Ask:

- Is growth from volume, price, product mix, cost decline, or accounting base effect?
- Is the promoted new business already more than a small percentage of revenue or profit?
- Does backlog or customer certification support future quarters?
- Are customers powerful enough to compress margin?

For concept-driven stocks, require the new business to show in segment revenue, order backlog, gross margin, or capex utilization before treating it as a durable growth driver.

### Balance Sheet and Funding Pressure

Check:

- Debt ratio, current ratio, quick ratio, interest-bearing debt, pledged shares, guarantees, receivables, inventory, and capex commitments.
- Whether controlling shareholders face pledge, exchangeable bond, margin, or reduction pressure.
- Whether buyback shares are being sold, lockups expire, or bankruptcy/restructuring shares may enter the market.

Supply pressure can overwhelm "good company" fundamentals over weeks or months.

### Governance and Capital-Market Signals

Bullish signals need caution if they coexist with:

- Large shareholder reduction, pledge extension, exchangeable debt pressure, frequent guarantees, related-party transactions, inquiry letters, or repeated concept announcements without financial delivery.
- "Good news followed by price decline" with expanding volume. Treat this as potential exit liquidity, not as automatic opportunity.

## Valuation and Long-Term Price Zones

Estimate long-term zones from fundamentals, not chart lines alone:

1. Reconstruct TTM earnings and cash flow from annual plus latest quarterly data.
2. Choose the valuation anchor that matches the business:
   - Stable profit manufacturing: PE, PB-ROE, EV/EBITDA.
   - Cyclical resources: normalized earnings, cycle margin, PB.
   - High-growth software/platform: revenue growth, FCF path, retention, unit economics.
   - Turnaround/loss-making: cash runway, liquidation value, dilution risk, probability-weighted recovery.
3. Build base, bull, and bear cases:
   - Bear case: growth slows, margin normalizes down, valuation multiple compresses.
   - Base case: current verified trend continues but no new narrative premium.
   - Bull case: hard orders and financial statements confirm narrative growth.
4. Translate into price zones using shares outstanding and reasonable multiples. Never present a single target as guaranteed.

When the stock is a concept follower rather than a fundamental leader, cap the long-term bull multiple unless the new business has already entered financial statements.

## Technical Integration

Use references/trend-stage-analysis.md for detailed trend-stage rules. For single stocks, combine it with event and valuation evidence:

- Short-term trend: 5 to 20 trading days. Use MA5/10/20, ATR, Donchian 20-day high/low, gaps, limit-up/limit-down behavior, volume, and event date.
- Medium trend: 2 to 12 weeks. Use MA20/50, Donchian 55-day high/low, 2ATR/3ATR Chandelier, MACD zero-line regime, relative strength versus sector.
- Long trend: 3 to 24 months. Use MA120/200, daily Vegas EMA144/169, weekly structure, 120/250-day range, valuation and earnings trend.
- Granville rules: classify whether price is breaking above, pulling back to, reclaiming, failing at, or overextending away from the relevant MA20/50/120/200. Use this to distinguish "trend repair", "healthy pullback", "failed rebound", "oversold bounce", and "distribution after overextension".
- Bottom reversal rules: in a downtrend, require daily bullish engulfing with the real body effectively exceeding the prior day's real-body high, material volume expansion versus the prior day, and proximity to a key MA/support or prior high-turnover support shelf before calling a high-confidence reversal. With only two of the three checks, downgrade to a reversal watch whose confidence depends on volume strength, body size, close location, and follow-through. With only one check, do not call a reversal.
- Key-MA reclaim rules: treat reversal as more durable when price reclaims a horizon-relevant MA, retests it without an effective break, and then rises with sustained healthy volume. Use MA20/30 for tactical, MA50/60 for swing, and MA120/200 or Vegas EMA144/169 for long trend repair.

For short-term price expectations, provide zones:

- Rebound resistance: nearest MA20/MA50/Vegas, high-volume breakdown area, gap, or failed breakout level.
- Weak support: current low, 20-day low, or volume shelf that may only produce a bounce.
- Stronger support: 55-day/120-day low, prior base, long-cycle MA/Vegas, or valuation-backed zone.
- Invalidation: level and behavior that proves the current thesis wrong, usually a close below support with failure to recover in 2-3 sessions.

For long-term price expectations, reconcile technical and valuation zones:

- If valuation support is far below technical support, warn that chart support may fail in a market-wide de-rating.
- If technical breakout occurs but valuation is already stretched and fundamentals are unconfirmed, call it momentum/speculation rather than durable value.
- If fundamentals improve and price reclaims MA50/MA120/Vegas with volume, upgrade from "bounce" to "trend repair".

## Decision Tree for Losing Positions

Start from the original buy thesis:

- If the buy thesis was short-term momentum or concept speculation and price loses MA20/MA50 or failed-breakout level, treat it as a trade failure. Reduce or cut on rebound rather than converting it into a long-term position.
- If the buy thesis was fundamental improvement, hold only if deducted profit, cash flow, margin, balance sheet, and sector demand still support the thesis. If financial evidence breaks, cut even if price looks "cheap".
- If the position is heavy or emotionally damaging, reduce first to survivable size, then analyze. Risk capacity is part of the signal for ordinary investors.
- Never average down only because the price fell. Add only after new hard evidence appears and price confirms with a reclaim/hold structure.

## Output Template

For individual stocks, include:

1. Data and confidence: symbol, market, latest date, data range, adjustment status, missing data.
2. One-sentence verdict: distinguish company quality, stock valuation, and trading trend.
3. Noise versus hard signals:
   - Discarded noise.
   - Watch-list signals.
   - Core signals that affect earnings/cash flow/valuation.
4. Fundamental read:
   - Profit quality.
   - Growth durability.
   - Balance sheet/funding pressure.
   - Governance/share-supply pressure.
   - Valuation versus growth.
5. Technical read:
   - Trend stage.
   - Short-term, medium-term, and long-term structure.
   - Granville moving-average state for the most relevant horizon.
   - Bottom bullish-engulfing or key-MA reclaim/retest signal state, if present.
   - Key support/resistance/invalidation levels.
6. Price zones:
   - Short-term rebound zone.
   - Short-term risk zone.
   - Medium trend repair zone.
   - Long-term valuation-backed zone, if data supports it.
7. Action framework:
   - High-cost/heavy position.
   - Light position.
   - New buyer.
   - Upgrade conditions and downgrade/stop conditions.

Use direct but bounded language. Prefer "reduce on rebound if X cannot be reclaimed" over vague "wait and see"; prefer "the story has not entered statements yet" over "good prospects".
