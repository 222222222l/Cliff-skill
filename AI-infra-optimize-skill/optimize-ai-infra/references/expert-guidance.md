# Guidance for professional developers

## Contents

1. Evidence ladder
2. Training diagnosis
3. Inference diagnosis
4. Kernel-worthiness gate
5. Kernel bottleneck analysis
6. Custom-kernel tool selection
7. Configuration search
8. Fair baselines
9. Numerical and business validation
10. Professional response format

## Evidence ladder

Move down only when the previous layer identifies a material target:

1. End-to-end workload metrics and quality constraints.
2. Framework profiler with shapes, call counts, memory, and stacks.
3. System timeline for CPU/GPU/transfer/communication critical path.
4. Selected-kernel counters and roofline-style reasoning.
5. Code generation, layout, tile, pipeline, and instruction analysis.

Use NVTX or equivalent regions to isolate a few stable training steps, requests, or prefill/decode phases. Avoid profiling entire long-running jobs with maximum-detail counters.

## Training diagnosis

Collect:

- step-time distribution after warm-up;
- forward/backward/optimizer/data/communication/checkpoint breakdown;
- per-rank timing and scaling efficiency;
- input shapes, tokens per batch, dtype, accumulation, and compilation state;
- allocated/reserved/peak memory plus activation and optimizer-state estimates;
- graph breaks, recompilation counts, accidental casts/copies/contiguous operations;
- data-loader queue depth, worker utilization, host-to-device overlap.

For training MFU, read [training-mfu-playbook.md](training-mfu-playbook.md) before configuration or kernel recommendations. Reconcile useful model FLOPs, executed precision peak, actual completed tokens/images and the slowest-rank full-step wall; distinct model/attention/token budgets form separate cohorts. Rank GC pauses, input/frozen-encoder work, redundant timer synchronizations, and rank arrival skew before assuming NCCL or compute kernels are inherently slow.

Strategy candidates:

- fix pipeline and synchronization before GPU kernels;
- use fused framework paths, compilation, graph capture, and static shape buckets;
- sweep microbatch/useful-token budget and accumulation at fixed global useful work, accounting for variable actual samples, memory headroom, and optimizer semantics;
- select DDP/FSDP/ZeRO/tensor or pipeline parallelism from capacity, topology, and communication evidence;
- overlap collectives only after verifying correctness and the actual critical path; first separate peer arrival skew from post-arrival transfer and optimizer matrix-workload imbalance;
- treat checkpoint I/O and evaluation cadence as part of system throughput.
- validate same-shape frozen-encoder batching, bounded CPU/metadata/VAE overlap, GC policy, and native FP8 weight-scale reuse with numerical, replay, and end-to-end gates; reject extra manual caches or custom fusions with no measured whole-step gain.

## Inference diagnosis

Separate cold start, queue, tokenization, prefill, decode, sampling/postprocess, and transport. For services, sweep concurrency and prompt/output distributions while recording TTFT, ITL/TPOT, output tokens/s, queue time, p95/p99, and error rate.

Inspect:

- continuous versus static batching;
- scheduler policy and head-of-line blocking;
- prefix/prompt cache hit rate and cache correctness;
- KV-cache block utilization, paging, fragmentation, and bytes per live token;
- tensor/pipeline parallel overhead and per-rank imbalance;
- graph capture and shape-bucket coverage;
- speculative decoding acceptance and overhead where applicable;
- quantization kernels, dequantization overhead, and quality gates.

## Kernel-worthiness gate

Require all of the following before custom-kernel work:

- The operator or fusible region is materially on the end-to-end critical path.
- Its shapes, strides, dtypes, and call frequency are known and reasonably stable.
- A mature library, compiler, layout change, or graph fusion does not already solve it.
- Hardware evidence shows plausible headroom or avoidable intermediate traffic/launches.
- Equivalent semantics and numerical tolerances are defined.
- The estimated end-to-end benefit justifies development and maintenance cost.

As a practical heuristic, ignore sub-3% items unless the change is almost free or unlocks broader fusion. Analyze 3–10% items selectively. Prioritize stable items above 10%, but still calculate Amdahl limits and headroom.

## Kernel bottleneck analysis

### Memory-bound

Estimate compulsory bytes and effective bandwidth. Investigate redundant global passes, intermediate tensors, coalescing, alignment, cache reuse, layout transforms, vectorization, and fusion. Avoid adding fusion that creates spills or reduces residency enough to lose end-to-end performance.

### Compute-bound

Check math mode, accumulator precision, Tensor Core eligibility, alignment, instruction mix, tile utilization, tail waste, and library algorithm selection. For standard dense GEMM/conv, use cuBLAS/cuDNN/CUTLASS-class implementations as the default ceiling and optimize surrounding epilogues or layout costs instead.

### Latency/dependency-bound

Check grid size, work per launch, reduction dependencies, small matrix shapes, eligible warps, barriers, and serialization. Candidate remedies include batching, persistent strategies, fusion, split/combined reductions, or a different algorithm—not blindly increasing occupancy.

### Resource-bound

Check registers/thread, shared memory/block, spill traffic, active blocks, barriers, and pipeline stages. Change tile size, warps, stages, or fusion depth as a constrained search and connect every result to changed resource use.

## Custom-kernel tool selection

- **Triton**: default for PyTorch-centric elementwise fusion, norms, reductions, sampling, custom loss, quant/dequant, and many specialized kernels; strongest first choice for AI-assisted iteration.
- **TileLang**: consider for more explicit tiled scheduling, shared-memory pipelines, complex GEMM/attention/quantization, or paper-style kernel reproduction.
- **CUDA C++/CuTe DSL/CUTLASS extensions**: reserve for NVIDIA-specific instruction/layout control and a bottleneck with sufficient value.
- **cuTile**: treat as an evolving NVIDIA tile path; verify current hardware, driver, toolkit, API, and ecosystem support before committing.

Do not select a DSL before identifying the optimization layer.

## Configuration search

Define the objective over the real shape distribution, not a showcase shape. Bound the search using:

- shared-memory and register limits;
- tensor-core and vector alignment;
- enough program instances to fill the target GPU;
- expected tail/mask waste;
- numerical mode and accumulator constraints.

Record JIT/compile time separately from steady state. Report p50 and tail or variance. Explain why a winning configuration changed memory traffic, reuse, instruction choice, program count, or latency hiding.

## Fair baselines

At minimum compare semantically equivalent:

- framework eager;
- framework compiled;
- current production implementation;
- mature library/runtime candidate;
- custom implementation.

Match dtype, accumulator, TF32 policy, layout/transpose, fusion boundary, workspace, warm-up, synchronization, forward/backward scope, and all conversions. For GEMM report effective TFLOP/s; for bandwidth work report compulsory/effective bytes per second; always report end-to-end impact as the deciding metric.

## Numerical and business validation

Use high-precision or trusted references where feasible. Record max/mean/percentile absolute error, relative error with near-zero handling, NaN/Inf counts, gradient and grad-gradient checks when required, and stress shapes/values.

Then validate:

- training loss, gradient norms, convergence, final evaluation, and multiple seeds when risk warrants;
- inference logits/task metric/perplexity or domain quality, top-k agreement if meaningful, and serving error/tail latency;
- memory and compilation regressions across the supported matrix.

## Professional response format

Return:

1. objective and evidence boundary;
2. facts/inferences/unknowns;
3. critical-path classification with confidence;
4. ranked hypotheses and minimum discriminating experiments;
5. optimization candidates with estimated end-to-end ceiling, risk, and prerequisites;
6. benchmark and numerical acceptance matrix;
7. recommended next action and explicit non-goals.
