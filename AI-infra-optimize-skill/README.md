# AI 基础设施性能诊断 Skill

[English](README.en.md)

> 这是 Cliff-skill 集合中的模块副本。以下相对路径与命令均以 `AI-infra-optimize-skill/` 为工作目录；历史来源见集合根目录的迁移清单。

`optimize-ai-infra` 用于组织训练、推理与服务性能诊断：先建立可重复的端到端基线，再沿数据、CPU、传输、计算、通信与内存链路定位瓶颈，选择能通过实验区分的优化假设。

交付物是诊断建议或执行计划，不是加速库。当前 Skill 的诊断/计划模式执行只读分析，不自动修改源码、配置或运行服务。

## 适用问题

训练 step、有效吞吐与多卡扩展；推理 TTFT、ITL/TPOT、p95/p99；OOM、KV 缓存与分配器；数据加载、编译/graph break、CPU dispatch、NCCL 暴露、慢 rank、存储及 checkpoint 阻塞。

优先验证成熟编译器、运行时和 serving 方案；只有关键路径证据支持时才进入算子或自定义 kernel。GPU 使用率本身不是瓶颈证据。

## 工作方式

1. 明确用户可见目标、工作负载、硬件和数值/质量约束。
2. 记录稳定阶段基线，提出可证伪假设和最小区分实验。
3. 用 Amdahl 上界约束局部优化价值。
4. 规划端到端性能、显存、正确性和质量验收，以及停止/回滚条件。

新手输出简明测量与候选方案；开发者输出 profiler 路径和验收口径；Agent 执行者可获得含权限、产物与门槛的 YAML 计划。详见 [SKILL.md](optimize-ai-infra/SKILL.md) 与 [参考资料](optimize-ai-infra/references/)。

## 安装与使用

将 `optimize-ai-infra/` 放入宿主支持的 Skill 目录，刷新其 Skill 索引。保留已有同名版本的备份，不盲目覆盖。

```text
使用 $optimize-ai-infra 诊断8卡DDP扩展效率，并给出最小测量与执行计划。
```

`agents/openai.yaml` 允许宿主在持续性能回归时隐式选择本 Skill；这不是操作系统监控钩子，也不保证每 N 步触发。冷启动、正常预热或无用户影响的单次抖动不能独立证明回归。

## 验证工具

在仓库根目录：

```bash
python optimize-ai-infra/scripts/validate_skill.py optimize-ai-infra
python optimize-ai-infra/scripts/estimate_impact.py --share 0.25 --speedup 2 --current-time-ms 100
```

结构校验仅检查包与引用完整性；Amdahl 结果是条件估算。性能声明仍需相同任务、精度、批次、并发和硬件下的实测，不能把微基准或单一有利 shape 外推为普遍收益。量化、低精度与卸载的质量代价须单列。

本仓库没有给出跨工作负载通用加速率，当前未提供顶层 `LICENSE`。

## 集合版本的训练MFU扩展

[training-mfu-playbook.md](optimize-ai-infra/references/training-mfu-playbook.md) 补充有效FLOPs与硬件峰值口径、预先声明的完整测量窗口、microbatch/梯度累加搜索、冻结编码器与数据重叠、GC/慢rank及FP8缓存的验证路径。MFU必须随工作量、精度、峰值定义和计时窗口一起报告；它不是单独的质量或成本收益指标。该扩展不表示独立仓库包含相同版本。
