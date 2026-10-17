# Diagnostic framework

## Contents

1. Evidence discipline
2. End-to-end decomposition
3. Training-specific decomposition
4. Inference-service decomposition
5. Bottleneck signatures
6. Memory decomposition
7. Decision tree
8. Prioritization and validation

## 1. Evidence discipline

Use four labels consistently:

- **Fact**: directly observed in a trace, log, benchmark, configuration, or code path.
- **Inference**: the best current explanation of facts.
- **Unknown**: information required to choose between live hypotheses.
- **Decision**: an action justified by facts and an explicit tradeoff.

Measure the same semantic workload before and after. Control warm-up, CUDA synchronization, compiler/JIT time, random seeds where relevant, input distribution, background load, power/clock state, and service concurrency. Report the distribution, not the minimum.

## 2. End-to-end decomposition

Model total time as:

`T_total = T_queue + T_CPU/data + T_launch + T_transfer + T_kernel + T_comm + T_sync + T_storage`

These terms can overlap. Use a timeline to find the critical path rather than summing profiler totals blindly.

Model peak device memory as:

`M_peak = parameters + optimizer + gradients + activations + KV_cache + temporary_workspace + allocator_fragmentation + external_allocations`

Optimization layers, from outside inward:

| Layer | Typical evidence | Typical strategy |
|---|---|---|
| Workload/algorithm | unnecessary tokens, resolution, steps, model size | reduce work, cache, distill, choose fit-for-purpose model |
| Service/scheduler | queue time, poor batching, head-of-line blocking | continuous batching, admission control, prefix cache, routing |
| Host/data | GPU gaps aligned with CPU/data work | parallel loading, tokenization cache, pinned memory, preprocessing |
| Runtime/framework | graph breaks, repeated compile, dispatch gaps | compilation, graph capture, shape bucketing, fewer sync points |
| Operator/graph | many small ops, temporary tensors | fused library or operator fusion |
| Kernel | one or a few important kernels | layout/tile/pipeline/kernel work |
| Communication | NCCL/collectives on critical path | overlap, sharding, topology-aware strategy, fewer messages |
| Capacity/memory | OOM, fragmentation, cache pressure | precision, checkpointing, offload, paging, allocator/cache policy |

## 3. Training-specific decomposition

Track at least:

- data wait versus GPU-active time;
- forward, backward, optimizer, gradient synchronization, and checkpoint I/O;
- tokens/s or samples/s and step-time distribution;
- achieved batch size and gradient accumulation;
- activation, gradient, parameter, and optimizer-state memory;
- compute/communication overlap and per-rank imbalance;
- recompilations, graph breaks, dynamic shapes, and accidental synchronization.

Common training hypotheses:

| Symptom | Candidate cause | Minimal discriminator |
|---|---|---|
| periodic GPU idle gaps | data loader or checkpoint I/O | replace input with preloaded synthetic batch; disable checkpoint for a short controlled run |
| backward dominates | expected math, unfused ops, recompute, or communication | split NVTX/profiler regions and inspect collective overlap |
| multi-GPU scaling collapses | collectives, imbalance, small per-GPU work | compare 1/2/N-device efficiency and per-rank timelines |
| memory grows each step | retained graph/tensors or cache growth | inspect live allocation history and object retention |
| memory high but stable | model state, activations, workspace, or reserved pool | calculate theoretical state sizes and compare allocated/reserved |

## 4. Inference-service decomposition

For generative serving, separate:

- queue latency;
- tokenization and request preprocessing;
- model load/cold start;
- prefill time and TTFT;
- decode inter-token latency (ITL/TPOT);
- output-token throughput;
- batching/scheduling efficiency;
- KV-cache capacity, fragmentation, paging, and hit rate;
- postprocessing and network serialization.

Measure at realistic prompt/output-length distributions and concurrency. A single-request microbenchmark does not predict serving throughput or tail latency.

Common inference hypotheses:

