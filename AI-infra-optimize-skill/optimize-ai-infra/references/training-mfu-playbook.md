# Training MFU optimization playbook

## Contents

1. Metric and comparability contract
2. Reproducible full-pipeline baseline
3. Rank-aware critical-path triage
4. Optimization experiment ladder
5. Controlled experiment design
6. Correctness, durability, and rejection gates
7. Reporting template

## 1. Metric and comparability contract

Model FLOPs Utilization (MFU) is a ratio of *useful model work* to the device's stated theoretical peak over elapsed time. State the accounting convention before calculating or comparing it.

MFU = actual useful trainable-model FLOPs in the window / (continuous window wall seconds × device count × dense peak FLOP/s per device).

- Record the exact numerator definition: model family, forward/backward factors, trainable/frozen boundaries, attention visibility, masks, actual image/text lengths, padding, alignment dummies, recomputation, and atypical first-layer input gradients. A transformer shorthand such as 6ND is an estimate, not an exact formula for variable-resolution DiT or attention-heavy workloads.
- Count the work of actually *completed* optimizer updates, not requested batch size, queued inputs, prefetched samples, nominal DeepSpeed batch fields, or discarded retries. Use actual image counts, useful token counts, and per-sample attention pair counts when workloads vary.
- Include the full critical-path wall time: input/CPU work, transfers, frozen VAE/text encoders, forward, backward, optimizer, EMA, collectives, coordination, accounting, and logging. Distinguish checkpoint/sampling policy and whether these events fall inside the window. Do not sum overlapping stage spans to reconstruct wall time.
- Use an explicit *dense* hardware peak for the executed math mode and actual GPU count. Record GPU model, peak-source/version, FP8/BF16/TF32 policy, and whether sparse peak is excluded. Changing peak convention changes MFU even if seconds/update does not.
- Separate MFU (defined useful model FLOPs) from HFU or executed hardware FLOPs, achieved GEMM TFLOP/s, GPU busy percentage, useful tokens/s, images/s, and time-to-quality. HFU can rise through recomputation without speeding the useful workload. A higher MFU can result from numerator changes without a higher useful-token throughput.
- Compare MFU percentages as a causal optimization only when the numerator's semantics, model, data/shape distribution, peak convention, and complete-window scope are aligned. If model width, frozen encoder, attention policy, objective, or useful-token budget changes, report separate cohorts and normalized throughput; do not splice their percentages into one improvement curve.

Minimum scorecard fields:

| Category | Required evidence |
|---|---|
| Work | trainable model/parameter count; exact useful FLOPs definition and total; completed updates, images, useful tokens; image/text shape distributions |
| Hardware | GPUs and topology; dense peak source and precision; memory capacity; software/compiler/library versions |
| Schedule | global useful work target, microbatch or token budget, gradient accumulation, data plan, active checkpoint/sampling/logging policy |
| Timing | predeclared contiguous step range; global/slowest-rank elapsed wall, step distribution, tokens/s, images/s, MFU |
| Risks | allocated/reserved peak memory, failure/skip count, numerical/quality results, checkpoint and replay behavior |
| Provenance | source/config revisions, seeds, data identity, cache/JIT state, repetitions, profiler instrumentation |

## 2. Reproducible full-pipeline baseline

1. Fix a representative real-data workload. Use identical model semantics, precision policy, seed/data plan and effective useful-work target when comparing configurations; record variable actual samples.
2. Separate process/model startup and initial compilation from selected warm windows. Predeclare a continuous window (for example, N completed updates after warm-up) before running. Retain every slow step inside it, including surprise JIT/autotune, GC and rank stalls; never retrospectively trim outliers to create a flattering steady state.
3. Report both all-in training throughput and, where needed, windows that include checkpoint/sampling/evaluation cadence. Do not claim production throughput from a fresh-only benchmark that disabled these features.
4. Take repeat runs in alternate or balanced order (such as OFF–ON–ON–OFF) for small differences. Report individual runs, variability and confounders; two repeats are not a universal confidence interval.
5. Do not run full CPU/CUDA profilers or tensor-by-tensor correctness scans in the throughput comparison. Run short, separate all-rank traces with aligned clocks and annotate trace-induced GC/compilation perturbations.
6. Use exact measured dense peak, actual useful FLOPs, and elapsed wall. Reconcile per-rank step/optimizer/EMA counters, data consumption ledger, and maximum-rank timing.

