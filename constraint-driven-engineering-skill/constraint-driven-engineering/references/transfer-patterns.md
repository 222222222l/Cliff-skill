# Engineering Transfer Patterns

Read this reference when cross-domain analogy, systems architecture, or an
engineering-research case study would materially improve the decision.
Examples are historical mechanisms, **not** an assertion that a particular
model, framework, or benchmark is currently state of the art.

## Transfer test

For every source-domain inspiration fill in:

| Field | Required answer |
| --- | --- |
| Source problem | What practical outcome was blocked? |
| Source constraint | Which measured or evidenced limitation mattered? |
| Mechanism | What structural change removed or relaxed it? |
| Target analog | Which target constraint has the **same causal structure**? |
| Mismatch | Which source assumptions fail in the target environment? |
| Discriminating experiment | What small result would support or falsify transfer? |

Do not equate visual similarity or shared terminology with a transferable
mechanism. Read original technical reports rather than relying on promotional
comparisons. Verify contemporary compatibility and capabilities before adoption.

## Public engineering cases

| Source | Transferable mechanism | Pitfall to check |
| --- | --- | --- |
| [Karpathy: autoresearch](https://github.com/karpathy/autoresearch) | Constrain the editable surface, fix the time budget, define one comparable evaluator, iterate and preserve results | A short training proxy can overfit the proxy or fail to predict full-run quality |
| [Google DeepMind: AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | Turn implementation/algorithm choices into a search space with executable fitness and independent correctness verification | Automated search can exploit flawed graders and require expensive validation |
| [FlashAttention](https://github.com/Dao-AILab/flash-attention) | Reconsider memory movement and data locality before assuming arithmetic is the primary bottleneck | Kernel gains depend on shape, dtype, hardware, integration and end-to-end time |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) | Define swappable capabilities and plugin lifecycle while keeping auditable session events and explicit contracts | Unbounded dynamic composition can hurt determinism and hot-path performance |
| [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) | Turn engineering conventions, architecture, plans and quality rules into repository-visible and executable constraints for agents | Generated-code volume is not equivalent to user value or correctness |
| [Anthropic: Agent Evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | Grade environment outcomes, traces, failure types and repeated trials, not merely the final text | An evaluator may be underspecified or easy to game |
| [Spotify: platform standardization](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint) | Reduce unnecessary technological variation and standardize migration interfaces to enable automation at scale | More automated PRs do not, alone, establish customer outcomes |
| [Physical Intelligence: pi0](https://www.physicalintelligence.company/blog/pi0) | Separate transferable semantic priors from platform-specific action execution; train on heterogeneous embodiments | A virtual animation success does not prove physical robot control |
| [Google SRE: error budgets](https://sre.google/workbook/error-budget-policy/) | Set reliability targets and use an explicit failure budget to balance change and stability | A target must match actual user-critical behavior |
| [Unreal: MassEntity](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine) | Separate data fragments from processing logic and organize hot-path data for locality | ECS does not replace business-level plugin contracts |
| [Mike Acton: Data-Oriented Design](https://www.youtube.com/watch?v=rX0ItVEVjHc) | Start from actual data transformations, access patterns and hardware instead of class hierarchies alone | Benchmark representative workloads, not microbenchmarks only |
| [OpenAI: Coding Eval Audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) | Audit whether a benchmark genuinely distinguishes capability and correctness | A higher pass rate can be driven by broken tasks, leakage or narrow tests |

## Domain playbooks

### A. AI training / inference optimization

1. Specify useful output: validated quality per GPU-hour, time-to-quality,
   inference latency/throughput **at fixed quality**, or production cost.
2. Separate data-pipeline, graph/kernel, HBM/transfer, communication, and
   quality/representation constraints with traces and fixed workloads.
3. Generate candidates from at least three different layers: data distribution,
   model/target representation, execution strategy.
4. Run a cheap paired experiment. A speedup with a quality regression is
   not an unconditional improvement; report the Pareto tradeoff.
5. Retain the profiler trace, exact code/data/hardware revision, quality gate,
   and full-pipeline wall time.

### B. Agent-native game development engine

1. Define acceptance as a *playable, correct and editable* game feature, not
   the number of generated scripts or plugins.
2. Separate four concerns: capability/plugin contract, world/state schema,
   real-time execution hot path, and replay/validation.
3. Use replaceable plugins for high-variation authoring functions; use tightly
   scheduled and data-oriented systems where frame-time or determinism binds.
4. Prototype two or three composable mechanics before building a new rendering
   or physics engine. Check contract replacement, conflict handling, game-state
   replay, frame-time and regression.
5. Compare with a simpler existing-engine adapter. Do not assume building a
   new core creates more customer value.

### C. Video-to-motion / robotics crossover

1. Separate image evidence, camera motion, canonical motion representation,
   morphology/retargeting and physical contact constraints as testable concepts.
2. Compare direct video-to-joints with one explicitly factorized alternative;
   do not assume factorization wins without data.
3. Split evaluation by subject, viewpoint, occlusion, action, and **unseen
   skeleton/morphology**. Never use only in-distribution joint error to
   claim generalization.
4. Measure geometric error where ground truth exists, temporal instability,
   foot sliding/contacts, user correction time, and execution success for any
   actual robot deployment.
5. Transfer knowledge from heterogeneous robot data and embodiment studies,
   but separate simulation/game animation quality from physical control evidence.

## What not to transfer blindly

- “Everything is a plugin” does not mean every high-frequency frame update
  should pass through a dynamic plugin dispatcher.
- A benchmark-optimizing agent is not a scientific discovery engine unless
  correctness and held-out validity survive independent tests.
- Better GPU utilization does not imply shorter time-to-quality.
- A shared action latent is not automatically safe for a robot with different
  dynamics, joints or contact limits.
- More agent-generated code and PRs are activity signals, not outcome metrics.
