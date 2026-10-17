# Statistical Weighting

Use this reference when converting evidence into quantitative or probability-style conclusions. A score is not automatically a calibrated probability.

## Horizon Mapping

Use the user's language to select a horizon:

| User wording | Target horizon | Primary windows | Timeframe weights |
| --- | --- | --- | --- |
| short, short-term, swing, intraday, this week | intraday to 10 trading days | hourly 60-240 bars, daily 60-252 bars | hourly 0.45, daily 0.35, weekly 0.15, monthly 0.05 |
| mid, medium, intermediate, next weeks | 2 to 12 weeks | daily 126-504 bars, weekly 52-156 bars | hourly 0.10, daily 0.45, weekly 0.35, monthly 0.10 |
| long, long-term, position, investment | 3 to 24 months | weekly 104-260 bars, monthly 60-180 bars | hourly 0.00, daily 0.20, weekly 0.45, monthly 0.35 |

If the requested horizon conflicts with available data, adapt the closest valid horizon and disclose the substitution.

## U.S. Equity Default Signal Family Weights

Use these priors before symbol-specific calibration:

| Signal family | Weight | Reason |
| --- | ---: | --- |
| trend_breakout_ma | 0.24 | Strongest long-sample U.S. evidence among classic technical rules. |
| momentum_relative_strength | 0.18 | Strong intermediate-horizon U.S. equity evidence. |
| volume_confirmation | 0.14 | Improves momentum/breakout interpretation and reversal risk. |
| macd_combo | 0.11 | Useful as trend/momentum confirmation; standalone evidence is weaker. |
| rsi_kdj_oscillator | 0.10 | Useful for exhaustion/timing; penalize isolated signals. |
| divergence | 0.11 | Useful reversal warning when confirmed by price structure and volume. |
| volatility_regime | 0.07 | Controls risk, squeeze/breakout, and probability confidence. |
| multi_timeframe_agreement | 0.05 | Boosts confidence when higher and lower timeframes align. |

Weights must sum to 1.0. Market branches may override these defaults.

## Signal Scoring

For each timeframe and signal family:

1. Assign direction: bullish = +1, bearish = -1, neutral = 0.
2. Assign strength from 0.0 to 1.0 based on recency, magnitude, and confirmation.
3. Multiply by family weight and timeframe weight.
4. Group correlated signals before scoring. Example: MA20 slope, price above MA20, and a nearby MACD improvement may all express one trend factor. Give the group a capped weight unless each signal adds demonstrably independent information.
5. Penalize stale signals:
   - Triggered in the latest 1-3 bars: full credit.
   - Triggered 4-10 bars ago: 50%-80% credit.
   - Older than 10 bars: context only unless still structurally active.

Compute:

```text
net_score = sum(weighted_bullish_components) - sum(weighted_bearish_components)
raw_buy_probability = sigmoid(2.6 * net_score)
raw_sell_probability = sigmoid(-2.6 * net_score)
hold_probability = max(0, 1 - abs(raw_buy_probability - raw_sell_probability) * confidence_scale)
```

Normalize buy/sell/hold to sum to 100%.

The bundled OHLCV helper uses the strongest signal per direction within each
family, then scales combined bullish and bearish contributions to that family's
weight cap. Repeating a correlated signal cannot increase its contribution.
`family_score_components` exposes this calculation. Inputs must provide
consistently adjusted OHLC columns; an adjusted close alone is rejected.

Label this output `model-implied probability`. Do not call it an empirical hit probability unless it has been calibrated on a defined historical sample. If expected move does not clear costs, volatility, or the user's decision threshold, increase the neutral/hold weight rather than forcing a directional call.

## Base Rates and Evidence Dependence

Start from a market-, asset-, horizon-, and regime-conditional prior. Update it only with evidence that has a plausible mechanism and is not already represented by another feature group.

- Use hierarchical groups such as trend, momentum, breadth, liquidity, fundamentals/revisions, valuation, positioning, actor/policy, and event risk.
- Cap each group before combining sub-signals. Do not let ten versions of trend overwhelm one independent liquidity or earnings warning.
- Use likelihood ratios or score increments only when their estimation sample matches the target regime reasonably well.
- Shrink unstable estimates toward the relevant base rate. Increase shrinkage after parameter search, regime change, taxonomy change, or source-methodology change.
- When groups conflict, widen the scenario distribution and lower confidence. Do not hide conflict in a single average score.

## Bayesian Multi-State Update

For mutually exclusive states such as `up`, `range`, and `down`, start with a horizon- and regime-conditional prior and update in log space:

