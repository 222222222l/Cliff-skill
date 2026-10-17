# Deep Learning Extension

Use this reference when the user wants to extend technical signal analysis into a trainable quantitative decision model. Treat the model as a decision-support system, not as a guaranteed price oracle.

## First-Principles Objective

Optimize for decision utility after costs, not for point-price prediction alone.

The model should learn a mapping:

```text
long daily market sequence -> return distribution, risk distribution, and position score
```

The decision objective is:

```text
net_pnl_t = position_t * return_{t+1}
            - transaction_cost * abs(position_t - position_{t-1})
            - slippage_penalty
```

Prefer direct decision usefulness:

- Predict next-day and multi-day log-return distributions.
- Predict direction probability and downside risk.
- Output a bounded position score in `[-1, 1]`.
- Explain which feature groups and historical tokens influenced the decision.

Do not optimize only for next-day close-price MSE. Price levels are non-stationary and scale-dependent. Predict normalized returns and convert back to price intervals only at the output layer.

## Recommended Architecture

Name: `Single-Timeframe Long-Context Market Transformer`

Use one primary timeframe at a time, usually daily bars for the first implementation. Each token represents one trading day.

```text
Daily token
  OHLCV normalized features
  return and volatility features
  technical indicators
  technical signal flags and prior weights
  market/index/sector context
  event/context flags
  missing-value mask
    |
Feature projection
    |
Feature gating / variable selection
    |
Patch or long-context temporal Transformer
    |
Market and asset adapters
    |
Prediction heads + decision head
```

## Input Schema

Minimum CSV columns:

```text
timestamp,symbol,market,open,high,low,close,volume
```

Recommended columns:

```text
timestamp
symbol
market
open,high,low,close,volume
ret_1d,ret_5d,ret_20d,ret_60d
realized_vol_20d,atr_14,relative_volume_20d
ma_20,ma_50,ma_200
macd,macd_signal,macd_hist
rsi_14,kdj_k,kdj_d,kdj_j
bollinger_pct,bollinger_width
trend_signal,volume_signal,macd_signal_flag,rsi_signal_flag,kdj_signal_flag,divergence_signal
prior_weight_trend,prior_weight_volume,prior_weight_macd,prior_weight_rsi_kdj,prior_weight_divergence
index_ret_1d,index_ret_20d,vix_level,vix_change,sector_ret_1d,sector_ret_20d
earnings_flag,macro_event_flag
```

Missing columns are allowed if the model receives a missing-value mask. During training, randomly mask feature groups so the model learns robust inference when upstream data is incomplete.

## Feature Normalization

Use only information available at or before each timestamp.

- Convert price targets to log returns.
- Normalize features with rolling z-scores or train-window statistics.
- Use per-market and per-symbol embeddings instead of leaking future global statistics.
- Keep raw close only for final price reconstruction; do not force the model to learn absolute price scale.

## Computational Cost Controls

Avoid full attention over very long raw sequences as the first version. Full attention costs `O(sequence_length^2)`.

MVP defaults:

```text
lookback: 512 trading days
patch_size: 5 trading days
effective_tokens: about 102
d_model: 128
layers: 4
heads: 4
dropout: 0.15
features: 40-150
```

Scale path:

```text
Phase 1: daily U.S. equities and ETFs, 512-day lookback, patch attention.
Phase 2: more symbols and market context, 1024-day lookback.
Phase 3: market adapters for A-shares, Hong Kong, futures, crypto.
Phase 4: asset adapters for single-symbol fine-tuning.
```

Use patching, memory tokens, sparse attention, or linear attention before increasing raw context length.

## Pretraining Tasks

Use multi-market or multi-symbol data to learn general market representations.

1. Masked feature reconstruction.
   - Randomly mask OHLCV, indicators, or market context.
   - Reconstruct normalized features.

2. Masked return modeling.
   - Predict hidden historical returns from surrounding context.
   - Helps the model learn price dynamics without relying only on labels.

3. Next return distribution.
   - Predict 1-day, 5-day, and 20-day log-return quantiles.

4. Market regime classification.
   - Labels may be heuristic: trend, range, high-volatility, low-volatility, crash, recovery.

5. Contrastive regime learning.
   - Pull similar market states closer in embedding space and push dissimilar states apart.

## Fine-Tuning Strategy

For a single market or single symbol:

1. Load the pretrained backbone.
2. Freeze most Transformer blocks initially.
3. Train market adapter, asset adapter, normalization layers, and heads.
4. Unfreeze the last 1-2 Transformer blocks only if validation improves.
5. Use walk-forward validation; never random-split time series.

Recommended fine-tuning target mix:

```text
quantile_loss for return distribution
binary_cross_entropy for direction
huber_loss for expected return
negative_utility_loss for decision pnl after costs
turnover_penalty for excessive trading
```

## Objective Function

Use a weighted loss:

```text
loss =
  1.00 * quantile_loss(return_quantiles, future_return)
  + 0.50 * direction_bce(up_probability, return > 0)
  + 0.25 * huber_loss(expected_return, future_return)
  + 0.50 * negative_decision_utility(position, future_return, costs)
  + 0.10 * turnover_penalty(position_t, position_t_minus_1)
```

For pure pretraining, reduce or disable decision utility until the model has learned stable market representations.

## Output Schema

The model should return:

```json
{
  "symbol": "NVDA",
  "timestamp": "2026-06-03",
  "horizon": "1d",
  "expected_log_return": 0.0032,
  "return_quantiles": {
    "p10": -0.018,
    "p50": 0.002,
    "p90": 0.024
  },
  "up_probability": 0.57,
  "downside_risk": 0.018,
  "position_score": 0.35,
  "target_price_interval": {
    "p10": 210.91,
    "p50": 215.18,
    "p90": 219.96
  },
  "feature_group_weights": {
    "trend": 0.19,
    "volume": 0.14,
    "macd": 0.08,
    "rsi_kdj": 0.06,
    "market_context": 0.22
  }
}
```

## Validation

Evaluate both forecast quality and decision quality:

- Direction accuracy.
- Information coefficient and rank IC.
- Quantile calibration.
- Brier score for up probability.
- Net return after costs.
- Sharpe, Sortino, max drawdown, turnover.
- Hit rate by market regime.
- Walk-forward stability.

Reject a model that has good prediction metrics but poor net decision utility after transaction costs.
