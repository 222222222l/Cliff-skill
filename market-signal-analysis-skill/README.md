# 市场信号分析 Skill

[English](README.en.md)

> 这是 Cliff-skill 集合中的模块副本。以下相对路径与命令均以 `market-signal-analysis-skill/` 为工作目录；历史来源见集合根目录的迁移清单。

`market-signal-analysis` 是面向股票、ETF、行业、指数与流动性宏观市场的分析方法包。它把价格结构、基本面、资金、政策、参与者激励与数据质量放入同一决策框架，并按问题加载必要模块。

交付物包括 Agent 指令、专题参考和确定性计算脚本。它不是经样本外验证的交易策略；模型给出的情景权重不等于实际胜率。

## 方法与覆盖

默认选择一个主模块及最多两个辅助模块。先固定市场、决策期限、数据版本与风险约束，再比较支持/反对证据和退出条件。

| 模块 | 内容 |
| --- | --- |
| 价格与趋势 | OHLCV、动量、波动、广度、多时间尺度、ATR风险边界 |
| ETF与拥挤 | 份额/净申赎估计、同类聚合、A股承接与退出、港股多柜台去重 |
| 企业与行业 | 盈利、现金流、估值、治理、供给和高估值叙事 |
| 宏观与政策 | 美国流动性、利率/财政、跨资产传导、主体激励与制度约束 |
| 周期与事件 | 库存/信用/capex周期、频域探索、交割/议息/调样 |
| 行动比较 | 成本、风险预算、退出失败、损失路径、条件性收益假设 |
| 数据审计 | 同口径、复权、发布滞后、历史版本与独立旁证 |

相关性、频域峰值和回归权重均不能独立证明因果或可交易性。数值概率须标明经验、模型隐含或主观情景来源；没有足量样本则保持定性。详见 [SKILL.md](SKILL.md) 和 [专题目录](references/)。

## 安装与使用

将本仓库包含 `SKILL.md` 的根目录安装到宿主支持的 Skill 目录，调用：

```text
使用 $market-signal-analysis 判断该ETF的回调是否改变原假设，
核对数据时间与口径，并给出反证、风险边界和下一验证点。
```

确定性 ETF 脚本接受长表：
`date,symbol,group,scope,close,nav,shares,turnover`。港股数据应先把多个交易柜台规范为同一基金/份额类别，使用 `--market hk`。

```bash
python scripts/analyze_etf_flows.py --input etf_daily.csv --scope broad --group csi300 --regime range_extraction --pretty
python scripts/recommend_behavior_mode.py --input behavior_priors.json --pretty
python scripts/validate_skill_graph.py
```

ETF 同类聚合采用估计资金流，不直接相加原始份额。行为比较器需要期限匹配的收益先验、成本和退出/破产路径；重要状态先验少于20个有效事件时不输出数值收益。这个最低门槛本身不保证估计稳健。

## 证据边界

验证脚本检查路由、引用与包结构，不证明投资绩效。正式研究应保留点时数据，处理复权、幸存者偏差、成本、重叠样本和多重试验，并区分开发集与样本外测试。

方法细节见 [统计权重](references/statistical-weighting.md)、[官方数据核验](references/official-data-verification.md)、[行为选择](references/behavior-mode-selection.md) 和 [研究路线](references/research-and-optimization-roadmap.md)。可选 Transformer 演示只是研究入口。

本仓库当前未提供顶层 `LICENSE`。任何资产行动仍需当前数据和适用的个人约束，文档不提供收益保证。
