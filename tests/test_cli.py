from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from aegisforge.cli import main


VALID_SKILL = """---
id: testing.example-skill
name: Example Skill
slug: example-skill
version: 1.0.0
status: stable
summary: Perform an example testing task.
description: Use when an example testing task is requested.
domains:
  - testing
capabilities:
  - analysis
skill_type: procedure
keywords:
  - example
  - testing
inputs:
  - request
outputs:
  - result
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
---
# Example Skill

## When to Use

Use for example testing tasks.

## Verification

Inspect the result.
"""


class UnifiedCliTests(unittest.TestCase):
    def test_assess_command_returns_json(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["assess", "--text", "delete production data"])
        payload = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(payload["risk_level"], "critical")
        self.assertEqual(payload["workflow"], "high-assurance")

    def test_search_command_returns_explainable_match(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_path = root / "skills" / "testing" / "example-skill" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text(VALID_SKILL, encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = main(["search", "testing example", "--root", str(root), "--limit", "1"])
            payload = json.loads(output.getvalue())
            self.assertEqual(status, 0)
            self.assertEqual(payload[0]["id"], "testing.example-skill")
            self.assertTrue(payload[0]["reasons"])


if __name__ == "__main__":
    unittest.main()