| Symptom | Candidate cause | Minimal discriminator |
|---|---|---|
| high TTFT, normal ITL | queue, tokenization, prefill, cold compile | split queue/preprocess/prefill timers and compare warm requests |
| normal TTFT, slow token stream | decode memory bandwidth, tiny GEMMs, scheduler | compare batch/concurrency and inspect decode timeline |
| throughput rises but p99 explodes | saturation or head-of-line blocking | concurrency sweep with queue-depth and per-stage timing |
| OOM at concurrency | KV cache or workspace, not just weights | estimate bytes/token and observe memory versus live tokens |
| first request slow only | model load, JIT, graph capture, cache coldness | report cold and warm separately |

## 5. Bottleneck signatures

Use multiple pieces of evidence. No single counter is definitive.

### CPU/data-bound

- GPU timeline contains gaps while CPU/data workers are active.
- Synthetic/preloaded inputs materially improve end-to-end time.
- A faster GPU does not improve throughput proportionally.

### Launch/dispatch-bound

- Many very short kernels and visible launch gaps.
- Small shapes or Python loops dominate.
- Fusion, graph capture, or compilation reduces kernel count and gaps.

### Transfer/synchronization-bound

- HtoD/DtoH copies or synchronization lie on the critical path.
- `.item()`, `.cpu()`, logging, device mismatch, or implicit copies correlate with gaps.

### Memory-bandwidth-bound kernel

- Low arithmetic intensity and high sustained memory throughput.
- Compute utilization is modest; reducing bytes or fusing passes helps.
- Typical candidates include elementwise, norm, softmax, embedding, transpose, and quantization.

### Compute-bound kernel

- High arithmetic intensity and compute/Tensor Core throughput near the practical ceiling.
- Dtype, alignment, tile shape, and mature GEMM/attention libraries dominate choices.
- Standard large dense GEMM is rarely a good first custom-kernel target.

### Latency/parallelism/dependency-bound kernel

- Memory and compute throughput are both low.
- Work is too small, dependency chains are long, reductions serialize, or eligible warps are scarce.
- More occupancy is useful only if it hides the limiting latency.

### Resource-bound kernel

- Registers, shared memory, spills, or barriers limit resident work.
- Reducing a resource is valuable only when the new configuration improves measured latency.

### Communication-bound

- Collectives occupy the critical path and do not overlap useful work.
- Per-rank timelines or payload sizes reveal imbalance or small-message overhead.

## 6. Memory decomposition

Distinguish:

- active framework allocations;
- allocator-reserved memory;
- temporary library workspace;
- non-framework CUDA allocations;
- long-lived cache, including KV cache;
- fragmentation versus a true live-set increase.

For training, estimate expected bytes for weights, master weights, optimizer states, gradients, and saved activations. For inference, estimate weights plus KV cache as a function of live tokens and concurrency. Do not call reserved memory a leak without allocation history.

## 7. Decision tree

```text
Is the user-visible baseline valid and repeatable?
├─ No: repair measurement first.
└─ Yes: is the accelerator continuously on the critical path?
   ├─ No: inspect queue, CPU/data, transfers, synchronization, launch, storage.
   └─ Yes: do a few kernels/operators dominate?
      ├─ No: inspect graph composition, batching, fusion, communication, algorithmic work.
      └─ Yes: is a dominant item a mature library operation?
         ├─ Yes: verify semantics/config/layout and test mature alternatives first.
         └─ No or fused opportunity: profile the selected kernel.
            ├─ memory-bound: reduce bytes, improve access, fuse.
            ├─ compute-bound: improve math path/tensor-core use or avoid custom work.
            ├─ latency/dependency-bound: increase useful parallelism or restructure.
            └─ resource-bound: trade tile/fusion depth against registers/shared memory.
```

## 8. Prioritization and validation

Rank candidates by:

`priority ≈ end_to_end_share × plausible_headroom × recurrence × confidence / (effort × risk × maintenance)`

Use the formula to structure judgment, not to fabricate precision.

Validate changes at four levels:

1. local numerical correctness and edge cases;
2. representative microbenchmark distribution;
3. end-to-end workload objective;
4. business/model quality and operational stability.

For training, include loss/gradient behavior and downstream quality where the change affects numerics. For inference, include logits or task metrics, output consistency targets, error rate, and tail latency. Revert or reject a change that wins a microbenchmark but fails an end-to-end or quality gate.
