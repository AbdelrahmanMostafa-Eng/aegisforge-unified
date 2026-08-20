from __future__ import annotations

import unittest

from aegisforge.evidence import EvidenceLedger
from aegisforge.governance import WorkRecord, WorkState
from aegisforge.policy import assess


class GovernanceTests(unittest.TestCase):
    def test_critical_work_cannot_skip_authorization(self):
        record = WorkRecord(assess("delete production data"))
        decision = record.transition(WorkState.AUTHORIZED)
        self.assertFalse(decision.allowed)
        self.assertEqual(record.state, WorkState.PLANNED)

    def test_critical_work_requires_evidence_before_verification(self):
        record = WorkRecord(assess("delete production data"))
        self.assertTrue(record.transition(WorkState.AUTHORIZED, actor="human").allowed)
        self.assertTrue(record.transition(WorkState.EXECUTED).allowed)
        decision = record.transition(WorkState.VERIFIED)
        self.assertFalse(decision.allowed)
        self.assertIn("evidence ledger", decision.reason)

    def test_complete_critical_work_can_reach_release(self):
        record = WorkRecord(assess("delete production data"))
        ledger = EvidenceLedger("Delete records", "User-approved retention request", approved_by="human", independently_verified=True, verifier="reviewer")
        ledger.add("test", "Deletion fixture passed", outcome="pass", command="pytest")
        ledger.add("verification", "Post-action count checked", outcome="pass")
        self.assertTrue(record.transition(WorkState.AUTHORIZED, actor="human").allowed)
        self.assertTrue(record.transition(WorkState.EXECUTED).allowed)
        self.assertTrue(record.transition(WorkState.VERIFIED, evidence=ledger).allowed)
        self.assertTrue(record.transition(WorkState.APPROVED, actor="human").allowed)
        self.assertTrue(record.transition(WorkState.RELEASED, actor="human").allowed)
        self.assertEqual(record.state, WorkState.RELEASED)


if __name__ == "__main__":
    unittest.main()
