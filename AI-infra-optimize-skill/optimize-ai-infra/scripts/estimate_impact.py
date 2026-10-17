#!/usr/bin/env python3
"""Estimate Amdahl-law end-to-end impact for one optimization candidate."""

from __future__ import annotations

import argparse
import json
import math


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate end-to-end speedup when a fraction of runtime is accelerated. "
            "This is an upper-bound model, not a benchmark."
        )
    )
    parser.add_argument(
        "--share",
        type=float,
        required=True,
        help="Fraction of end-to-end time occupied by the candidate, in [0, 1].",
    )
    parser.add_argument(
        "--speedup",
        type=float,
        required=True,
        help="Expected local speedup for the candidate, >= 1.",
    )
    parser.add_argument(
        "--current-time-ms",
        type=float,
        help="Optional current end-to-end time in milliseconds.",
    )
    return parser


def estimate(share: float, local_speedup: float, current_time_ms: float | None) -> dict:
    if not 0.0 <= share <= 1.0:
        raise ValueError("share must be between 0 and 1")
    if local_speedup < 1.0 or not math.isfinite(local_speedup):
        raise ValueError("speedup must be finite and at least 1")
    if current_time_ms is not None and (current_time_ms <= 0 or not math.isfinite(current_time_ms)):
        raise ValueError("current-time-ms must be finite and greater than 0")

    denominator = (1.0 - share) + share / local_speedup
    total_speedup = 1.0 / denominator
    maximum_speedup = None if share == 1.0 else 1.0 / (1.0 - share)

    result = {
        "candidate_time_share": share,
        "candidate_local_speedup": local_speedup,
        "estimated_total_speedup": total_speedup,
        "estimated_end_to_end_reduction_fraction": 1.0 - 1.0 / total_speedup,
        "theoretical_maximum_total_speedup_if_candidate_were_free": maximum_speedup,
        "theoretical_maximum_note": (
            "unbounded in this simplified model" if maximum_speedup is None else "finite Amdahl bound"
        ),
        "caveat": "Amdahl-law estimate only; validate with representative end-to-end benchmarks.",
    }
    if current_time_ms is not None:
        result["current_time_ms"] = current_time_ms
        result["estimated_time_ms"] = current_time_ms / total_speedup
        result["estimated_time_saved_ms"] = current_time_ms - result["estimated_time_ms"]
    return result


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = estimate(args.share, args.speedup, args.current_time_ms)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
