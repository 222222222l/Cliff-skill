#!/usr/bin/env python3
"""Record a human preference score for an agent run."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import sys
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_dimension(value: str) -> tuple[str, float]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("dimension must use name=score")
    name, raw_score = value.split("=", 1)
    name = name.strip()
    if not name:
        raise argparse.ArgumentTypeError("dimension name cannot be empty")
    try:
        score = float(raw_score)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("dimension score must be numeric") from exc
    return name, score


def prompt_score(max_score: int) -> int:
    print("Human preference score")
    print("1 = unusable or harmful")
    print("2 = major repair needed")
    print("3 = usable with caveats")
    print("4 = good with minor edits")
    print("5 = excellent / accept as-is")
    while True:
        raw = input(f"Score 1-{max_score}: ").strip()
        try:
            score = int(raw)
        except ValueError:
            print("Enter an integer.")
            continue
        if 1 <= score <= max_score:
            return score
        print(f"Enter a value between 1 and {max_score}.")


def preview_artifact(path: pathlib.Path, preview_chars: int) -> None:
    if not path.exists():
        print(f"artifact not found: {path}", file=sys.stderr)
        return
    print(f"\n--- artifact preview: {path} ---")
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    if len(text) > preview_chars:
        print(text[:preview_chars])
        print(f"\n--- preview truncated at {preview_chars} chars ---")
    else:
        print(text)
    print("--- end preview ---\n")


def append_jsonl(path: pathlib.Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Record human preference scores for agent evaluations.")
    parser.add_argument("--run-id", required=True, help="Run identifier to match automated run records.")
    parser.add_argument("--task-id", required=True, help="Task identifier to match automated run records.")
    parser.add_argument("--artifact", help="Optional trace/result artifact to preview before scoring.")
    parser.add_argument("--out", default="human_scores.jsonl", help="Output JSONL file.")
    parser.add_argument("--score", type=int, help="Human score. If omitted, prompt interactively.")
    parser.add_argument("--max-score", type=int, default=5, help="Maximum score. Default: 5.")
    parser.add_argument("--dimension", action="append", type=parse_dimension, default=[], help="Optional dimension score, e.g. trust=4")
    parser.add_argument("--notes", help="Reviewer notes. If omitted in interactive mode, prompt for notes.")
    parser.add_argument("--reviewer", help="Reviewer id or name.")
    parser.add_argument("--preview-chars", type=int, default=4000, help="Artifact preview length.")
    args = parser.parse_args(argv)

    if args.max_score <= 0:
        parser.error("--max-score must be positive")

    artifact_path = pathlib.Path(args.artifact) if args.artifact else None
    if artifact_path:
        preview_artifact(artifact_path, args.preview_chars)

    score = args.score if args.score is not None else prompt_score(args.max_score)
    if not (1 <= score <= args.max_score):
        parser.error(f"--score must be between 1 and {args.max_score}")

    notes = args.notes
    if notes is None and args.score is None:
        notes = input("Notes (optional): ").strip()

    record: Dict[str, Any] = {
        "timestamp": utc_now_iso(),
        "run_id": args.run_id,
        "task_id": args.task_id,
        "score": score,
        "max_score": args.max_score,
    }
    if artifact_path:
        record["artifact"] = str(artifact_path)
    if args.reviewer:
        record["reviewer"] = args.reviewer
    if notes:
        record["notes"] = notes
    if args.dimension:
        record["dimensions"] = {name: value for name, value in args.dimension}

    out_path = pathlib.Path(args.out)
    append_jsonl(out_path, record)
    print(f"recorded score {score}/{args.max_score} for run_id={args.run_id}, task_id={args.task_id}")
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