## 3. Rank-aware critical-path triage

Profile a short *representative* set of ranks and stable steps. Correlate CPU runtime APIs, CUDA kernels, collectives and application spans on the same time base.

- Locate GPU idle intervals while pending work exists. Attribute them to upstream CPU/data submission, Python GC, synchronization, compile/autotune, I/O, frozen encoder, or another rank; do not diagnose from nvidia-smi alone.
- For each collective, match the same process group, sequence and payload across ranks. Split first-to-last arrival skew from last-arrival-to-all-complete time. A long collective span with a very short post-arrival tail indicates straggler wait, not necessarily slow network transport.
- Inspect the slowest rank. An optimizer that partitions by parameter bytes may not balance matrix-specific work (for example, orthogonalization). Estimate compute cost for each owned matrix; do not rebalance solely by matrix count or tensor element count.
- Separate CUDA Event spans, GPU kernel duration, CPU launch/submission time and synchronization wait. Event spans can include host enqueue gaps. CPU synchronization can overlap work already running on GPU; avoid double-counting.
- Audit framework or training-engine throughput timers that silently synchronize every microbatch. Disable only demonstrably redundant timer syncs, never correctness- or lifetime-critical synchronization, and verify with unprofiled whole-step repeats.
- Inspect long Python GC pauses and process/RSS trends. Test freeze, threshold or scheduled-collection policies in isolated trials with long-run memory and cycle-leak checks. Never globally disable collection just to win a short benchmark.
- Decompose data.next / queue-wait from VAE encode, text encoder, metadata claim/read, commit, HtoD/pinning, and rank rendezvous. A broad data_wait span may include GPU work or peer waiting; it is not automatically CPU starvation.

## 4. Optimization experiment ladder

Test one bounded hypothesis at a time. This is a prioritization ladder, not a checklist to enable every feature.

### A. Useful-work packing and accumulation

- Sweep microbatch size or useful-token budget against gradient accumulation while keeping the *same global useful-work target* and optimizer semantics.
- Track per-micro packing efficiency, actual image/text lengths, kernel work, launch count, peak allocated/reserved memory, and rank imbalance.
- Expect a non-monotonic optimum: more work per micro can amortize launches, but can hurt occupancy, temporary memory, attention complexity or long-tail shapes. A partial run near full VRAM or a hung collective does not establish a sustainable optimum or prove CUDA OOM.
- Preserve loss scaling when actual sample count varies and framework nominal batch fields assume fixed microbatch sizes.

### B. Data and frozen-encoder critical path

- Try representative inputs already resident in memory as a discriminator; only then tune CPU decoding/resize, tokenization, queue depth and prefetch.
- Batch frozen vision encoders by compatible shape where valid; preserve original per-sample indexing, no silent resize/padding, and a numerical comparison against a high-precision reference. If batch-size changes FP16/BF16 roundoff, record failed gates and scope of any accepted tolerance.
- Compare CPU versus GPU encoder placement on the *full* critical path; GPU encoding can speed local inference yet serialize with DiT. Test an independent stream or overlap only with bounded workspace, explicit dependencies, and input lifetime management.
- Overlap CPU metadata claim/read, tokenization and future VAE work with current microbatches or across steps when measured stalls justify it. Bound lookahead; preserve FIFO ordering, data pin/unpin, retry/abort, resume and optimizer-success commit semantics. Prefetch is not training consumption.
- Pin processes and workers to suitable CPU cores only after measuring scheduling contention. A machine-specific affinity profile must not become a portable default. Stop increasing workers once queue waits are negligible.

### C. Compilers, graph and shape buckets

- Inspect short-kernel launch gaps, graph breaks, recompiles and library-specific JIT/autotune buckets. Torch compiler counts may not include third-party attention or quantization kernels.
- Use validated compile scopes, graph capture, stable shape buckets, and supported fused libraries. Prewarming observed rare buckets can reduce first-hit stalls but cannot guarantee unseen dynamic lengths will never compile.
- Track cold/warm behavior and cache fingerprints separately. Cache lookup is not proof of a compile, and all nested JIT/autotune spans must not be added as independent losses.

