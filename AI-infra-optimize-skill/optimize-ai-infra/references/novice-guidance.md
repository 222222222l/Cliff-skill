# Guidance for non-technical users

## Response order

Always answer in this order:

1. **Plain-language explanation**: describe what the symptom means using an everyday analogy.
2. **What is known versus guessed**: name the evidence gap without blaming the user.
3. **Safest next measurement**: give one small action, not a profiler curriculum.
4. **Ranked mature solutions**: recommend at most three paths matched to the symptom.
5. **Tradeoffs and safety**: state quality, compatibility, privacy, and rollback implications.
6. **What not to do yet**: usually custom CUDA/kernel work until evidence supports it.

Example framing:

> GPU utilization is like seeing how often a kitchen stove is lit. It does not tell us whether time is lost waiting for ingredients, cooking, moving dishes, or serving customers. We first need to separate waiting time from actual model computation.

Avoid unexplained terms. When a technical term is necessary, define it in one sentence and connect it to the user's symptom.

## Mature-solution ladder

Recommend a project only after checking hardware, OS, model architecture, framework, license, quality tolerance, and maintenance status. Prefer documented releases over experimental branches.

### Measurement and visibility

- **PyTorch Profiler**: first framework-level view for PyTorch training and inference.
- **PyTorch memory snapshot/summary**: distinguish live tensors from reserved memory and fragmentation.
- **Nsight Systems**: use when a timeline is needed to distinguish CPU waiting, copies, launches, GPU kernels, and communication.
- **OpenTelemetry plus service metrics**: use for queue, preprocessing, model, and response-stage latency in a service.

Do not send beginners directly to Nsight Compute unless a specific important kernel has already been isolated.

### Local or single-node inference

- **llama.cpp**: practical local inference for supported model families across CPU and multiple accelerator backends, especially quantized models.
- **Ollama**: convenient local model packaging and service UX when operational simplicity matters more than fine-grained scheduling control.
- **ONNX Runtime**: useful for supported exported models and cross-platform execution providers.
- **OpenVINO**: consider for supported Intel CPU/iGPU/NPU deployments.
- **TensorRT-LLM**: consider for NVIDIA-focused deployments that justify a more specialized build and compatibility surface.

### Higher-throughput LLM serving

- **vLLM** or **SGLang**: consider for continuous batching, KV-cache-aware scheduling, and high-throughput supported-model serving.
- **Hugging Face Text Generation Inference**: consider when its supported deployment model and integrations fit the project.

Do not promise one engine will be fastest. Benchmark the user's prompt/output lengths, concurrency, and hardware.

### PyTorch graph and fused operators

- **`torch.compile`**: test before writing custom kernels; watch for graph breaks, compile latency, and dynamic-shape churn.
- **PyTorch SDPA**, **FlashAttention**, or **xFormers**: prefer supported attention implementations over handwritten attention kernels.
- Use framework-provided fused optimizers and normalization/activation paths when semantics match.

### Memory pressure and model size

- Use smaller or purpose-built models before complex low-level tuning when quality allows.
- Consider supported **8-bit/4-bit quantization** through mature paths such as bitsandbytes, GPTQ, or AWQ implementations; validate task quality and hardware kernels.
- For training, consider **activation checkpointing**, **mixed precision**, **PyTorch FSDP**, **DeepSpeed ZeRO**, or **Hugging Face Accelerate** according to scale and operational skill.
- For supported fine-tuning workflows, specialized projects such as **Unsloth** may reduce setup and memory costs, but still require version and quality validation.

Never present quantization, reduced precision, offload, or a smaller model as free optimization. Explain possible quality, latency, memory, and compatibility tradeoffs.

## Symptom-to-first-action map

| User symptom | Plain explanation | First safe action | Mature solution class |
|---|---|---|---|
| “GPU usage jumps up and down” | the GPU may be waiting for data or instructions | capture a short system timeline or compare preloaded data | data pipeline, compile/graph, batching |
| “first answer is slow” | loading or compilation may dominate only the cold request | measure cold and second request separately | model preload, warm-up, compile/cache |
| “answers arrive slowly token by token” | decode is different from initial prompt processing | record TTFT and inter-token latency separately | serving scheduler, quantization, optimized runtime |
| “more users make everything stall” | the service may be saturated or batching poorly | run a small concurrency sweep with p95 latency | continuous batching, admission control, vLLM/SGLang class |
| “VRAM looks full” | reserved memory may not be actively used | compare allocated, reserved, and peak memory | memory snapshot, cache/precision policy |
| “training is slow” | time may be in data, forward, backward, communication, or saving | time several stable steps by phase | profiler, data loading, compile, FSDP/ZeRO |

## Recommendation rules

- Give exact project names as candidates, not endorsements detached from evidence.
- State prerequisites and the easiest rollback for each recommendation.
- Prefer one change at a time.
- Provide a “no-code path” when possible: configuration, supported engine, batch/concurrency, model choice, or precision mode.
- Escalate to a professional appendix only when the user needs it or evidence points below the framework layer.
