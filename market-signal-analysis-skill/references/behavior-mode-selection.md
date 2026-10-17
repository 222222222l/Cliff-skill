# Market Behavior Mode Selection

Use this reference when the user asks which behavior, exposure pattern, or
execution style best fits the current market stage; asks for the
highest-return-per-unit-risk mode; or asks for an expected return after costs,
risk, and exit mechanics.

This module selects a behavior after the market state has been classified. It
does not replace the market-specific state model, and it does not turn a
technical score into a promised return.

## Contents

1. Decision objective
2. Data gate
3. Behavior library
4. Market-specific state maps
5. Volatility and path features
6. State posterior
7. Return-prior model
8. Risk-budget selection
9. Structured calculator input
10. Calibration and bias controls
11. Execution and cost overlays
12. Required output

## 1. Decision Objective

Prefer survival-adjusted log growth over raw arithmetic return:

```text
choose behavior b
to maximize expected net log growth
subject to expected-shortfall, drawdown, ruin, leverage, and liquidity limits
```

Do not call a behavior optimal without specifying:

- market and instrument;
- horizon;
- current market state and state uncertainty;
- entry and exit rules;
- capital and time exposure;
- fees, spread, slippage, tax, funding, borrow, and impact;
- expected shortfall, drawdown, and forced-exit risk;
- empirical or model-implied status of the return estimate.

Cash or no trade is a valid behavior. Opportunity cost is not the same as
market-loss exposure.

## 2. Data Gate

Require these inputs before giving a numeric expected return:

- adjusted OHLCV with a defined timestamp and frequency;
- short- and long-horizon realized volatility;
- a state posterior or explicit scenario weights;
- regime-matched return priors for every candidate behavior;
- a complete entry, sizing, and exit rule;
- round-trip implementation costs;
- failed trades, stopped strategies, liquidations, and inactive periods in the
  calibration sample;
- at least 20 non-overlapping or effectively independent historical events per
  material state.

With fewer than 20 events, or without a regime-matched behavior prior, give a
qualitative mode recommendation and list the missing calibration data. Do not
manufacture a numeric expected return from indicator weights.

## 3. Behavior Library

Use stable IDs in analysis and structured inputs.

| ID | Behavior | Core exposure | Default use | Main hidden risk |
| --- | --- | --- | --- | --- |
| `cash_first` | Cash-first conditional participation | Minimal market and time exposure | Unconfirmed, chaotic, or distribution states | Opportunity cost and inflation |
| `diversified_low_turnover` | Unlevered diversified low-turnover accumulation | Persistent but diversified directional exposure | Stable fundamental expansion and healthy pullbacks | Long market drawdown and concentration inside an index |
| `confirmed_etf_trend` | Confirmed broad/sector ETF trend participation | Conditional directional exposure with mechanical exits | A-share policy-floor repair or broad/main-line acceleration | T+1, price limits, false policy confirmation, breadth divergence |
| `event_spot_trend` | Event-confirmed, unlevered spot trend | Short-duration event exposure; low exposure outside the window | Crypto event/liquidity trend with spot-flow confirmation | Jump, venue, custody, adverse selection, liquidation spillover |
| `market_neutral_small_edges` | Diversified small-edge, low-net-direction system | Low beta but high operational intensity | Professional, capacity-limited implementation | Model decay, crowding, leg risk, borrow, venue and infrastructure failure |

Do not classify concentrated stock picking, leveraged pyramiding, leaderboard
trading, or unrestricted liquidity provision as low-risk merely because their
observed winners had high returns.

## 4. Market-Specific State Maps

Treat each market profile as a conditional prior, not a permanent identity.
Hold global macro and external liquidity constant when comparing market
microstructure, but still allow the observed state to override the structural
prior.

### Crypto Spot

Use these primary states:

| State | Observable pattern | Preferred behavior |
| --- | --- | --- |
| `compression_unconfirmed` | Short volatility falls, direction efficiency is low, event/flow confirmation is absent | `cash_first` |
| `event_trend_confirmed` | Event is known ex ante; spot volume and real flow confirm; direction efficiency rises; leverage is not extreme | `event_spot_trend` |
| `leverage_expansion` | Perpetual open interest and funding rise faster than spot demand | Reduce `event_spot_trend`; prefer `cash_first` |
| `liquidation_cascade` | Short and long volatility are high, liquidity thins, forced sales dominate | `cash_first` |
| `post_event_decay` | Price stops responding to good news, spot flow decays, failed breakouts rise | Exit to `cash_first` |
| `maturing_broad_adoption` | Long volatility declines persistently; regulated spot/ETF flow broadens; leverage share falls | Test `diversified_low_turnover` only for highly liquid majors |

