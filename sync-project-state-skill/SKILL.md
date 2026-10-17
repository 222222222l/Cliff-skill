---
name: sync-project-state
description: Restore and checkpoint agent-friendly Git projects across computers by synchronizing a private project-memory index, checking project remotes, comparing Codex Skills/plugins/MCP/config requirements, installing bundled portable Skills, and explicitly reporting unrecoverable environment differences. Use when starting, resuming, handing off, or finishing project work across devices, or when Codex must verify that another machine can reproduce the current working state.
---

# Sync Project State

Use the memory repository as a portable control plane. Keep source code in each project's own Git repository; keep only project identity, immutable checkpoints, and non-secret environment requirements here.

## Resolve the memory repository

Use `CODEX_MEMORY_HOME` when set. Otherwise let `project_memory.py` discover `memory-config.json` from the current directory or the local pointer stored under `CODEX_HOME`.

Locate a Python 3.11+ interpreter. Prefer the current workspace dependency runtime when Codex exposes one.

```text
python <skill>/scripts/project_memory.py <command>
```

## Start or resume a project

1. Run `start <project-path>`.
2. Let it pull the memory repository with fast-forward-only semantics.
3. Let it fetch the project remote and fast-forward only when the working tree is clean and the branch is strictly behind.
4. Read the latest immutable checkpoint and the environment report.
5. Surface every `BLOCKING` and `WARNING` item before doing project work.
6. Run `install-skills --apply` only for missing Skills bundled in the memory repository. Do not replace a differing local Skill without explicit approval; replacement creates a backup.
7. For missing plugins, use the exact plugin ID through Codex Plugin Management when callable. If installation or authorization is unavailable, state that the environment could not be restored.
8. Never claim the project is portable while it has uncommitted files or unpushed commits.

Use `--json` when a structured report is more useful:

```text
python <skill>/scripts/project_memory.py --json start .
```

## Create a handoff checkpoint

Before switching devices:

1. Inspect the project Git state.
2. Commit and push project code when authorized. If code remains dirty or ahead of its upstream, record that as non-portable.
3. Run `finish` with a concise summary and exact next action. Add decisions, blockers, and test evidence when present.
4. Use `--push-memory` to commit and push the new checkpoint after the memory repository is authenticated.
5. Report any rejected push, divergence, or authentication failure explicitly.

```text
python <skill>/scripts/project_memory.py finish . \
  --summary "<current outcome>" \
  --next-action "<first exact action on the next device>" \
  --test "<command and result>" \
  --push-memory
```

Checkpoints are append-only files. Do not rewrite historical checkpoints to resolve concurrent work.

## Register requirements

Registration is automatic on first start or finish. Add project-specific requirements when they materially affect reproducibility:

```text
python <skill>/scripts/project_memory.py register . \
  --require-skill agentic-project-development \
  --require-plugin github@openai-curated-remote
```

Global requirements live in `environment/requirements.json`. Project-specific requirements live in `projects/index.json`. Read `references/state-contract.md` before changing either schema.

## Bootstrap another computer

From a fresh clone of the memory repository:

```text
python skills/sync-project-state/scripts/project_memory.py bootstrap \
  --device "<stable-device-name>" \
  --apply
```

This installs missing bundled Skills, writes a non-secret device inventory, and runs the environment doctor. It does not copy credentials, OAuth sessions, browser state, raw Codex memories, conversations, SQLite databases, or machine-specific runtime paths.

## Failure policy

- Treat memory-repository divergence, project divergence, missing blocking Skills, missing Git, and inaccessible required remotes as blocking.
- Treat optional plugin differences, safe config differences, and Skill hash differences as warnings unless requirements mark them blocking.
- Never auto-merge divergent project branches.
- Never upload `.codex` databases, `auth.json`, `secrets/`, session logs, or browser profiles.
- Distinguish “checkpoint restored” from “Codex thread/sidebar history restored”; this Skill does not migrate Codex UI threads.
