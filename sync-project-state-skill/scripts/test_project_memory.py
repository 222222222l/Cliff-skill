from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import project_memory as pm


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.strip()


class ProjectMemoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.memory = self.base / "memory"
        self.remote = self.base / "remote.git"
        self.project = self.base / "project"
        self.other = self.base / "other"
        pm.ensure_layout(self.memory)
        git(self.base, "init", "--bare", str(self.remote))
        git(self.base, "clone", str(self.remote), str(self.project))
        git(self.project, "config", "user.name", "Test User")
        git(self.project, "config", "user.email", "test@example.invalid")
        (self.project / "file.txt").write_text("one\n", encoding="utf-8")
        git(self.project, "add", "file.txt")
        git(self.project, "commit", "-m", "initial")
        git(self.project, "push", "-u", "origin", "HEAD")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_register_is_stable_and_path_free(self) -> None:
        first, changed = pm.register_project(self.memory, self.project)
        second, changed_again = pm.register_project(self.memory, self.project)
        self.assertTrue(changed)
        self.assertFalse(changed_again)
        self.assertEqual(first["id"], second["id"])
        serialized = (self.memory / "projects" / "index.json").read_text(encoding="utf-8")
        self.assertNotIn(str(self.project), serialized)

    def test_fast_forward_clean_project(self) -> None:
        git(self.base, "clone", str(self.remote), str(self.other))
        git(self.other, "config", "user.name", "Other User")
        git(self.other, "config", "user.email", "other@example.invalid")
        (self.other / "file.txt").write_text("two\n", encoding="utf-8")
        git(self.other, "commit", "-am", "remote change")
        git(self.other, "push")
        before = git(self.project, "rev-parse", "HEAD")
        state = pm.project_git_state(self.project, fetch=True, apply_ff=True)
        self.assertNotEqual(before, state["commit"])
        self.assertEqual(state["behind"], 0)
        self.assertTrue(state["fast_forward"]["ok"])

    def test_dirty_project_is_not_fast_forwarded(self) -> None:
        git(self.base, "clone", str(self.remote), str(self.other))
        git(self.other, "config", "user.name", "Other User")
        git(self.other, "config", "user.email", "other@example.invalid")
        (self.other / "file.txt").write_text("remote\n", encoding="utf-8")
        git(self.other, "commit", "-am", "remote change")
        git(self.other, "push")
        (self.project / "local.txt").write_text("dirty\n", encoding="utf-8")
        before = git(self.project, "rev-parse", "HEAD")
        state = pm.project_git_state(self.project, fetch=True, apply_ff=True)
        self.assertEqual(before, state["commit"])
        self.assertTrue(state["dirty"])
        self.assertIn("dirty", state["fast_forward"]["detail"].lower())

    def test_environment_reports_restorable_missing_skill(self) -> None:
        source = self.memory / "skills" / "demo"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\n", encoding="utf-8")
        pm.atomic_json(
            self.memory / "environment" / "requirements.json",
            {
                "schema_version": 1,
                "required_skills": [
                    {"name": "demo", "severity": "blocking", "source": "skills/demo"}
                ],
                "required_plugins": [],
                "required_mcp_servers": [],
                "config_expectations": {},
            },
        )
        fake_home = self.base / "codex"
        with patch.dict(os.environ, {"CODEX_HOME": str(fake_home)}):
            findings = pm.environment_findings(self.memory)
        missing = next(item for item in findings if item["code"] == "skill-missing")
        self.assertEqual(missing["level"], "BLOCKING")
        self.assertTrue(missing["restorable"])

    def test_checkpoint_is_append_only(self) -> None:
        entry, _ = pm.register_project(self.memory, self.project)
        checkpoint_dir = self.memory / "projects" / entry["id"] / "checkpoints"
        checkpoint_dir.mkdir(parents=True)
        pm.atomic_json(checkpoint_dir / "20260101T000000.000000Z-a.json", {"summary": "first"})
        pm.atomic_json(checkpoint_dir / "20260102T000000.000000Z-b.json", {"summary": "second"})
        self.assertEqual(pm.latest_checkpoint(self.memory, entry["id"])["summary"], "second")

    def test_secret_scanner_rejects_private_key(self) -> None:
        skill = self.base / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "-----BEGIN " + "PRIVATE KEY-----\nnot-a-real-key\n", encoding="utf-8"
        )
        self.assertTrue(pm.scan_skill_for_secrets(skill))


if __name__ == "__main__":
    unittest.main()
