from __future__ import annotations

import unittest
from pathlib import Path

from aegisforge.evaluation import evaluate_all, load_scenarios


class EvaluationTests(unittest.TestCase):
    def test_repository_scenarios_pass(self):
        scenarios = load_scenarios(Path(__file__).parents[1] / "evaluation" / "scenarios.json")
        report = evaluate_all(scenarios)
        self.assertEqual(report.failed, 0)
        self.assertEqual(report.pass_rate, 1.0)
        self.assertGreaterEqual(report.total, 8)


if __name__ == "__main__":
    unittest.main()
