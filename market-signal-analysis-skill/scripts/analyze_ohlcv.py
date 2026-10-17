#!/usr/bin/env python3
"""Analyze OHLCV CSV data and emit technical signal probabilities as JSON."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


FAMILY_WEIGHTS = {
    "trend_breakout_ma": 0.24,
    "momentum_relative_strength": 0.18,
    "volume_confirmation": 0.14,
    "macd_combo": 0.11,
    "rsi_kdj_oscillator": 0.10,
    "divergence": 0.11,
    "volatility_regime": 0.07,
    "multi_timeframe_agreement": 0.05,
}

TIMEFRAME_WEIGHTS = {
    "short": {"hourly": 0.45, "daily": 0.35, "weekly": 0.15, "monthly": 0.05},
    "mid": {"hourly": 0.10, "daily": 0.45, "weekly": 0.35, "monthly": 0.10},
    "long": {"hourly": 0.00, "daily": 0.20, "weekly": 0.45, "monthly": 0.35},
}


@dataclass
class Bar:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


IMPORTANCE_SCORES = {"high": 1.0, "medium": 0.65, "low": 0.35}


def parse_float(value: str) -> float:
    if value is None or str(value).strip() == "":
        return float("nan")
    return float(str(value).replace(",", "").strip())


def parse_date(value: str) -> Optional[date]:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    raw = raw.replace("/", "-")
    candidates = [raw[:10], raw]
    for candidate in candidates:
        try:
            return date.fromisoformat(candidate)
        except ValueError:
            pass
    for fmt in ("%Y%m%d", "%m-%d-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            pass
    return None


def normalize_columns(fieldnames: Iterable[str]) -> Dict[str, str]:
    aliases = {
        "timestamp": ("timestamp", "date", "datetime", "time"),
        "open": ("open", "o"),
        "high": ("high", "h"),
        "low": ("low", "l"),
        "close": ("close", "c"),
        "volume": ("volume", "vol", "v"),
    }
    normalized = {name.lower().strip(): name for name in fieldnames}
    result = {}
    for target, names in aliases.items():
        for name in names:
            if name in normalized:
                result[target] = normalized[name]
                break
    missing = [key for key in aliases if key not in result]
    if missing:
        if 'close' in missing and {'adj_close', 'adjusted_close'} & normalized.keys():
            raise ValueError('Adjusted close alone cannot be mixed with raw OHLC; provide consistently adjusted open/high/low/close columns.')
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return result


def score_signal_families(signals: List[dict]) -> Dict[str, dict]:
    families: Dict[str, dict] = {}
    for signal in signals:
        direction = signal['direction']
        if direction not in {'bullish', 'bearish'}:
            continue
        scores = families.setdefault(signal['family'], {'bullish': 0.0, 'bearish': 0.0})
        scores[direction] = max(scores[direction], min(1.0, max(0.0, signal['strength'])))
    for family, scores in families.items():
        scale = FAMILY_WEIGHTS[family] / max(1.0, sum(scores.values()))
        for direction in scores:
            scores[direction] *= scale
    return families


def load_bars(path: str) -> List[Bar]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        cols = normalize_columns(reader.fieldnames)
        bars = []
        for row in reader:
            bar = Bar(
                timestamp=str(row[cols["timestamp"]]),
                open=parse_float(row[cols["open"]]),
                high=parse_float(row[cols["high"]]),
                low=parse_float(row[cols["low"]]),
                close=parse_float(row[cols["close"]]),
                volume=parse_float(row[cols["volume"]]),
            )
            if any(math.isnan(x) for x in [bar.open, bar.high, bar.low, bar.close, bar.volume]):
                continue
            bars.append(bar)
    bars.sort(key=lambda item: item.timestamp)
    return bars


def third_friday(year: int, month: int) -> date:
    current = date(year, month, 1)
    while current.weekday() != 4:
        current += timedelta(days=1)
    return current + timedelta(days=14)


def standard_us_options_events(as_of: date, window_days: int) -> List[dict]:
    events = []
    months = []
    for offset in range(-1, 3):
        month = as_of.month + offset
        year = as_of.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        months.append((year, month))
    for year, month in months:
        expiry = third_friday(year, month)
        distance = (expiry - as_of).days
        if abs(distance) > window_days:
            continue
        quarterly = month in {3, 6, 9, 12}
        events.append({
            "date": expiry.isoformat(),
            "event_type": "quarterly_triple_witching" if quarterly else "us_monthly_options_expiration",
            "importance": "high" if quarterly else "medium",
            "asset_scope": "us_equity,index_etf,index_futures",
            "description": (
                "Quarterly index futures/options and equity options expiration; watch gamma reset, "
                "settlement liquidity, and false breakout risk."
                if quarterly
                else "Standard U.S. monthly equity/index options expiration; watch gamma pinning, "
                "volatility crush, and post-expiry positioning reset."
            ),
            "days_from_as_of": distance,
            "source": "computed_standard_calendar",
        })
    return events


def normalize_event_columns(fieldnames: Iterable[str]) -> Dict[str, str]:
    aliases = {
        "date": {"date", "event_date", "timestamp", "time"},
        "event_type": {"event_type", "type", "name", "event", "title"},
        "importance": {"importance", "impact", "level", "priority"},
        "description": {"description", "details", "note", "notes", "summary"},
        "asset_scope": {"asset_scope", "scope", "asset", "assets", "market"},
    }
    normalized = {name.lower().strip(): name for name in fieldnames}
    result = {}
    for target, names in aliases.items():
        for name in names:
            if name in normalized:
                result[target] = normalized[name]
                break
    if "date" not in result:
        raise ValueError("Event calendar is missing a date/event_date column")
    return result


def normalize_importance(value: str) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"high", "h", "3", "重要", "高"}:
        return "high"
    if raw in {"low", "l", "1", "低"}:
        return "low"
    return "medium"


def load_event_calendar(path: str, as_of: date, window_days: int) -> List[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("Event calendar CSV has no header row")
        cols = normalize_event_columns(reader.fieldnames)
        events = []
        for row in reader:
            event_date = parse_date(row.get(cols["date"], ""))
            if event_date is None:
                continue
            distance = (event_date - as_of).days
            if abs(distance) > window_days:
                continue
            event_type = row.get(cols.get("event_type", ""), "scheduled_event") or "scheduled_event"
            importance = normalize_importance(row.get(cols.get("importance", ""), "medium"))
            events.append({
                "date": event_date.isoformat(),
                "event_type": event_type,
                "importance": importance,
                "asset_scope": row.get(cols.get("asset_scope", ""), ""),
                "description": row.get(cols.get("description", ""), ""),
                "days_from_as_of": distance,
                "source": "input_calendar",
            })
    return events


def build_special_date_alerts(market: str, as_of: Optional[date], window_days: int, calendar_events: Optional[List[dict]]) -> Tuple[List[dict], Optional[float], Optional[str]]:
    if as_of is None:
        return [], None, None

    events = list(calendar_events or [])
    if market in {"us_equity", "us_index", "us_etf"} or "us" in market.lower():
        events.extend(standard_us_options_events(as_of, window_days))

    alerts = []
    max_score = 0.0
    for event in events:
        importance = normalize_importance(event.get("importance", "medium"))
        proximity = max(0.0, 1 - abs(float(event["days_from_as_of"])) / (window_days + 1))
        score = 100 * (0.55 * proximity + 0.45 * IMPORTANCE_SCORES[importance])
        max_score = max(max_score, score)
        alerts.append({
            "date": event["date"],
            "event_type": event.get("event_type", "scheduled_event"),
            "importance": importance,
            "days_from_as_of": event["days_from_as_of"],
            "asset_scope": event.get("asset_scope", ""),
            "description": event.get("description", ""),
            "source": event.get("source", "calendar"),
            "risk_score": round(score, 1),
            "analysis_effect": (
                "Calendar event can distort short-term price, volatility, liquidity, or technical confirmation; "
                "require post-event confirmation before upgrading directional confidence."
            ),
        })

    if not alerts:
        return [], 0.0, "none"
    if max_score >= 75:
        level = "severe"
    elif max_score >= 50:
        level = "high"
    elif max_score >= 25:
        level = "medium"
    else:
        level = "low"
    alerts.sort(key=lambda item: (-item["risk_score"], abs(item["days_from_as_of"]), item["date"]))
    return alerts, round(max_score, 1), level


def sma(values: List[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    if period <= 0:
        return out
    total = 0.0
    for index, value in enumerate(values):
        total += value
        if index >= period:
            total -= values[index - period]
        if index >= period - 1:
            out[index] = total / period
    return out


def ema(values: List[float], period: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    if not values or period <= 0:
        return out
    alpha = 2 / (period + 1)
    current = values[0]
    for index, value in enumerate(values):
        current = value if index == 0 else alpha * value + (1 - alpha) * current
        if index >= period - 1:
            out[index] = current
    return out


def rsi(values: List[float], period: int = 14) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(values)
    gains: List[float] = []
    losses: List[float] = []
    for index in range(1, len(values)):
        delta = values[index] - values[index - 1]
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))
        if index >= period:
            avg_gain = sum(gains[index - period:index]) / period
            avg_loss = sum(losses[index - period:index]) / period
            out[index] = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
    return out


def macd(values: List[float]) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    ema12 = ema(values, 12)
    ema26 = ema(values, 26)
    line: List[Optional[float]] = [None] * len(values)
    compact = []
    compact_indexes = []
    for index, (fast, slow) in enumerate(zip(ema12, ema26)):
        if fast is not None and slow is not None:
            value = fast - slow
            line[index] = value
            compact.append(value)
            compact_indexes.append(index)
    compact_signal = ema(compact, 9)
    signal: List[Optional[float]] = [None] * len(values)
    for source_index, value in zip(compact_indexes, compact_signal):
        signal[source_index] = value
    hist = [
        None if line_value is None or signal_value is None else line_value - signal_value
        for line_value, signal_value in zip(line, signal)
    ]
    return line, signal, hist


def stochastic_kdj(bars: List[Bar], period: int = 9) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    k: List[Optional[float]] = [None] * len(bars)
    d: List[Optional[float]] = [None] * len(bars)
    j: List[Optional[float]] = [None] * len(bars)
    current_k = 50.0
    current_d = 50.0
    for index in range(len(bars)):
        if index < period - 1:
            continue
        window = bars[index - period + 1:index + 1]
        low = min(bar.low for bar in window)
        high = max(bar.high for bar in window)
        rsv = 50.0 if high == low else (bars[index].close - low) / (high - low) * 100
        current_k = 2 / 3 * current_k + 1 / 3 * rsv
        current_d = 2 / 3 * current_d + 1 / 3 * current_k
        k[index] = current_k
        d[index] = current_d
        j[index] = 3 * current_k - 2 * current_d
    return k, d, j


def atr(bars: List[Bar], period: int = 14) -> List[Optional[float]]:
    true_ranges = []
    for index, bar in enumerate(bars):
        if index == 0:
            true_ranges.append(bar.high - bar.low)
        else:
            prev_close = bars[index - 1].close
            true_ranges.append(max(bar.high - bar.low, abs(bar.high - prev_close), abs(bar.low - prev_close)))
    return sma(true_ranges, period)


def latest(values: List[Optional[float]]) -> Optional[float]:
    for value in reversed(values):
        if value is not None:
            return value
    return None


def crossed_up(a: List[Optional[float]], b: List[Optional[float]]) -> bool:
    if len(a) < 2 or len(b) < 2:
        return False
    return None not in (a[-1], a[-2], b[-1], b[-2]) and a[-2] <= b[-2] and a[-1] > b[-1]


def crossed_down(a: List[Optional[float]], b: List[Optional[float]]) -> bool:
    if len(a) < 2 or len(b) < 2:
        return False
    return None not in (a[-1], a[-2], b[-1], b[-2]) and a[-2] >= b[-2] and a[-1] < b[-1]


def swing_points(values: List[float], lookback: int = 80) -> Tuple[List[int], List[int]]:
    start = max(2, len(values) - lookback)
    highs = []
    lows = []
    for index in range(start, len(values) - 2):
        window = values[index - 2:index + 3]
        if values[index] == max(window):
            highs.append(index)
        if values[index] == min(window):
            lows.append(index)
    return highs, lows


def detect_divergence(closes: List[float], indicator: List[Optional[float]]) -> Tuple[bool, bool]:
    highs, lows = swing_points(closes)
    clean_indicator = [float("nan") if value is None else value for value in indicator]
    bearish = False
    bullish = False
    if len(highs) >= 2:
        first, second = highs[-2], highs[-1]
        bearish = closes[second] > closes[first] and clean_indicator[second] < clean_indicator[first]
    if len(lows) >= 2:
        first, second = lows[-2], lows[-1]
        bullish = closes[second] < closes[first] and clean_indicator[second] > clean_indicator[first]
    return bullish, bearish


def add_signal(signals: List[dict], family: str, signal: str, direction: str, strength: float, evidence: str) -> None:
    signals.append({
        "family": family,
        "signal": signal,
        "direction": direction,
        "strength": round(max(0.0, min(1.0, strength)), 3),
        "evidence": evidence,
    })


def analyze(
    bars: List[Bar],
    horizon: str,
    market: str,
    calendar_events: Optional[List[dict]] = None,
    as_of: Optional[date] = None,
    event_window_days: int = 5,
) -> dict:
    warnings = []
    if len(bars) < 60:
        warnings.append("Fewer than 60 bars; probability confidence is low.")
    if any(bar.high < max(bar.open, bar.close) or bar.low > min(bar.open, bar.close) for bar in bars):
        warnings.append("Some OHLC rows are internally inconsistent.")

    latest_bar_date = parse_date(bars[-1].timestamp) if bars else None
    analysis_date = as_of or latest_bar_date
    special_alerts, calendar_risk_score, calendar_warning_level = build_special_date_alerts(
        market, analysis_date, event_window_days, calendar_events
    )
    if calendar_warning_level in {"high", "severe"}:
        warnings.append(
            "High special-date event risk near the analysis date; lower short-term confidence and require post-event confirmation."
        )

    closes = [bar.close for bar in bars]
    volumes = [bar.volume for bar in bars]
    ma20 = sma(closes, 20)
    ma50 = sma(closes, 50)
    ma200 = sma(closes, 200)
    vol20 = sma(volumes, 20)
    rsi14 = rsi(closes)
    macd_line, macd_signal, macd_hist = macd(closes)
    k, d, j = stochastic_kdj(bars)
    atr14 = atr(bars)
    signals: List[dict] = []

    close = closes[-1]
    prev_close = closes[-2] if len(closes) > 1 else close
    current_ma20 = latest(ma20)
    current_ma50 = latest(ma50)
    current_ma200 = latest(ma200)
    current_vol20 = latest(vol20)
    current_rsi = latest(rsi14)
    current_k = latest(k)
    current_d = latest(d)
    current_atr = latest(atr14)
    current_macd = latest(macd_line)
    current_macd_signal = latest(macd_signal)
    current_hist = latest(macd_hist)

    current_bar = bars[-1]
    prev_bar = bars[-2] if len(bars) > 1 else bars[-1]
    support_tolerance = 0.03
    if current_atr is not None and close:
        support_tolerance = max(0.025, min(0.08, 1.5 * current_atr / close))

    if len(bars) > 1:
        prev_ma20 = ma20[-2] if len(ma20) > 1 else None
        prev_ma50 = ma50[-2] if len(ma50) > 1 else None
        downtrend_reasons = []
        if prev_ma20 is not None and prev_close < prev_ma20:
            downtrend_reasons.append("previous close below MA20")
        if prev_ma20 is not None and prev_ma50 is not None and prev_ma20 < prev_ma50:
            downtrend_reasons.append("MA20 below MA50")
        if len(closes) > 22 and prev_close < closes[-22] * 0.95:
            downtrend_reasons.append("20-bar decline exceeds 5%")
        if len(closes) > 64 and prev_close < closes[-64] * 0.90:
            downtrend_reasons.append("63-bar decline exceeds 10%")
        downtrend_context = bool(downtrend_reasons)

        prev_body_high = max(prev_bar.open, prev_bar.close)
        prev_body_low = min(prev_bar.open, prev_bar.close)
        current_body_low = min(current_bar.open, current_bar.close)
        body_buffer = max(0.003 * prev_body_high, 0.05 * (current_atr or 0.0))
        prior_weak = prev_bar.close < prev_bar.open or (len(closes) > 2 and prev_bar.close < closes[-3])
        bullish_engulfing = (
            current_bar.close > current_bar.open
            and prior_weak
            and current_bar.close > prev_body_high + body_buffer
            and current_body_low <= prev_body_low + body_buffer
        )

        vol_vs_prev = current_bar.volume / prev_bar.volume if prev_bar.volume > 0 else None
        vol_vs_20 = current_bar.volume / current_vol20 if current_vol20 else None
        effective_volume_expansion = (
            vol_vs_prev is not None
            and vol_vs_prev >= 1.3
            and (vol_vs_20 is None or vol_vs_20 >= 1.0)
        )

        support_refs: List[Tuple[str, float]] = []
        for name, value in [("MA20", current_ma20), ("MA50", current_ma50), ("MA200", current_ma200)]:
            if value is not None:
                support_refs.append((name, value))
        if len(bars) > 21:
            support_refs.append(("20-bar low", min(bar.low for bar in bars[-21:-1])))
        if len(bars) > 56:
            support_refs.append(("55-bar low", min(bar.low for bar in bars[-56:-1])))
        if len(bars) > 30 and current_vol20:
            high_volume_closes = [bar.close for bar in bars[-61:-1] if bar.volume >= current_vol20 * 1.3]
            if high_volume_closes:
                support_refs.append(("high-volume shelf", sum(high_volume_closes) / len(high_volume_closes)))

        nearby_supports = []
        for name, level in support_refs:
            if level <= 0:
                continue
            if (
                current_bar.low <= level <= current_bar.close
                or abs(current_bar.low - level) / level <= support_tolerance
                or abs(current_bar.close - level) / level <= support_tolerance
            ):
                nearby_supports.append(name)
        near_support = bool(nearby_supports)

        bottom_condition_count = sum([bullish_engulfing, effective_volume_expansion, near_support])
        if downtrend_context and bullish_engulfing and bottom_condition_count >= 2:
            candle_range = max(current_bar.high - current_bar.low, 0.0)
            close_location = 0.5 if candle_range == 0 else (current_bar.close - current_bar.low) / candle_range
            body_gain = current_bar.close / prev_body_high - 1 if prev_body_high else 0.0
            volume_bonus = min(0.15, max(0.0, (vol_vs_prev or 1.0) - 1.3) / 2)
            body_bonus = min(0.10, max(0.0, body_gain) / 0.08)
            close_bonus = 0.05 if close_location >= 0.7 else 0.0
            strength = 0.50 + 0.10 * (bottom_condition_count - 2) + volume_bonus + body_bonus + close_bonus
            signal_name = (
                "bottom_bullish_engulfing_reversal"
                if bottom_condition_count == 3
                else "bottom_bullish_engulfing_watch"
            )
            support_text = ",".join(nearby_supports) if nearby_supports else "not confirmed"
            volume_text = f"{vol_vs_prev:.2f}x previous day" if vol_vs_prev is not None else "unavailable vs previous day"
            add_signal(
                signals,
                "trend_breakout_ma",
                signal_name,
                "bullish",
                strength,
                (
                    f"Downtrend context ({'; '.join(downtrend_reasons)}); {bottom_condition_count}/3 "
                    f"bottom checks matched: bullish engulfing body, volume {volume_text}, "
                    f"support near {support_text}."
                ),
            )

    if len(bars) >= 25:
        for ma_name, ma_values, base_strength in [("MA20", ma20, 0.52), ("MA50", ma50, 0.62)]:
            current_ma = ma_values[-1]
            if current_ma is None or close <= current_ma:
                continue
            lookback = min(6, len(bars))
            start_index = len(bars) - lookback
            tested_without_break = False
            material_break = False
            for index in range(start_index, len(bars) - 1):
                ma_value = ma_values[index]
                if ma_value is None:
                    continue
                test_band = max(0.012, support_tolerance / 2)
                if bars[index].low <= ma_value * (1 + support_tolerance) and bars[index].close >= ma_value * (1 - test_band):
                    tested_without_break = True
                if bars[index].close < ma_value * (1 - test_band):
                    material_break = True
            if not tested_without_break or material_break:
                continue
            recent_volume = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else volumes[-1]
            prior_volume = sum(volumes[-25:-5]) / 20 if len(volumes) >= 25 else (current_vol20 or recent_volume)
            healthy_volume = prior_volume > 0 and recent_volume >= prior_volume * 1.05 and current_bar.volume >= prev_bar.volume * 0.8
            if healthy_volume:
                add_signal(
                    signals,
                    "trend_breakout_ma",
                    "key_ma_reclaim_retest_reversal",
                    "bullish",
                    base_strength,
                    (
                        f"Price reclaimed {ma_name}, retested without an effective close below it, "
                        f"and recent volume is {recent_volume / prior_volume:.2f}x the prior baseline."
                    ),
                )

    if current_ma20 and current_ma50:
        if close > current_ma20 > current_ma50:
            add_signal(signals, "trend_breakout_ma", "bullish_ma_regime", "bullish", 0.65, "Close is above MA20 and MA20 is above MA50.")
        elif close < current_ma20 < current_ma50:
            add_signal(signals, "trend_breakout_ma", "bearish_ma_regime", "bearish", 0.65, "Close is below MA20 and MA20 is below MA50.")
    if current_ma200:
        if close > current_ma200:
            add_signal(signals, "trend_breakout_ma", "above_ma200", "bullish", 0.35, "Close is above MA200.")
        else:
            add_signal(signals, "trend_breakout_ma", "below_ma200", "bearish", 0.35, "Close is below MA200.")

    if len(closes) > 21:
        prior_high = max(closes[-21:-1])
        prior_low = min(closes[-21:-1])
        rel_vol = volumes[-1] / current_vol20 if current_vol20 else 1.0
        if close > prior_high:
            strength = 0.65 + min(0.25, max(0.0, rel_vol - 1.0) / 2)
            add_signal(signals, "trend_breakout_ma", "twenty_bar_breakout", "bullish", strength, f"Close broke prior 20-bar high; relative volume {rel_vol:.2f}.")
        elif close < prior_low:
            strength = 0.65 + min(0.25, max(0.0, rel_vol - 1.0) / 2)
            add_signal(signals, "trend_breakout_ma", "twenty_bar_breakdown", "bearish", strength, f"Close broke prior 20-bar low; relative volume {rel_vol:.2f}.")
        if rel_vol > 1.3 and close > prev_close:
            add_signal(signals, "volume_confirmation", "bullish_volume_expansion", "bullish", min(1.0, rel_vol / 2.5), f"Up bar volume is {rel_vol:.2f}x the 20-bar average.")
        elif rel_vol > 1.3 and close < prev_close:
            add_signal(signals, "volume_confirmation", "bearish_volume_expansion", "bearish", min(1.0, rel_vol / 2.5), f"Down bar volume is {rel_vol:.2f}x the 20-bar average.")

    if len(closes) > 63:
        ret63 = close / closes[-64] - 1
        if ret63 > 0.08 and close > (current_ma50 or close):
            add_signal(signals, "momentum_relative_strength", "positive_3m_momentum", "bullish", min(1.0, abs(ret63) * 3), f"Approximate 3-month momentum is {ret63:.1%}.")
        elif ret63 < -0.08 and close < (current_ma50 or close):
            add_signal(signals, "momentum_relative_strength", "negative_3m_momentum", "bearish", min(1.0, abs(ret63) * 3), f"Approximate 3-month momentum is {ret63:.1%}.")

    if crossed_up(macd_line, macd_signal):
        add_signal(signals, "macd_combo", "bullish_macd_cross", "bullish", 0.65, "MACD crossed above signal line.")
    elif crossed_down(macd_line, macd_signal):
        add_signal(signals, "macd_combo", "bearish_macd_cross", "bearish", 0.65, "MACD crossed below signal line.")
    if current_macd is not None and current_macd_signal is not None and current_hist is not None:
        if current_macd > 0 and current_hist > 0:
            add_signal(signals, "macd_combo", "bullish_macd_regime", "bullish", 0.45, "MACD is above zero with positive histogram.")
        elif current_macd < 0 and current_hist < 0:
            add_signal(signals, "macd_combo", "bearish_macd_regime", "bearish", 0.45, "MACD is below zero with negative histogram.")

    if current_rsi is not None:
        if current_rsi < 30:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_oversold", "bullish", 0.45, f"RSI is oversold at {current_rsi:.1f}.")
        elif current_rsi > 70:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_overbought", "bearish", 0.45, f"RSI is overbought at {current_rsi:.1f}.")
        elif current_rsi > 55:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_bullish_regime", "bullish", 0.35, f"RSI is in bullish regime at {current_rsi:.1f}.")
        elif current_rsi < 45:
            add_signal(signals, "rsi_kdj_oscillator", "rsi_bearish_regime", "bearish", 0.35, f"RSI is in bearish regime at {current_rsi:.1f}.")

    if current_k is not None and current_d is not None:
        if crossed_up(k, d):
            add_signal(signals, "rsi_kdj_oscillator", "bullish_kdj_cross", "bullish", 0.45 if current_k < 50 else 0.30, "K crossed above D.")
        elif crossed_down(k, d):
            add_signal(signals, "rsi_kdj_oscillator", "bearish_kdj_cross", "bearish", 0.45 if current_k > 50 else 0.30, "K crossed below D.")

    bullish_div_rsi, bearish_div_rsi = detect_divergence(closes, rsi14)
    bullish_div_macd, bearish_div_macd = detect_divergence(closes, macd_hist)
    if bullish_div_rsi or bullish_div_macd:
        add_signal(signals, "divergence", "bottom_divergence", "bullish", 0.60, "Price made a lower low while RSI or MACD made a higher low.")
    if bearish_div_rsi or bearish_div_macd:
        add_signal(signals, "divergence", "top_divergence", "bearish", 0.60, "Price made a higher high while RSI or MACD made a lower high.")

    if current_atr is not None and close:
        atr_pct = current_atr / close
        if atr_pct > 0.05:
            add_signal(signals, "volatility_regime", "high_volatility_risk", "bearish", 0.35, f"ATR is elevated at {atr_pct:.1%} of price.")
        elif atr_pct < 0.02:
            add_signal(signals, "volatility_regime", "low_volatility_constructive", "bullish", 0.20, f"ATR is contained at {atr_pct:.1%} of price.")

    family_scores = score_signal_families(signals)
    bullish = sum(scores['bullish'] for scores in family_scores.values())
    bearish = sum(scores['bearish'] for scores in family_scores.values())

    net = bullish - bearish
    buy_raw = 1 / (1 + math.exp(-2.6 * net))
    sell_raw = 1 / (1 + math.exp(2.6 * net))
    confidence_scale = 0.65 if len(bars) >= 200 else 0.45
    hold_raw = max(0.05, 1 - abs(buy_raw - sell_raw) * confidence_scale)
    total = buy_raw + sell_raw + hold_raw
    probabilities = {
        "buy": round(100 * buy_raw / total, 1),
        "sell": round(100 * sell_raw / total, 1),
        "hold": round(100 * hold_raw / total, 1),
    }
    probability_basis = "model_implied_probability"
    warnings.append('Model-implied probability from heuristic scores; not calibrated empirical frequencies.')

    confidence = "medium" if len(bars) >= 200 else "low"
    if len(bars) < 60:
        confidence = "insufficient"
        probability_basis = "insufficient_data"
        probabilities = {"buy": None, "sell": None, "hold": None}

    return {
        "market": market,
        "horizon": horizon,
        "bars": len(bars),
        "latest_timestamp": bars[-1].timestamp if bars else None,
        "indicator_snapshot": {
            "close": close,
            "ma20": current_ma20,
            "ma50": current_ma50,
            "ma200": current_ma200,
            "rsi14": current_rsi,
            "macd": current_macd,
            "macd_signal": current_macd_signal,
            "macd_histogram": current_hist,
            "kdj_k": current_k,
            "kdj_d": current_d,
            "kdj_j": latest(j),
            "atr14": current_atr,
        },
        "score_components": {"bullish": round(bullish, 4), "bearish": round(bearish, 4), "net": round(net, 4)},
        "family_score_components": family_scores,
        "special_date_risk_score": calendar_risk_score,
        "special_date_warning_level": calendar_warning_level,
        "special_date_alerts": special_alerts,
        "probabilities": probabilities,
        "probability_basis": probability_basis,
        "confidence": confidence,
        "matched_signals": signals,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze OHLCV technical signals.")
    parser.add_argument("--input", required=True, help="Path to OHLCV CSV file.")
    parser.add_argument("--market", default="us_equity", help="Market profile name.")
    parser.add_argument("--horizon", choices=["short", "mid", "long"], default="mid")
    parser.add_argument("--calendar", help="Optional event calendar CSV with date,event_type,importance,description,asset_scope.")
    parser.add_argument("--as-of", help="Analysis date in YYYY-MM-DD format. Defaults to the latest bar timestamp.")
    parser.add_argument("--event-window-days", type=int, default=5, help="Calendar warning window around the analysis date.")
    args = parser.parse_args()

    bars = load_bars(args.input)
    if not bars:
        raise SystemExit("No valid bars found in CSV.")
    as_of = parse_date(args.as_of) if args.as_of else None
    if args.as_of and as_of is None:
        raise SystemExit("--as-of must be parseable as a date, preferably YYYY-MM-DD.")
    event_base_date = as_of or parse_date(bars[-1].timestamp)
    calendar_events = load_event_calendar(args.calendar, event_base_date, args.event_window_days) if args.calendar and event_base_date else None
    print(json.dumps(analyze(bars, args.horizon, args.market, calendar_events, as_of, args.event_window_days), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
