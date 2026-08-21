"""Structured evidence records for trustworthy agent work.

The ledger is deliberately dependency-free and serializes to stable JSON so it
can be checked into review artifacts or consumed by automation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Literal

Outcome = Literal["pass", "fail", "not-run", "unknown"]
VALID_OUTCOMES = {"pass", "fail", "not-run", "unknown"}


@dataclass(frozen=True)
class EvidenceItem:
    """One observable claim or verification action."""

    kind: str
    description: str
    outcome: Outcome = "unknown"
    command: str | None = None
    artifact: str | None = None
    notes: str | None = None


@dataclass
class EvidenceLedger:
    """A reviewable record of what changed and how completion was verified."""

    change_summary: str
    rationale: str
    approved_by: str | None = None
    items: list[EvidenceItem] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    independently_verified: bool = False
    verifier: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add(
        self,
        kind: str,
        description: str,
        *,
        outcome: Outcome = "unknown",
        command: str | None = None,
        artifact: str | None = None,
        notes: str | None = None,
    ) -> EvidenceItem:
        """Append one observable evidence item and return it."""
        item = EvidenceItem(
            kind=kind.strip(),
            description=description.strip(),
            outcome=outcome,
            command=command.strip() if command else None,
            artifact=artifact.strip() if artifact else None,
            notes=notes.strip() if notes else None,
        )
        if not item.kind or not item.description:
            raise ValueError("evidence kind and description must be non-empty")
        if item.outcome not in VALID_OUTCOMES:
            raise ValueError(f"evidence outcome must be one of {sorted(VALID_OUTCOMES)}")
        self.items.append(item)
        return item

    def add_uncertainty(self, statement: str) -> None:
        """Record an unresolved limitation instead of silently inferring success."""
        statement = statement.strip()
        if not statement:
            raise ValueError("uncertainty must be non-empty")
        self.uncertainties.append(statement)

    def validate(self, *, require_approval: bool = False) -> list[str]:
        """Return actionable completeness findings without hiding uncertainty."""
        findings: list[str] = []
        if not self.change_summary.strip():
            findings.append("change_summary is required")
        if not self.rationale.strip():
            findings.append("rationale is required")
        if not self.items:
            findings.append("at least one evidence item is required")
        if not any(item.kind in {"test", "verification", "build", "security", "runtime"} for item in self.items):
            findings.append("at least one test or verification item is required")
        non_passing = [item for item in self.items if item.outcome != "pass"]
        if non_passing:
            findings.append("all evidence items must pass before work can be verified or released")
        if any(item.outcome == "fail" for item in self.items) and not self.uncertainties:
            findings.append("failed evidence requires an uncertainty or remediation note")
        if require_approval and not self.approved_by:
            findings.append("explicit approval is required for this risk level")
        if self.independently_verified and not self.verifier:
            findings.append("verifier is required when independently_verified is true")
        return findings

    @property
    def passed(self) -> bool:
        """Whether the ledger is complete and contains no failed checks."""
        return not self.validate() and not any(item.outcome == "fail" for item in self.items)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["items"] = [asdict(item) for item in self.items]
        return payload

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True) + "\n"

    def save(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.to_json(), encoding="utf-8")
        return output

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceLedger":
        raw_items = payload.get("items", [])
        if not isinstance(raw_items, list) or not all(isinstance(item, dict) for item in raw_items):
            raise ValueError("evidence items must be a list of objects")
        items = [EvidenceItem(**item) for item in raw_items]
        for item in items:
            if item.outcome not in VALID_OUTCOMES:
                raise ValueError(f"evidence outcome must be one of {sorted(VALID_OUTCOMES)}")
        values = {key: value for key, value in payload.items() if key != "items"}
        return cls(items=items, **values)

    @classmethod
    def load(cls, path: str | Path) -> "EvidenceLedger":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("evidence ledger must contain a JSON object")
        return cls.from_dict(payload)
