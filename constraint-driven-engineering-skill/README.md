# 约束驱动工程思维 Skill

[English](README.en.md)

`constraint-driven-engineering` 把“参考顶尖工程师的方法在真实业务中发散思路”转化为可重复使用的工程决策流程。核心不是模仿名人或套用新技术，而是明确业务目标，识别约束，迁移**结构相同的机制**，用最小实验排除错误方向，并将有效结论沉淀为可复用资产。

## 五阶段流程

1. **定义结果**：用户验收、基线、质量/延迟/成本/可靠性边界。
2. **寻找约束**：建立输入—状态—输出链路；区分已测量瓶颈与推测。
3. **跨域发散**：从业务、表示、数据、算法、系统、硬件、组织层提出机制不同的方案。
4. **实验反证**：写出假设、相反预测、最小对照实验、评价标准和停止条件。
5. **系统复利**：把结果编码为测试、合同、Schema、基准、回放、数据集、模块或决策记录。

## 使用

将 [constraint-driven-engineering/](constraint-driven-engineering/) 目录安装至支持 Skill 的宿主，或在会话中调用：

```text
使用 $constraint-driven-engineering 分析这个实际工程问题：
先定义业务验收和瓶颈，再从至少三个不同抽象层提出方案，
对每个主要方案设计最低成本的反证实验，并推荐下一步行动。
```

支持架构方案发散、技术选型、系统瓶颈分析、AI 训练与推理研究、Agent 原生游戏引擎、视频到骨骼动作/机器人交叉研究，以及每天 20 分钟的工程思维练习。仅询问分析或诊断时不会自行修改代码、部署或启动昂贵训练。

## 文件

- [SKILL.md](constraint-driven-engineering/SKILL.md)：调用模式、五阶段操作流程和输出契约。
- [transfer-patterns.md](constraint-driven-engineering/references/transfer-patterns.md)：一手工程案例、跨域机制映射、AI/游戏/动作生成的设计提示。
- [practice-templates.md](constraint-driven-engineering/references/practice-templates.md)：每日问题卡、工程决策记录、实验台账、每周复盘。
- [openai.yaml](constraint-driven-engineering/agents/openai.yaml)：Skill 入口元数据。

## 与现有模块分工

本模块负责**高层问题定义、方案发散、跨域迁移和最小实验决策**。GPU 性能深度排查使用仓库中的 AI 性能诊断；Agent 指标与任务集设计使用 Agent 评估；因果识别与反事实建模使用因果与决策模块。不要把这些模块无差别叠加。

## 证据和限制

案例对应公开的一手项目和工程文档，其绩效数字通常来自原团队披露；不意味着所有方法在其他业务中必然有效。Skill 的结构验证不代表下游能力提升已经经过成对实验验证。实际收益应通过用户场景中的独立任务、固定基线、失败记录和成本统计评估。仓库当前未提供顶层统一 LICENSE；保留第三方来源与其各自授权边界。
