# A-Share Macro ETF Trading Model

Use this reference for A-share broad-index ETFs, sector-index ETFs, policy-driven index support, "index range-bound while retail accounts bleed", national-team or operator-capital inference, ETF share contraction, turnover concentration, and questions about when ordinary investors can hold ETFs with lower risk and when they should exit.

For daily peer-aggregated broad-ETF monitoring and support-withdrawal inference, also read `references/a-share-broad-etf-monitoring.md`. For one sector ETF's share trend, crowding, and redemption feedback, also read `references/a-share-sector-etf-crowding.md`.

This model is an evidence framework, not proof of a coordinated operator. Infer "operator capital" only from observable price, breadth, ETF share, turnover, fund-flow, policy, and leader-stock behavior.

## Core Premise

In a weak macro and liquidity-constrained A-share regime, the market can stay index-stable while most stocks trend down. Broad indices may be supported to stabilize expectations, while the tradable profit pool concentrates into one or two main lines. Retail losses often arise from chasing crowded leaders late, averaging down weak small caps, or holding broad exposure when ETF support is being withdrawn.

Separate three questions:

- Is the broad index still being stabilized?
- Is the main line still attracting incremental risk capital, or only recycling existing liquidity?
- Can an ordinary investor hold the ETF with tolerable drawdown risk, or is the position becoming exit liquidity?

## Required Data

Prefer structured data from exchange, fund, or market APIs:

- Broad-index OHLCV: CSI 300, CSI A500, SSE 50, STAR 50, ChiNext, all-share or equal-weight proxies.
- Representative ETF shares and NAV/market value: current share field plus quarterly fund-scale table; do not infer historical shares from back-adjusted turnover if the data vendor backfills turnover using current shares.
- Market breadth: median 20/60-day return, percentage below MA20/50/120/200, percentage with negative 60-day returns, new highs minus new lows.
- Concentration: top 20/50/100 stocks by turnover share, top industries by turnover, theme turnover share versus market-cap share.
- Leader behavior: returns, turnover, long upper shadows, high-volume down days, failed breakout, and main-fund flow for top turnover leaders.
- Policy/liquidity support: capital-market policy, PBOC liquidity tools, insurance/pension/public-fund guidance, margin financing, ETF subscription/redemption, buyback/reloan tools when available.
- Macro stress: credit impulse, property/fiscal stress, RMB and USD liquidity, risk-free rate, bank/wealth-product stress signals.

If data is missing, lower confidence and label the conclusion as a structural hypothesis.

## Market State Machine

Classify the A-share market into one primary state.

| State | Observable Pattern | ETF Read |
| --- | --- | --- |
| Policy floor repair | Broad indices reclaim MA50/MA120; breadth stops worsening; ETF shares stabilize or grow; policy/liquidity support is visible. | Broad ETFs can be accumulated in batches if hard stops are defined. |
| Range-stabilized extraction | Broad index holds range; ETF shares fall or stagnate; median stock return is negative; turnover concentrates in a few themes. | Broad ETF is tactical, not safe buy-and-hold; sector ETF only if main-line score is strong. |
| Main-line acceleration | Sector ETF above MA20/MA50 with rising relative strength; leader basket expands; pullbacks shrink volume; breadth inside the theme improves. | Hold sector ETF with trailing exits; avoid weak non-main-line exposure. |
| Crowded distribution | Leaders make new highs but breadth narrows; top turnover share rises; ETF/fund inflow becomes hot; high-volume down days appear. | Reduce sector ETF; do not add after failed breakouts. |
| Broad breakdown | Broad index loses MA120/MA200 or Vegas and fails recovery; breadth collapses; ETF support and policy bid fail; leaders also break. | Exit or keep only defensive minimal exposure. |
| Accumulation after washout | Indices stop making lows; median stock returns improve before headlines; leaders stop falling on bad news; ETF shares stabilize. | Rebuild in batches after confirmation, not during falling-knife phase. |

## Broad ETF Holdability Score

Compute a 0-100 score for broad-index ETFs such as CSI 300, CSI A500, SSE 50, STAR 50, and broad-market ETFs.

| Factor | Weight | Bullish Evidence | Bearish Evidence |
| --- | ---: | --- | --- |
| Index trend structure | 20 | Close above rising MA50/MA120/MA200; pullbacks recover quickly. | Close below MA120/MA200 with failed recovery. |
| Breadth and median stock health | 20 | Median 20/60-day return improves; share above MA50 rises; new lows contract. | Index flat/up while median 60-day return below -10%; more than 60% of stocks negative over 60 days. |
| ETF share and flow consistency | 15 | Representative ETF shares stabilize or rise; redemptions slow; ETF premium/discount normal. | Large share contraction while index is held up; redemptions accelerate. |
| Turnover concentration risk | 15 | Top turnover share falls; gains broaden beyond one theme; turnover/mcap ratio normalizes. | Top 100 turnover share above about 35%, or one theme turnover share materially exceeds its market-cap share. |
| Policy and liquidity support | 15 | Capital-market support tools are active and price confirms them. | Policy language without price/breadth confirmation, or liquidity support is used mainly to offset stress. |
| Leader-stock stability | 10 | Top leaders pull back on shrinking volume and hold MA20/MA50. | Top leaders show high-volume down days, failed breakouts, or synchronized main-fund outflows. |
| Macro stress overlay | 5 | RMB, credit, bank/liquidity, and property stress are not accelerating. | Macro stress second-derivative worsens and equity support becomes defensive. |

