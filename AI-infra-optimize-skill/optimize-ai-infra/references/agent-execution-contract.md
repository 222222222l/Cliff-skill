# Infra Agent execution-plan contract

## Contents

1. Purpose
2. Planning rules
3. Required machine-first schema
4. Phase ordering
5. Command quality contract
6. Optimization task contract
7. Handling insufficient evidence

## Purpose

Produce an auditable handoff or guide authorized implementation. In explicitly requested execution-plan mode, analyze and plan only. In execution mode, continue through implementation and verification within the user's authorization and host permissions.

## Planning rules

- Inspect local files, configuration, logs, tests, and existing traces read-only when available.
- Preserve the parent task and record whether the trigger came from the user or from an agent-observed performance signal.
- Continue the parent task after recording a non-blocking issue when safe; stop before the next expensive iteration when capacity, cost, stability, or completion is at risk.
- Never invent hardware, versions, traffic, shapes, measurements, or profiler results.
- Encode missing evidence as an acquisition task, not a guessed fact.
- Make each optimization action depend on a hypothesis and a gate.
- Order work from lowest-risk system changes to lower-level implementation.
- Keep commands as candidates with working directory, permissions, expected artifacts, and timeout/cost notes.
- Reuse authorization for source/config changes and necessary bounded verification. Obtain missing approval at the action boundary for additional installs, disruptive restarts, costly benchmarks, production changes, or destructive actions outside the authorized scope.
- Define rollback before any future mutation.
- Stop when the target passes; do not continue polishing for its own sake.

## Required machine-first schema

Use YAML when the output will be consumed directly by another model. Follow it with a short human summary only if useful.

```yaml
performance_plan:
  version: 1
  mode: execution-plan-only | execution
  audience: infra-agent
  trigger:
    source: user-request | agent-observed
    signals: []
    impact_on_parent_task: informational | degrading | blocking | unsafe
    parent_task: unknown
  workload:
    kind: training | offline-inference | online-inference | mixed
    entrypoints: []
    target_hardware: unknown
    software_stack: []
  objective:
    primary_metric: unknown
    target: unknown
    quality_constraints: []
    operational_constraints: []
  scope:
    in_scope: []
    out_of_scope: []
    allowed_now: [] # Populate from current user authorization and host permissions.
    prohibited_now: [] # Plan-only requests exclude planned mutations.
  evidence:
    facts: []
    inferences: []
    unknowns: []
    existing_artifacts: []
  baseline:
    protocol: []
    metrics: []
    representative_cases: []
    cold_warm_split: true
  hypotheses:
    - id: H1
      layer: service | host | runtime | graph | kernel | communication | memory | storage
      claim: ""
      evidence_for: []
      evidence_against: []
      confidence: low | medium | high
      discriminator:
        action: ""
        expected_if_true: ""
        reject_if: ""
        cost_risk: ""
  phases:
    - id: P0
      name: acquire-baseline
      depends_on: []
      hypothesis_ids: [H1]
      actions: []
      candidate_commands:
        - command: ""
          cwd: ""
          permission: read-only | authorized-mutation | approval-required
          expected_artifact: ""
          timeout_or_cost: ""
      acceptance_gate: ""
      rollback: not-applicable
      stop_conditions: []
  candidate_changes:
    - id: C1
      layer: ""
      rationale: ""
      prerequisites: []
      estimated_impact: unknown
      impact_basis: measurement | amdahl-bound | hypothesis
      numerical_or_quality_risk: ""
      verification: []
      rollback: ""
  validation_matrix:
    correctness: []
    numerical_quality: []
    performance: []
    memory: []
    operational: []
  final_gates:
    success: []
    reject_change: []
    stop_work: []
  approvals_required: []
  handoff_next_action: ""
```

Omit empty optional candidates, but never omit trigger, facts/inferences/unknowns, scope, baseline protocol, hypotheses, gates, and approvals.

## Phase ordering

Use this default sequence and remove irrelevant phases:

1. **P0 — Reproduce and baseline**: stable workload, warm/cold split, metrics, versions, hardware, quality baseline.
2. **P1 — Locate the critical path**: framework table and short system timeline; memory snapshot if needed.
3. **P2 — Run discriminating experiments**: one-variable tests for the top hypotheses.
4. **P3 — Test mature system candidates**: configuration/runtime/library/compiler/batching/precision/distributed changes.
5. **P4 — Isolate operator or kernel**: only after a material candidate survives; capture selected-kernel evidence.
6. **P5 — Implement candidate**: execute when already authorized; defer in plan-only mode. Preserve baseline evidence and use the smallest reversible slice.
7. **P6 — End-to-end validate**: supported matrix, quality, tail, memory, regression, and rollback rehearsal.

Execution-plan mode normally ends after specifying P0–P6; it does not execute P5.

## Command quality contract

For each candidate command:

- use an exact working directory;
- constrain the capture to a small region or bounded duration;
- state whether it is read-only or needs approval;
- state the output artifact and how it changes the next decision;
- avoid placeholders that look runnable unless clearly marked;
- avoid destructive cleanup, hidden package installation, or unbounded profiling.

## Optimization task contract

Every future implementation task must include:

- one bottleneck hypothesis;
- files/components allowed to change;
- behavior and numerical invariants;
- a failing or baseline test/benchmark first;
- expected artifact and measurement;
- acceptance threshold;
- rollback path;
- stop condition.

Prefer tracer-bullet slices. Example:

```yaml
task:
  id: C2
  hypothesis: excessive launch and intermediate-memory traffic in residual-plus-norm region
  allowed_files: [path/to/operator.py, tests/test_operator.py, benchmarks/bench_operator.py]
  invariants: [same supported shapes, defined fp16/bf16 tolerance, backward preserved]
  baseline_first: true
  acceptance:
    correctness: all targeted tests pass
    microbenchmark: p50 improves by at least the approved threshold on representative shapes
    end_to_end: target metric improves without p95 or memory regression
  rollback: revert C2 files/config only
  stop: reject if compiled baseline already meets the target or numerical gate fails
```

## Handling insufficient evidence

Do not emit a fake optimization plan. Emit an evidence-acquisition plan with at most three top hypotheses. State which artifact will unlock the next stage. If the project is unavailable, provide portable commands as candidates and mark every environment-dependent value as unknown.
