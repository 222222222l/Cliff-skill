# Practice and Decision Templates

Read this reference when the user wants deliberate practice, an engineering
decision memo, or a repeatable research/optimization ritual. Keep the answer
lightweight unless an experiment actually warrants full documentation.

## Daily 20-minute engineering thinking card

```markdown
# Engineering thinking card — YYYY-MM-DD
Business / user outcome:
Observed problem (not a preferred solution):
Known baseline and acceptance metric:
Main constraint: [observed / inferred / unknown] + evidence:
System boundary: input -> state/transformations -> output -> feedback

Three different mechanisms:
1. Remove/simplify/change representation:
2. Transfer from another field (source mechanism, mismatch):
3. Data/algorithm/runtime/system alternative:

Strongest competing explanation:
Cheapest falsifying experiment:
Prediction if right / prediction if wrong:
Decision after the result, not before:
What can be reused or codified:
```

Timebox: 3 minutes to define the outcome, 4 to map constraints, 6 to generate
mechanisms, 5 to design the test, 2 to choose the next action. If no reliable
baseline exists, make baseline collection the next action.

## One-page engineering decision record

```markdown
# Decision: <problem / date>
Owner / user-visible goal:
Scope / deadline / current baseline:
Primary metric:
Hard guardrails (quality, latency, cost, correctness, reliability):
What we actually observed:
Uncertain or conflicting facts:
Binding constraint and rival hypotheses:

| Option | Mechanism | Expected benefit | Cost/risk | Fastest discriminator |
| --- | --- | --- | --- | --- |
| Status quo / simpler baseline | | | | |
| A | | | | |
| B | | | | |

Chosen first experiment / why:
Fixed dataset, workload, hardware and revision:
Expected result if hypothesis holds:
Result that would falsify it:
Decision threshold and stop/rollback rule:
Evidence/artifact links:
Decision: adopt / reject / gather evidence
Next check and owner:
```

Do not force numeric estimates without empirical support. State which benefits
are forecasts and which are measured. For stochastic evals include independent
runs and dispersion; for GPU work include warm-up and synchronization.

## Research experiment ledger

Store one record per run, preferably CSV/JSONL or a versioned Markdown table:

| Field | Meaning |
| --- | --- |
| experiment_id, date | Stable identity and experiment chronology |
| hypothesis, alternative | Prior mechanism and competing explanation |
| code_sha, config_sha, dataset_version | Reproducibility |
| hardware, runtime, seed | Comparison conditions |
| workload and budget | Actual examples/steps/GPU-hours |
| primary_metric, guardrail_metrics | Full results, not only favorable values |
| unexpected_failures | Outliers, crashes, invalid trials, data leak concerns |
| verdict, why | Supported / weakened / inconclusive / rejected |
| next_test, reusability | Follow-up and durable artifact |

Preserve negative results and avoid changing multiple uncontrolled variables
before a causal conclusion. If multiple changes are necessary, compare an
appropriate factorial/ablation design rather than pretending there is one cause.

## Weekly 30-minute review

Answer in order:

1. Which belief did evidence change?
2. Which improvement moved an end-to-end acceptance metric?
3. Which experiments were uninformative and why?
4. Which source-domain mechanism transferred successfully, if any?
5. Which repeated failure should become a contract, test, dataset, or tool?
6. Which one next experiment has the best decision value per unit cost?

Optional process indicators:

- Median time from hypothesis to retain/reject decision.
- Fraction of experiments that produced an actionable conclusion, including
  credible negative conclusions.
- Fraction of accepted changes that passed independent downstream guards.
- Number of demonstrated cross-project reuses, not hypothetical reuse claims.

These are process indicators, not a validated score of individual intelligence
or engineer quality. Do not optimize for experiment or documentation counts.

## Example invocation prompts

- “使用 $constraint-driven-engineering 评估视频到骨骼动作模型的泛化瓶颈，
  在数据、表示、算法和系统层各提出一个方案与最小消融实验。”
- “用 $constraint-driven-engineering 对 Agent 原生游戏引擎做系统边界设计，
  对比插件架构、ECS 和编译器式中间表示，并设计可反证的 MVP。”
- “用 $constraint-driven-engineering 带我进行今天的20分钟工程思维训练，
  只引导我完成一个问题卡，不直接替我做决定。”
