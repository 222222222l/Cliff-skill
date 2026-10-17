#!/usr/bin/env python3
"""Validate the market-signal-analysis skill's progressive-disclosure graph."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE_PATTERN = re.compile(r"`?(references/[A-Za-z0-9._/-]+\.md)`?")
SCRIPT_PATTERN = re.compile(r"`?(scripts/[A-Za-z0-9._/-]+\.py)`?")
MAX_SKILL_LINES = 140
MAX_SKILL_WORDS = 1_900


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    text = SKILL.read_text(encoding="utf-8")
    lines = text.splitlines()
    words = re.findall(r"\b[\w-]+\b", text)

    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md is missing YAML frontmatter")
    else:
        keys = re.findall(r"^([A-Za-z0-9_-]+):", frontmatter.group(1), re.MULTILINE)
        if keys != ["name", "description"]:
            errors.append(f"frontmatter keys must be name,description; found {keys}")

    if len(lines) > MAX_SKILL_LINES:
        errors.append(f"SKILL.md has {len(lines)} lines; budget is {MAX_SKILL_LINES}")
    if len(words) > MAX_SKILL_WORDS:
        errors.append(f"SKILL.md has {len(words)} words; budget is {MAX_SKILL_WORDS}")

    linked = set(REFERENCE_PATTERN.findall(text))
    existing = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "references").glob("*.md")
    }

    missing = sorted(linked - existing)
    orphaned = sorted(existing - linked)
    if missing:
        errors.extend(f"missing linked reference: {path}" for path in missing)
    if orphaned:
        errors.extend(f"reference is not directly routed from SKILL.md: {path}" for path in orphaned)

    for markdown in [SKILL, *sorted((ROOT / "references").glob("*.md"))]:
        body = markdown.read_text(encoding="utf-8")
        for target in REFERENCE_PATTERN.findall(body):
            if target not in existing:
                errors.append(f"{markdown.relative_to(ROOT)} links missing {target}")

    linked_scripts = set(SCRIPT_PATTERN.findall(text))
    existing_scripts = {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*.py")
    }
    missing_scripts = sorted(linked_scripts - existing_scripts)
    orphaned_scripts = sorted(existing_scripts - linked_scripts)
    if missing_scripts:
        errors.extend(f"missing linked script: {path}" for path in missing_scripts)
    if orphaned_scripts:
        errors.extend(
            f"script is not directly routed from SKILL.md: {path}"
            for path in orphaned_scripts
        )

    openai_yaml = ROOT / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append("agents/openai.yaml is missing")
    elif "$market-signal-analysis" not in openai_yaml.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml default_prompt must invoke $market-signal-analysis")

    readme = ROOT / "README.md"
    if readme.exists() and "research-basis.md" in readme.read_text(encoding="utf-8"):
        warnings.append("README.md still mentions merged references/research-basis.md")

    print(f"SKILL.md: {len(lines)} lines, {len(words)} words")
    print(f"References: {len(existing)} files, {len(linked)} directly routed")
    print(
        f"Scripts: {len(existing_scripts)} files, "
        f"{len(linked_scripts)} directly routed"
    )
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: progressive-disclosure graph is valid ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
