# Optimize AI Infra

一个面向 Codex 的训练、推理与本地 AI 服务性能诊断 Skill。它先定位端到端瓶颈，再选择最低成本、可验证、可回滚的系统优化路径，而不是看到 GPU 使用率异常就直接编写自定义 Kernel。

The skill diagnoses end-to-end AI training, inference, and serving bottlenecks, then produces evidence-gated optimization advice or an execution plan for humans and infra-capable agents.

## 适用场景

- 训练 step、tokens/s 或多卡扩展效率低于预期；
- 推理 TTFT、ITL/TPOT、p95/p99 或吞吐异常；
- OOM、显存持续增长、KV cache pressure 或 allocator fragmentation；
- GPU 利用率波动、GPU 时间线空洞、大量短 Kernel；
- 数据加载、CPU dispatch、传输、同步、编译或 graph break；
- NCCL 暴露、rank 负载不均衡、存储或 checkpoint 阻塞；
- 判断是否需要 `torch.compile`、量化、vLLM/SGLang、FSDP/ZeRO、Triton、TileLang、CUTLASS 或 CUDA 优化。

## 设计原则

1. **先诊断，后优化**：区分事实、推断和未知信息。
2. **先系统，后 Kernel**：从 workload、service、host、runtime、graph、communication 和 memory 逐层下钻。
3. **端到端收益优先**：使用 Amdahl 上界约束局部优化价值。
4. **成熟方案优先**：优先验证现有编译器、运行时、Serving Engine 和融合库。
5. **可验证、可回滚**：所有建议都需要基线、验收门槛、数值质量与停止条件。
6. **不越权实施**：执行请求只生成只读分析与执行计划，不自动修改代码、配置或服务。

## 受众与输出模式

| 受众 | 响应方式 |
|---|---|
| 技术小白 | 先用通俗语言解释，再给不超过三个成熟开源方案和低风险操作 |
| 专业开发者 | 给出分层证据、可证伪假设、Profiler/Nsight 路径、数值与端到端验收标准 |
| Infra Agent | 输出机器友好的 YAML 计划，包括阶段、候选命令、权限、产物、门槛、回滚和停止条件 |

Skill 独立区分两种意图：

- **Advice mode**：解释问题、比较候选方案、给出下一项最小测量。
- **Execution-plan mode**：对项目进行只读分析，生成可供 Agent 执行的优化框架与计划；本轮不实施变更。

## 主动发现

`agents/openai.yaml` 显式启用了：

```yaml
policy:
  allow_implicit_invocation: true
```

因此，Agent 在自主训练、推理、压测或部署过程中观察到下列信号时，可以在用户没有点名 Skill 的情况下主动选择它：

- 稳态 step time、吞吐、延迟、显存或成本持续偏离基线；
- OOM、near-OOM、KV cache preemption 或异常内存增长；
- 有待执行工作时出现 Accelerator idle gap；
- 并发或设备数增加后 p95/p99、吞吐或扩展效率恶化；
- graph break、recompile、动态 shape churn 或大量短 Kernel；
- 通信暴露、rank imbalance、checkpoint 或存储阻塞。

单次冷启动、正常 warm-up/compile 或没有用户可见回归的瞬时利用率波动不会单独触发。

> 隐式调用是模型与运行环境的语义路由，不是操作系统级事件钩子。需要每 N 步强制检查时，应在训练或服务运行时增加显式监控钩子。

## 工作流

```text
定义用户可见目标
        ↓
建立可重复基线
        ↓
定位 critical path
        ↓
提出可证伪假设
        ↓
最小区分实验
        ↓
成熟系统方案
        ↓
必要时进入算子 / Kernel
        ↓
数值、质量、内存与端到端验收
```

## 安装

将 `optimize-ai-infra` 目录复制到 Codex 的个人 Skill 目录：

```powershell
git clone https://github.com/222222222l/AI-infra-optimize-skill.git
cd AI-infra-optimize-skill

$destination = Join-Path $env:USERPROFILE '.codex\skills\optimize-ai-infra'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
Copy-Item -Path '.\optimize-ai-infra\*' -Destination $destination -Recurse -Force
```

新建 Codex 任务或重启 Codex，使 Skill 目录刷新。

## 使用示例

显式调用：

```text
Use $optimize-ai-infra to diagnose why my 8-GPU DDP training scales poorly.
```

```text
使用 $optimize-ai-infra 分析本地 vLLM 服务在并发 8 时 TTFT p95 恶化的问题，只给出执行计划。
```

不显式调用也可以触发：例如 Agent 在自主训练中发现 warm step time 翻倍、GPU 持续空闲且任务可能超出时间预算。

## 仓库结构

```text
AI-infra-optimize-skill/
├── README.md
└── optimize-ai-infra/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── diagnostic-framework.md
    │   ├── novice-guidance.md
    │   ├── expert-guidance.md
    │   ├── agent-execution-contract.md
    │   └── profiling-playbooks.md
    └── scripts/
        ├── estimate_impact.py
        └── validate_skill.py
```

`SKILL.md` 只负责触发、路由和主流程；详细知识按受众与任务类型渐进加载。

## 验证

校验 Skill 结构、命名、隐式调用配置、引用完整性和 UI 元数据：

```powershell
python .\optimize-ai-infra\scripts\validate_skill.py .\optimize-ai-infra
```

估算某个局部优化的 Amdahl 端到端收益上界：

```powershell
python .\optimize-ai-infra\scripts\estimate_impact.py `
  --share 0.25 `
  --speedup 2 `
  --current-time-ms 100
```

估算结果不是性能声明，仍需使用代表性 workload 做端到端 benchmark。

## 安全边界

- 不把 `nvidia-smi` 利用率当成瓶颈结论；
- 不在没有等价语义基线时比较融合与非融合实现；
- 不隐藏量化、低精度、offload 或小模型带来的质量代价；
- 不在单个有利 shape 上宣称普遍加速；
- 不把微基准提升当作端到端提升；
- 不在诊断或计划请求中擅自安装依赖、修改源码、重启服务或运行生产压测。