Interpretation:

- 75-100: lower-risk broad ETF holding window. Use batch entries and MA50/MA120 exits.
- 60-74: conditional trend holding. Hold smaller size; do not add after concentration spikes.
- 45-59: tactical only. Prefer cash plus short trades; require quick confirmation.
- Below 45: avoid or exit broad ETF exposure unless using a deliberate hedge or very small policy-option position.

Hard downgrade broad ETFs when at least two occur together:

- The index closes below MA120 or MA200 and fails to recover within 2-3 sessions.
- Broad ETF shares keep falling while the index is flat/up.
- Median 60-day stock return is below -10% and more than 60% of stocks are negative over 60 days.
- Top 100 turnover share exceeds about 35% while the main-line leader basket prints high-volume down days.
- Policy support appears, but breadth and price do not repair within one to two weeks.

## Sector ETF Main-Line Score

Use this score for semiconductor, AI hardware, CPO, power grid, robotics, brokerages, dividend, biotech, or other A-share sector ETFs.

| Factor | Weight | What To Check |
| --- | ---: | --- |
| Sector price trend | 20 | Sector ETF above MA20/MA50; MA20 rising; pullbacks hold MA20 in acceleration. |
| Relative strength | 20 | Sector outperforms CSI 300/A500 and peer sectors over 10/20/60 days. |
| Internal breadth | 15 | More constituents above MA20/MA50; equal-weight sector keeps up with cap-weighted sector. |
| Leader basket health | 15 | Top leaders rotate without synchronized breakdown; no repeated failed breakouts. |
| Flow and turnover quality | 10 | Volume expands on breakout and contracts on pullback; ETF shares not in euphoric blow-off or sharp redemption. |
| Fundamental validation | 10 | Orders, pricing, earnings revisions, policy procurement, or utilization validate the story. |
| Bubble-risk penalty | 10 | Deduct for extreme valuation, parabolic extension, hot fund inflow, margin heat, insider selling, and media euphoria. |

Interpretation:

- 75-100: main-line ETF can be held as trend exposure with mechanical exits.
- 60-74: participate in batches; avoid chasing after vertical moves.
- 45-59: only short tactical trades after pullbacks stabilize.
- Below 45: no low-risk holding window.

Hard exit or reduce sector ETFs when:

- The ETF loses MA20 and cannot recover within about three sessions after a parabolic run.
- The ETF loses MA50 or a 55-day low with expanding downside volume.
- Leaders fall together on high turnover while laggards do not rotate up.
- The sector index rises but equal-weight or median constituent return deteriorates.
- A widely publicized catalyst stops lifting price, or good news produces distribution candles.

## Operator-Capital Flow Patterns

When the user asks how main funds may behave, classify the observed flows:

1. Broad support
   - Broad ETF shares or large-cap baskets rise.
   - Index pullbacks are bought near MA50/MA120.
   - Breadth improves or at least stops deteriorating.
   - Retail strategy: broad ETF batch exposure is acceptable if the holdability score is above 60.

2. Range support with liquidity extraction
   - Index remains range-bound while broad ETF shares decline or stagnate.
   - Median stock returns are negative.
   - Top turnover share and main-line turnover/mcap ratio rise.
   - Retail strategy: avoid pretending this is a healthy bull market; hold only leading ETFs with strict exits.

3. Crowded main-line distribution
   - Leaders remain high turnover but stop making clean highs.
   - Long upper shadows, high-volume down days, and failed breakouts increase.
   - Main-fund net flow turns negative in several leaders on the same day.
   - Retail strategy: reduce exposure before the formal index break.

4. Defensive de-risking
   - Broad index loses MA120/MA200.
   - Policy support does not repair price or breadth.
   - Former leaders fall with the index.
   - Retail strategy: cash first; wait for accumulation evidence.

## Ordinary-Investor Playbook

Use ETF exposure to follow confirmed capital, not to predict policy intentions.

- Prefer broad and sector ETFs over single stocks when the goal is to follow operator capital.
- Enter in batches only after price, breadth, and flow agree; do not add because of slogans or headlines alone.
- Use hard exits before narratives: MA20/MA50 for sector ETFs, MA50/MA120/MA200 for broad ETFs.
- Treat broad-index stability with weak breadth as a warning, not comfort.
- Do not average down weak sectors when capital is concentrating elsewhere.
- Cap theme exposure when turnover concentration is extreme; high liquidity can be distribution liquidity.
- Keep cash as a position when the model state is range-stabilized extraction or crowded distribution.

## Output Add-On

For A-share ETF macro-trading questions, add this compact dashboard:

```text
A-share regime: policy-floor repair / range-stabilized extraction / main-line acceleration / crowded distribution / broad breakdown / post-washout accumulation
Broad ETF holdability score: 0-100
Sector ETF main-line score: 0-100
Crowding/distribution risk: low / medium / high
Operator-capital pattern: broad support / range support with liquidity extraction / main-line acceleration / high-level distribution / defensive de-risking
Retail action: batch hold / small follow / short tactical only / reduce / wait in cash
Hard exit signals: ...
Re-entry signals: ...
```

State clearly whether the conclusion is supported by data or only inferred from partial evidence.