Do not equate HODL exposure with active trend skill. Do not classify
cross-venue arbitrage as a trend behavior.

### A-Shares

Use the state names in `references/a-share-macro-trading-model.md`:

| State | Preferred behavior |
| --- | --- |
| `policy_floor_repair` | Small, staged `confirmed_etf_trend` after price, breadth, and ETF action confirm |
| `range_stabilized_extraction` | `cash_first`; a stable index with weak median-stock returns is not a safe holding state |
| `main_line_acceleration` | `confirmed_etf_trend` in a liquid sector ETF only when internal breadth confirms |
| `crowded_distribution` | Reduce or exit to `cash_first` |
| `broad_breakdown` | `cash_first` |
| `post_washout_accumulation` | Rebuild broad ETF exposure in stages; do not catch the falling knife |

Policy language is an expectation. Upgrade the state only after observable,
costly action appears in price, breadth, ETF shares/flows, credit, or repeated
implementation.

### U.S. Equities

Use these primary states for broad, liquid equities:

| State | Observable pattern | Preferred behavior |
| --- | --- | --- |
| `fundamental_expansion` | Earnings/revisions, breadth, and medium/long trend agree; long volatility is contained | `diversified_low_turnover` |
| `healthy_pullback` | Short volatility rises but long volatility and fundamental breadth remain intact | Continue or stage `diversified_low_turnover`; avoid reactive turnover |
| `concentrated_late_cycle` | Index rises while equal-weight breadth and revisions weaken; crowding rises | Reduce concentration; mix `diversified_low_turnover` with `cash_first` |
| `event_shock` | Short volatility jumps around a dated event while long state is unresolved | Delay entry or use small conditional exposure; require post-event confirmation |
| `broad_deterioration` | Long volatility rises with falling breadth and revisions | `cash_first` or tightly controlled trend exposure |
| `recovery_confirmation` | Breadth and revisions improve after a washout; failed downside breaks increase | Stage `diversified_low_turnover` |

Do not apply this stable-market prior to illiquid small caps, binary biotech,
meme stocks, or options-dominated single names without an event-risk branch.

## 5. Volatility and Path Features

Compare volatility with the same market's history, not with one universal
absolute threshold.

Compute:

```text
short_vol = annualized realized volatility over the short window
long_vol = annualized realized volatility over the long window
vol_ratio = short_vol / long_vol
short_vol_percentile = percentile of short_vol in the market-matched history
long_vol_percentile = percentile of long_vol in the market-matched history
trend_efficiency = abs(P_t - P_t-n) / sum(abs(P_j - P_j-1))
jump_share = jump variance / total realized variance
cost_to_move = all-in round-trip cost / expected gross move
```

Suggested windows:

- crypto: 7/30 days for short state; 365 days and two-year weekly history for
  long state;
- A-shares and U.S. equities: 20 trading days for short state; 252 trading days
  and three-year weekly history for long state.

Interpretation:

| Short vol | Long vol | Trend efficiency | Default read |
| --- | --- | --- | --- |
| Low | Low | Medium/high | Persistent low-turnover exposure can be efficient |
| High | Low/medium | High | A shock may be becoming a trend; require flow confirmation |
| High | High | Low | Chaotic or forced-flow state; prefer cash |
| Low | High | Low | Compression, not an automatic buy |
| Medium | Medium | Low | Range/cost-drag state; do not force a trade |

Price limits can suppress observed intraday volatility while accumulating
latent exit demand. For A-shares, add limit-down breadth, sealed-order depth,
T+1 inventory, suspensions, and failed exits to the risk state.

## 6. State Posterior

Let `s` index mutually exclusive market states and `g` index independent
evidence families:

```text
log posterior_s =
    log prior_s
    + sum_g reliability_g * log(LR_g,s)

posterior_s = exp(log posterior_s) / sum_k exp(log posterior_k)
```

Use evidence groups, not individual indicators:

- trend/path;
- breadth;
- realized liquidity and flow;
- fundamentals/revisions;
- valuation or leverage state;
- policy/actor action;
- event and positioning risk.