### D. Precision and quantization work

- Validate mixed BF16/FP8 precision at model-specific sensitive layers, using loss/gradient/quality gates; do not assume every linear supports the same quantized recipe.
- If weight parameters are unchanged across gradient-accumulation micros, test reuse of *native* FP8 weight quantization workspace within one optimizer update. Refresh at the required boundary; do not reuse stale scales across updates or incorrectly cache activation/gradient quantization.
- Compare the exact native recipe, forward/backward, bytes/scales and master/optimizer/EMA updates on representative layers before a full model trial.
- Reject a custom activation-quantization fusion if paired microbenchmarks lose, even if it reduces the number of kernels or launch calls. Kernel-count reduction is not a performance guarantee.

### E. Attention and small operator candidates

- Select attention backend by real sequence-length, mask, layout and forward-plus-backward distribution, including gather/reorder/index costs and numerical visibility. One backend may win at short sequences and lose at long ones; changing attention semantics invalidates an MFU comparison.
- Test fused norm/RoPE/modulation or custom kernels only after a critical-path share is demonstrated. Include noncontiguous layouts, explicit BF16 rounding, backward, and real optimizer-step results.
- Prefer native library/JIT caches unless an extra manual cache delivers repeatable whole-call or end-to-end benefit. A microsecond reduction in CPU submit cost may disappear behind GPU backpressure.

### F. Distributed optimizer and communication

- Inspect overlap of gradient reduction and backward, per-rank payload/arrival skew, large AllGather transfer, and matrix-workload imbalance in preconditioning or optimizer epilogues.
- Model a rebalance candidate's maximum whole-step headroom from *max minus mean* rank work, not from the wait experienced by the fastest rank. Repartitioning parameter owners can affect checkpoint layout and state semantics; do not apply without reshard/recovery validation.
- Keep collective correctness, identical ordering and zero skipped optimizer/EMA updates as hard gates.

## 5. Controlled experiment design

For each candidate, write an experiment card with:

1. Exact hypothesis and critical-path evidence;
2. One controlled change, fixed workload and source/config fingerprints;
3. Baseline and candidate predeclared windows, repetitions and monitoring overhead;
4. Expected changes in whole-step seconds, useful tokens/s, images/s, MFU, memory and quality;
5. Numerical, recovery and failure gates;
6. Decision: **accepted**, **rejected**, **inconclusive**, or **not yet executed**.

A staged combined pipeline may improve end-to-end MFU; report its *cumulative* result and identify which intermediate comparisons are not single-variable causal evidence. Do not represent a later experiment's expected benefit as measured.

## 6. Correctness, durability, and rejection gates

Reject or pause when:

- the throughput trial changes token semantics, model math, precision peak or optimizer objective without a new comparison cohort;
- compilation, profiler overhead, first-run caches, checkpoint/sampling exclusions, or missing slow steps make the window incomparable;
- a candidate is faster locally but loses in end-to-end wall time, useful-token throughput, stability or cost;
- peak memory approaches capacity without headroom for rare long sequences, or a stalled trial has no completed benchmark window;
- cached FP8 state, fused forward/backward, attention masking or batched encoding fails its declared numeric/quality gate;
- async prefetch violates exactly-once consumption, checkpoint resume, source lifecycle, or abort semantics;
- GC/timer/affinity changes have not passed sustained-memory and production-duration checks.

Microbenchmarks, smoke tests and complete training runs answer different questions. A finite short run is not convergence equivalence; a valid local kernel result is not an MFU improvement; fresh-only throughput is not a production-resume guarantee.

## 7. Reporting template

Return a compact evidence table with columns:

Candidate | Workload and changed variable | Baseline/candidate full-step window | MFU and useful throughput | Memory and numerical gates | Confidence | Adopt/reject/next test.

Then state: (a) the critical-path root cause, (b) the best *measured* configuration for the stated objective, (c) the remaining bottleneck and maximum plausible whole-step benefit, (d) what must be revalidated for a different GPU, model, shape distribution, precision or production checkpoint path.

Never hardcode someone else's device peak, microbatch setting, tuning threshold, JIT cache or compiler version as a universal recommendation.
