# State contract

## Repository boundaries

- The memory repository owns project identities, checkpoints, portable Skills, and environment requirements.
- Each project repository owns source code, artifacts, branches, commits, tests, and its agent-friendly documentation.
- Codex owns local conversations and runtime databases. They are never synchronized by this repository.

## Project index

`projects/index.json` contains stable project identities derived from the canonical Git remote. It must not contain device-local absolute paths or credentials.

Each entry may contain:

- `id`, `name`, `remote`
- `created_at`, `updated_at`
- `requirements.skills`
- `requirements.plugins`
- `requirements.mcp_servers`

## Checkpoint

`projects/<project-id>/checkpoints/*.json` is append-only. A checkpoint contains:

- UTC timestamp and device ID
- Git remote, branch, commit, upstream, ahead/behind counts
- Dirty-file status
- Summary and exact next action
- Decisions, blockers, and test evidence
- Portability verdict
- Environment findings at checkpoint time

A checkpoint is portable only when the working tree is clean, the current commit is reachable from the configured remote, and every blocking environment requirement is satisfied.

## Environment requirements

`environment/requirements.json` has four requirement groups:

- `required_skills`: name, severity, and optional bundled source path
- `required_plugins`: exact `plugin@marketplace` ID and severity
- `required_mcp_servers`: configured server name and severity
- `config_expectations`: safe dotted config key plus an expected or allowed value

Only non-secret configuration is inventoried. Authentication is tested through the required operation and never serialized.

## Status levels

- `OK`: requirement satisfied.
- `WARNING`: work may proceed, but behavior can differ.
- `BLOCKING`: automatic restoration is incomplete; surface it before project work.

## Merge model

- Checkpoints use unique timestamp/device filenames and are not edited after creation.
- Device inventories use one stable filename per device.
- Project registration changes the central index and may require ordinary Git conflict resolution.
- Never solve a rejected push by force-pushing.
