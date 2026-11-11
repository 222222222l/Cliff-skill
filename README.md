# Cliff Skills

[English](README.en.md)

面向AI助手的分析与工程方法集合，包含市场/政策分析、Agent评估、性能诊断、约束驱动工程决策、项目状态同步和因果决策建模。各模块由指令、参考资料及部分确定性脚本组成；它们是方法与工具，不构成已验证的通用能力提升或预测收益。

## 模块

| 模块 | 任务与入口 |
| --- | --- |
| [市场信号](market-signal-analysis-skill/README.md) | 数据核验、资金/估值、趋势和行动条件 |
| [中国政策](China-policy-analysis-skill/README.md) | 执行约束、资金/风险传导、数据一致性和因果识别 |
| [Agent评估](Agent-Evaluation-Skill/README.md) | 遥测、验收门槛、人工偏好与透明聚合 |
| [AI性能诊断](AI-infra-optimize-skill/README.md) | 训练/推理关键路径、MFU口径和最小验证 |
| [约束驱动工程思维](constraint-driven-engineering-skill/README.md) | 业务目标、真实约束、跨行业机制迁移、反证实验与复用沉淀 |
| [项目同步](sync-project-state-skill/README.md) | Git项目检查点、环境差异和跨设备交接 |
| [因果与决策](model-causes-and-decisions-skill/README.md) | 反事实、识别、竞争解释和决策规则 |

每个模块均提供中英文README。实际行为以其 `SKILL.md` 为准；按任务需要选用，不应把整个集合无差别注入每个会话。

## 来源与版本

[MIGRATION-MANIFEST.json](MIGRATION-MANIFEST.json) 记录2026-10-17从同一维护者的独立仓库迁入的来源与提交。它是历史来源快照，文件哈希不是此后修改的实时校验清单；不要重写历史来源来掩盖版本变化。

集合中的政策模块增加了 [因果扩展](China-policy-analysis-skill/docs/causal-extension-integration.md)，性能模块增加了 [训练MFU流程](AI-infra-optimize-skill/optimize-ai-infra/references/training-mfu-playbook.md)。因此集合版本不必与独立仓库逐字相同。当前状态应以Git提交和实际模块文件为准。

## 使用与验证

从模块README确认真正包含 `SKILL.md` 的目录，再安装至宿主支持的Skill位置。检查同名版本与本地修改，避免重复安装或覆盖。保持权限和项目约束。

已有验证脚本检查各模块的结构、引用或计算行为；[VALIDATION.json](VALIDATION.json) 是既往记录，不是新提交已重新运行的证明。方法对真实任务的收益需要固定基线、代表性样本、独立验收、失败记录和成本统计。

本仓库不含模型权重或统一Agent运行时，也没有为所有模块提供共享实验基准。当前未提供顶层 `LICENSE`；第三方引用和各模块来源应保留，不能仅凭公开托管推定统一再分发授权。
