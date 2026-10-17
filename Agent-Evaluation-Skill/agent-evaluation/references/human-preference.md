# Human Preference Review

## When To Use

Use human scoring for qualities that are real but not objective:

- answer usefulness
- communication style
- trust and confidence
- product judgment
- research judgment
- design taste
- explanation quality
- interaction burden

## Trace Packet

Give reviewers enough evidence to judge the run:

- original task
- key context shown to the agent
- final answer or artifact
- relevant trace excerpts
- tool/test results
- known constraints
- any automatic score summary

Avoid showing hidden expected answers unless the review is specifically about correctness against that answer.

## Default Rubric

Use 1 to 5:

- 1: unusable, misleading, or harmful
- 2: partially relevant but requires major human repair
- 3: usable with clear caveats or moderate repair
- 4: good, minor edits or checks needed
- 5: excellent, would accept or ship as-is

Normalize as:

```text
human_preference_score = score / max_score
```

## Reviewer Dimensions

Use dimensions when a single score hides tradeoffs:

- usefulness
- trust
- clarity
- concision
- taste
- interaction burden

Keep the final score explicit even when dimensions are recorded.

## Recording Scores

Interactive:

```bash
python scripts/record_human_score.py --artifact trace.md --run-id run-001 --task-id task-001 --out human_scores.jsonl
```

Non-interactive:

```bash
python scripts/record_human_score.py --run-id run-001 --task-id task-001 --score 4 --max-score 5 --notes "Good but verbose." --out human_scores.jsonl
```

Use at least two reviewers for high-stakes subjective evaluation. Report disagreement instead of averaging it away when reviewers diverge sharply.
