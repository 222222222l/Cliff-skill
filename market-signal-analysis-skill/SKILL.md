---
name: market-signal-analysis
description: Analyze stocks, ETFs, sectors, indices, and liquid markets with OHLCV, fundamentals, breadth, liquidity, ETF shares/flows, valuation, policy, actor incentives, cycles/FFT, event risk, and market-stage-specific behavior selection. Use for trend-stage or trend-end analysis, Granville/Vegas signals, probability-weighted buy/sell/hold views, high-return-per-unit-risk behavior recommendations, cost- and exit-adjusted return priors, A-share broad-ETF support/withdrawal, A/H sector-ETF crowding and redemption, Hong Kong ETF Connect and multi-counter flows, sector rotation and high-valuation bubbles, A/H-share ETF regimes, single-stock news and valuation, official-data verification, multi-actor game equilibria, U.S. liquidity and Fed policy, macro stress, special-date risk, or quantitative market-model design.
---

# Market Signal Analysis

## Mission

Produce horizon-specific, causal, probability-aware market decision support. Explain what is observed, what is inferred, what could change the view, and which evidence matters most. Do not turn indicators, narratives, or policy motives into certainty.

## First Principles

1. **Gate on data quality.** Verify symbol, market, timestamp, frequency, range, adjustment status, missing fields, and source freshness. If essential data is missing or stale, narrow the claim or withhold numeric probabilities.
2. **Fix the horizon before selecting signals.** Intraday, short, medium, and long horizons use different data, actors, transmission speeds, and invalidation levels. Use `us_equity` only when the market is genuinely U.S. equity or unspecified; otherwise read `references/market-profiles.md`.
3. **Separate state, flow, and expectation.** Valuation and leverage are states; fund flows and earnings revisions are flows; policy promises and narratives are expectations. A vulnerable state is not a timing signal without a flow or catalyst.
4. **Build the causal chain before using correlation.** Identify driver -> transmission -> market variable -> price/earnings effect -> confirmation. Treat correlation, Fourier coherence, and historical analogies as supporting evidence unless a plausible mechanism exists.
5. **Prefer revealed action to unsupported language.** Compare dated words with costly, repeated, scalable, and hard-to-reverse actions within the actor's control. Preserve principal-agent, desk, subsidiary, mandate, and balance-sheet distinctions.
6. **Use independent evidence and base rates.** Group correlated indicators, cap duplicate weight, condition priors on market and regime, and shrink small samples. Label probabilities as empirical, model-implied, or scenario weights.
7. **Model paths, not isolated targets.** Give a horizon, catalyst or transmission path, range, probability, and invalidation condition. A point target without a path and time window is low-value precision.
8. **Try to disprove the preferred view.** State the strongest opposing explanation and observable evidence that would change the conclusion. Do not average genuine contradictions into a false neutral.
9. **Use the minimum sufficient model.** Load one primary module and normally no more than two overlays. Add another module only when it can materially change the decision, probability, or risk boundary.
10. **Keep analysis non-guaranteed.** Distinguish market analysis from personalized financial advice and account for costs, slippage, liquidity, leverage, and gap risk when relevant.

## Workflow

1. Frame the target, market, asset type, decision horizon, and user's actual question.
2. Run the data gate. Record source, as-of time, adjustment status, sample length, and material omissions.
3. Select the minimum primary module and overlays from the routing table.
4. Build an evidence ledger with four labels: verified observation, estimated value, inference, and scenario assumption.
5. Classify the regime and write the shortest causal transmission chain that explains the relevant price path.
6. When the user asks what behavior fits the state or requests expected return after risk and exit mechanics, read `references/behavior-mode-selection.md`; select only after market-specific state classification.
7. Score only decision-relevant, sufficiently independent evidence. Use `references/statistical-weighting.md` for quantitative probabilities and calibration.
8. Compare the base case with at least one credible opposing case. Run actor deviation, regime-change, behavior-switch, and event-risk checks when applicable.
9. Deliver the conclusion first, then evidence, scenarios, behavior when requested, levels or time windows, and explicit update/invalidation triggers. Use `references/output-format.md` for structured or complex answers.

## Module Router

