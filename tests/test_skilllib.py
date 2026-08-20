from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aegisforge.skilllib.frontmatter import parse_front_matter
from aegisforge.skilllib.registry import discover, validate_skill
from aegisforge.skilllib.router import route, search


VALID_SKILL = """---
id: test.example-skill
name: Example Skill
slug: example-skill
version: 1.0.0
status: stable
summary: Do an example task.
description: Use when an example task is requested.
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

Use for example tasks.

## Verification

Inspect the result.
"""


class SkillLibraryTests(unittest.TestCase):
    def test_parser_supports_lists_and_nested_mappings(self):
        metadata, body = parse_front_matter(VALID_SKILL)
        self.assertEqual(metadata["domains"], ["testing"])
        self.assertEqual(metadata["risk"]["level"], "low")
        self.assertIn("# Example Skill", body)

    def test_discovery_and_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "skills" / "testing" / "example-skill" / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_SKILL, encoding="utf-8")
            records, issues = discover(root)
            self.assertEqual(len(records), 1)
            self.assertFalse([issue for issue in issues if issue.severity == "error"])
            self.assertEqual(validate_skill(path), [])

    def test_search_exposes_match_reasons(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "skills" / "testing" / "example-skill" / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(VALID_SKILL, encoding="utf-8")
            records, _ = discover(root)
            matches = search(records, "testing example", limit=3)
            self.assertEqual(matches[0].record.id, "test.example-skill")
            self.assertTrue(matches[0].reasons)

    def test_route_prefers_stable_low_risk_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "skills" / "testing"
            for slug, status, risk in [("stable-skill", "stable", "low"), ("draft-skill", "draft", "high")]:
                path = base / slug / "SKILL.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(VALID_SKILL.replace("test.example-skill", f"testing.{slug}").replace("example-skill", slug).replace("status: stable", f"status: {status}").replace("level: low", f"level: {risk}"), encoding="utf-8")
            records, _ = discover(root)
            matches = route(records, "example testing", limit=2)
            self.assertEqual(matches[0].record.status, "stable")


if __name__ == "__main__":
    unittest.main()