```text
log_posterior_s = log(prior_s) + sum_g reliability_g * log(LR_g,s)
posterior_s = exp(log_posterior_s) / sum_k exp(log_posterior_k)
```

Each `g` must be an independent evidence family, not an indicator. Examples are trend, breadth, ETF flow, fundamentals/revisions, valuation, policy/liquidity, positioning, and event risk. Combine correlated observations inside a family before assigning one likelihood ratio.

Rules:

- Estimate likelihood ratios from regime-matched historical events when possible.
- If using heuristic likelihood mapping, cap each family LR to roughly 0.5-2.0, label the result `model-implied scenario weights`, and run alternative-prior sensitivity.
- Use reliability from 0 to 1 for freshness, source quality, coverage, and sample stability.
- Do not let posterior probabilities fall below 3%-5% when event or policy risk is material.
- If a neutral prior and the selected regime prior produce different leading states, report low confidence and the posterior range.
- Do not use the posterior as a price target. Pair each state with a path, horizon, conditional return range, and invalidation evidence.

## Historical Hit Analysis

When sufficient history exists, replace or adjust priors with symbol-specific statistics:

- Define a signal event without lookahead.
- Measure forward returns over the selected horizon.
- Track hit rate, mean return, median return, payoff ratio, Sharpe-like return/volatility, maximum adverse excursion, maximum favorable excursion, and trade count.
- Use walk-forward or train/test splits when possible.
- Apply shrinkage toward the U.S. equity default prior when samples are small.

Minimum sample guidance:

| Sample count | Use |
| ---: | --- |
| fewer than 20 | Do not use as probability evidence; list as anecdotal. |
| 20-49 | Low confidence; shrink at least 70% toward default prior. |
| 50-99 | Medium confidence; shrink 40%-60% toward default prior. |
| 100+ | Higher confidence if out-of-sample performance is stable. |

Use Wilson confidence intervals for hit rate when possible. Penalize rules whose confidence interval includes 50% and whose average return does not exceed estimated costs.

## Confidence

Report confidence as high, medium, low, or insufficient:

- High: enough bars, enough historical signal events, multiple independent signal families align, no major data-quality warnings.
- Medium: adequate bars but limited event history or partial conflict across timeframes.
- Low: small sample, strong conflict, high volatility regime, or reliance on oscillators/divergence alone.
- Insufficient: missing OHLCV, too few bars, unknown adjustment status, or no reliable timeframe.

## Research Basis for Default Priors

Use the ranking below only as a U.S.-equity prior. Academic results vary by sample, costs, liquidity, and data-snooping exposure; recalibrate on the actual symbol, horizon, and regime.

1. **Trend following and range breakouts** receive the highest classic-technical prior. Brock, Lakonishok, and LeBaron (1992) found information in moving-average and trading-range rules on the Dow; Han, Yang, and Zhou found moving-average timing strongest in higher-volatility portfolios in their sample.
2. **Intermediate-horizon momentum and relative strength** receive a high prior. Jegadeesh and Titman (1993) documented winner-minus-loser momentum over 3-12 month horizons.
3. **Volume-confirmed momentum/breakout** receives supporting weight. Lee and Swaminathan found volume helped explain momentum persistence and reversal risk.
4. **Patterns and divergence** are supporting evidence. Lo, Mamaysky, and Wang found some systematic chart patterns contained incremental information, but this does not justify pattern-only decisions.
5. **MACD, RSI, KDJ, and similar oscillators** are timing and exhaustion tools. Standalone results are sample-dependent and generally weaker than trend/momentum evidence.

Apply the Sullivan-Timmermann-White data-snooping caution, out-of-sample checks, costs, slippage, turnover, shorting constraints, and tax horizon. Marshall, Sun, and Young found many popular rules were rarely profitable across broad U.S. stock samples, so do not claim universal applicability.

Sources:

- Brock, Lakonishok, LeBaron: https://ideas.repec.org/a/bla/jfinan/v47y1992i5p1731-64.html
- Lo, Mamaysky, Wang: https://ideas.repec.org/p/nbr/nberwo/7613.html
- Han, Yang, Zhou: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1656460
- Jegadeesh, Titman: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html
- Lee, Swaminathan: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=92589
- Sullivan, Timmermann, White: https://www.fmg.ac.uk/publications/discussion-papers/data-snooping-technical-trading-rule-performance-and-bootstrap
- Marshall, Sun, Young: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=929954
- Chio: https://arxiv.org/abs/2206.12282
