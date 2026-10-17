# Research and Optimization Roadmap

Use this reference when the user wants to position the market Transformer as a publishable research project, compare it with financial deep learning literature, or select standard datasets for training and evaluation.

## Publishable Research Positioning

Avoid framing the work as another "Transformer predicts stock prices" paper. A stronger framing is:

```text
Prior-Guided Long-Context Market Transformer for Cost-Aware Trading Decisions
```

The core claim should be decision-oriented:

```text
Technical-analysis priors, long-context daily self-attention, and multi-market pretraining can learn transferable market-state representations that improve cost-aware trading decisions under limited target-market data.
```

## Research Lines To Borrow From

### 1. Empirical Asset Pricing With Machine Learning

Gu, Kelly, and Xiu show that machine learning improves asset-return prediction by learning nonlinear interactions among high-dimensional predictors. Their dominant predictor groups include trend/momentum, liquidity, and volatility.

Borrow:

- Use return prediction and portfolio-level economic value, not only forecast error.
- Evaluate feature groups such as momentum, liquidity/volume, and volatility.
- Include regularization and strict out-of-sample validation.

Source: https://academic.oup.com/rfs/article/33/5/2223/5758276

### 2. Temporal Fusion Transformer

TFT contributes variable selection, gating, multi-horizon quantile prediction, and interpretability.

Borrow:

- Add feature-level and group-level variable selection.
- Report dynamic feature importance by horizon and market regime.
- Predict return quantiles, not just point targets.

Source: https://arxiv.org/abs/1912.09363

### 3. PatchTST And Long-Context Time-Series Transformers

PatchTST uses patches to retain local sequence semantics while reducing attention cost and allowing longer history.

Borrow:

- Keep single-timeframe daily modeling, but patch 5 or 20 bars into tokens.
- Compare raw-day tokens versus patch tokens.
- Use masked patch reconstruction as self-supervised pretraining.

Source: https://arxiv.org/abs/2211.14730

### 4. MASTER Market-Guided Stock Transformer

MASTER models dynamic feature effectiveness and complex stock correlations with market-guided feature selection.

Borrow:

- Add market context as a first-class conditioning signal.
- Let market state modulate feature gates.
- Consider cross-asset context without forcing a heavy graph model in the first version.

Source: https://ojs.aaai.org/index.php/AAAI/article/view/27767

### 5. Graph-Based Stock Prediction

Relational Stock Ranking, HATS, and later heterogeneous/dynamic graph models show that stock interdependencies can improve stock movement prediction.

Borrow:

- Add a lightweight cross-asset context branch first: index ETFs, sector ETFs, peer leaders.
- Later compare against graph branches using industry, supply-chain, ownership, price-correlation, or news co-mention edges.
- Use ranking metrics and portfolio construction, not only binary movement accuracy.

Sources:

- https://arxiv.org/abs/1809.09441
- https://github.com/dmis-lab/hats

### 6. Deep Reinforcement Learning And Decision Utility

FinRL and related DRL trading work emphasize that trading models should output actions under costs, risk, and execution constraints.

Borrow:

- Add a differentiable decision head for position score.
- Penalize transaction costs, slippage, turnover, and downside risk.
- Keep supervised return-distribution heads to stabilize training before using heavier RL.

Source: https://arxiv.org/abs/2011.09607

### 7. Financial Foundation Models And Time-Series Foundation Models

TimesFM, Chronos, and MOMENT demonstrate large-scale time-series pretraining and transfer. Financial foundation model surveys point to data availability, scaling, and evaluation as open problems.

Borrow:

- Use multi-market pretraining and single-market/asset adapter fine-tuning.
- Test low-data transfer: pretrained backbone versus training from scratch.
- Include missing-feature robustness through masked pretraining.

Sources:

- https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/
- https://arxiv.org/abs/2403.07815
- https://arxiv.org/abs/2402.03885

### 8. Financial Validation And Backtest Overfitting

Financial machine learning papers are vulnerable to data leakage, backtest overfitting, and multiple testing.

Borrow:

- Use walk-forward validation.
- Add purging/embargo when labels overlap in time.
- Report deflated Sharpe or probability of backtest overfitting when many model variants are tested.

Source: https://escholarship.org/uc/item/4w1110bb

## Executable Optimization Plan

### Priority 1: Prior-Guided Group Gating

Add grouped gates:

```text
trend group
volume/liquidity group
macd group
rsi_kdj group
volatility group
divergence group
market_context group
event_context group
```

Use the existing technical-analysis priors as gate bias:

```text
group_logit = learned_logit + alpha * log(prior_weight)
```

Evaluate:

- no gate
- learned gate only
- fixed prior only
- prior-guided learned gate

### Priority 2: Self-Supervised Pretraining

Implement:

- masked feature reconstruction
- masked indicator-group reconstruction
- masked return reconstruction
- contrastive regime learning

