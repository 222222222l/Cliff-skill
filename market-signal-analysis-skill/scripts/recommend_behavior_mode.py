#!/usr/bin/env python3
"""Rank behavior modes from state probabilities and calibrated return priors."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EPSILON = 1e-12


class InputError(ValueError):
    """Raised when the structured behavior-model input is invalid."""


@dataclass
class StateEstimate:
    low: float
    mean: float
    high: float
    log_growth: float
    expected_shortfall: float
    max_drawdown: float
    ruin_probability: float
    sample_count: int
    out_of_sample: bool
    includes_failures: bool


def require_number(
    mapping: dict[str, Any],
    key: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if key not in mapping:
        raise InputError(f"Missing required number: {key}")
    value = mapping[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{key} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise InputError(f"{key} must be finite")
    if minimum is not None and value < minimum:
        raise InputError(f"{key} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise InputError(f"{key} must be <= {maximum}")
    return value


def optional_number(
    mapping: dict[str, Any],
    key: str,
    default: float,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if key not in mapping:
        return default
    return require_number(mapping, key, minimum=minimum, maximum=maximum)


def require_bool(mapping: dict[str, Any], key: str) -> bool:
    if key not in mapping or not isinstance(mapping[key], bool):
        raise InputError(f"{key} must be true or false")
    return bool(mapping[key])


def validate_return(value: float, label: str) -> None:
    if value <= -1.0:
        raise InputError(f"{label} must be greater than -1.0")


def total_cost(costs: dict[str, Any]) -> tuple[float, dict[str, float]]:
    allowed = ("fees", "spread", "slippage", "tax", "funding", "borrow", "impact")
    components = {key: optional_number(costs, key, 0.0, minimum=0.0) for key in allowed}
    return sum(components.values()), components


def state_estimate(prior: dict[str, Any], cost: float) -> StateEstimate:
    low = require_number(prior, "normal_return_low")
    mean = require_number(prior, "normal_return_mean")
    high = require_number(prior, "normal_return_high")
    if not low <= mean <= high:
        raise InputError(
            "normal_return_low <= normal_return_mean <= normal_return_high is required"
        )

    exit_probability = require_number(
        prior, "exit_probability", minimum=0.0, maximum=1.0
    )
    exit_loss = require_number(prior, "exit_loss", minimum=0.0, maximum=1.0)
    ruin_probability = require_number(
        prior, "ruin_probability", minimum=0.0, maximum=1.0
    )
    ruin_loss = require_number(prior, "ruin_loss", minimum=0.0, maximum=1.0)
    if exit_probability + ruin_probability > 1.0 + EPSILON:
        raise InputError("exit_probability + ruin_probability must be <= 1")

    normal_probability = max(0.0, 1.0 - exit_probability - ruin_probability)

    def mixture(normal_return: float) -> float:
        return (
            normal_probability * (normal_return - cost)
            - exit_probability * (exit_loss + cost)
            - ruin_probability * ruin_loss
        )

    normal_net = mean - cost
    exit_net = -exit_loss - cost
    ruin_net = -ruin_loss
    active_paths = (
        (normal_probability, normal_net, "normal return after cost"),
        (exit_probability, exit_net, "exit loss after cost"),
        (ruin_probability, ruin_net, "ruin loss"),
    )
    for probability, value, label in active_paths:
        if probability > 0.0:
            validate_return(value, label)

    log_growth = sum(
        probability * math.log1p(value)
        for probability, value, _ in active_paths
        if probability > 0.0
    )

    sample_count_raw = prior.get("sample_count")
    if isinstance(sample_count_raw, bool) or not isinstance(sample_count_raw, int):
        raise InputError("sample_count must be an integer")
    if sample_count_raw < 0:
        raise InputError("sample_count must be >= 0")

    return StateEstimate(
        low=mixture(low),
        mean=mixture(mean),
        high=mixture(high),
        log_growth=log_growth,
        expected_shortfall=require_number(
            prior, "expected_shortfall", minimum=0.0, maximum=1.0
        ),
        max_drawdown=require_number(prior, "max_drawdown", minimum=0.0, maximum=1.0),
        ruin_probability=ruin_probability,
        sample_count=sample_count_raw,
        out_of_sample=require_bool(prior, "out_of_sample"),
        includes_failures=require_bool(prior, "includes_failures"),
    )


def confidence_label(estimates: list[StateEstimate]) -> str:
    if not estimates or any(item.sample_count < 20 for item in estimates):
        return "insufficient"
    if all(
        item.sample_count >= 100 and item.out_of_sample and item.includes_failures
        for item in estimates
    ):
        return "high"
    if all(item.sample_count >= 50 and item.includes_failures for item in estimates):
        return "medium"
    return "low"


def aggregate_mode(
    mode: dict[str, Any],
    state_probabilities: dict[str, float],
    risk_budget: dict[str, Any],
    long_vol: float,
) -> dict[str, Any]:
    mode_id = str(mode.get("id", "")).strip()
    if not mode_id:
        raise InputError("Each mode requires a non-empty id")
    label = str(mode.get("label", mode_id)).strip() or mode_id
    exit_defined = require_bool(mode, "exit_defined")
    leverage = require_number(mode, "max_gross_leverage", minimum=0.0)
    outside_exposure = require_number(
        mode, "outside_state_exposure", minimum=0.0, maximum=1.0
    )
    costs_raw = mode.get("costs", {})
    if not isinstance(costs_raw, dict):
        raise InputError(f"{mode_id}.costs must be an object")
    cost, cost_components = total_cost(costs_raw)

    priors = mode.get("state_priors")
    if not isinstance(priors, dict):
        raise InputError(f"{mode_id}.state_priors must be an object")

    weighted = {
        "low": 0.0,
        "mean": 0.0,
        "high": 0.0,
        "log_growth": 0.0,
        "expected_shortfall": 0.0,
        "max_drawdown": 0.0,
        "ruin_probability": 0.0,
    }
    used_estimates: list[StateEstimate] = []
    state_details: dict[str, Any] = {}

    for state, probability in state_probabilities.items():
        if probability <= 0.0:
            continue
        prior = priors.get(state)
        if not isinstance(prior, dict):
            raise InputError(f"{mode_id} is missing a prior for state '{state}'")
        estimate = state_estimate(prior, cost)
        used_estimates.append(estimate)
        for key in weighted:
            weighted[key] += probability * getattr(estimate, key)
        state_details[state] = {
            "probability": round(probability, 8),
            "net_return_low": estimate.low,
            "net_return_mean": estimate.mean,
            "net_return_high": estimate.high,
            "expected_log_growth": estimate.log_growth,
            "expected_shortfall": estimate.expected_shortfall,
            "max_drawdown": estimate.max_drawdown,
            "ruin_probability": estimate.ruin_probability,
            "sample_count": estimate.sample_count,
            "out_of_sample": estimate.out_of_sample,
            "includes_failures": estimate.includes_failures,
        }

    confidence = confidence_label(used_estimates)
    violations: list[str] = []
    if not exit_defined:
        violations.append("exit rule is not defined")
    if confidence == "insufficient":
        violations.append("one or more material state priors have fewer than 20 events")

    constraints = (
        ("expected_shortfall", "max_expected_shortfall"),
        ("max_drawdown", "max_drawdown"),
        ("ruin_probability", "max_ruin_probability"),
    )
    for metric, limit_key in constraints:
        limit = require_number(risk_budget, limit_key, minimum=0.0, maximum=1.0)
        if weighted[metric] > limit + EPSILON:
            violations.append(
                f"{metric} {weighted[metric]:.6f} exceeds {limit_key} {limit:.6f}"
            )

    max_leverage = require_number(risk_budget, "max_gross_leverage", minimum=0.0)
    if leverage > max_leverage + EPSILON:
        violations.append(
            f"max_gross_leverage {leverage:.6f} exceeds budget {max_leverage:.6f}"
        )

    max_outside = require_number(
        risk_budget,
        "max_outside_state_exposure",
        minimum=0.0,
        maximum=1.0,
    )
    if outside_exposure > max_outside + EPSILON:
        violations.append(
            "outside_state_exposure "
            f"{outside_exposure:.6f} exceeds budget {max_outside:.6f}"
        )

    max_cost_to_move = require_number(
        risk_budget, "max_cost_to_expected_move", minimum=0.0
    )
    expected_move = abs(weighted["mean"])
    cost_to_move = cost / max(expected_move, EPSILON)
    if cost_to_move > max_cost_to_move + EPSILON:
        violations.append(
            f"cost_to_expected_move {cost_to_move:.6f} exceeds budget "
            f"{max_cost_to_move:.6f}"
        )

    volatility_exposure = leverage * outside_exposure * long_vol
    conservative_efficiency = weighted["low"] / max(
        weighted["expected_shortfall"], EPSILON
    )
    numeric_return_available = confidence != "insufficient"

    return {
        "id": mode_id,
        "label": label,
        "eligible": not violations,
        "violations": violations,
        "confidence": confidence,
        "net_return_range": (
            {
                "low": weighted["low"],
                "mean": weighted["mean"],
                "high": weighted["high"],
            }
            if numeric_return_available
            else {"low": None, "mean": None, "high": None}
        ),
        "expected_log_growth": (
            weighted["log_growth"] if numeric_return_available else None
        ),
        "expected_shortfall": weighted["expected_shortfall"],
        "max_drawdown": weighted["max_drawdown"],
        "ruin_probability": weighted["ruin_probability"],
        "max_gross_leverage": leverage,
        "outside_state_exposure": outside_exposure,
        "volatility_exposure_proxy": volatility_exposure,
        "all_in_cost": cost,
        "cost_components": cost_components,
        "cost_to_expected_move": cost_to_move,
        "conservative_return_to_shortfall": (
            conservative_efficiency if numeric_return_available else None
        ),
        "state_details": state_details,
    }


def validate_state_probabilities(raw: Any) -> dict[str, float]:
    if not isinstance(raw, dict) or not raw:
        raise InputError("state_probabilities must be a non-empty object")
    result: dict[str, float] = {}
    for state, value in raw.items():
        if not isinstance(state, str) or not state.strip():
            raise InputError("state names must be non-empty strings")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InputError(f"Probability for state '{state}' must be numeric")
        probability = float(value)
        if not 0.0 <= probability <= 1.0:
            raise InputError(f"Probability for state '{state}' must be in [0,1]")
        result[state.strip()] = probability
    total = sum(result.values())
    if abs(total - 1.0) > 1e-6:
        raise InputError(f"state_probabilities must sum to 1; found {total:.9f}")
    return result


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    market = str(payload.get("market", "")).strip()
    if not market:
        raise InputError("market is required")
    horizon_days_raw = payload.get("horizon_days")
    if isinstance(horizon_days_raw, bool) or not isinstance(horizon_days_raw, int):
        raise InputError("horizon_days must be an integer")
    if horizon_days_raw <= 0:
        raise InputError("horizon_days must be positive")

    probability_label = str(payload.get("probability_label", "")).strip()
    if probability_label not in {
        "empirical_probability",
        "model_implied_probability",
        "scenario_weights",
    }:
        raise InputError(
            "probability_label must be empirical_probability, "
            "model_implied_probability, or scenario_weights"
        )

    context = payload.get("context")
    if not isinstance(context, dict):
        raise InputError("context must be an object")
    short_vol = require_number(context, "short_vol", minimum=0.0)
    long_vol = require_number(context, "long_vol", minimum=EPSILON)
    trend_efficiency = require_number(
        context, "trend_efficiency", minimum=0.0, maximum=1.0
    )
    short_vol_percentile = require_number(
        context, "short_vol_percentile", minimum=0.0, maximum=1.0
    )
    long_vol_percentile = require_number(
        context, "long_vol_percentile", minimum=0.0, maximum=1.0
    )
    jump_share = require_number(context, "jump_share", minimum=0.0, maximum=1.0)

    state_probabilities = validate_state_probabilities(
        payload.get("state_probabilities")
    )
    risk_budget = payload.get("risk_budget")
    if not isinstance(risk_budget, dict):
        raise InputError("risk_budget must be an object")
    modes = payload.get("modes")
    if not isinstance(modes, list) or not modes:
        raise InputError("modes must be a non-empty list")

    results = [
        aggregate_mode(mode, state_probabilities, risk_budget, long_vol)
        for mode in modes
        if isinstance(mode, dict)
    ]
    if len(results) != len(modes):
        raise InputError("Every modes entry must be an object")

    eligible = [item for item in results if item["eligible"]]
    eligible.sort(
        key=lambda item: (
            item["expected_log_growth"],
            item["conservative_return_to_shortfall"],
            -item["all_in_cost"],
            -item["volatility_exposure_proxy"],
        ),
        reverse=True,
    )
    recommended = eligible[0]["id"] if eligible else "cash_or_no_trade"

    warnings: list[str] = []
    if probability_label != "empirical_probability":
        warnings.append(
            "Return output is a model-implied prior estimate, not an empirical "
            "forecast probability."
        )
    if short_vol_percentile >= 0.7 and long_vol_percentile >= 0.7:
        warnings.append(
            "Both short- and long-horizon volatility are elevated; verify that "
            "forced flow and exit liquidity are represented in the priors."
        )
    if trend_efficiency < 0.35 and short_vol_percentile >= 0.7:
        warnings.append(
            "High short volatility with low trend efficiency is a chaotic state, "
            "not a clean trend signal."
        )
    if jump_share >= 0.3:
        warnings.append(
            "Jump risk is material; continuous-volatility estimates may understate "
            "exit loss."
        )

    return {
        "market": market,
        "as_of": payload.get("as_of"),
        "horizon_days": horizon_days_raw,
        "probability_label": probability_label,
        "context": {
            "short_vol": short_vol,
            "long_vol": long_vol,
            "vol_ratio": short_vol / long_vol,
            "short_vol_percentile": short_vol_percentile,
            "long_vol_percentile": long_vol_percentile,
            "trend_efficiency": trend_efficiency,
            "jump_share": jump_share,
        },
        "state_probabilities": state_probabilities,
        "recommended_mode": recommended,
        "ranking": eligible,
        "rejected_modes": [item for item in results if not item["eligible"]],
        "warnings": warnings,
        "method": (
            "State-probability mixture of calibrated behavior priors, after "
            "implementation costs, exit-failure and ruin paths; constrained by "
            "explicit risk budgets and ranked by expected net log growth."
        ),
    }


def load_payload(path: str) -> dict[str, Any]:
    if path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(path).read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise InputError("Input JSON must be an object")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rank market behavior modes from state probabilities, calibrated "
            "return priors, implementation costs, exit risk, and risk budgets."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a JSON input file, or '-' to read JSON from stdin.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON result.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = analyze(load_payload(args.input))
    except (InputError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
