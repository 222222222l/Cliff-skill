# Cliff Skills

[中文](README.md)

A collection of analysis and engineering methods for AI assistants: market/policy analysis, Agent evaluation, performance diagnosis, constraint-driven engineering decisions, project-state synchronization, and causal decision modeling. Modules contain instructions, references, and selected deterministic scripts. They are methods/tools, not established general capability gains or predictive returns.

## Modules

| Module | Task and entry point |
| --- | --- |
| [Market signals](market-signal-analysis-skill/README.en.md) | Data validation, flows/valuation, trends, action conditions |
| [China policy](China-policy-analysis-skill/README.en.md) | Implementation constraints, funding/risk transmission, consistency, causal identification |
| [Agent evaluation](Agent-Evaluation-Skill/README.en.md) | Telemetry, gates, human preferences, transparent aggregation |
| [AI performance](AI-infra-optimize-skill/README.en.md) | Training/inference critical paths, MFU definitions, minimal experiments |
| [Constraint-driven engineering](constraint-driven-engineering-skill/README.en.md) | Outcomes, binding constraints, cross-domain transfer, falsifiable experiments, reusable systems |
| [Project state](sync-project-state-skill/README.en.md) | Git checkpoints, environment differences, cross-device handoffs |
| [Causes/decisions](model-causes-and-decisions-skill/README.en.md) | Counterfactuals, identification, rival hypotheses, decision rules |

Each module has Chinese and English READMEs. Its `SKILL.md` defines behavior. Select modules by task rather than injecting the entire collection into every session.

## Provenance and versions

[MIGRATION-MANIFEST.json](MIGRATION-MANIFEST.json) records source repositories and commits imported from the same maintainer on 2026-10-17. It is historical provenance, not a live checksum inventory after later edits. Do not rewrite historical sources to conceal changes.

The collection's policy module includes a [causal extension](China-policy-analysis-skill/docs/causal-extension-integration.md), and its infrastructure module adds a [training-MFU playbook](AI-infra-optimize-skill/optimize-ai-infra/references/training-mfu-playbook.md). Collection versions therefore need not be identical to standalone repositories. Git history and current module files define their state.

## Use and verification

Use each module's README to identify the directory containing `SKILL.md`, then install it in the host's supported Skill location. Check existing versions/local changes to avoid duplicate discovery or overwriting. Preserve permissions and project constraints.

Existing validators check module structure, references, or calculator behavior. [VALIDATION.json](VALIDATION.json) is a historical record, not proof that checks were rerun on a new commit. Real-task benefit requires matched baselines, representative samples, independent acceptance, failure records, and cost accounting.

This collection contains neither model weights nor a unified Agent runtime, and has no shared experimental benchmark covering all modules. No top-level `LICENSE` is supplied. Preserve third-party attribution and module provenance; public hosting alone does not establish a uniform redistribution license.
