import unittest
from pathlib import Path

from aegisforge.validator import validate_repo


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def test_current_repository_has_no_validation_errors(self):
        findings = validate_repo(ROOT)
        errors = [finding for finding in findings if finding.severity == "error"]
        self.assertEqual(errors, [], msg=errors)

    def test_skill_files_are_present(self):
        skill_files = list((ROOT / "skills").glob("**/SKILL.md"))
        self.assertGreaterEqual(len(skill_files), 10)


if __name__ == "__main__":
    unittest.main()
