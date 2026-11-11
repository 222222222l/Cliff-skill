# Constraint-Driven Engineering Skill

[中文](README.md)

`constraint-driven-engineering` turns inspiration from strong engineering teams into a repeatable way to reason about real business problems. Instead of copying a celebrated architecture, define the outcome, identify binding constraints, transfer the **underlying mechanism** across domains, falsify ideas with economical tests, and preserve successful methods as reusable systems.

## Five-stage workflow

1. **Define the result:** User acceptance, baseline, quality/latency/cost/reliability constraints.
2. **Find the constraint:** Map input, state, output and feedback; distinguish measurements from hypotheses.
3. **Generate transfers:** Explore business, representation, data, algorithm, system, hardware and organizational levers.
4. **Falsify cheaply:** Predeclare predictions, controls, evaluation criteria and stop/rollback conditions.
5. **Compound learning:** Preserve tests, contracts, schemas, benchmarks, traces, datasets, modules and decision records.

## Usage

Install the [constraint-driven-engineering/](constraint-driven-engineering/) folder in a Skill-capable host, or invoke:

```text
Use $constraint-driven-engineering to analyze this engineering problem.
Define the business acceptance criteria and constraints, propose at least three
mechanistically distinct alternatives, then design the cheapest falsifying test
and recommend the next reversible decision.
```

Use it for architecture exploration, technology tradeoffs, systems research, AI training and inference, agent-native game engines, video-to-motion/robotics transfer, or a 20-minute daily deliberate-practice session. Analysis or diagnosis does not authorize code changes, deployment or expensive experiments.

## Files

- [SKILL.md](constraint-driven-engineering/SKILL.md): Invocation modes, procedure and output contract.
- [transfer-patterns.md](constraint-driven-engineering/references/transfer-patterns.md): Original engineering cases, mechanism mapping, AI/game/motion playbooks.
- [practice-templates.md](constraint-driven-engineering/references/practice-templates.md): Daily question card, decision memo, experiment ledger, weekly review.
- [openai.yaml](constraint-driven-engineering/agents/openai.yaml): User-facing skill metadata.

## Relationship to other skills

This module frames the **high-level outcome, alternatives, cross-domain transfer and first discriminating test**. Use the repository's AI performance skill for in-depth GPU diagnostics, Agent Evaluation for formal task suites and metrics, and Causes/Decisions for causal identification. Avoid automatically stacking every skill.

## Evidence and limitations

Cases link to original public engineering projects. Reported outcomes often come from the originating teams and do not establish transferability to an unrelated business. Structural validation does not demonstrate an improvement in downstream task quality; test the skill with representative paired evaluations, fixed baselines, failure traces and cost accounting. No repository-wide license is currently supplied; preserve original-source attribution and license boundaries.
