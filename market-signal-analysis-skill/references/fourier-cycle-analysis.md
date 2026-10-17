# Fourier Cycle Analysis

Use this reference when a request asks about Fourier transform, FFT, spectral analysis, frequency-domain signals, hidden cycles, dominant cycles, cycle stability, denoising, Fourier trend lines, high-frequency noise, frequency-domain correlation, or Fourier features for market models.

Fourier analysis is a rhythm and risk tool, not a standalone predictor. It should answer:

- Is the current move dominated by trend, swing-cycle, shock, or noise?
- Are recently observed cycles stable across rolling windows or only one-off artifacts?
- Does frequency-domain evidence confirm or weaken the existing macro/industry/technical cycle view?
- Should position size, trading frequency, or entry timing be adjusted because noise energy is rising?

Do not use a single FFT peak as a buy/sell signal. Markets are non-stationary; cycle length, amplitude, and phase drift as liquidity, policy, positioning, and industry fundamentals change.

## Conceptual Decomposition

Treat a liquid market series as:

```text
observed move = low-frequency trend + medium-frequency cycle + shock + high-frequency noise
```

Frequency-domain interpretation:

| Band | Market Meaning | Practical Use |
| --- | --- | --- |
| Low frequency | Main trend, slow liquidity or earnings cycle, long risk-appetite regime | Trend confirmation and regime filter. |
| Medium frequency | Swing cycle, sector rotation rhythm, inventory/order/rebalance rhythm | Pullback timing only when major trend agrees. |
| High frequency | Noise, event disturbance, liquidity fragmentation, short-term crowding | Position-size and trade-frequency control. |

## Data Preparation

Prefer stationary or detrended inputs:

- Log returns: `r_t = ln(P_t / P_{t-1})`.
- Detrended log price when the objective is a Fourier trend line.
- Volume growth/change rate, turnover, realized volatility, relative strength, ETF NAV returns, spread changes, or valuation/earnings-revision changes when relevant.

Avoid directly running FFT on raw price and then calling the lowest-frequency component a "cycle"; raw prices often embed trend, splits, inflation, regime shifts, and structural growth.

## HP and BK Pre-Filtering

Treat a filter as a declared preprocessing choice, not as evidence that a cycle exists. Select the target horizon and economic question before selecting the filter.

| Filter | Best Use | Required Disclosure | Main Failure Modes |
| --- | --- | --- | --- |
| Hodrick-Prescott (HP) | Separate a smooth low-frequency trend from a residual cycle, especially in monthly or quarterly macro series; optionally detrend log price before exploratory FFT. | Sampling frequency, smoothing parameter `lambda`, full-sample versus rolling/one-sided construction, and endpoint revision size. | Two-sided look-ahead, severe endpoint instability, arbitrary smoothness, spurious cycles, and amplitude/phase distortion. |
| Baxter-King (BK) | Extract a predeclared period band for ex-post business-, inventory-, sector-, or rotation-cycle research. | Lower and upper periods in observations, truncation length `K`, sample lost at both ends, and whether the band was chosen before inspecting results. | Symmetric and non-causal output, loss of `K` observations at each edge, poor live-end usability, leakage, and circular band selection. |

Selection rules:

1. Use log returns first when the question is short-horizon market rhythm or risk. They usually need less model-dependent detrending.
2. Use HP when the question requires a broad trend-cycle split. There is no universal `lambda` for daily market data; justify it from the sampling frequency and target horizon. `lambda = 1600` is a conventional quarterly macro anchor, not a default for every frequency.
3. Use BK when testing a known band such as a business or inventory cycle. Express cutoffs in observations and require several complete target cycles plus the observations lost to `K`.
4. Use HP and BK in parallel as robustness checks when both are material. Do not serially HP-filter and then BK-filter by default; repeated filtering can manufacture smoothness and distort phase or amplitude.
5. For a live turning-point decision, avoid a full-sample symmetric HP endpoint and the latest symmetric BK value. Prefer a rolling or expanding one-sided HP estimate, a causal/state-space alternative, or delay the signal until enough future observations exist.

### HP -> FFT Workflow

1. Define the horizon that the HP trend should remove.
2. Compute `cycle_t = transformed_series_t - hp_trend_t` using only data available at each historical decision date when backtesting.
3. Run rolling FFT on the cycle, not one full-sample residual.
4. Re-run across a small predeclared `lambda` grid and compare with log returns plus a simple linear or moving-average detrend.
5. Accept a dominant period only if its band, energy share, and phase interpretation remain materially stable. Treat a full-sample endpoint reversal that disappears in the one-sided estimate as look-ahead, not a signal.

### BK -> FFT Workflow

1. Set the lower period, upper period, and `K` from an economic or market-horizon prior before viewing the target spectrum.
2. Apply BK only when the sample contains enough complete cycles after losing `K` observations at each edge.
3. Use FFT on the BK component to verify energy concentration and rolling stability inside the predeclared band; do not use it to rediscover the band imposed by BK.
4. Compare the result with the unfiltered or independently detrended spectrum and adjacent placebo bands.
5. Do not issue a current-period timing signal from a symmetric BK endpoint. Label the output ex-post or use a causal approximation with explicit phase-delay analysis.