The key paper claim is stronger if the model demonstrates useful transfer when downstream labels are scarce.

### Priority 3: Market Context Conditioning

Keep the model single-timeframe daily, but add context inputs:

```text
SPY, QQQ, sector ETF, VIX, rates, dollar index, market breadth
```

Condition gates and attention on this context.

### Priority 4: Cost-Aware Decision Head

Continue predicting return distribution, then add a decision head:

```text
position_score in [-1, 1]
```

Train with:

```text
loss =
  quantile_loss
  + direction_loss
  + huber_return_loss
  + negative_net_pnl_after_costs
  + turnover_penalty
  + downside_penalty
```

### Priority 5: Robust Evaluation Protocol

Use:

- chronological split, never random time split
- walk-forward windows
- transaction costs and slippage
- ablation experiments
- regime-wise metrics
- single-market and single-asset fine-tuning tests

Report:

- direction accuracy
- IC / Rank IC
- quantile calibration
- Brier score
- annualized return
- Sharpe / Sortino
- max drawdown
- turnover
- deflated Sharpe or PBO when applicable

## Standard Dataset Candidates

### Daily Multi-Asset Panel: Microsoft Qlib

Best first benchmark for the proposed daily long-context model.

- Type: daily stock panel, engineered features, benchmark workflows.
- Markets: China A-share and U.S. stock data are supported by Qlib download scripts in documentation.
- Features: Alpha158 and Alpha360 are common Qlib benchmark feature sets.
- Use for: daily return prediction, stock ranking, IC/Rank IC, portfolio backtest.
- Pros: reproducible workflows, existing baselines, direct match to the model's daily timeframe.
- Cons: Qlib feature definitions and data handling must be carefully aligned with no-lookahead rules.

Sources:

- https://github.com/microsoft/qlib/blob/main/examples/benchmarks/README.md
- https://qlib.readthedocs.io/en/v0.7.2/component/data.html

Recommended role:

```text
Primary benchmark for MVP and ablation experiments.
```

### Multimodal Price + Text: StockNet

- Type: stock prices plus tweets.
- Period: commonly used ACL 2018 stock movement prediction dataset.
- Use for: testing whether news/social text improves the daily market Transformer.
- Pros: known academic dataset, manageable size, suitable for multimodal extension.
- Cons: older and smaller than large market datasets; Twitter access/licensing context should be checked.

Sources:

- https://aclanthology.org/P18-1183/
- https://github.com/yumoxu/stocknet-dataset
- https://huggingface.co/datasets/nomnomshark41/stocknet-dataset

Recommended role:

```text
Secondary multimodal benchmark after price-only model is stable.
```

### Large Price + News Dataset: FNSPID

- Type: financial news and stock price integration dataset.
- Scale: repository states 29.7M stock prices and 15.7M financial news records for 4,775 S&P 500 companies from 1999 to 2023.
- Use for: large-scale multimodal pretraining and news-aware market context.
- Pros: much larger than StockNet; useful for foundation-style pretraining.
- Cons: news source quality, timestamp alignment, survivorship bias, and licensing require careful audit.

Sources:

- https://github.com/Zdong104/FNSPID_Financial_News_Dataset
- https://arxiv.org/abs/2402.06698

Recommended role:

```text
Large multimodal pretraining candidate.
```

### Relational Stock Data: HATS / RSR Repositories

HATS:

- Type: S&P 500 price-related data plus corporate relation data.
- Period: repository states 2013-02-08 to 2019-06-17.
- Use for: benchmarking relation-aware extensions.

Source: https://github.com/dmis-lab/hats

RSR / Temporal Relational Ranking:

- Type: stock ranking with temporal relational modeling.
- Use for: ranking and relation-aware comparison.

Sources:

- https://github.com/fulifeng/Temporal_Relational_Stock_Ranking
- https://arxiv.org/abs/1809.09441

Recommended role:

```text
Graph/context extension benchmark, not the first MVP dataset.
```

### High-Frequency Benchmark: FI-2010

- Type: limit order book benchmark for mid-price forecasting.
- Market: NASDAQ Nordic order book data in the original benchmark.
- Use for: testing whether architecture generalizes to microstructure tasks.
- Pros: classic public LOB benchmark used by DeepLOB and many follow-up papers.
- Cons: not daily data; small and often considered too narrow for broad trading claims.

Sources:

- https://www.research.ed.ac.uk/en/datasets/benchmark-dataset-for-mid-price-forecasting-of-limit-order-book-d/
- https://arxiv.org/abs/1705.03233

Recommended role:

```text
High-frequency generalization benchmark, separate from daily model claims.
```

### Professional Microstructure: LOBSTER

- Type: NASDAQ TotalView-ITCH-derived limit order book data.
- Access: academic research access; often institution-dependent.
- Use for: stronger microstructure experiments beyond FI-2010.
- Pros: high-quality LOB data for specific NASDAQ names.
- Cons: access restrictions; not ideal for fully open reproducibility.

