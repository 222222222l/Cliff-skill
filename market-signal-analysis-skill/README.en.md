# Market Signal Analysis Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `market-signal-analysis-skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

`market-signal-analysis` is a methodological package for stocks, ETFs, sectors, indices, and liquid macro markets. It connects price structure, fundamentals, flows, policy, actor incentives, and data quality to a decision, loading only relevant modules.

The deliverable comprises Agent instructions, references, and deterministic calculators. It is not an out-of-sample validated trading strategy. Model-implied scenario weights are not observed win rates.

## Method and coverage

Use one primary module with at most two overlays by default. Fix the market, horizon, data vintage, and risk constraints before comparing evidence and exit conditions.

| Module | Scope |
| --- | --- |
| Price and trend | OHLCV, momentum, volatility, breadth, timeframes, ATR risk boundaries |
| ETF flows and crowding | Share changes, estimated flows, peer aggregation, A-share support/withdrawal, Hong Kong counter deduplication |
| Firms and sectors | Earnings, cash flow, valuation, governance, supply, narrative risk |
| Macro and policy | U.S. liquidity, rates/fiscal conditions, transmission, incentives, constraints |
| Cycles and events | Inventory/credit/capex cycles, exploratory frequency analysis, expiry/FOMC/rebalancing |
| Action comparison | Costs, risk budgets, exit failures, loss paths, conditional return assumptions |
| Data audit | Comparable definitions, adjustments, publication lags, vintages, independent evidence |

Correlation, spectral peaks, or regression weights alone establish neither causality nor tradability. Label probabilities as empirical, model-implied, or judgmental. Insufficient evidence calls for qualitative conclusions. See [SKILL.md](SKILL.md) and [references](references/).

## Install and use

Install the repository root containing `SKILL.md` in the host's supported Skill directory, then invoke:

```text
Use $market-signal-analysis to assess whether this ETF pullback changes
the original hypothesis, verify dates and definitions, and state
counterevidence, risk boundaries, and the next verification point.
```

The ETF calculator accepts long-form data:
`date,symbol,group,scope,close,nav,shares,turnover`. For Hong Kong ETFs, first normalize trading counters to a canonical fund/share class and use `--market hk`.

```bash
python scripts/analyze_etf_flows.py --input etf_daily.csv --scope broad --group csi300 --regime range_extraction --pretty
python scripts/recommend_behavior_mode.py --input behavior_priors.json --pretty
python scripts/validate_skill_graph.py
```

ETF peers are aggregated by estimated money flow rather than raw share counts. Behavior selection requires horizon-matched priors, costs, and exit/ruin paths. Numeric returns are withheld when a material state prior has fewer than 20 effective events; that minimum alone does not establish robustness.

## Evidence limits

The validator checks routing, references, and structure, not investment performance. Formal evaluation needs point-in-time data, adjustments, survivorship/cost controls, treatment of overlapping observations and multiple trials, and separate development/holdout periods.

See [statistical weighting](references/statistical-weighting.md), [official-data verification](references/official-data-verification.md), [behavior selection](references/behavior-mode-selection.md), and the [research roadmap](references/research-and-optimization-roadmap.md). The optional Transformer demo is a research starting point.

No top-level `LICENSE` is currently supplied. Asset decisions require current data and applicable individual constraints; no return is guaranteed.
