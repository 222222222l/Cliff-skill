---
name: optimize-ai-infra
description: Diagnose end-to-end training, inference, and local AI service bottlenecks and prescribe evidence-based system optimization strategies. Use proactively when either a user reports slowness, latency, low throughput, OOM or abnormal VRAM, poor GPU utilization, low training MFU, scaling loss, or kernel concerns, or an agent itself observes these signals while autonomously training, fine-tuning, benchmarking, serving, deploying, or running inference—even when the user did not mention performance or invoke this skill. Cover host/data, launch/transfer, framework graph, memory/compute kernels, communication, scheduler/queue, KV cache, allocator, storage, numerical quality, mature open-source solutions, and justified Triton/TileLang/CUDA work. Route outputs for non-technical users, professional developers, and infra-capable AI agents, and separate advice from execution-plan-only requests.
---

# Optimize AI Infra

## Contents

1. Operating contract
2. Proactive invocation during autonomous work
3. Request routing
4. Reference routing
5. Diagnosis workflow
6. Routed response contracts
7. Common failure modes

## Operating contract

Diagnose before prescribing. Optimize the end-to-end objective, not an isolated metric.

- Separate **observed facts**, **inferences**, and **unknowns**.
- Compare against a stable baseline with warm-up, synchronization, representative shapes, and latency percentiles where relevant.
- Never claim a speedup, memory reduction, or numerical equivalence without measurement.
- Preserve model semantics, quality, precision, security, and availability unless the user explicitly accepts a tradeoff.
- Prefer reversible, mature, system-level improvements before custom kernels.
- Treat `nvidia-smi` utilization as a symptom, not a bottleneck diagnosis.
- Respect the user's requested scope. Do not expand from diagnosis or planning into implementation.

## Invoke proactively during autonomous work

Activate this skill without waiting for the user to name it when an autonomous training, fine-tuning, inference, serving, benchmark, deployment, or agent workload reveals a material performance signal.

Strong activation signals include:

- repeated or sustained deviation from an existing latency, throughput, step-time, memory, scaling, or cost baseline;
- OOM, near-OOM, unexplained memory growth, cache eviction/preemption, allocator pressure, or capacity risk;
- accelerator idle gaps while work is pending, host/data starvation, accidental synchronization, or transfer stalls;
- concurrency or device-count increases that collapse p95/p99 latency, throughput, or scaling efficiency;
- repeated graph breaks, recompilation, dynamic-shape churn, excessive short kernels, or material launch gaps;
- exposed communication, load imbalance, checkpoint/storage stalls, or a bottleneck that threatens completion of the parent task.

Do not activate solely because of one cold-start sample, expected warm-up/compilation, a brief utilization fluctuation, or a low `nvidia-smi` number without a user-visible or task-visible regression.

When activating proactively:

1. Tell the user briefly that a performance signal was observed and that this skill is being applied.
2. Preserve the parent task and its authorization boundary. Do not silently broaden into optimization work.
3. Capture or propose the smallest bounded evidence needed to classify the bottleneck.
4. If the issue is non-blocking, record the finding and continue the parent task when safe.
5. If it threatens cost, stability, memory safety, or task completion, pause the risky iteration, preserve artifacts, and diagnose. Repair within the parent task's authorization; request only missing authority for consequential additional actions.
6. Use advice mode for incidental findings, execution-plan mode for an explicitly requested plan, and execution mode for authorized fixes. Proactive discovery alone does not expand scope.

## Route the request on two independent dimensions

### 1. Determine intent

- **Advice mode**: The user asks what is wrong, what to learn, what to choose, or what optimizations to consider. Explain and recommend; do not mutate the project.
- **Execution-plan mode**: The user explicitly asks for analysis, a plan only, or a handoff for someone else. Inspect evidence read-only and deliver the requested plan; do not perform planned mutations.
- **Execution mode**: The user asks to directly optimize or fix performance, or the parent task already authorizes the needed repair. Diagnose, implement the smallest justified change, and verify quality and end-to-end performance. Reuse existing authorization; obey host permission gates and ask only for additional consequential actions outside that scope.

If intent is ambiguous, default to advice mode.

### 2. Determine audience

- **Non-technical**: The user lacks profiler vocabulary, gives only experiential symptoms, or requests a simple explanation. Start with a plain-language explanation, then recommend mature open-source paths with low operational risk.
- **Professional developer**: The user supplies code, shapes, framework details, profiler output, or asks for technical tradeoffs. Give detailed layered diagnosis, experiments, metrics, and implementation candidates.
- **Infra Agent**: The output will be consumed by an advanced AI model or automation agent, or the user explicitly requests an LLM-friendly handoff. Use a strict, evidence-gated plan contract.

Infer the audience from evidence instead of asking for a self-rating. When uncertain, give a short plain-language summary followed by a clearly labeled technical appendix.

## Load only the references needed

Always read [diagnostic-framework.md](references/diagnostic-framework.md) before diagnosing.

- For non-technical users, also read [novice-guidance.md](references/novice-guidance.md).
- For professional developers or low-level optimization, also read [expert-guidance.md](references/expert-guidance.md).
- For training MFU, useful-FLOP accounting, gradient-accumulation/batch search, or multi-rank training throughput, also read [training-mfu-playbook.md](references/training-mfu-playbook.md) before prescribing or changing settings.
- For Infra Agent handoffs or execution-plan mode, also read [agent-execution-contract.md](references/agent-execution-contract.md).
- When concrete profiling commands or evidence capture are needed, read [profiling-playbooks.md](references/profiling-playbooks.md).

## Run the diagnosis workflow

### 1. Define the user-visible objective

