"""Explicit governance state transitions for agent-controlled work."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable

from .evidence import EvidenceLedger
from .policy import Assessment


class WorkState(StrEnum):
    PLANNED = "planned"
    AUTHORIZED = "authorized"
    EXECUTED = "executed"
    VERIFIED = "verified"
    APPROVED = "approved"
    RELEASED = "released"


_ALLOWED_TRANSITIONS: dict[WorkState, frozenset[WorkState]] = {
    WorkState.PLANNED: frozenset({WorkState.AUTHORIZED}),
    WorkState.AUTHORIZED: frozenset({WorkState.EXECUTED}),
    WorkState.EXECUTED: frozenset({WorkState.VERIFIED}),
    WorkState.VERIFIED: frozenset({WorkState.APPROVED}),
    WorkState.APPROVED: frozenset({WorkState.RELEASED}),
    WorkState.RELEASED: frozenset(),
}


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    state: WorkState
    reason: str


@dataclass
class WorkRecord:
    """Minimal state machine that prevents silent release claims."""

    assessment: Assessment
    state: WorkState = WorkState.PLANNED
    evidence: EvidenceLedger | None = None
    approval_actor: str | None = None

    def transition(
        self,
        target: WorkState,
        *,
        actor: str | None = None,
        evidence: EvidenceLedger | None = None,
    ) -> GovernanceDecision:
        if target not in _ALLOWED_TRANSITIONS[self.state]:
            return GovernanceDecision(False, self.state, f"invalid transition: {self.state} -> {target}")
        if target == WorkState.AUTHORIZED and self.assessment.risk_level in {"high", "critical"} and not actor:
            return GovernanceDecision(False, self.state, "high-assurance work requires an authorizing actor")
        if target in {WorkState.VERIFIED, WorkState.APPROVED, WorkState.RELEASED}:
            ledger = evidence or self.evidence
            if ledger is None:
                return GovernanceDecision(False, self.state, "evidence ledger is required before verification")
            findings = ledger.validate(require_approval=target in {WorkState.APPROVED, WorkState.RELEASED})
            if findings:
                return GovernanceDecision(False, self.state, "; ".join(findings))
            if target in {WorkState.APPROVED, WorkState.RELEASED} and self.assessment.risk_level in {"high", "critical"}:
                if not (self.approval_actor or actor or ledger.approved_by):
                    return GovernanceDecision(False, self.state, "explicit approval is required before approval or release")
            self.evidence = ledger
        if target == WorkState.AUTHORIZED:
            self.approval_actor = actor
        self.state = target
        return GovernanceDecision(True, self.state, f"transitioned to {target}")

    def required_controls(self) -> tuple[str, ...]:
        controls: list[str] = ["task framing", "observable verification"]
        if self.assessment.risk_level in {"medium", "high", "critical"}:
            controls.append("additional verification")
        if self.assessment.risk_level in {"high", "critical"}:
            controls.extend(("explicit authorization", "rollback or recovery plan", "independent review"))
        if self.assessment.risk_level == "critical":
            controls.extend(("release evidence", "human approval"))
        return tuple(dict.fromkeys(controls))


def controls_for(assessment: Assessment) -> tuple[str, ...]:
    """Return deterministic controls required by an assessment."""
    record = WorkRecord(assessment)
    return record.required_controls()


def valid_states() -> Iterable[str]:
    return (state.value for state in WorkState)