| Primary question | Read | Add only when material |
| --- | --- | --- |
| General OHLCV signal or probability view | `references/signal-taxonomy.md`, `references/statistical-weighting.md` | `references/market-profiles.md` |
| Market-stage behavior choice, return/risk tradeoff, prior net-return estimate, or exit-aware mode recommendation | `references/behavior-mode-selection.md` | market profile; relevant state module; statistical weighting |
| Trend stage/end, Granville, Vegas, breakout, reversal, stop level | `references/trend-stage-analysis.md` | signal taxonomy, statistical weighting |
| Sector/theme rotation, breadth, leadership, high-valuation bubble | `references/sector-bubble-analysis.md` | trend stage; actor/game; cycles |
| A-share broad or sector ETF, index support, crowding, ordinary-investor holdability | `references/a-share-macro-trading-model.md` | trend stage; sector bubble; actor/game |
| A-share broad-ETF group shares, policy support/withdrawal, ETF migration | `references/a-share-broad-etf-monitoring.md` | A-share macro; actor/game; statistical weighting |
| Single sector ETF share trend, crowding, redemption feedback, flow-price divergence | `references/a-share-sector-etf-crowding.md` | A-share macro; sector bubble; statistical weighting |
| Hong Kong ETF units, multi-counter identity, Southbound ETF Connect, market-maker inventory | `references/hong-kong-etf-flow-monitoring.md` | A-share/H-share macro; statistical weighting; actor/game |
| Individual stock fundamentals, valuation, announcement/news quality, hold/cut decision | `references/single-stock-fundamental-technical-analysis.md` | trend stage; event risk |
| Official macro, regulator, exchange, central-bank, or statistical data | `references/official-data-verification.md` | relevant macro or policy module |
| Policy-maker, institution, dealer, insider, or strategic interaction | `references/actor-optimal-path-analysis.md` | official-data verification; event risk |
| Economic, liquidity, inventory, capex, industry, or market cycles | `references/cycle-overlay-analysis.md` | Fourier; sector bubble |
| FFT/Fourier rhythm, denoising, dominant-cycle stability, frequency correlation | `references/fourier-cycle-analysis.md` | cycle overlay; trend stage |
| U.S. liquidity, Fed, Treasury issuance, rates, USD, gold, Nasdaq | `references/us-macro-liquidity-fed-policy.md` | macro stress derivatives; official data; event risk |
| Early crisis, marginal deterioration, acceleration, contagion | `references/macro-stress-derivative-analysis.md` | U.S. macro or relevant regional framework |
| Expiry, delivery, FOMC/data release, QRA/auction, rebalance, month/quarter-end | `references/special-date-event-risk.md` | relevant primary module |
| Trainable Transformer/TFT market model | `references/deep-learning-extension.md` | `references/research-and-optimization-roadmap.md` for research design |

## Composition Rules

- Treat technicals as timing and path evidence, fundamentals as cash-flow and valuation evidence, liquidity as discount-rate and marginal-demand evidence, and actor analysis as a scenario prior. Do not substitute one family for another.
- For policy or actor questions, compare words versus actions and model direct and second-round strategic responses. Call an equilibrium stable only after a unilateral-deviation test and observable confirmation.
- For bubble regimes, separate "expensive but strengthening" from "expensive and weakening." Valuation can define fragility; breadth, flows, revisions, credit, and failed price structure usually determine timing.
- For cycles and Fourier analysis, use rolling, regime-aware evidence. When HP or BK filtering is used, disclose parameters and causal versus two-sided construction, treat symmetric endpoints as descriptive only, and do not count the filter and the FFT of its output as independent evidence. Long cycles and spectral peaks adjust priors or confidence; they do not independently cause price moves.
- For official data, decompose components, definitions, revisions, base effects, and independent proxies before raising confidence.
- For ETF-flow inference, aggregate peer ETFs by exposure, use share changes rather than AUM changes, separate secondary-market selling from primary-market redemption, and never identify a seller from shares alone.
- For behavior selection, classify the market state first, then compare modes with regime-matched return priors after costs, exit failures, and ruin paths. Filter by explicit risk constraints before ranking expected net log growth. If calibrated priors are absent, recommend qualitatively and withhold numeric expected return.
- When evidence families conflict, preserve the conflict, explain which horizon each governs, and widen ranges or lower confidence.

## Minimum Output Contract

Lead with the answer. State the as-of time and horizon, data quality, regime, causal chain, strongest supporting and opposing evidence, probability type, base/upside/downside scenarios, relevant levels or time windows, and observable invalidation/update triggers. When behavior selection is requested, add the chosen mode, capital/time exposure, executable exit, gross prior, all-in costs, exit/ruin mixture, net return range, calibration label, rejected alternatives, and switch triggers. Match the user's language. Never fabricate precision when the data cannot support it.

## Scripts

Use `scripts/analyze_ohlcv.py` for CSV OHLCV analysis. Expected columns are `timestamp,open,high,low,close,volume`; case-insensitive aliases are accepted. Add `--calendar events.csv` when a known event calendar is available.

```powershell
python scripts/analyze_ohlcv.py --input prices.csv --market us_equity --horizon short
```

Use `scripts/analyze_etf_flows.py` for daily A/H-share ETF share/flow, crowding, unwind, and three-state Bayesian scenario analysis. Read the market-specific ETF reference for the input schema and interpretation limits.

```powershell
python scripts/analyze_etf_flows.py --input etf_daily.csv --scope broad --group csi300
```

Add `--market hk` for canonical fund-level Hong Kong data. Do not pass repeated multi-counter units as separate funds.

Use `scripts/recommend_behavior_mode.py` only after the market-specific state posterior and regime-matched behavior priors are available. It calculates cost-adjusted return ranges, survival-adjusted log growth, risk-budget violations, and the eligible-mode ranking.

```powershell
python scripts/recommend_behavior_mode.py --input behavior_priors.json --pretty
```

Use `scripts/train_market_transformer_demo.py` only for a requested trainable-model demo. It expects panel data with `timestamp,symbol,market,open,high,low,close,volume` plus optional numeric features.

```powershell
python scripts/train_market_transformer_demo.py --input panel_daily_features.csv --lookback 256 --horizon 1 --epochs 5
```

Run `scripts/validate_skill_graph.py` after changing the skill architecture.
