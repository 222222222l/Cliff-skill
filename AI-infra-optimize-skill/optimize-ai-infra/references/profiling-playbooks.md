# Profiling playbooks

## Contents

1. Benchmark discipline
2. PyTorch framework profile
3. PyTorch memory evidence
4. Nsight Systems candidate
5. Nsight Compute candidate
6. Training baseline record
7. Inference-service baseline record
8. Minimal experiments by hypothesis

Use these as starting points and adapt to the actual framework, versions, OS, and permissions. Keep captures bounded. Do not run heavy profilers against production without approval.

## Benchmark discipline

- Warm up model, allocator, libraries, JIT, and graph capture.
- Synchronize accelerators around manual timers.
- Separate compile/load/cold latency from warm steady state.
- Use representative shapes, prompt/output lengths, batch, and concurrency.
- Report median and p95/p99 or variance; never use the fastest single run.
- Preserve precision, quality, and semantics across baselines.

## PyTorch framework profile

Use a small stable region:

```python
import torch
from torch.profiler import ProfilerActivity, profile, record_function

for _ in range(5):
    run_one_unit()
torch.cuda.synchronize()

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    record_shapes=True,
    profile_memory=True,
    with_stack=True,
) as prof:
    with record_function("target_region"):
        for _ in range(5):
            run_one_unit()

torch.cuda.synchronize()
print(prof.key_averages().table(sort_by="self_cuda_time_total", row_limit=30))
```

Interpret `self` time, total time, call count, shapes, memory, and child kernels together. A high-level op with high total time may only wrap expensive children.

## PyTorch memory evidence

Start with:

```python
torch.cuda.reset_peak_memory_stats()
run_target()
torch.cuda.synchronize()
print("allocated", torch.cuda.memory_allocated())
print("reserved", torch.cuda.memory_reserved())
print("peak", torch.cuda.max_memory_allocated())
```

For allocation history, use the version-appropriate PyTorch memory-history and snapshot APIs, then inspect the snapshot with the official visualizer. Verify APIs against the installed PyTorch version before embedding them in project code.

## Nsight Systems candidate

Use a dedicated short script or NVTX-delimited region:

```text
nsys profile --trace=cuda,nvtx,osrt,cublas,cudnn --output=<report> python <bounded_profile_script.py>
```

Look for GPU gaps, CPU launch behavior, copies, synchronization, library calls, collectives, and the critical path. Limit training to a few stable steps and serving to a small bounded request set.

## Nsight Compute candidate

Run only after identifying a high-value kernel:

```text
ncu --set full --kernel-name regex:<escaped_kernel_name> --launch-count 1 python <bounded_kernel_script.py>
```

Start with duration, roofline/compute and memory throughput, registers, shared memory, achieved occupancy, eligible warps, spills, and top stall categories. Avoid scanning the full application with `--set full`.

## Training baseline record

Record:

```text
hardware and topology:
framework/CUDA/library versions:
model and precision:
global/micro batch and accumulation:
sequence or input shape distribution:
compile/graph/checkpointing/distributed settings:
warm-up units and measured units:
step p50/p95:
tokens or samples per second:
forward/backward/optimizer/data/communication/checkpoint breakdown:
allocated/reserved/peak device memory:
quality/loss baseline:
```

## Inference-service baseline record

Record:

```text
model/runtime/quantization:
hardware and replica topology:
prompt and output length distribution:
concurrency and arrival pattern:
cold-start latency:
queue p50/p95/p99:
TTFT p50/p95/p99:
ITL or TPOT p50/p95/p99:
request and output-token throughput:
error rate/timeouts:
KV-cache usage/hit or eviction behavior:
allocated/reserved/peak memory:
task/model-quality baseline:
```

Run a concurrency sweep that includes underload, near-saturation, and overload only when the environment is safe and the user authorizes load generation.

## Minimal experiments by hypothesis

| Hypothesis | Controlled experiment | Supporting result |
|---|---|---|
| data input bottleneck | replace input path with preloaded representative tensors | step time drops and GPU gaps shrink |
| Python/launch overhead | compare eager with supported compile/graph path | gaps/kernel count fall and end-to-end improves |
| transfer/sync overhead | remove or batch host reads/copies in a controlled branch | critical-path copies/syncs shrink |
| memory capacity dominated by activations | sweep microbatch/checkpointing with same effective batch | peak allocated memory follows activation prediction |
| KV cache dominates | sweep live tokens/concurrency | memory grows near predicted bytes per token |
| communication bottleneck | compare 1/N-device and inspect overlap/per-rank trace | scaling loss aligns with collectives/imbalance |
| one kernel is material | isolate equivalent microbenchmark plus selected counters | local share and headroom survive isolation |

Use each result to update confidence; do not jump directly from a supporting result to implementation when a cheaper alternative remains untested.