Sources:

- https://data.lobsterdata.com/
- https://data.lobsterdata.com/info/help_faq_general.php

Recommended role:

```text
Optional high-quality extension if academic access is available.
```

### Institutional Daily Equity Standard: CRSP / WRDS

- Type: U.S. stock prices, returns, dividends, shares, delisting-aware data.
- Use for: publication-grade U.S. equity return prediction and asset-pricing comparisons.
- Pros: academic finance gold standard; reduces survivorship and adjustment concerns.
- Cons: paid/institutional access through WRDS; not open.

Sources:

- https://www.library.hbs.edu/services/help-center/finding-a-time-series-of-stock-prices-in-crsp
- https://www.cbs.dk/en/library/search-library/online-resources/crsp

Recommended role:

```text
Best publication-grade dataset if WRDS access exists.
```

### Competition / External Evaluation: Numerai

- Type: obfuscated global stock-market panel.
- Use for: robust live-style ML evaluation and era-based modeling.
- Pros: free, clean, regularized, ongoing tournament evaluation.
- Cons: features are obfuscated; not suitable for technical-indicator interpretability claims.

Sources:

- https://docs.numer.ai/tournament/learn
- https://docs.numer.ai/numerai-tournament/data

Recommended role:

```text
External robustness benchmark, not primary interpretability dataset.
```

### Auction / Volatility Competitions: Optiver Kaggle

- Type: market microstructure, volatility, closing auction prediction.
- Use for: testing cost-aware prediction on public competition-style datasets.
- Pros: practical prediction tasks and strong public baselines.
- Cons: Kaggle access/login; competition objective may not align with daily trading model.

Sources:

- https://optiver.com/kaggle-and-optiver-predicting-nasdaqs-closing-cross-auction-movements/
- https://www.kaggle.com/c/optiver-realized-volatility-prediction

Recommended role:

```text
Optional applied benchmark for volatility or auction-specific extensions.
```

### Forecasting-To-Investment Competition: M6

- Type: financial forecasting and investment decision competition.
- Use for: comparing probabilistic forecast quality and investment allocation.
- Pros: directly studies gap between forecasts and investment decisions.
- Cons: competition setup differs from single-symbol daily trading.

Sources:

- https://arxiv.org/abs/2310.13357
- https://arxiv.org/abs/2303.01855

Recommended role:

```text
Decision-forecasting benchmark reference, especially for probabilistic outputs.
```

## Recommended Dataset Plan

### MVP

Use Qlib daily stock data:

```text
Train: multi-symbol daily panel
Features: Alpha158/Alpha360 plus custom technical-indicator priors
Targets: 1d, 5d, 20d log return
Metrics: IC, Rank IC, quantile calibration, cost-aware portfolio backtest
```

### Publication-Grade If Data Access Exists

Use CRSP/WRDS:

```text
Train: U.S. stock panel with delisting-aware returns
Context: SPY/QQQ/VIX/sector ETFs/macroeconomic variables
Evaluation: walk-forward, purged validation, deflated Sharpe, ablations
```

### Transfer Learning Tests

Use:

```text
Pretrain: Qlib U.S. and China daily panels or CRSP if available
Fine-tune: single market / single symbol / sector subset
Test: low-data regime and cross-market transfer
```

### Multimodal Extension

Use:

```text
StockNet for small text-price benchmark
FNSPID for large-scale news-price pretraining
```

### Microstructure Extension

Use:

```text
FI-2010 for public LOB benchmark
LOBSTER if institutional academic access exists
```

## Ablation Matrix

Run these comparisons:

| Variant | Purpose |
| --- | --- |
| Linear / XGBoost baseline | Establish strong low-cost baseline. |
| LSTM / TCN | Compare against classic sequence models. |
| Vanilla Transformer | Show benefit of architecture changes. |
| Patch Transformer | Measure long-context cost/performance tradeoff. |
| Patch Transformer + feature gate | Test dynamic weighting. |
| Prior-guided feature gate | Test value of technical-analysis priors. |
| Prior-guided gate + pretraining | Test representation learning. |
| Prior-guided gate + pretraining + decision head | Test final decision utility. |
| With and without market context | Test MASTER-inspired conditioning. |
| With and without single-asset adapter | Test fine-tuning design. |

## Minimum Claims For A Strong Paper

A credible paper should demonstrate:

1. Forecast quality improves on at least one standard dataset.
2. Decision utility improves after costs, not only in raw prediction metrics.
3. Prior-guided dynamic weighting improves over fixed technical-analysis weights and learned-only gates.
4. Pretraining improves low-data fine-tuning.
5. Long-context patching improves cost/performance versus shorter context or raw full attention.
6. Results survive walk-forward validation and reasonable transaction costs.
7. Interpretability outputs identify sensible feature groups across regimes.