Avoid circular confirmation: if HP or BK mechanically creates the input passed to FFT, the filtered shape and its FFT are one evidence family. Agreement between them does not provide two independent votes.

Minimum practical windows:

| Horizon | Rolling Window | Typical Question |
| --- | ---: | --- |
| Short-term | 60-120 trading days | Is there a recent trading rhythm or noise surge? |
| Medium-term | 252 trading days | Is a 1-6 month sector/ETF cycle recurring? |
| Long-term | 504-756 trading days | Is a multi-year macro/industry rhythm visible enough to use as weak prior? |

Use rolling windows. Do not run one static multi-year FFT and infer a permanent 30-day or 43-day cycle.

## Rolling FFT Workflow

1. Choose the input series and horizon.
2. Clean missing data, corporate-action gaps, duplicate timestamps, and impossible values.
3. Transform into log returns or a declared detrended series. If using HP or BK, record all filter parameters, endpoint loss/revision, and whether the historical value is causal.
4. Demean the series. Apply a window such as Hann/Hanning to reduce spectral leakage.
5. Run FFT or real FFT.
6. Convert frequencies into periods: `period = 1 / frequency`.
7. Ignore `freq = 0`, periods shorter than practical trading costs allow, and periods longer than roughly half the window length.
8. Record dominant peaks by power share, not only by absolute maximum.
9. Roll the window forward and test whether the same period band repeatedly appears.
10. Compare the inferred phase with price/trend behavior, but treat phase as a probability rhythm, not a deterministic clock.

Stability rule:

- High reliability: the same period band appears in at least 3 consecutive or nearby windows, with similar phase behavior and no contradiction from trend/breadth/fundamentals.
- Medium reliability: the band appears in several windows but amplitude or phase drifts.
- Low reliability: the peak appears once, only after parameter searching, or disappears after a small window change.

## Fourier Trend Line

Use Fourier low-pass filtering as a trend extraction tool:

1. Take log price.
2. Run FFT on a rolling window.
3. Keep only the lowest-frequency components that represent the target horizon.
4. Inverse-transform back into the time domain.
5. Use the reconstructed line as a smoothed trend line.

Decision rules:

| State | Interpretation | Action Bias |
| --- | --- | --- |
| Price above Fourier trend line and line slope up | Trend is supported | Hold or small add if other evidence agrees. |
| Price above line but line slope flat | Trend momentum is cooling | Avoid chasing; wait for pullback or renewed slope. |
| Price below line and line slope down | Trend damage | Reduce exposure or require right-side repair. |
| Price far above or below line | Emotional overextension risk | Do not use distance alone; combine with breadth, valuation, volume, and support/resistance. |

Avoid full-sample leakage. A historical chart may use only data known up to each date when drawing the Fourier trend line for backtesting.

HP trend and Fourier low-pass trend are alternative smoothers of the same series. Their visual agreement is a robustness observation, not independent evidence; disagreement should trigger parameter and endpoint-sensitivity checks.

## Cycle Pullback Framework

Use medium-frequency cycles only as a timing overlay:

1. Identify a stable medium-frequency band, for example 30-40 trading days.
2. Extract the band using a rolling band-pass reconstruction.
3. Require the major trend to agree with the trade direction.
4. Consider staged entry when the cycle component turns up from a low zone and price/breadth stop deteriorating.
5. Consider staged reduction when the cycle component approaches a high zone and momentum/breadth weaken.

Rules:

- If trend and cycle conflict, trend dominates.
- If fundamentals or liquidity regime deteriorates, downgrade the cycle signal.
- If high-frequency noise energy is rising sharply, reduce position size even when the cycle looks favorable.

## Noise Energy and Risk Control

Compute frequency-band energy shares:

```text
low_energy_share = sum(power in low-frequency band) / total_power
mid_energy_share = sum(power in medium-frequency band) / total_power
high_energy_share = sum(power in high-frequency band) / total_power
```

Interpretation:

| Signal | Meaning | Risk Response |
| --- | --- | --- |
| Rising low-frequency energy with positive trend | Trend persistence improving | Increase patience; avoid premature exit. |
| Stable medium-frequency energy | Tradable rotation rhythm may exist | Use pullbacks only if trend agrees. |
| Rising high-frequency energy | Noise, event risk, or liquidity disturbance increasing | Lower leverage, reduce single-trade size, avoid overtrading. |
| All bands unstable | Structure is noisy or regime is shifting | Lower confidence and wait for clearer confirmation. |

Common high-frequency-noise catalysts: earnings clusters, policy meetings, CPI/PCE/NFP/FOMC, options expiration, index rebalancing, geopolitical shocks, liquidity squeezes, and rumor-driven markets.

## Frequency-Domain Correlation

Use frequency-domain or multi-horizon correlation to test diversification:

