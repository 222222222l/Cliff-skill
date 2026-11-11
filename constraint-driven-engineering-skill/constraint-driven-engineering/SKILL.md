---
name: constraint-driven-engineering
description: >-
  Apply first-principles, constraint-driven systems thinking to concrete engineering
  decisions: define business outcomes, expose bottlenecks, transfer mechanisms from
  other fields, design distinct alternatives and falsifiable experiments, and turn
  proven improvements into reusable systems. Use for 工程化思维训练、工程优化思路发散、
  跨行业方法迁移、系统架构权衡、AI训练或推理方案、Agent原生游戏引擎、机器人/动作生成研究、
  and engineering research planning. Invoke when the user asks for systematic
  exploration or a decision, not for routine coding edits or generic explanations.
---

# Constraint-Driven Engineering

## Operating principles

Start with the measurable result, not a favored framework, model, or famous engineer.
Search for mechanisms that remove constraints, not superficial similarities between
products. Distinguish measured bottlenecks from plausible ones and experiments from
claims of success. Optimize the end-to-end objective subject to quality, latency,
budget, reliability, and maintenance constraints. Treat the simplest adequate
baseline as a genuine candidate.

Use the user's language. Scale depth to the decision: a quick design question needs
a few decisive alternatives; a costly architectural decision needs a tradeoff matrix
and experiments. Do not turn an explanation or diagnosis into implementation unless
the user authorized a change. Never run costly training or mutate live systems merely
because this skill suggests an experiment.

## Route the task

1. **Explore**: Generate mechanistically different ideas when the user requests
   brainstorming, cross-domain inspiration, or creative engineering options.
2. **Decide**: Compare feasible architectures/optimizations and recommend a bounded
   choice when the user requests tradeoffs or planning.
3. **Diagnose**: Gather available evidence and isolate bottlenecks when performance,
   reliability, cost, or quality is unexpectedly poor. Do not prescribe a low-level
   fix from a single proxy metric.
4. **Practice**: Use the 20-minute question card and weekly reflection for a user
   trying to cultivate engineering judgment. Read
   [practice-templates.md](references/practice-templates.md).
5. **Implement**: Only with explicit change authorization, make a reversible,
   testable change and verify it against the declared baseline.

For a narrow GPU/MFU/inference bottleneck, use the existing `optimize-ai-infra`
skill's diagnostic playbooks when available. For formal agent evaluation, use
`agent-evaluation`; for causal identification, use `model-causes-and-decisions`.
This skill frames the larger decision and avoids duplicating those specialties.

## Core workflow: outcome → constraint → transfer → falsification → compounding

### 1. Define the actual result

Capture, without inventing missing numbers:

- User/stakeholder and the outcome that matters (e.g., playable feature, editable
  animation, robot task success, validated quality gain).
- A baseline and outcome metric; explicit guardrails for quality, p95/p99 latency,
  GPU-hours/money, reliability, and human correction effort as applicable.
- Available levers, deadlines, reversible vs. irreversible choices, and scope of
  authorization.

Write the decision as `maximize outcome under constraints`, not as a universal
weighted score. If the proposed metric is only a proxy (loss, PR count, MFU,
benchmark pass rate), name the missing user-level acceptance test.

### 2. Map the system and find the binding constraint

Sketch the shortest useful input → transformation → state → output → feedback
chain. Inspect the critical path, data flows, ownership boundaries, failure modes,
and resource costs. Identify at most two likely limiting constraints and label
each `observed`, `inferred`, or `unknown`.

Ask in order:

1. Can the demand or step be removed, simplified, or postponed?
2. Is the problem represented in an unnecessarily difficult way?
3. Is data quality, coverage, feedback, or measurement the real bottleneck?
4. Is the critical path limited by compute, bandwidth, memory, coordination,
   human review, or organizational variation?

Use profiler, traces, real execution results, and logs when available. Do not equate
GPU utilization, a single benchmark score, or code volume with actual value.

### 3. Generate alternatives at different abstraction layers

Build at least three **mechanistically distinct** candidates for substantial
design questions, including a minimal/no-new-system baseline. Search layers:

| Layer | Transformation operators |
| --- | --- |
| Business | Eliminate, narrow, redefine acceptance, change workflow |
| Representation | Change intermediate representation, coordinates, state, or schema |
| Data/feedback | Curate, stratify, synthesize, annotate failures, change sampling |
| Algorithm | Decompose, exploit structure, approximate, change objective |
| System | Batch, cache, pipeline, parallelize, defer, replay, isolate |
| Hardware | Minimize transfers, improve locality, overlap work, tune precision |
| Organization | Standardize contracts, automate checks, document decisions |

For cross-domain transfer, explicitly map five elements:

`source problem → source constraint → successful mechanism → target analog → mismatch / test`.

Reject name-dropping as evidence. A plugin architecture solves replaceability;
data-oriented ECS solves hot-path locality. They may coexist at different boundaries,
but neither implies the other. Read
[transfer-patterns.md](references/transfer-patterns.md) for grounded mechanisms
and cases in AI, games, and robotics.

### 4. Design the cheapest discriminating test

For each serious candidate record:

1. Falsifiable hypothesis and mechanism.
2. Prediction **before** observing the data; expected result if false.
3. Smallest experiment distinguishing it from the baseline or rival.
4. Fixed comparison conditions (dataset split, workload, hardware, seeds,
   evaluator, version, warm-up, or environment as relevant).
5. Primary success metric and quality/reliability guardrails.
6. Estimated experiment cost, rollback/stop condition, and decision threshold.

Choose for **decision-relevant information per unit cost**, not the flashiest
technology. For stochastic models or agents, repeat trials and report variability;
retain negative results. Treat the evaluator itself as a fallible component and
audit for leakage, reward hacking, task underspecification, and missing edge cases.

### 5. Decide and compound the result

Separate `verified`, `promising`, `unresolved`, and `rejected` ideas. Recommend
one next action, explain the evidence and tradeoff, and state what observation
would reverse it. Prefer incremental, reversible decisions under uncertainty.

When a method works, encode it as one or more durable artifacts: contract, schema,
benchmark, data split, replay trace, test, profiler recipe, reusable module,
experiment runner, design decision, or reproducibility record. Successful
experiments are not automatically production-ready.

## Output contract

Lead with a concrete judgment. For a significant engineering decision include:

1. **Outcome & constraints**: target, baseline, non-negotiable guardrails.
2. **Bottleneck**: strongest evidence, competing explanation, unknowns.
3. **Alternatives**: 3–5 distinct mechanisms, predicted benefit, cost/risk,
   and the original source-domain mechanism if transferred.
4. **Experiment**: smallest next test, observable pass/fail criteria, resources,
   and stopping condition.
5. **Decision**: recommended next step, its reversibility, and what to record
   for future reuse.

For a practice request, use the compact daily/weekly templates instead of a
full architecture report. For an explicit implementation request, report observed
before/after measurements and any unmet acceptance criteria; never invent gains.

## Quality gates

- Can the recommended action change the requested business outcome?
- Are the top constraint and evidence grade explicit?
- Are the alternatives genuinely different mechanisms or merely new tools?
- Does the transferred method preserve the source mechanism and account for
  different target constraints?
- Could the experiment falsify the preferred proposal, and is its metric valid?
- Are cost, quality, reliability, user review, and rollback accounted for?
- Does the answer respect the user's requested scope and authorization?

Do not claim that this skill generally improves engineering outcomes without
paired representative tests against a no-skill baseline.