Cap heuristic likelihood ratios and label the result `model-implied scenario
weights`. Use `empirical probability` only after regime-matched,
out-of-sample calibration.

## 7. Return-Prior Model

For behavior `b`, market `m`, and state `s`, estimate these priors from
walk-forward historical episodes:

```text
normal_return_low_bms
normal_return_mean_bms
normal_return_high_bms
exit_probability_bms
exit_loss_bms
ruin_probability_bms
ruin_loss_bms
expected_shortfall_bms
max_drawdown_bms
```

The normal-return values are gross price/strategy returns over the stated
horizon before implementation costs. `exit_loss` is a positive loss magnitude
when the planned exit fails or gaps. `ruin_loss` includes liquidation or
strategy termination.

Let:

```text
p_normal = 1 - p_exit - p_ruin
cost = fees + spread + slippage + tax + funding + borrow + impact
```

State-conditional net expected return:

```text
E[R_net | b,m,s] =
    p_normal * (normal_return_mean - cost)
    - p_exit * (exit_loss + cost)
    - p_ruin * ruin_loss
```

Compute low and high estimates by replacing `normal_return_mean` with the
empirical low and high priors. Do not assume normality merely to manufacture a
confidence interval.

State-mixture expected return:

```text
E[R_net | b,m] =
    sum_s posterior_s * E[R_net | b,m,s]
```

Survival-adjusted log growth:

```text
G_bms =
    p_normal * log(1 + normal_return_mean - cost)
    + p_exit * log(1 - exit_loss - cost)
    + p_ruin * log(1 - ruin_loss)

G_bm = sum_s posterior_s * G_bms
```

If any log argument is non-positive, treat the path as ruin and reject the
behavior under a long-term survival objective.

Do not annualize a partial-window event return. Convert to annualized log
growth only when the full calendar-time process, including inactive cash
periods and all triggered windows, is observed.

## 8. Risk-Budget Selection

Avoid hiding risk preferences inside arbitrary score weights. First reject
behaviors that violate explicit constraints:

```text
weighted expected shortfall <= max_expected_shortfall
weighted max drawdown <= max_drawdown
weighted ruin probability <= max_ruin_probability
gross leverage <= max_gross_leverage
outside-state exposure <= max_outside_state_exposure, when applicable
exit rule is defined and executable
cost_to_move < configured maximum
```

Among eligible behaviors:

1. choose the highest expected net log growth;
2. break close ties with the higher conservative net-return lower bound divided
   by expected shortfall;
3. then prefer lower cost, lower exposure time, and simpler execution.

If no behavior is eligible, recommend `cash_first` or no trade. Never relax the
risk budget merely to force a non-cash answer.

Use `scripts/recommend_behavior_mode.py` to calculate the state mixture,
cost-adjusted return range, log growth, constraint failures, and ranking from
structured priors.

## 9. Structured Calculator Input

Pass JSON to `scripts/recommend_behavior_mode.py`. All returns, volatility,
loss, costs, exposure, and probabilities use decimal units over the stated
horizon; `0.05` means 5%. The return priors for every mode must use the same
horizon as `horizon_days`.

```json
{
  "market": "a_share",
  "as_of": "YYYY-MM-DD",
  "horizon_days": 60,
  "probability_label": "model_implied_probability",
  "context": {
    "short_vol": 0.0,
    "long_vol": 0.0,
    "short_vol_percentile": 0.0,
    "long_vol_percentile": 0.0,
    "trend_efficiency": 0.0,
    "jump_share": 0.0
  },
  "state_probabilities": {
    "policy_floor_repair": 1.0
  },
  "risk_budget": {
    "max_expected_shortfall": 0.0,
    "max_drawdown": 0.0,
    "max_ruin_probability": 0.0,
    "max_gross_leverage": 1.0,
    "max_outside_state_exposure": 0.0,
    "max_cost_to_expected_move": 0.0
  },
  "modes": [
    {
      "id": "confirmed_etf_trend",
      "label": "Confirmed ETF trend",
      "exit_defined": true,
      "max_gross_leverage": 1.0,
      "outside_state_exposure": 0.0,
      "costs": {
        "fees": 0.0,
        "spread": 0.0,
        "slippage": 0.0,
        "tax": 0.0,
        "funding": 0.0,
        "borrow": 0.0,
        "impact": 0.0
      },
      "state_priors": {
        "policy_floor_repair": {
          "normal_return_low": 0.0,
          "normal_return_mean": 0.0,
          "normal_return_high": 0.0,
          "exit_probability": 0.0,
          "exit_loss": 0.0,
          "ruin_probability": 0.0,
          "ruin_loss": 0.0,
          "expected_shortfall": 0.0,
          "max_drawdown": 0.0,
          "sample_count": 0,
          "out_of_sample": false,
          "includes_failures": false
        }
      }
    }
  ]
}
```