Translate “slow” or “uses too much memory” into one or more measurable objectives:

- Training: step time, actual samples/s or useful tokens/s, training MFU with an explicit FLOP/peak convention, time-to-quality, scaling efficiency, peak allocated memory, or cost per trained token.
- Offline inference: latency, tokens/s, peak memory, energy/cost per sample, or cold-start time.
- Online service: request rate, queue time, TTFT, ITL/TPOT, p50/p95/p99 latency, output tokens/s, concurrency, error rate, or cost per request.

Record workload, hardware, software versions, shapes or sequence lengths, dtype/quantization, batch/concurrency, and quality constraints when available. Ask only for missing information that changes the next decision; otherwise state assumptions and continue.

### 2. Establish the evidence boundary

For a local project or service, inspect read-only when tools are available:

- entrypoints and benchmark scripts;
- model/runtime/serving configuration;
- dependency and hardware assumptions;
- batching, caching, precision, compilation, distributed, and data-loading settings;
- existing profiler traces, logs, tests, and quality gates.

Do not infer current runtime behavior from configuration alone. Mark unmeasured claims as hypotheses.

### 3. Decompose the system before descending to kernels

Classify the dominant loss into the narrowest supported layer:

1. workload or algorithm;
2. request queue, scheduler, batching, or service overhead;
3. CPU/Python/data/tokenization/storage;
4. transfer, synchronization, launch, graph breaks, or compilation churn;
5. framework graph/operator composition and temporary tensors;
6. GPU kernel memory, compute, latency, dependency, or resource limits;
7. multi-device communication or load imbalance;
8. capacity, allocator fragmentation, KV cache, activations, optimizer state, or workspace.

Do not use Nsight Compute before a system or framework trace identifies an important kernel.

### 4. Rank falsifiable hypotheses

For each candidate, state:

- evidence for and against;
- the minimum experiment that can accept or reject it;
- expected observation if true;
- cost and risk of the experiment;
- plausible end-to-end impact.

Prefer one-variable-at-a-time experiments. Distinguish cold start, warm steady state, throughput saturation, and tail latency. For MFU, compare only compatible model/data/precision/peak conventions, fix actual useful-work targets, predeclare complete consecutive windows, retain all slow steps, and use unprofiled full-pipeline wall time for performance claims.

### 5. Select the lowest sufficient optimization layer

Use this order unless evidence justifies skipping a layer:

1. eliminate correctness bugs, accidental copies, synchronization, leaks, and pathological configuration;
2. use a mature runtime, serving engine, fused library, compiler, or distributed strategy;
3. tune batching, concurrency, shapes, caching, precision, data movement, and overlap;
4. restructure the graph or fuse operators;
5. write or tune a custom kernel only when a stable, material bottleneck remains.

For mature-solution selection, verify current hardware, framework, model, license, numerical, and maintenance compatibility. Do not recommend a tool merely because it is popular.

### 6. Quantify value before low-level work

Use Amdahl's law for a candidate occupying fraction `p` of end-to-end time and local speedup `s`:

`total_speedup = 1 / ((1 - p) + p / s)`

Run `scripts/estimate_impact.py --share <0..1> --speedup <>=1>` when numeric inputs exist. Treat its result as an upper-bound estimate, not a benchmark.

Only recommend a custom kernel when the candidate is frequent, stable, material to the end-to-end objective, has demonstrated headroom, and has acceptable correctness and maintenance costs. Compare equivalent semantics against eager, compiled, and mature-library baselines.

### 7. Define verification and stop conditions

Require, in proportion to risk:

- correctness and numerical stress tests;
- representative shape/dtype/batch/concurrency sweeps;
- warm and cold measurements;
- p50/p95/p99 or variance, not a single fastest run;
- peak allocated and reserved memory where relevant;
- end-to-end improvement, not only microbenchmark improvement;
- regression, rollback, and quality gates.

Stop when the objective passes, the next change has poor expected value, a quality or safety gate fails, or evidence shows the bottleneck moved outside scope.

## Produce the routed response

### Advice mode

Return:

1. diagnosis confidence and evidence boundary;
2. likely bottleneck layer in audience-appropriate language;
3. ranked recommendations with expected benefit, risk, and prerequisites;
4. the next minimum measurement;
5. what not to optimize yet.

For non-technical users, put the plain-language explanation first and prefer mature open-source solutions. For professionals, include metrics, experimental design, baselines, numerical constraints, and kernel-level options where justified.

### Execution-plan mode

For an explicit handoff or plan-only request, return analysis and the plan schema in [agent-execution-contract.md](references/agent-execution-contract.md). For authorized execution, carry out the applicable phases and report observed results, artifacts, acceptance gates, rollback, and unresolved constraints. Make every action traceable to a hypothesis.

## Avoid common failure modes

- Do not equate low GPU utilization with a slow kernel.
- Do not optimize the largest allocation without distinguishing active tensors, reserved allocator memory, workspace, and non-framework allocations.
- Do not compare fused and unfused implementations with different semantics.
- Do not hide precision or quality loss inside a performance recommendation.
- Do not recommend CUDA/Triton merely because the workload uses a GPU.
- Do not tune one favorable shape while ignoring the production distribution.
- Do not list every possible optimization. Rank a small set by evidence and expected end-to-end value.
- Do not use nominal batch, requested tokens, padded/dummy work, frozen-encoder FLOPs, or the wrong dense/sparse/precision peak to inflate training MFU.
- Do not sum ranks' NCCL wait or CPU/CUDA scope durations as additive wall time; inspect straggler arrival skew and overlapping work.
- Do not turn a local kernel or fresh-only short benchmark into a production MFU, long-run memory, convergence, or resume claim.
