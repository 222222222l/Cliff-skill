# Cross-Device Project State Skill

[中文](README.md)

> This is the module copy in Cliff-skill. Relative paths and commands below use `sync-project-state-skill/` as the working directory. Historical provenance is recorded in the collection's migration manifest.

`sync-project-state` supports resuming and handing off Git projects through a private project-memory index, immutable checkpoints, and environment requirements. Source code remains in each project's own repository; this Skill records non-secret control information needed for recovery.

It does not migrate the Codex sidebar, conversation history, authentication, browser state, or a complete machine environment. Uncommitted or unpushed work is not made portable by a checkpoint.

## Behavior

- `start`: fast-forward the memory repository, fetch the project, and fast-forward only a clean, strictly-behind working tree.
- `finish`: append a checkpoint containing outcomes, the exact next action, tests, and blockers.
- `register`: declare required Skills, plugins, and environment requirements.
- `bootstrap` / `install-skills`: inspect the environment and install missing bundled Skills; differing-version replacement requires explicit authorization and a backup.

Divergent histories must not be auto-merged. Report blocking and warning conditions before continuing; missing plugins or permissions cannot be hidden by a successful-recovery claim.

## Use

Requires Python 3.11+, Git, and authorized project/memory remotes. Resolve memory storage through `CODEX_MEMORY_HOME`, `memory-config.json`, or the local pointer. Read [SKILL.md](SKILL.md) first.

From this repository:

```bash
python scripts/project_memory.py --json start /absolute/path/to/project
python scripts/project_memory.py register /absolute/path/to/project --require-skill agentic-project-development
python scripts/project_memory.py finish /absolute/path/to/project --summary "Completed work" --next-action "Exact next step" --test "Command and result" --push-memory
```

`--push-memory` commits and pushes the memory repository and should be used only with authorization and working authentication. Confirm project code is committed and pushed first; otherwise record non-portability.

## Data and verification

See [state-contract.md](references/state-contract.md) and the existing [tests](scripts/test_project_memory.py). Checkpoints are append-only; do not rewrite history to conceal concurrent changes.

Do not store authentication files, secrets, raw sessions, databases, browser profiles, or unapproved company/customer data. File presence and environment matching support only bounded recovery claims; full cross-device acceptance requires execution on the destination device.

Install the directory containing `SKILL.md` in the host's supported Skill location to invoke `$sync-project-state`. No top-level `LICENSE` is currently supplied.
