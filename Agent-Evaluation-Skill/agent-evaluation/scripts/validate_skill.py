#!/usr/bin/env python3
"""Validate the agent-evaluation skill without third-party dependencies."""

from __future__ import annotations

import argparse
import pathlib
import py_compile
import re
import sys
from typing import Dict, List


NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")
REF_RE = re.compile(r"`((?:references|scripts)/[^`]+)`")


def parse_frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end].strip().splitlines()
    data: Dict[str, str] = {}
    for line in raw:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_skill(skill_dir: pathlib.Path) -> List[str]:
    errors: List[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8-sig")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not NAME_RE.match(name):
        errors.append("frontmatter name must be lowercase hyphen-case under 64 chars")
    if name != skill_dir.name:
        errors.append(f"frontmatter name '{name}' must match folder name '{skill_dir.name}'")
    if not description or "TODO" in description:
        errors.append("frontmatter description must be complete")
    if len(description) < 80:
        errors.append("frontmatter description should explain triggers and use cases")

    for match in REF_RE.finditer(text):
        rel = match.group(1)
        if not (skill_dir / rel).exists():
            errors.append(f"referenced file does not exist: {rel}")

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if not agents_yaml.exists():
        errors.append("missing agents/openai.yaml")
    else:
        agents_text = agents_yaml.read_text(encoding="utf-8-sig")
        if f"${name}" not in agents_text:
            errors.append("agents/openai.yaml default_prompt should mention the skill name")
        if "short_description:" not in agents_text:
            errors.append("agents/openai.yaml missing short_description")

    for script in sorted((skill_dir / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"script does not compile: {script.name}: {exc.msg}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the agent-evaluation skill.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Path to the skill folder.")
    args = parser.parse_args()
    skill_dir = pathlib.Path(args.skill_dir).resolve()
    errors = validate_skill(skill_dir)
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Skill validation passed: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
