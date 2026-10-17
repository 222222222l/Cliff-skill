#!/usr/bin/env python3
"""Validate this skill package without third-party YAML dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
QUOTED_FIELD_RE = re.compile(r'^\s{2}([a-z_]+):\s+"(.*)"\s*$', re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z_]+):\s+(.+)", line)
        if not match:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = match.groups()
        if key in fields:
            raise ValueError(f"duplicate frontmatter key: {key}")
        fields[key] = value.strip().strip('"')
    return fields, text[end + 5 :]


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    skill_root = skill_root.resolve()
    skill_path = skill_root / "SKILL.md"
    agent_path = skill_root / "agents" / "openai.yaml"

    if not NAME_RE.fullmatch(skill_root.name) or len(skill_root.name) >= 64:
        errors.append("skill folder name must be hyphen-case and shorter than 64 characters")
    if not skill_path.is_file():
        return errors + ["missing SKILL.md"]

    try:
        skill_text = skill_path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(skill_text)
    except (UnicodeDecodeError, ValueError) as exc:
        return errors + [f"invalid SKILL.md: {exc}"]

    if set(fields) != {"name", "description"}:
        errors.append("frontmatter must contain only name and description")
    if fields.get("name") != skill_root.name:
        errors.append("frontmatter name must match the skill folder")
    description = fields.get("description", "")
    lowered_description = description.lower()
    has_trigger_phrase = "use when" in lowered_description or "use proactively when" in lowered_description
    if len(description) < 80 or not has_trigger_phrase:
        errors.append("description must explain capability and concrete trigger contexts")
    if "proactively" not in lowered_description or "agent itself observes" not in lowered_description:
        errors.append("description must explicitly support agent-observed proactive invocation")
    if len(body.splitlines()) > 500:
        errors.append("SKILL.md body must stay under 500 lines")

    for path in skill_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"not UTF-8: {path.relative_to(skill_root)}")
            continue
        placeholder = "TO" + "DO"
        if placeholder in text or f"[{placeholder}" in text:
            errors.append(f"placeholder remains: {path.relative_to(skill_root)}")
        if path.suffix.lower() == ".md" and len(text.splitlines()) > 100 and "## Contents" not in text:
            errors.append(f"long Markdown file lacks a Contents section: {path.relative_to(skill_root)}")

    for target in LINK_RE.findall(body):
        target = target.strip().split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target):
            continue
        if not (skill_root / target).is_file():
            errors.append(f"broken SKILL.md link: {target}")

    if not agent_path.is_file():
        errors.append("missing agents/openai.yaml")
    else:
        try:
            agent_text = agent_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append("agents/openai.yaml is not UTF-8")
        else:
            values = dict(QUOTED_FIELD_RE.findall(agent_text))
            expected = {"display_name", "short_description", "default_prompt"}
            if set(values) != expected:
                errors.append("openai.yaml must contain the three required quoted interface fields")
            short = values.get("short_description", "")
            if not 25 <= len(short) <= 64:
                errors.append("short_description must be 25-64 characters")
            if f"${skill_root.name}" not in values.get("default_prompt", ""):
                errors.append("default_prompt must explicitly mention the skill")
            if "policy:\n  allow_implicit_invocation: true" not in agent_text:
                errors.append("openai.yaml must explicitly enable implicit invocation")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.skill_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Skill validation passed: {args.skill_root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