- Short-cycle correlation: do assets move together in daily/weekly risk-on/risk-off bursts?
- Medium-cycle correlation: do sectors rotate together over 1-3 month swings?
- Low-frequency correlation: do assets share the same dollar-liquidity, policy, inflation, or capex regime?
- Crisis resonance: do normally diversified assets become low-frequency synchronized when liquidity tightens?

Do not rely only on full-sample Pearson correlation. If two assets are low-frequency synchronized, they may fail as hedges during macro stress even if daily correlation looks modest.

## Macro Applications

Use FFT only when enough structured time series exist:

- Dollar liquidity: DXY, real yields, reserve balances, ON RRP, TGA, credit spreads, financial conditions, broad equity index returns.
- Inflation and growth rhythm: CPI/PCE components, ISM, PMI, payroll breadth, oil/commodity changes.
- Treasury and funding cycle: bill/coupon issuance, auction dates, term premium, SOFR-IORB spread, repo stress.
- Commodity and energy: inventory, seasonality, spreads, realized volatility, forward curves.

Macro use should be conservative:

- Long cycles are priors, not timing signals.
- Policy regime breaks can invalidate past cycle frequency.
- Compare FFT evidence with official-data verification, liquidity plumbing, actor optimal paths, and special-date event risk.

## Micro and Sector Applications

For stocks, ETFs, sectors, and themes, use Fourier analysis on:

- Relative strength versus benchmark.
- Turnover or volume change.
- Realized volatility and intraday range.
- Breadth such as constituents above MA20/MA50/MA120.
- Earnings-revision or order/backlog proxies when available.

Best-fit use cases:

- Sector ETF rotation rhythm.
- High-beta theme overextension and pullback timing.
- Noise detection before or after major announcements.
- Portfolio co-movement across crowded themes.

Weak use cases:

- Illiquid small caps with discontinuous trading.
- Newly listed stocks with too few bars.
- Price-limit dominated data where true volatility is censored.
- Series with major structural breaks, suspensions, or policy resets.

## Integration With Multi-Cycle Bayesian Overlay

Fourier evidence can adjust the reliability of the sector market cycle or liquidity cycle layer; it should rarely create a new thesis by itself.

Suggested adjustments:

| Fourier Evidence | Bayesian Treatment |
| --- | --- |
| Stable low-frequency trend agrees with macro/industry/technical evidence | Increase relevant cycle-layer reliability by `+0.05` to `+0.15`, capped at `1.0`. |
| Stable medium-frequency pullback rhythm agrees with trend and breadth | Add `+0.05` to `+0.15` logit for timing confidence, not fundamental upside. |
| High-frequency noise share surges | Subtract `0.05` to `0.25` logit from position confidence or reduce suggested position size. |
| FFT peak appears once or requires parameter search | No positive adjustment; mention as low-quality observation only. |
| Frequency-domain correlation shows hedge failure | Increase downside/tail vulnerability and reduce diversification confidence. |

Do not double-count:

- If the same price trend already contributed to technical momentum, FFT trend confirmation should adjust reliability, not add a separate large bullish score.
- If high-frequency noise comes from a known special date, report it through both lenses but count the risk once.

## Fourier Features for Quant Models

For machine-learning or statistical models, use periodic features when the calendar rhythm is known:

```text
sin(2*pi*t/T), cos(2*pi*t/T)
```

Possible `T` values:

- Weekday effect.
- Month-end or quarter-end.
- Earnings season.
- Intraday time bucket.
- Macro release cadence.
- Options expiration or futures delivery cycle.

Fourier features are safer when they encode known calendar periodicity than when they are mined from noisy prices without validation.

## Validation and Caveats

Require:

- Rolling-window stability.
- Sample-out or forward-window validation when enough history exists.
- Comparison with a simple moving-average or momentum baseline.
- Transaction-cost and turnover check.
- No future-data leakage in filtered trend lines.
- HP endpoint-revision and `lambda` sensitivity checks when HP is used.
- BK cutoff, `K`, edge-loss, and adjacent-band placebo checks when BK is used.
- A causal or rolling reconstruction for any claimed real-time signal.
- No parameter fishing across many window lengths without penalty.

Downgrade confidence when:

- The market regime changed materially.
- Liquidity or policy broke the historical rhythm.
- The signal disappears after a small window change.
- The series has censored volatility, suspensions, or frequent limit-up/limit-down days.
- The FFT conclusion conflicts with strong fundamentals, breadth, or liquidity evidence.

## Output Add-On

When Fourier analysis materially affects the answer, add:

1. Input series, date range, frequency, and window length.
2. Data transform and filter used: returns, detrended log price, volatility, volume change, relative strength, or breadth; for HP report `lambda` and endpoint method, and for BK report the period band, `K`, and observations lost.
3. Dominant period bands and rolling stability.
4. Energy split: low, medium, high frequency.
5. Fourier trend-line state when used.
6. How the FFT evidence changes the existing cycle/Bayesian view.
7. Invalidation: what signal disappearance, trend break, liquidity change, or data contradiction would reduce confidence.