The zero values above document the schema; they are not market defaults or
recommended risk limits. `state_probabilities` must sum to one. Supply a prior
for every state with positive probability and every candidate mode.

## 10. Calibration and Bias Controls

Build each behavior prior from a fixed sampling frame:

- use all funded accounts, products, or strategy activations at the state
  start, not only visible winners;
- include closed, liquidated, delisted, and abandoned paths;
- consolidate all accounts assigned to the same strategy;
- include cash and inactive periods in calendar-time performance;
- predefine state transitions, entry, sizing, and exit rules;
- deduct realistic spread, slippage, tax, funding, borrow, gas, and impact;
- preserve path order when leverage or forced exits are possible;
- use walk-forward or locked out-of-sample evaluation;
- report the number of tested parameter sets and correct multiple comparisons;
- shrink small samples toward the relevant market/state base rate;
- run leave-best-year and leave-top-trades-out sensitivity;
- reject backtests whose expected move does not clear costs under adverse
  liquidity.

Evidence guidance:

| Effective event count | Numeric use |
| ---: | --- |
| `<20` | Insufficient; no numeric expected return |
| `20-49` | Low confidence; heavy shrinkage |
| `50-99` | Medium confidence; partial shrinkage |
| `100+` | Higher confidence only if out-of-sample and failures are included |

## 11. Execution and Cost Overlays

### Crypto

Separate spot, centralized derivatives, and on-chain execution. Include
maker/taker fees, spread, slippage, funding, liquidation, transfer, custody,
gas, failed transaction, and MEV costs. A low maker fee does not remove
adverse-selection risk. Treat fragmented venue volume as partial evidence.

### A-Shares

Include commissions, spread, impact, applicable tax, ETF expenses, T+1,
price-limit and suspension risk. Prefer liquid ETFs for broad or sector
exposure when the objective is to reduce single-stock exit and information
risk. A planned stop is not an executable exit when the position is locked at
the limit.

### U.S. Equities

Include spread, route/execution quality, ETF expenses, tax horizon, borrow and
options costs when present. Zero commission is not zero cost. Distinguish T+1
settlement from an A-share-style prohibition on same-day resale. Add overnight
and earnings-gap loss to the exit mixture.

## 12. Required Output

When this module is used, add:

```text
Market and horizon:
Data quality and material omissions:
Market-specific state:
State probabilities and label:
Selected behavior mode:
Why this mode fits the state:
Capital/time exposure:
Entry and sizing:
Exit rule and executable-exit risk:
Gross return prior:
All-in cost estimate:
Exit-failure and ruin mixture:
Net expected return range:
Expected net log growth:
Expected shortfall / drawdown / ruin probability:
Estimate label and calibration sample:
Rejected alternatives and constraint failures:
Switch / invalidation triggers:
```

Use ranges. If calibration is insufficient, replace the numeric-return fields
with `insufficient data` and identify the exact priors required.

## Evidence Basis

- A-share extrapolation and disposition in the 2014-2015 bubble:
  https://academic.oup.com/rfs/article/35/4/1682/6304879
- A-share price limits and destructive trading:
  https://www.nber.org/papers/w24014
- A-share leverage-induced fire sales:
  https://www.nber.org/papers/w25040
- Crypto DeFi leverage:
  https://www.bis.org/publ/work1171.pdf
- Crypto liquidation and market fragility:
  https://www.bis.org/publ/work1062.pdf
- U.S. retail turnover and net performance:
  https://faculty.haas.berkeley.edu/odean/papers/returns/individual_investor_performance_4-99.pdf
- Backtest versus out-of-sample performance:
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2745220
- Order and ETF implementation costs:
  https://www.investor.gov/introduction-investing/investing-basics/how-stock-markets-work/types-orders
  and
  https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24
