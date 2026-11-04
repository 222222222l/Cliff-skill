# AI Infrastructure Performance Diagnosis Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `AI-infra-optimize-skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

`optimize-ai-infra` structures diagnosis of training, inference, and serving performance. It starts with a reproducible end-to-end baseline and investigates data, host, transfer, compute, communication, and memory paths through discriminating experiments.

The deliverable is diagnostic advice or an execution plan, not an acceleration library. The current diagnostic/planning modes perform read-only analysis rather than modifying code, configuration, or running services.

## Scope

Training steps, useful throughput, multi-GPU scaling; inference TTFT, ITL/TPOT, p95/p99; OOM, KV cache and allocation; data loading, compilation/graph breaks, CPU dispatch, exposed NCCL time, slow ranks, storage, and checkpoint stalls.

Established compilers, runtimes, and serving systems are evaluated first. Operator or custom-kernel work requires critical-path evidence. GPU utilization alone is not a bottleneck diagnosis.

## Method

1. Define the user-visible objective, workload, hardware, and numerical/quality constraints.
2. Record steady-state baselines and specify falsifiable hypotheses and minimal discriminating experiments.
3. Use Amdahl's bound to constrain the value of local optimization.
4. Define end-to-end performance, memory, correctness, and quality acceptance, with stop/rollback conditions.

Outputs range from concise beginner measurements to developer profiling paths and machine-readable YAML plans with permissions, artifacts, and gates. See [SKILL.md](optimize-ai-infra/SKILL.md) and [references](optimize-ai-infra/references/).

## Install and use

Place `optimize-ai-infra/` in the host's supported Skill directory and refresh discovery. Preserve a backup of an existing version rather than overwriting it blindly.

```text
Use $optimize-ai-infra to diagnose 8-GPU DDP scaling and propose
the smallest useful measurement and an execution plan.
```

`agents/openai.yaml` allows host-driven implicit selection for sustained regressions. This is not an OS event hook or a guaranteed every-N-steps check. Cold starts, normal warm-up, and isolated fluctuations without user-visible regression are insufficient triggers.

## Validation utilities

From the repository root:

```bash
python optimize-ai-infra/scripts/validate_skill.py optimize-ai-infra
python optimize-ai-infra/scripts/estimate_impact.py --share 0.25 --speedup 2 --current-time-ms 100
```

Structural validation checks package/reference integrity; the Amdahl output is a conditional estimate. Performance claims require matched workloads, precision, batches, concurrency, and hardware. Microbenchmarks or favorable shapes do not establish general gains. Report quality costs from quantization, lower precision, and offloading separately.

The repository provides no universal cross-workload speedup estimate. No top-level `LICENSE` is currently supplied.

## Collection-specific training-MFU extension

[training-mfu-playbook.md](optimize-ai-infra/references/training-mfu-playbook.md) adds effective-FLOP and hardware-peak definitions, prespecified complete measurement windows, microbatch/gradient-accumulation search, frozen-encoder/data overlap, GC/slow-rank diagnosis, and FP8-cache validation. Report MFU with workload, precision, peak definition, and timing window; MFU alone is not quality or cost benefit. This extension does not imply the standalone repository contains the same version.
