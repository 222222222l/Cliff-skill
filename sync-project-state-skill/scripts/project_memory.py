#!/usr/bin/env python3
"""Portable project checkpoint and Codex environment synchronizer."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None


SCHEMA_VERSION = 1
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".py", ".ps1",
    ".sh", ".js", ".ts", ".tsx", ".jsx", ".ini", ".cfg",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^<'\"]{8,}"),
]


class CommandError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def slug(value: str, fallback: str = "item") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-._").lower()
    return cleaned or fallback


def run(
    args: list[str],
    cwd: Path | None = None,
    timeout: int = 60,
    check: bool = False,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    if extra_env:
        env.update(extra_env)
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=env,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CommandError(f"Could not run {' '.join(args)}: {exc}") from exc
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise CommandError(f"{' '.join(args)} failed ({proc.returncode}): {detail}")
    return proc


def git(cwd: Path, *args: str, check: bool = False, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return run(["git", "-c", "core.quotepath=false", *args], cwd=cwd, check=check, timeout=timeout)


def atomic_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="\n", delete=False, dir=path.parent
    ) as handle:
        handle.write(payload)
        temp_name = handle.name
    os.replace(temp_name, path)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def find_upwards(start: Path, marker: str) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / marker).exists():
            return candidate
    return None


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve()


def resolve_memory_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    if os.environ.get("CODEX_MEMORY_HOME"):
        return Path(os.environ["CODEX_MEMORY_HOME"]).expanduser().resolve()
    discovered = find_upwards(Path.cwd(), "memory-config.json")
    if discovered:
        return discovered
    script_discovered = find_upwards(Path(__file__).resolve(), "memory-config.json")
    if script_discovered:
        return script_discovered
    pointer = codex_home() / "sync-project-state.json"
    if pointer.exists():
        data = load_json(pointer, {})
        if data.get("memory_root"):
            return Path(data["memory_root"]).expanduser().resolve()
    raise CommandError(
        "Memory repository not found. Set CODEX_MEMORY_HOME or run from a clone containing memory-config.json."
    )


def ensure_layout(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    defaults: list[tuple[Path, Any]] = [
        (
            root / "memory-config.json",
            {
                "schema_version": SCHEMA_VERSION,
                "name": "codex-project-memory",
                "checkpoint_policy": "append-only",
            },
        ),
        (root / "projects" / "index.json", {"schema_version": SCHEMA_VERSION, "projects": []}),
        (
            root / "environment" / "requirements.json",
            {
                "schema_version": SCHEMA_VERSION,
                "required_skills": [],
                "required_plugins": [],
                "required_mcp_servers": [],
                "config_expectations": {},
            },
        ),
    ]
    for path, data in defaults:
        if not path.exists():
            atomic_json(path, data)


def normalize_remote(remote: str) -> str:
    value = remote.strip().replace("\\", "/")
    if value.endswith(".git"):
        value = value[:-4]
    match = re.match(r"git@([^:]+):(.+)", value)
    if match:
        value = f"https://{match.group(1)}/{match.group(2)}"
    return value.rstrip("/")


def project_git_state(project: Path, fetch: bool = False, apply_ff: bool = False) -> dict[str, Any]:
    top = git(project, "rev-parse", "--show-toplevel", check=True).stdout.strip()
    root = Path(top).resolve()
    remote_proc = git(root, "config", "--get", "remote.origin.url")
    remote = remote_proc.stdout.strip() if remote_proc.returncode == 0 else ""
    branch_proc = git(root, "branch", "--show-current")
    branch = branch_proc.stdout.strip() or "(detached)"
    fetch_result: dict[str, Any] = {"attempted": False, "ok": None, "detail": ""}
    if fetch and remote:
        fetch_result["attempted"] = True
        proc = git(root, "fetch", "--prune", "origin", timeout=120)
        fetch_result["ok"] = proc.returncode == 0
        fetch_result["detail"] = (proc.stderr or proc.stdout).strip()

    commit = git(root, "rev-parse", "HEAD", check=True).stdout.strip()
    status_lines = [line for line in git(root, "status", "--short").stdout.splitlines() if line]
    upstream_proc = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    upstream = upstream_proc.stdout.strip() if upstream_proc.returncode == 0 else ""
    if not upstream and branch != "(detached)" and remote:
        candidate = f"origin/{branch}"
        if git(root, "rev-parse", "--verify", candidate).returncode == 0:
            upstream = candidate

    ahead = behind = None
    if upstream:
        counts = git(root, "rev-list", "--left-right", "--count", f"HEAD...{upstream}")
        if counts.returncode == 0:
            fields = counts.stdout.split()
            if len(fields) == 2:
                ahead, behind = int(fields[0]), int(fields[1])

    ff_result: dict[str, Any] = {"attempted": False, "ok": None, "detail": ""}
    if apply_ff and upstream and behind and behind > 0:
        if status_lines:
            ff_result["detail"] = "Working tree is dirty; fast-forward was not attempted."
        elif ahead == 0:
            ff_result["attempted"] = True
            proc = git(root, "merge", "--ff-only", upstream)
            ff_result["ok"] = proc.returncode == 0
            ff_result["detail"] = (proc.stderr or proc.stdout).strip()
            if proc.returncode == 0:
                commit = git(root, "rev-parse", "HEAD", check=True).stdout.strip()
                ahead, behind = 0, 0
        else:
            ff_result["detail"] = "Local and upstream histories diverged; automatic merge is forbidden."

    return {
        "root": str(root),
        "remote": remote,
        "canonical_remote": normalize_remote(remote) if remote else "",
        "branch": branch,
        "commit": commit,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "dirty": bool(status_lines),
        "status": status_lines,
        "fetch": fetch_result,
        "fast_forward": ff_result,
    }


def project_id(state: dict[str, Any], explicit: str | None = None) -> str:
    if explicit:
        return slug(explicit, "project")
    name = Path(state["root"]).name
    identity = state["canonical_remote"] or name
    digest = hashlib.sha256(identity.lower().encode("utf-8")).hexdigest()[:8]
    return f"{slug(name, 'project')}-{digest}"


def load_index(root: Path) -> dict[str, Any]:
    ensure_layout(root)
    return load_json(root / "projects" / "index.json", {"schema_version": SCHEMA_VERSION, "projects": []})


def register_project(
    memory_root: Path,
    project: Path,
    name: str | None = None,
    explicit_id: str | None = None,
    skills: list[str] | None = None,
    plugins: list[str] | None = None,
    mcp_servers: list[str] | None = None,
) -> tuple[dict[str, Any], bool]:
    state = project_git_state(project)
    pid = project_id(state, explicit_id)
    index = load_index(memory_root)
    now = utc_now()
    existing = None
    for item in index["projects"]:
        if item["id"] == pid or (
            state["canonical_remote"]
            and normalize_remote(item.get("remote", "")).lower() == state["canonical_remote"].lower()
        ):
            existing = item
            break
    changed = False
    if existing is None:
        existing = {
            "id": pid,
            "name": name or Path(state["root"]).name,
            "remote": state["canonical_remote"],
            "created_at": now,
            "updated_at": now,
            "requirements": {"skills": [], "plugins": [], "mcp_servers": []},
        }
        index["projects"].append(existing)
        changed = True
    else:
        pid = existing["id"]
        desired = {
            "name": name or existing.get("name") or Path(state["root"]).name,
            "remote": state["canonical_remote"] or existing.get("remote", ""),
        }
        for key, value in desired.items():
            if existing.get(key) != value:
                existing[key] = value
                changed = True
        existing.setdefault("requirements", {"skills": [], "plugins": [], "mcp_servers": []})

    additions = {
        "skills": skills or [],
        "plugins": plugins or [],
        "mcp_servers": mcp_servers or [],
    }
    for group, values in additions.items():
        current = existing["requirements"].setdefault(group, [])
        for value in values:
            if value not in current:
                current.append(value)
                changed = True
        current.sort()
    if changed:
        existing["updated_at"] = now
        index["projects"].sort(key=lambda item: item["id"])
        atomic_json(memory_root / "projects" / "index.json", index)
    return existing, changed


def hash_tree(path: Path) -> str:
    digest = hashlib.sha256()
    if not path.exists():
        return ""
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        if any(part in IGNORED_PARTS for part in file.parts):
            continue
        rel = file.relative_to(path).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def read_config(home: Path) -> dict[str, Any]:
    path = home / "config.toml"
    if not path.exists() or tomllib is None:
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, ValueError):
        return {}


def safe_config_snapshot(config: dict[str, Any]) -> dict[str, Any]:
    root_keys = [
        "model", "model_provider", "model_reasoning_effort", "model_verbosity",
        "approval_policy", "sandbox_mode", "web_search", "personality",
    ]
    result = {key: config[key] for key in root_keys if key in config}
    for section in ("agents", "features"):
        if isinstance(config.get(section), dict):
            result[section] = config[section]
    plugins = config.get("plugins", {})
    if isinstance(plugins, dict):
        result["plugins"] = {
            key: {"enabled": bool(value.get("enabled"))}
            for key, value in plugins.items()
            if isinstance(value, dict)
        }
    servers = config.get("mcp_servers", {})
    result["mcp_servers"] = sorted(servers.keys()) if isinstance(servers, dict) else []
    return result


def skill_inventory(home: Path) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    base = home / "skills"
    if not base.exists():
        return found
    candidates = [p for p in base.iterdir() if p.is_dir() and p.name != ".system"]
    system = base / ".system"
    if system.exists():
        candidates.extend(p for p in system.iterdir() if p.is_dir())
    for path in sorted(candidates, key=lambda p: p.name.lower()):
        if (path / "SKILL.md").exists():
            found.append(
                {
                    "name": path.name,
                    "scope": "system" if system in path.parents else "user",
                    "sha256": hash_tree(path),
                }
            )
    return found


def plugin_inventory(home: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    enabled = {
        key for key, value in config.get("plugins", {}).items()
        if isinstance(value, dict) and value.get("enabled")
    } if isinstance(config.get("plugins"), dict) else set()
    result: list[dict[str, Any]] = []
    cache = home / "plugins" / "cache"
    if not cache.exists():
        return result
    for market in sorted(p for p in cache.iterdir() if p.is_dir()):
        for plugin in sorted(p for p in market.iterdir() if p.is_dir()):
            versions = sorted(p.name for p in plugin.iterdir() if p.is_dir() and p.name != "latest")
            exact_id = f"{plugin.name}@{market.name}"
            result.append(
                {
                    "id": exact_id,
                    "versions": versions,
                    "enabled_in_config": exact_id in enabled,
                }
            )
    return result


def environment_snapshot(home: Path, device: str) -> dict[str, Any]:
    config = read_config(home)
    git_version = run(["git", "--version"]).stdout.strip() if shutil.which("git") else ""
    gh = shutil.which("gh")
    gh_authenticated = False
    if gh:
        gh_authenticated = run([gh, "auth", "status"], timeout=20).returncode == 0
    return {
        "schema_version": SCHEMA_VERSION,
        "captured_at": utc_now(),
        "device": slug(device, "device"),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "tools": {
            "git": {"available": bool(shutil.which("git")), "version": git_version},
            "gh": {"available": bool(gh), "authenticated": gh_authenticated},
        },
        "codex": {
            "skills": skill_inventory(home),
            "plugins": plugin_inventory(home, config),
            "config": safe_config_snapshot(config),
        },
    }


def dotted_get(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def finding(level: str, code: str, message: str, restorable: bool = False) -> dict[str, Any]:
    return {"level": level, "code": code, "message": message, "restorable": restorable}


def environment_findings(memory_root: Path, project_entry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    home = codex_home()
    snapshot = environment_snapshot(home, "current")
    requirements = load_json(memory_root / "environment" / "requirements.json", {})
    findings: list[dict[str, Any]] = []
    local_skills = {item["name"]: item for item in snapshot["codex"]["skills"]}
    local_plugins = {item["id"]: item for item in snapshot["codex"]["plugins"]}
    local_mcp = set(snapshot["codex"]["config"].get("mcp_servers", []))

    required_skills = list(requirements.get("required_skills", []))
    required_plugins = list(requirements.get("required_plugins", []))
    required_mcp = list(requirements.get("required_mcp_servers", []))
    if project_entry:
        preq = project_entry.get("requirements", {})
        required_skills.extend({"name": name, "severity": "blocking"} for name in preq.get("skills", []))
        required_plugins.extend({"id": pid, "severity": "blocking"} for pid in preq.get("plugins", []))
        required_mcp.extend({"name": name, "severity": "blocking"} for name in preq.get("mcp_servers", []))

    seen_skills: set[str] = set()
    for req in required_skills:
        name = req["name"]
        if name in seen_skills:
            continue
        seen_skills.add(name)
        severity = req.get("severity", "warning").upper()
        source = memory_root / req["source"] if req.get("source") else None
        if name not in local_skills:
            findings.append(
                finding(severity, "skill-missing", f"Skill '{name}' is missing.", bool(source and source.exists()))
            )
        elif source and source.exists():
            expected = hash_tree(source)
            if local_skills[name]["sha256"] != expected:
                findings.append(
                    finding(
                        severity,
                        "skill-version-mismatch",
                        f"Skill '{name}' differs from bundled source.",
                        True,
                    )
                )

    seen_plugins: set[str] = set()
    for req in required_plugins:
        pid = req["id"]
        if pid in seen_plugins:
            continue
        seen_plugins.add(pid)
        if pid not in local_plugins:
            findings.append(
                finding(
                    req.get("severity", "warning").upper(),
                    "plugin-missing",
                    f"Plugin '{pid}' is not installed; use Codex Plugin Management.",
                    False,
                )
            )

    seen_mcp: set[str] = set()
    for req in required_mcp:
        name = req["name"]
        if name in seen_mcp:
            continue
        seen_mcp.add(name)
        if name not in local_mcp:
            findings.append(
                finding(
                    req.get("severity", "warning").upper(),
                    "mcp-missing",
                    f"MCP server '{name}' is not configured; credentials are not portable.",
                    False,
                )
            )

    safe_config = snapshot["codex"]["config"]
    for key, expectation in requirements.get("config_expectations", {}).items():
        actual = dotted_get(safe_config, key)
        ok = actual == expectation.get("equals") if "equals" in expectation else actual in expectation.get("allowed", [])
        if not ok:
            findings.append(
                finding(
                    expectation.get("severity", "warning").upper(),
                    "config-mismatch",
                    f"Config '{key}' is {actual!r}; expected {expectation.get('equals', expectation.get('allowed'))!r}.",
                    False,
                )
            )

    if not snapshot["tools"]["git"]["available"]:
        findings.append(finding("BLOCKING", "git-missing", "Git is not available.", False))
    if not findings:
        findings.append(finding("OK", "environment-ready", "All declared environment requirements are satisfied."))
    return findings


def scan_skill_for_secrets(source: Path) -> list[str]:
    issues: list[str] = []
    for file in (p for p in source.rglob("*") if p.is_file()):
        if any(part in IGNORED_PARTS for part in file.parts):
            continue
        lower_parts = {part.lower() for part in file.parts}
        if ".env" in lower_parts or "secrets" in lower_parts or file.name.lower() == "auth.json":
            issues.append(f"forbidden path: {file.relative_to(source)}")
            continue
        if file.suffix.lower() not in TEXT_SUFFIXES or file.stat().st_size > 1_000_000:
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            issues.append(f"possible secret: {file.relative_to(source)}")
    return issues


def copy_skill(source: Path, target: Path) -> None:
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".pytest_cache"),
    )


def install_skills(memory_root: Path, apply: bool, replace: bool) -> dict[str, Any]:
    home = codex_home()
    source_root = memory_root / "skills"
    target_root = home / "skills"
    actions: list[dict[str, Any]] = []
    if not source_root.exists():
        return {"actions": actions, "pointer_written": False}
    for source in sorted(p for p in source_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
        target = target_root / source.name
        source_hash = hash_tree(source)
        target_hash = hash_tree(target)
        if source_hash == target_hash:
            actions.append({"skill": source.name, "status": "unchanged"})
            continue
        if target.exists() and not replace:
            actions.append({"skill": source.name, "status": "mismatch", "action": "approval-required"})
            continue
        if not apply:
            actions.append({"skill": source.name, "status": "missing" if not target.exists() else "replace-planned"})
            continue
        target_root.mkdir(parents=True, exist_ok=True)
        backup = None
        if target.exists():
            backup_root = home / "skill-backups"
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            backup = backup_root / f"{source.name}-{stamp}"
            shutil.move(str(target), str(backup))
        copy_skill(source, target)
        actions.append(
            {"skill": source.name, "status": "installed", "backup": str(backup) if backup else None}
        )
    pointer_written = False
    if apply:
        atomic_json(home / "sync-project-state.json", {"memory_root": str(memory_root)})
        pointer_written = True
    return {"actions": actions, "pointer_written": pointer_written}


def export_skill(memory_root: Path, name: str, replace: bool) -> dict[str, Any]:
    source = codex_home() / "skills" / name
    target = memory_root / "skills" / name
    if not (source / "SKILL.md").exists():
        raise CommandError(f"Skill '{name}' was not found under {source.parent}.")
    issues = scan_skill_for_secrets(source)
    if issues:
        raise CommandError("Skill export refused: " + "; ".join(issues))
    if target.exists():
        if hash_tree(source) == hash_tree(target):
            return {"skill": name, "status": "unchanged"}
        if not replace:
            return {"skill": name, "status": "mismatch", "action": "rerun-with---replace"}
        shutil.rmtree(target)
    copy_skill(source, target)
    return {"skill": name, "status": "exported", "sha256": hash_tree(target)}


def memory_pull(root: Path) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {"status": "warning", "detail": "Memory directory is not a Git repository."}
    if git(root, "status", "--porcelain").stdout.strip():
        return {"status": "blocking", "detail": "Memory repository is dirty; pull was not attempted."}
    remote = git(root, "remote", "get-url", "origin")
    if remote.returncode != 0:
        return {"status": "warning", "detail": "Memory repository has no origin remote."}
    fetch = git(root, "fetch", "--prune", "origin", timeout=120)
    if fetch.returncode != 0:
        return {"status": "blocking", "detail": (fetch.stderr or fetch.stdout).strip()}
    upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream.returncode != 0:
        return {"status": "warning", "detail": "Current memory branch has no upstream."}
    merge = git(root, "merge", "--ff-only", upstream.stdout.strip())
    return {
        "status": "ok" if merge.returncode == 0 else "blocking",
        "detail": (merge.stderr or merge.stdout).strip(),
    }


def commit_and_push_memory(root: Path, project: dict[str, Any], checkpoint_path: Path) -> dict[str, Any]:
    rel_checkpoint = checkpoint_path.relative_to(root).as_posix()
    paths = [rel_checkpoint]
    index_path = root / "projects" / "index.json"
    if git(root, "status", "--porcelain", "--", "projects/index.json").stdout.strip():
        paths.append("projects/index.json")
    add = git(root, "add", "--", *paths)
    if add.returncode != 0:
        return {"status": "blocking", "detail": (add.stderr or add.stdout).strip()}
    staged = git(root, "diff", "--cached", "--quiet")
    if staged.returncode == 0:
        return {"status": "ok", "detail": "No memory changes to commit."}
    message = f"checkpoint({project['id']}): update project handoff"
    commit = git(root, "commit", "-m", message)
    if commit.returncode != 0:
        return {"status": "blocking", "detail": (commit.stderr or commit.stdout).strip()}
    pull = git(root, "pull", "--rebase", timeout=120)
    if pull.returncode != 0:
        return {"status": "blocking", "detail": (pull.stderr or pull.stdout).strip()}
    push = git(root, "push", timeout=120)
    return {
        "status": "ok" if push.returncode == 0 else "blocking",
        "detail": (push.stderr or push.stdout).strip(),
    }


def latest_checkpoint(root: Path, pid: str) -> dict[str, Any] | None:
    directory = root / "projects" / pid / "checkpoints"
    if not directory.exists():
        return None
    candidates = sorted(directory.glob("*.json"))
    return load_json(candidates[-1], None) if candidates else None


def project_portability(state: dict[str, Any], findings: list[dict[str, Any]]) -> dict[str, Any]:
    reasons: list[str] = []
    if state["dirty"]:
        reasons.append("working tree has uncommitted changes")
    if state["ahead"] is None:
        reasons.append("upstream is not configured")
    elif state["ahead"] > 0:
        reasons.append(f"{state['ahead']} local commit(s) are not on upstream")
    if not state["remote"]:
        reasons.append("origin remote is missing")
    blocking = [item["message"] for item in findings if item["level"] == "BLOCKING"]
    reasons.extend(blocking)
    return {"portable": not reasons, "reasons": reasons}


def render_report(data: dict[str, Any]) -> str:
    lines = [f"# {data.get('title', 'Project memory report')}"]
    if data.get("memory_sync"):
        lines.append(f"- Memory sync: {data['memory_sync']['status'].upper()} — {data['memory_sync']['detail']}")
    if data.get("project"):
        project = data["project"]
        lines.extend(
            [
                f"- Project: {project.get('name', project.get('id', 'unknown'))}",
                f"- Branch/commit: {project.get('git', {}).get('branch')} / {project.get('git', {}).get('commit', '')[:12]}",
                f"- Upstream: ahead={project.get('git', {}).get('ahead')} behind={project.get('git', {}).get('behind')}",
            ]
        )
    checkpoint = data.get("checkpoint")
    if checkpoint:
        lines.extend(
            [
                "## Latest checkpoint",
                f"- Summary: {checkpoint.get('summary') or '(empty)'}",
                f"- Next action: {checkpoint.get('next_action') or '(empty)'}",
                f"- Portable: {checkpoint.get('portability', {}).get('portable')}",
            ]
        )
    findings = data.get("environment_findings", [])
    if findings:
        lines.append("## Environment")
        lines.extend(f"- {item['level']}: {item['message']}" for item in findings)
    if data.get("portability"):
        lines.append("## Current portability")
        lines.append(f"- Portable: {data['portability']['portable']}")
        lines.extend(f"- BLOCKING: {reason}" for reason in data["portability"]["reasons"])
    if data.get("result"):
        lines.append(f"## Result\n- {data['result']}")
    return "\n".join(lines)


def emit(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_report(data))


def cmd_start(args: argparse.Namespace, root: Path) -> int:
    memory_sync = {"status": "skipped", "detail": "Disabled by --no-memory-pull."}
    if not args.no_memory_pull:
        memory_sync = memory_pull(root)
    entry, _ = register_project(root, Path(args.project))
    state = project_git_state(Path(args.project), fetch=not args.no_fetch, apply_ff=not args.check_only)
    findings = environment_findings(root, entry)
    checkpoint = latest_checkpoint(root, entry["id"])
    portability = project_portability(state, findings)
    report = {
        "title": "Cross-device project start",
        "memory_sync": memory_sync,
        "project": {"id": entry["id"], "name": entry["name"], "git": state},
        "checkpoint": checkpoint,
        "environment_findings": findings,
        "portability": portability,
    }
    emit(report, args.json)
    blocked = memory_sync["status"] == "blocking" or any(i["level"] == "BLOCKING" for i in findings)
    if state["ahead"] and state["behind"]:
        blocked = True
    return 2 if blocked else 0


def cmd_finish(args: argparse.Namespace, root: Path) -> int:
    entry, _ = register_project(root, Path(args.project))
    state = project_git_state(Path(args.project), fetch=True, apply_ff=False)
    findings = environment_findings(root, entry)
    portability = project_portability(state, findings)
    device = slug(args.device or os.environ.get("CODEX_DEVICE_ID") or platform.node(), "device")
    timestamp = utc_now()
    filename_stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    checkpoint = {
        "schema_version": SCHEMA_VERSION,
        "created_at": timestamp,
        "device": device,
        "project_id": entry["id"],
        "summary": args.summary,
        "next_action": args.next_action,
        "decisions": args.decision,
        "blockers": args.blocker,
        "tests": args.test,
        "git": {key: state[key] for key in (
            "remote", "canonical_remote", "branch", "commit", "upstream",
            "ahead", "behind", "dirty", "status"
        )},
        "environment_findings": findings,
        "portability": portability,
    }
    path = root / "projects" / entry["id"] / "checkpoints" / f"{filename_stamp}-{device}.json"
    atomic_json(path, checkpoint)
    sync_result = None
    if args.push_memory:
        sync_result = commit_and_push_memory(root, entry, path)
    report = {
        "title": "Cross-device project checkpoint",
        "project": {"id": entry["id"], "name": entry["name"], "git": state},
        "checkpoint": checkpoint,
        "environment_findings": findings,
        "portability": portability,
        "result": f"Checkpoint written to {path.relative_to(root).as_posix()}",
    }
    if sync_result:
        report["memory_sync"] = sync_result
    emit(report, args.json)
    blocked = not portability["portable"] or (sync_result and sync_result["status"] == "blocking")
    return 2 if blocked else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory-root", help="Path to the project-memory repository.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize repository data files.")

    bootstrap = sub.add_parser("bootstrap", help="Install bundled Skills, capture environment, and run doctor.")
    bootstrap.add_argument("--device", required=True)
    bootstrap.add_argument("--apply", action="store_true")
    bootstrap.add_argument("--replace", action="store_true")

    capture = sub.add_parser("capture-env", help="Write a non-secret device inventory.")
    capture.add_argument("--device", required=True)

    sub.add_parser("doctor", help="Compare this device with declared requirements.")

    install = sub.add_parser("install-skills", help="Install portable Skills from the memory repository.")
    install.add_argument("--apply", action="store_true")
    install.add_argument("--replace", action="store_true")

    export = sub.add_parser("export-skill", help="Copy a local Skill into the private memory repository.")
    export.add_argument("name")
    export.add_argument("--replace", action="store_true")

    register = sub.add_parser("register", help="Register or update a project identity.")
    register.add_argument("project")
    register.add_argument("--name")
    register.add_argument("--id")
    register.add_argument("--require-skill", action="append", default=[])
    register.add_argument("--require-plugin", action="append", default=[])
    register.add_argument("--require-mcp", action="append", default=[])

    start = sub.add_parser("start", help="Synchronize and restore a project checkpoint.")
    start.add_argument("project")
    start.add_argument("--no-memory-pull", action="store_true")
    start.add_argument("--no-fetch", action="store_true")
    start.add_argument("--check-only", action="store_true")

    finish = sub.add_parser("finish", help="Create an immutable project checkpoint.")
    finish.add_argument("project")
    finish.add_argument("--summary", required=True)
    finish.add_argument("--next-action", required=True)
    finish.add_argument("--decision", action="append", default=[])
    finish.add_argument("--blocker", action="append", default=[])
    finish.add_argument("--test", action="append", default=[])
    finish.add_argument("--device")
    finish.add_argument("--push-memory", action="store_true")

    sync = sub.add_parser("sync-memory", help="Fast-forward the memory repository.")
    sync.add_argument("--pull", action="store_true", default=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        root = resolve_memory_root(args.memory_root)
        ensure_layout(root)
        if args.command == "init":
            emit({"title": "Memory repository initialized", "result": str(root)}, args.json)
            return 0
        if args.command == "capture-env":
            snapshot = environment_snapshot(codex_home(), args.device)
            path = root / "environment" / "devices" / f"{slug(args.device, 'device')}.json"
            atomic_json(path, snapshot)
            emit({"title": "Environment captured", "result": str(path.relative_to(root))}, args.json)
            return 0
        if args.command == "doctor":
            findings = environment_findings(root)
            emit({"title": "Codex environment doctor", "environment_findings": findings}, args.json)
            return 2 if any(item["level"] == "BLOCKING" for item in findings) else 0
        if args.command == "install-skills":
            result = install_skills(root, args.apply, args.replace)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("# Skill installation")
                for item in result["actions"]:
                    print(f"- {item['skill']}: {item['status']}")
            return 0
        if args.command == "export-skill":
            result = export_skill(root, args.name, args.replace)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"# Skill export\n- {result['skill']}: {result['status']}")
            return 0
        if args.command == "bootstrap":
            install_result = install_skills(root, args.apply, args.replace)
            snapshot = environment_snapshot(codex_home(), args.device)
            path = root / "environment" / "devices" / f"{slug(args.device, 'device')}.json"
            atomic_json(path, snapshot)
            findings = environment_findings(root)
            report = {
                "title": "Cross-device bootstrap",
                "environment_findings": findings,
                "result": f"Inventory: {path.relative_to(root)}; Skills: {install_result['actions']}",
            }
            emit(report, args.json)
            return 2 if any(item["level"] == "BLOCKING" for item in findings) else 0
        if args.command == "register":
            entry, changed = register_project(
                root,
                Path(args.project),
                args.name,
                args.id,
                args.require_skill,
                args.require_plugin,
                args.require_mcp,
            )
            payload = {
                "title": "Project registration",
                "project": {"id": entry["id"], "name": entry["name"], "git": project_git_state(Path(args.project))},
                "result": "updated" if changed else "unchanged",
            }
            emit(payload, args.json)
            return 0
        if args.command == "start":
            return cmd_start(args, root)
        if args.command == "finish":
            return cmd_finish(args, root)
        if args.command == "sync-memory":
            result = memory_pull(root)
            emit({"title": "Memory synchronization", "memory_sync": result}, args.json)
            return 2 if result["status"] == "blocking" else 0
        parser.error(f"Unhandled command: {args.command}")
    except (CommandError, json.JSONDecodeError, OSError) as exc:
        if getattr(args, "json", False):
            print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"BLOCKING: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
