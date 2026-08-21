from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from aegisforge.evidence import EvidenceLedger


class EvidenceTests(unittest.TestCase):
    def test_empty_ledger_is_incomplete(self):
        ledger = EvidenceLedger("Change", "Reason")
        self.assertIn("at least one evidence item is required", ledger.validate())
        self.assertFalse(ledger.passed)

    def test_failed_check_requires_uncertainty(self):
        ledger = EvidenceLedger("Change", "Reason")
        ledger.add("test", "Regression test", outcome="fail")
        self.assertIn("failed evidence requires an uncertainty or remediation note", ledger.validate())
        ledger.add_uncertainty("Failure is tracked for follow-up.")
        self.assertFalse(ledger.passed)

    def test_unknown_evidence_cannot_pass(self):
        ledger = EvidenceLedger("Change", "Reason")
        ledger.add("verification", "Result was not observed", outcome="unknown")
        self.assertFalse(ledger.passed)
        self.assertIn("all evidence items must pass before work can be verified or released", ledger.validate())

    def test_not_run_evidence_blocks_release(self):
        ledger = EvidenceLedger("Change", "Reason", approved_by="reviewer")
        ledger.add("test", "Production test was skipped", outcome="not-run")
        self.assertIn("all evidence items must pass before work can be verified or released", ledger.validate(require_approval=True))

    def test_ledger_round_trips_and_passes(self):
        ledger = EvidenceLedger("Change", "Reason", approved_by="reviewer", independently_verified=True, verifier="independent")
        ledger.add("test", "Unit tests passed", outcome="pass", command="python -m unittest")
        ledger.add("verification", "CLI output inspected", outcome="pass")
        with tempfile.TemporaryDirectory() as directory:
            path = ledger.save(Path(directory) / "evidence.json")
            loaded = EvidenceLedger.load(path)
        self.assertTrue(loaded.passed)
        self.assertEqual(loaded.items[0].command, "python -m unittest")
        self.assertEqual(loaded.approved_by, "reviewer")


if __name__ == "__main__":
    unittest.main()
