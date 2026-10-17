#!/usr/bin/env python3
"""Analyze A/H-share ETF shares, crowding, unwind risk, and scenario weights.

Input is a daily long-form CSV. Required columns:
date,symbol,group,scope,close,nav,shares,turnover

Optional columns:
breadth_ma20,breadth_ma50,top10_weight,free_float_mcap,
valuation_percentile,fundamental_signal,policy_signal,
derivatives_signal,cross_market_signal

Hong Kong optional columns:
fund_id,fund_structure,counter_currency,premium_discount,spread_bps,
nav_stale,southbound_holding,southbound_net_buy

Ratios may be supplied as decimals or percentages. Money fields must use a
consistent currency unit. Results are heuristic model-implied scenario weights,
not calibrated empirical probabilities.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REQUIRED = {"date", "symbol", "group", "scope", "close", "nav", "shares", "turnover"}
OPTIONAL_RATIO_FIELDS = {
    "breadth_ma20",
    "breadth_ma50",
    "top10_weight",
    "valuation_percentile",
}
SIGNAL_FIELDS = {
    "fundamental_signal",
    "policy_signal",
    "derivatives_signal",
    "cross_market_signal",
}
SIGNED_RATIO_FIELDS = {"premium_discount"}
HK_NUMBER_FIELDS = {"spread_bps", "southbound_holding", "southbound_net_buy"}

BROAD_PRIORS = {
    "neutral": (0.34, 0.38, 0.28),
    "policy_floor": (0.45, 0.40, 0.15),
    "range_extraction": (0.25, 0.50, 0.25),
    "crowded_distribution": (0.20, 0.35, 0.45),
    "broad_breakdown": (0.10, 0.25, 0.65),
    "washout": (0.35, 0.50, 0.15),
}

SECTOR_PRIORS = {
    "neutral": (0.35, 0.40, 0.25),
    "acceleration": (0.55, 0.30, 0.15),
    "healthy_pullback": (0.40, 0.45, 0.15),
    "distribution": (0.25, 0.35, 0.40),
    "unwind": (0.15, 0.30, 0.55),
    "washout": (0.25, 0.50, 0.25),
}

HK_PRIORS = {
    "neutral": (0.32, 0.40, 0.28),
    "southbound_support": (0.40, 0.42, 0.18),
    "southbound_offset": (0.25, 0.48, 0.27),
    "cross_border_distribution": (0.18, 0.37, 0.45),
    "broad_breakdown": (0.10, 0.25, 0.65),
    "washout": (0.30, 0.50, 0.20),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--market", choices=("a_share", "hk"), default="a_share")
    parser.add_argument("--scope", choices=("broad", "sector"), required=True)
    parser.add_argument("--group", help="Analyze one group; omit for every group in scope")
    parser.add_argument("--regime", default="neutral", help="Regime key used for the prior")
    parser.add_argument("--prior-up", type=float)
    parser.add_argument("--prior-range", type=float)
    parser.add_argument("--prior-down", type=float)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def number(value: str | None, *, default: float | None = None) -> float | None:
    if value is None or value.strip() == "":
        return default
    return float(value)


def ratio(value: str | None) -> float | None:
    parsed = number(value)
    if parsed is None:
        return None
    return parsed / 100.0 if abs(parsed) > 1.0 else parsed


def boolean(value: str | None) -> bool | None:
    if value is None or value.strip() == "":
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")


def clipped(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def scaled(value: float, low: float, high: float) -> float:
    if high <= low:
        raise ValueError("invalid scale")
    return clipped((value - low) / (high - low), 0.0, 1.0)


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def load_rows(path: Path, market: str, scope: str, selected_group: str | None) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = REQUIRED - set(reader.fieldnames)
        if missing:
            raise ValueError(f"missing required columns: {','.join(sorted(missing))}")

        rows: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for raw in reader:
            if raw["scope"].strip().lower() != scope:
                continue
            if selected_group and raw["group"].strip() != selected_group:
                continue
            parsed_date = date.fromisoformat(raw["date"].strip())
            symbol = raw["symbol"].strip()
            fund_id = (raw.get("fund_id") or symbol).strip()
            duplicate_key = (parsed_date.isoformat(), fund_id)
            if duplicate_key in seen:
                label = "canonical fund" if market == "hk" else "symbol"
                raise ValueError(
                    f"duplicate date/{label} row: {duplicate_key[0]},{fund_id}; "
                    "consolidate multi-counter data before analysis"
                )
            seen.add(duplicate_key)

            parsed: dict[str, Any] = {
                "date": parsed_date,
                "symbol": symbol,
                "fund_id": fund_id,
                "group": raw["group"].strip(),
                "scope": scope,
                "market": market,
                "close": float(raw["close"]),
                "nav": float(raw["nav"]),
                "shares": float(raw["shares"]),
                "turnover": float(raw["turnover"]),
                "free_float_mcap": number(raw.get("free_float_mcap")),
                "fund_structure": (raw.get("fund_structure") or "physical").strip().lower(),
                "counter_currency": (raw.get("counter_currency") or "").strip().upper(),
                "nav_stale": boolean(raw.get("nav_stale")),
            }
            if parsed["close"] <= 0 or parsed["nav"] <= 0 or parsed["shares"] <= 0:
                raise ValueError(f"close, nav, and shares must be positive: {parsed_date},{symbol}")
            if parsed["turnover"] < 0:
                raise ValueError(f"turnover must be non-negative: {parsed_date},{symbol}")
            for field in OPTIONAL_RATIO_FIELDS:
                parsed[field] = ratio(raw.get(field))
                if parsed[field] is not None and not 0.0 <= parsed[field] <= 1.0:
                    raise ValueError(f"{field} must resolve to a 0-1 ratio: {parsed_date},{symbol}")
            for field in SIGNAL_FIELDS:
                value = number(raw.get(field))
                parsed[field] = None if value is None else clipped(value)
            for field in SIGNED_RATIO_FIELDS:
                parsed[field] = ratio(raw.get(field))
                if parsed[field] is not None and not -1.0 <= parsed[field] <= 1.0:
                    raise ValueError(f"{field} must resolve to a -1 to 1 ratio: {parsed_date},{symbol}")
            for field in HK_NUMBER_FIELDS:
                parsed[field] = number(raw.get(field))
            if parsed["spread_bps"] is not None and parsed["spread_bps"] < 0:
                raise ValueError(f"spread_bps must be non-negative: {parsed_date},{symbol}")
            if parsed["southbound_holding"] is not None and parsed["southbound_holding"] < 0:
                raise ValueError(f"southbound_holding must be non-negative: {parsed_date},{symbol}")
            rows.append(parsed)
    if not rows:
        raise ValueError("no rows matched scope/group")
    return rows


def weighted_optional(rows: list[dict[str, Any]], field: str) -> float | None:
    available = [(row[field], row["shares"] * row["nav"]) for row in rows if row.get(field) is not None]
    if not available:
        return None
    total_weight = sum(weight for _, weight in available)
    if total_weight <= 0:
        return mean([value for value, _ in available])
    return sum(value * weight for value, weight in available) / total_weight


def build_group_series(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_symbol[row["fund_id"]].append(row)
    for symbol_rows in by_symbol.values():
        symbol_rows.sort(key=lambda item: item["date"])
        previous: dict[str, Any] | None = None
        for row in symbol_rows:
            row["aum"] = row["shares"] * row["nav"]
            if previous is None:
                row["flow"] = None
                row["return"] = None
                row["previous_aum"] = None
            else:
                row["flow"] = (row["shares"] - previous["shares"]) * row["nav"]
                row["return"] = row["close"] / previous["close"] - 1.0
                row["previous_aum"] = previous["aum"]
            previous = row

    by_date: dict[date, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_date[row["date"]].append(row)

    expected_symbols = set(by_symbol)
    series: list[dict[str, Any]] = []
    synthetic_price = 100.0
    for current_date in sorted(by_date):
        day_rows = by_date[current_date]
        valid_returns = [row for row in day_rows if row["return"] is not None and row["previous_aum"]]
        if valid_returns:
            denom = sum(row["previous_aum"] for row in valid_returns)
            group_return = sum(row["return"] * row["previous_aum"] for row in valid_returns) / denom
            synthetic_price *= 1.0 + group_return
        else:
            group_return = None

        valid_flows = [row for row in day_rows if row["flow"] is not None]
        flow = sum(row["flow"] for row in valid_flows) if valid_flows else None
        previous_aum = sum(row["previous_aum"] or 0.0 for row in valid_flows)
        southbound_rows = [row for row in day_rows if row["southbound_holding"] is not None]
        southbound_value = sum(row["southbound_holding"] * row["nav"] for row in southbound_rows) if southbound_rows else None
        southbound_net_buy_rows = [row["southbound_net_buy"] for row in day_rows if row["southbound_net_buy"] is not None]
        total_aum = sum(row["aum"] for row in day_rows)
        series.append(
            {
                "date": current_date,
                "price": synthetic_price,
                "return": group_return,
                "flow": flow,
                "flow_rate": None if flow is None or previous_aum <= 0 else flow / previous_aum,
                "aum": total_aum,
                "turnover": sum(row["turnover"] for row in day_rows),
                "breadth_ma20": weighted_optional(day_rows, "breadth_ma20"),
                "breadth_ma50": weighted_optional(day_rows, "breadth_ma50"),
                "top10_weight": weighted_optional(day_rows, "top10_weight"),
                "valuation_percentile": weighted_optional(day_rows, "valuation_percentile"),
                "fundamental_signal": weighted_optional(day_rows, "fundamental_signal"),
                "policy_signal": weighted_optional(day_rows, "policy_signal"),
                "derivatives_signal": weighted_optional(day_rows, "derivatives_signal"),
                "cross_market_signal": weighted_optional(day_rows, "cross_market_signal"),
                "premium_discount": weighted_optional(day_rows, "premium_discount"),
                "spread_bps": weighted_optional(day_rows, "spread_bps"),
                "nav_stale": any(row["nav_stale"] is True for row in day_rows),
                "southbound_holding_share": None if southbound_value is None or total_aum <= 0 else southbound_value / total_aum,
                "southbound_net_buy": sum(southbound_net_buy_rows) if southbound_net_buy_rows else None,
                # The denominator describes the underlying exposure and may be
                # repeated on every peer ETF row; averaging avoids double count.
                "free_float_mcap": weighted_optional(day_rows, "free_float_mcap"),
                "symbols": sorted(row["symbol"] for row in day_rows),
                "fund_ids": sorted(row["fund_id"] for row in day_rows),
                "fund_structures": sorted({row["fund_structure"] for row in day_rows}),
                "counter_currencies": sorted({row["counter_currency"] for row in day_rows if row["counter_currency"]}),
                "peer_coverage": len({row["fund_id"] for row in day_rows}) / len(expected_symbols),
            }
        )
    return series


def window_return(series: list[dict[str, Any]], size: int) -> float | None:
    if len(series) <= size:
        return None
    return series[-1]["price"] / series[-size - 1]["price"] - 1.0


def window_flow_rate(series: list[dict[str, Any]], size: int) -> float | None:
    if len(series) <= size:
        return None
    window = series[-size:]
    flows = [row["flow"] for row in window if row["flow"] is not None]
    starting_aum = series[-size - 1]["aum"]
    if not flows or starting_aum <= 0:
        return None
    return sum(flows) / starting_aum


def window_field_change(series: list[dict[str, Any]], field: str, size: int) -> float | None:
    if len(series) <= size:
        return None
    starting = series[-size - 1].get(field)
    latest = series[-1].get(field)
    if starting is None or latest is None:
        return None
    return latest - starting


def window_money_rate(series: list[dict[str, Any]], field: str, size: int) -> float | None:
    if len(series) <= size:
        return None
    values = [row[field] for row in series[-size:] if row.get(field) is not None]
    starting_aum = series[-size - 1]["aum"]
    if not values or starting_aum <= 0:
        return None
    return sum(values) / starting_aum


def peer_share_trend(rows: list[dict[str, Any]], size: int) -> dict[str, float | None]:
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_symbol[row["fund_id"]].append(row)

    observations: list[tuple[float, float]] = []
    positive = 0
    negative = 0
    for symbol_rows in by_symbol.values():
        symbol_rows.sort(key=lambda item: item["date"])
        if len(symbol_rows) <= size:
            continue
        starting = symbol_rows[-size - 1]
        latest = symbol_rows[-1]
        change = latest["shares"] / starting["shares"] - 1.0
        observations.append((change, starting["shares"] * starting["nav"]))
        if change > 0.002:
            positive += 1
        elif change < -0.002:
            negative += 1

    if not observations:
        return {"change_rate": None, "expansion_peer_fraction": None, "redemption_peer_fraction": None}
    total_weight = sum(weight for _, weight in observations)
    weighted_change = sum(change * weight for change, weight in observations) / total_weight
    count = len(observations)
    return {
        "change_rate": weighted_change,
        "expansion_peer_fraction": positive / count,
        "redemption_peer_fraction": negative / count,
    }


def flow_z_score(series: list[dict[str, Any]], window: int = 5, history: int = 252) -> float | None:
    rates: list[float] = []
    start = max(window + 1, len(series) - history)
    for index in range(start, len(series) + 1):
        subset = series[index - window:index]
        flows = [row["flow"] for row in subset if row["flow"] is not None]
        starting_aum = series[index - window - 1]["aum"]
        if flows and starting_aum > 0:
            rates.append(sum(flows) / starting_aum)
    if len(rates) < 21:
        return None
    historical = rates[:-1]
    sigma = statistics.pstdev(historical)
    if sigma == 0:
        return None
    return (rates[-1] - statistics.fmean(historical)) / sigma


def score_from_factors(factors: list[tuple[str, float, float | None]]) -> dict[str, Any]:
    available = [(name, weight, value) for name, weight, value in factors if value is not None]
    coverage = sum(weight for _, weight, _ in available) / sum(weight for _, weight, _ in factors)
    if len(available) < 3:
        return {"score": None, "coverage": round(coverage, 3), "factors": {name: value for name, _, value in factors}}
    score = sum(weight * value for _, weight, value in available) / sum(weight for _, weight, _ in available) * 100.0
    return {
        "score": round(score, 1),
        "coverage": round(coverage, 3),
        "factors": {name: None if value is None else round(value, 3) for name, _, value in factors},
    }


def scenario_update(prior: tuple[float, float, float], signals: dict[str, tuple[float, float]]) -> dict[str, float]:
    states = ("up", "range", "down")
    logs = {state: math.log(probability) for state, probability in zip(states, prior)}
    for signal, reliability in signals.values():
        signal = clipped(signal)
        reliability = clipped(reliability, 0.0, 1.0)
        log_lr = {
            "up": 0.60 * signal,
            "down": -0.60 * signal,
            "range": 0.35 * (1.0 - abs(signal)),
        }
        for state in states:
            logs[state] += reliability * log_lr[state]
    maximum = max(logs.values())
    raw = {state: math.exp(value - maximum) for state, value in logs.items()}
    total = sum(raw.values())
    posterior = {state: value / total for state, value in raw.items()}
    floor = 0.03
    floored = {state: max(floor, value) for state, value in posterior.items()}
    excess = sum(floored.values()) - 1.0
    if excess > 0:
        adjustable = {state: value - floor for state, value in floored.items() if value > floor}
        capacity = sum(adjustable.values())
        for state, room in adjustable.items():
            floored[state] -= excess * room / capacity
    return {state: round(value, 4) for state, value in floored.items()}


def analyze_group(
    group: str,
    market: str,
    scope: str,
    rows: list[dict[str, Any]],
    prior: tuple[float, float, float],
    regime: str,
) -> dict[str, Any]:
    series = build_group_series(rows)
    latest = series[-1]
    prices = [row["price"] for row in series]
    turnovers = [row["turnover"] for row in series]
    ma20 = mean(prices[-20:])
    ma50 = mean(prices[-50:])
    turnover20 = mean(turnovers[-20:])
    ret5, ret20, ret60 = (window_return(series, size) for size in (5, 20, 60))
    flow5, flow20, flow60 = (window_flow_rate(series, size) for size in (5, 20, 60))
    share5, share20, share60 = (peer_share_trend(rows, size) for size in (5, 20, 60))
    southbound_holding_change20 = window_field_change(series, "southbound_holding_share", 20)
    southbound_net_buy20 = window_money_rate(series, "southbound_net_buy", 20)
    z5 = flow_z_score(series)
    turnover_heat = None if not turnover20 else latest["turnover"] / turnover20
    recent_peer_coverage = mean([row["peer_coverage"] for row in series[-20:]])
    flow_pressure = None
    if latest["flow"] is not None and turnover20:
        flow_pressure = abs(latest["flow"]) / turnover20

    risky_structures = {"synthetic", "futures", "futures_based", "leveraged", "inverse", "leveraged_inverse"}
    has_complex_structure = any(structure in risky_structures for structure in latest["fund_structures"])
    market_quality_risk = score_from_factors(
        [
            (
                "premium_discount_stress",
                25,
                None if latest["premium_discount"] is None else scaled(abs(latest["premium_discount"]), 0.005, 0.03),
            ),
            ("spread_stress", 30, None if latest["spread_bps"] is None else scaled(latest["spread_bps"], 20.0, 100.0)),
            ("nav_staleness", 20, 1.0 if latest["nav_stale"] else 0.0),
            ("structure_complexity", 25, 1.0 if has_complex_structure else 0.0),
        ]
    ) if market == "hk" else None

    price_direction = 0 if ret5 is None or abs(ret5) < 0.002 else (1 if ret5 > 0 else -1)
    flow_direction = 0 if flow5 is None or abs(flow5) < 0.002 else (1 if flow5 > 0 else -1)
    quadrant = {
        (1, 1): "price_up_flow_up",
        (1, -1): "price_up_flow_down",
        (-1, 1): "price_down_flow_up",
        (-1, -1): "price_down_flow_down",
    }.get((price_direction, flow_direction), "mixed_or_flat")

    capacity = None
    if latest["free_float_mcap"] and latest["free_float_mcap"] > 0:
        capacity = latest["aum"] / latest["free_float_mcap"]
    extension = None if not ma20 else latest["price"] / ma20 - 1.0

    positive_flow_factor = None
    negative_flow_factor = None
    if z5 is not None:
        positive_flow_factor = scaled(z5, 1.0, 3.0)
        negative_flow_factor = scaled(-z5, 1.0, 3.0)
    elif flow20 is not None:
        positive_flow_factor = scaled(flow20, 0.10, 0.35)
        negative_flow_factor = scaled(-flow20, 0.10, 0.35)

    crowding = score_from_factors(
        [
            ("positive_flow_acceleration", 25, positive_flow_factor),
            ("turnover_heat", 20, None if turnover_heat is None else scaled(turnover_heat, 1.2, 2.5)),
            ("top10_concentration", 15, None if latest["top10_weight"] is None else scaled(latest["top10_weight"], 0.45, 0.70)),
            ("aum_free_float_capacity", 15, None if capacity is None else scaled(capacity, 0.03, 0.10)),
            ("price_extension", 15, None if extension is None else scaled(extension, 0.08, 0.25)),
            ("valuation_percentile", 10, None if latest["valuation_percentile"] is None else scaled(latest["valuation_percentile"], 0.75, 1.00)),
        ]
    )

    hk_cross_border_crowding = None
    if market == "hk":
        hk_cross_border_crowding = score_from_factors(
            [
                (
                    "southbound_holding_concentration",
                    35,
                    None
                    if latest["southbound_holding_share"] is None
                    else scaled(latest["southbound_holding_share"], 0.15, 0.40),
                ),
                (
                    "southbound_holding_acceleration",
                    30,
                    None
                    if southbound_holding_change20 is None
                    else scaled(southbound_holding_change20, 0.03, 0.10),
                ),
                ("primary_creation_pressure", 20, positive_flow_factor),
                (
                    "valuation_percentile",
                    15,
                    None
                    if latest["valuation_percentile"] is None
                    else scaled(latest["valuation_percentile"], 0.75, 1.00),
                ),
            ]
        )

    trend_break = None
    if ma20 is not None:
        below20 = latest["price"] < ma20
        below50 = ma50 is not None and latest["price"] < ma50
        trend_break = (0.55 if below20 else 0.0) + (0.30 if below50 else 0.0)
        if ret20 is not None and ret20 < -0.10:
            trend_break += 0.15
        trend_break = clipped(trend_break, 0.0, 1.0)
    price_flow_unwind = 1.0 if quadrant == "price_down_flow_down" else (0.45 if price_direction < 0 else 0.0)
    breadth_unwind = None
    if latest["breadth_ma20"] is not None:
        breadth_unwind = scaled(0.50 - latest["breadth_ma20"], 0.0, 0.30)
    nonconfirmation = None
    if latest["fundamental_signal"] is not None or latest["policy_signal"] is not None:
        supplied = [value for value in (latest["fundamental_signal"], latest["policy_signal"]) if value is not None]
        nonconfirmation = scaled(-statistics.fmean(supplied), 0.0, 1.0)
    unwind = score_from_factors(
        [
            ("negative_flow_acceleration", 30, negative_flow_factor),
            ("trend_break", 25, trend_break),
            ("price_flow_confirmation", 20, price_flow_unwind),
            ("breadth_break", 15, breadth_unwind),
            ("fundamental_policy_nonconfirmation", 10, nonconfirmation),
        ]
    )

    broad_withdrawal = None
    if scope == "broad":
        breadth_risk = None if latest["breadth_ma50"] is None else scaled(0.50 - latest["breadth_ma50"], 0.0, 0.30)
        policy_risk = None if latest["policy_signal"] is None else scaled(-latest["policy_signal"], 0.0, 1.0)
        cross_risk = None if latest["cross_market_signal"] is None else scaled(-latest["cross_market_signal"], 0.0, 1.0)
        derivatives_risk = None if latest["derivatives_signal"] is None else scaled(-latest["derivatives_signal"], 0.0, 1.0)
        broad_withdrawal = score_from_factors(
            [
                ("peer_aggregated_flow", 30, negative_flow_factor),
                ("price_trend", 20, trend_break),
                ("breadth", 20, breadth_risk),
                ("turnover_derivatives", 10, derivatives_risk),
                ("policy_liquidity", 10, policy_risk),
                ("cross_market", 10, cross_risk),
            ]
        )

    trend_signal_parts: list[float] = []
    if ma20 is not None:
        trend_signal_parts.append(0.5 if latest["price"] > ma20 else -0.5)
    if ma50 is not None:
        trend_signal_parts.append(0.3 if latest["price"] > ma50 else -0.3)
    if ret20 is not None:
        trend_signal_parts.append(clipped(ret20 / 0.12))
    trend_signal = clipped(statistics.fmean(trend_signal_parts)) if trend_signal_parts else 0.0

    flow_signal_parts: list[float] = []
    if flow20 is not None:
        flow_signal_parts.append(clipped(flow20 / 0.12))
    if z5 is not None:
        flow_signal_parts.append(clipped(z5 / 3.0))
    flow_signal = clipped(statistics.fmean(flow_signal_parts)) if flow_signal_parts else 0.0

    flow_reliability = 0.9 if z5 is not None else 0.6
    if market == "hk":
        if latest["nav_stale"]:
            flow_reliability *= 0.55
        if latest["spread_bps"] is not None and latest["spread_bps"] > 50:
            flow_reliability *= 0.75
        if latest["premium_discount"] is not None and abs(latest["premium_discount"]) > 0.02:
            flow_reliability *= 0.75
        if has_complex_structure:
            flow_reliability *= 0.70

    cross_border_parts: list[float] = []
    if southbound_holding_change20 is not None:
        cross_border_parts.append(clipped(southbound_holding_change20 / 0.05))
    if southbound_net_buy20 is not None:
        cross_border_parts.append(clipped(southbound_net_buy20 / 0.08))
    cross_border_signal = clipped(statistics.fmean(cross_border_parts)) if cross_border_parts else None

    cross_border_state = None
    if market == "hk" and cross_border_signal is not None:
        if cross_border_signal > 0.15 and flow_signal < -0.15:
            cross_border_state = "southbound_absorbing_primary_redemption"
        elif cross_border_signal > 0.15 and flow_signal > 0.15:
            cross_border_state = "southbound_and_primary_flow_confirm"
        elif cross_border_signal < -0.15 and flow_signal < -0.15:
            cross_border_state = "cross_border_and_primary_outflow_confirm"
        elif cross_border_signal < -0.15 and flow_signal > 0.15:
            cross_border_state = "primary_creation_offsets_southbound_selling"
        else:
            cross_border_state = "mixed_or_flat"

    flow_family = "primary_flow" if market == "hk" else "flow"
    signals: dict[str, tuple[float, float]] = {
        "trend": (trend_signal, 0.9 if len(series) >= 50 else 0.6),
        flow_family: (flow_signal, flow_reliability),
    }
    if market == "hk" and cross_border_signal is not None:
        signals["cross_border"] = (cross_border_signal, 0.7)
    if latest["breadth_ma50"] is not None:
        signals["breadth"] = (clipped((latest["breadth_ma50"] - 0.5) * 2.5), 0.8)
    if latest["fundamental_signal"] is not None:
        signals["fundamentals"] = (latest["fundamental_signal"], 0.7)
    if latest["policy_signal"] is not None:
        signals["policy"] = (latest["policy_signal"], 0.6)
    if latest["valuation_percentile"] is not None:
        valuation_signal = clipped((0.5 - latest["valuation_percentile"]) * 1.2)
        signals["valuation"] = (valuation_signal, 0.5)
    if latest["derivatives_signal"] is not None:
        signals["derivatives"] = (latest["derivatives_signal"], 0.6)
    if latest["cross_market_signal"] is not None:
        signals["cross_market"] = (latest["cross_market_signal"], 0.6)

    posterior = scenario_update(prior, signals)
    neutral_posterior = scenario_update((1 / 3, 1 / 3, 1 / 3), signals)
    selected_leader = max(posterior, key=posterior.get)
    neutral_leader = max(neutral_posterior, key=neutral_posterior.get)
    coverage = len(signals) / (9.0 if market == "hk" else 8.0)
    poor_hk_market_quality = market == "hk" and (
        latest["nav_stale"]
        or (latest["spread_bps"] is not None and latest["spread_bps"] > 100)
        or has_complex_structure
    )
    if len(series) < 60 or selected_leader != neutral_leader or coverage < 0.5 or poor_hk_market_quality:
        confidence = "low"
    elif len(series) >= 120 and coverage >= 0.75:
        confidence = "medium-high"
    else:
        confidence = "medium"

    warnings: list[str] = []
    if len(series) < 60:
        warnings.append("fewer than 60 daily group observations")
    if z5 is None:
        warnings.append("insufficient history for rolling 5-day flow Z-score")
    if scope == "broad" and len(latest["fund_ids"]) < 2:
        warnings.append("broad group has fewer than two peer ETFs; migration cannot be checked")
    if latest["breadth_ma50"] is None:
        warnings.append("constituent breadth is missing")
    if recent_peer_coverage is not None and recent_peer_coverage < 0.90:
        warnings.append("recent peer-ETF date coverage is below 90%; aggregated flows may be incomplete")
    if market == "hk":
        if latest["nav_stale"]:
            warnings.append("latest NAV is marked stale; premium/discount and primary-flow reliability are reduced")
        if latest["spread_bps"] is not None and latest["spread_bps"] > 50:
            warnings.append("wide spread reduces Hong Kong ETF flow-signal reliability")
        if has_complex_structure:
            warnings.append("synthetic/futures/leveraged structure requires product-specific exposure analysis")
        if latest["southbound_holding_share"] is None and latest["southbound_net_buy"] is None:
            warnings.append("Southbound evidence is missing; cross-border demand cannot be separated")

    sensitivity_range = {
        state: [min(posterior[state], neutral_posterior[state]), max(posterior[state], neutral_posterior[state])]
        for state in ("up", "range", "down")
    }

    return {
        "group": group,
        "market": market,
        "scope": scope,
        "as_of": latest["date"].isoformat(),
        "symbols": latest["symbols"],
        "fund_ids": latest["fund_ids"],
        "observations": len(series),
        "metrics": {
            "return_5d": ret5,
            "return_20d": ret20,
            "return_60d": ret60,
            "estimated_flow_rate_5d": flow5,
            "estimated_flow_rate_20d": flow20,
            "estimated_flow_rate_60d": flow60,
            "share_change_rate_5d": share5["change_rate"],
            "share_change_rate_20d": share20["change_rate"],
            "share_change_rate_60d": share60["change_rate"],
            "expansion_peer_fraction_20d": share20["expansion_peer_fraction"],
            "redemption_peer_fraction_20d": share20["redemption_peer_fraction"],
            "flow_z_5d": z5,
            "latest_flow_pressure": flow_pressure,
            "turnover_heat": turnover_heat,
            "price_vs_ma20": extension,
            "price_vs_ma50": None if ma50 is None else latest["price"] / ma50 - 1.0,
            "price_flow_quadrant": quadrant,
            "top10_weight": latest["top10_weight"],
            "aum_free_float_ratio": capacity,
            "recent_peer_coverage": recent_peer_coverage,
            "southbound_holding_share": latest["southbound_holding_share"],
            "southbound_holding_share_change_20d": southbound_holding_change20,
            "southbound_net_buy_rate_20d": southbound_net_buy20,
            "premium_discount": latest["premium_discount"],
            "spread_bps": latest["spread_bps"],
            "nav_stale": latest["nav_stale"],
        },
        "crowding": crowding,
        "unwind": unwind,
        "broad_support_withdrawal": broad_withdrawal,
        "hong_kong_context": None if market != "hk" else {
            "fund_structures": latest["fund_structures"],
            "counter_currencies": latest["counter_currencies"],
            "cross_border_state": cross_border_state,
            "cross_border_crowding": hk_cross_border_crowding,
            "market_quality_risk": market_quality_risk,
        },
        "bayesian_scenarios": {
            "label": "model-implied scenario weights",
            "regime": regime,
            "prior": {"up": prior[0], "range": prior[1], "down": prior[2]},
            "evidence_signals": {name: {"value": round(value, 3), "reliability": reliability} for name, (value, reliability) in signals.items()},
            "posterior": posterior,
            "neutral_prior_sensitivity": neutral_posterior,
            "sensitivity_range": sensitivity_range,
            "confidence": confidence,
        },
        "warnings": warnings,
    }


def select_prior(args: argparse.Namespace) -> tuple[float, float, float]:
    custom = (args.prior_up, args.prior_range, args.prior_down)
    if any(value is not None for value in custom):
        if any(value is None for value in custom):
            raise ValueError("custom prior requires --prior-up, --prior-range, and --prior-down")
        if any(value <= 0 for value in custom if value is not None):
            raise ValueError("every custom prior component must be positive")
        total = sum(custom)  # type: ignore[arg-type]
        return tuple(value / total for value in custom)  # type: ignore[return-value,union-attr]
    if args.market == "hk":
        priors = HK_PRIORS
    else:
        priors = BROAD_PRIORS if args.scope == "broad" else SECTOR_PRIORS
    if args.regime not in priors:
        raise ValueError(f"unknown regime for {args.market}/{args.scope}: {args.regime}; choose from {','.join(priors)}")
    return priors[args.regime]


def main() -> int:
    try:
        args = parse_args()
        prior = select_prior(args)
        regime = "custom" if any(value is not None for value in (args.prior_up, args.prior_range, args.prior_down)) else args.regime
        rows = load_rows(args.input, args.market, args.scope, args.group)
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[row["group"]].append(row)
        result = {
            "model": "a-h-share-etf-flow-crowding-bayes-v1.2",
            "market": args.market,
            "probability_label": "model-implied scenario weights",
            "results": [
                analyze_group(group, args.market, args.scope, group_rows, prior, regime)
                for group, group_rows in sorted(grouped.items())
            ],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, default=str))
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
