# Agent 评估 Skill

[English](README.en.md)

> 这是 Cliff-skill 集合中的模块副本。以下相对路径与命令均以 `Agent-Evaluation-Skill/` 为工作目录；历史来源见集合根目录的迁移清单。

`agent-evaluation` 用于设计和汇总垂直领域、任务型 Agent 的重复评估。它将直接测量的性能、验收门槛和人工偏好分开，保留任务与运行记录，再进行透明的聚合。

这是评估流程与评分工具，不是已经验证的通用 Agent 排行榜。任务集、评分权重和人工量表须针对使用场景校准。

## 评估层次

| 层次 | 示例 | 解释边界 |
| --- | --- | --- |
| 定量遥测 | 成本、tokens、耗时、工具调用、重试 | 需要一致采集口径，缺失值不能当零 |
| 验收门槛 | 真实完成、测试通过、无回归、无关键风险 | 应由可复核的证据或独立检查判定 |
| 人工偏好 | 可读性、结果适用性 | 保留产物与量表，不能称为完全客观指标 |

默认聚合为 `0.35 × quantitative + 0.45 × gates + 0.20 × human preference`。这是一组可配置默认值，不是经验证的普适效用函数。每次都应同时报告分项、样本量和关键失败；严重失败不得被平均分掩盖。

## 安装与使用

将 `agent-evaluation/` 安装至宿主支持的 Skill 目录，调用：

```text
使用 $agent-evaluation 为这个任务型Agent制定任务集、运行记录、
验收门槛与人工偏好量表，并说明聚合规则。
```

输入为 JSON/JSONL 运行记录，核心字段为 `run_id`、`task_id`、`metrics`、`checks`、`human`。详细结构见 [运行记录契约](agent-evaluation/references/run-record-schema.md)；先按任务汇总重复运行，再汇总整个任务集。

## 命令

在仓库根目录：

```bash
python agent-evaluation/scripts/score_runs.py --self-test
python agent-evaluation/scripts/score_runs.py --print-default-config > agent_eval_config.json
python agent-evaluation/scripts/score_runs.py --runs path/to/runs --config agent_eval_config.json --out summary.json
python agent-evaluation/scripts/record_human_score.py --artifact path/to/trace.md --run-id run-001 --task-id task-001 --out human_scores.jsonl
python agent-evaluation/scripts/score_runs.py --runs path/to/runs --human-scores human_scores.jsonl
python agent-evaluation/scripts/validate_skill.py agent-evaluation
```

人工分数也可用 `--score`、`--max-score`、`--notes` 非交互记录。结构检查与 self-test 不等于跨任务效度验证。

## 方法与证据

- [SKILL.md](agent-evaluation/SKILL.md)
- [任务集设计](agent-evaluation/references/task-suite-design.md)
- [指标分类](agent-evaluation/references/metric-taxonomy.md)
- [人工偏好](agent-evaluation/references/human-preference.md)

比较 Agent 或 Skill 时，应固定任务/资源条件，重复随机运行，保留失败轨迹，并使用未参与调试的验收任务。没有这些证据，不能把评分提高解释为通用能力提高。

本仓库当前未提供顶层 `LICENSE`。
