"""Risk classification and workflow selection for AegisForge.

The classifier is intentionally deterministic and explainable. It is a first-pass
policy engine, not a replacement for human judgment or domain-specific review.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import IntEnum
import re
from typing import Iterable


class RiskLevel(IntEnum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


@dataclass(frozen=True)
class Assessment:
    """Explainable assessment returned by the policy engine."""

    risk_level: str
    workflow: str
    task_type: str
    reversible: bool
    external_side_effects: bool
    sensitive_data: bool
    production_scope: bool
    authorization_impact: bool
    ambiguity: bool
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["reasons"] = list(self.reasons)
        return result


_HIGH_ASSURANCE_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b(prod|production|live)\b", "production scope"),
    (r"\b(delete|destroy|drop|purge|wipe|revoke)\b", "destructive action"),
    (r"\b(migrat|backfill|schema change|database)\b", "data or schema change"),
    (r"\b(password|secret|credential|token|private key|api key)\b", "secret handling"),
    (r"\b(oauth|sso|authentication|authorization|rbac|permission|access control)\b", "identity or authorization"),
    (r"\b(payment|billing|transfer|purchase|financial)\b", "financial impact"),
    (r"\b(health|medical|patient|hipaa|personal data|pii|privacy)\b", "sensitive or regulated data"),
    (r"\b(deploy|release|rollout|infrastructure|terraform|kubernetes|cloud)\b", "operational or infrastructure impact"),
    (r"\b(external email|send email|publish|post|webhook|notify customer)\b", "external side effect"),
)

_MEDIUM_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b(feature|endpoint|api|service|integration|refactor|dependency)\b", "cross-file or integration change"),
    (r"\b(ui|frontend|mobile|browser|workflow)\b", "user-facing behavior"),
    (r"\b(test|bug|fix|regression|performance)\b", "behavior requiring verification"),
)

_AMBIGUITY_PATTERNS: tuple[str, ...] = (
    r"\b(make|build|improve|update|optimize)\b",
    r"\b(better|best|everything|all|as needed)\b",
)


def _matches(text: str, patterns: Iterable[tuple[str, str]]) -> list[str]:
    return [reason for pattern, reason in patterns if re.search(pattern, text, re.IGNORECASE)]


def assess(text: str) -> Assessment:
    """Classify a natural-language task using conservative, explainable rules."""

    normalized = " ".join(text.split())
    if not normalized:
        return Assessment(
            risk_level="medium",
            workflow="standard",
            task_type="unspecified",
            reversible=True,
            external_side_effects=False,
            sensitive_data=False,
            production_scope=False,
            authorization_impact=False,
            ambiguity=True,
            reasons=("the task description is empty",),
        )

    high_reasons = _matches(normalized, _HIGH_ASSURANCE_PATTERNS)
    medium_reasons = _matches(normalized, _MEDIUM_PATTERNS)
    ambiguity = any(re.search(pattern, normalized, re.IGNORECASE) for pattern in _AMBIGUITY_PATTERNS)
    trivial_documentation = bool(
        re.search(r"\b(typo|spelling|grammar)\b", normalized, re.IGNORECASE)
        and re.search(r"\b(readme|documentation|docs)\b", normalized, re.IGNORECASE)
    )
    if trivial_documentation:
        medium_reasons = []
        ambiguity = False

    production_scope = any(word in normalized.lower().split() for word in ("prod", "production", "live"))
    external_side_effects = any(
        phrase in normalized.lower()
        for phrase in ("send email", "publish", "post", "webhook", "notify customer")
    )
    sensitive_data = any(
        phrase in normalized.lower()
        for phrase in ("secret", "credential", "token", "personal data", "pii", "patient", "medical")
    )
    authorization_impact = bool(
        re.search(r"\b(oauth|sso|authentication|authorization|rbac|permission|access control)\b", normalized, re.I)
    )
    reversible = not bool(re.search(r"\b(delete|destroy|drop|purge|wipe|revoke|migrat|backfill)\b", normalized, re.I))

    if high_reasons:
        level = RiskLevel.CRITICAL if not reversible or production_scope else RiskLevel.HIGH
        workflow = "high-assurance"
    elif medium_reasons or ambiguity:
        level = RiskLevel.MEDIUM
        workflow = "standard"
    else:
        level = RiskLevel.LOW
        workflow = "lightweight"

    task_type = "feature"
    lower = normalized.lower()
    if trivial_documentation:
        task_type = "documentation"
    elif re.search(r"\b(debug|bug|fix|regression)\b", lower):
        task_type = "bugfix"
    elif re.search(r"\b(refactor|cleanup|reorganize)\b", lower):
        task_type = "refactor"
    elif re.search(r"\b(doc|documentation|readme)\b", lower):
        task_type = "documentation"
    elif re.search(r"\b(prototype|spike|explore|experiment)\b", lower):
        task_type = "prototype"
    elif re.search(r"\b(deploy|release|rollout|infrastructure)\b", lower):
        task_type = "operations"

    reasons = tuple(dict.fromkeys(high_reasons + medium_reasons))
    if ambiguity:
        reasons += ("the request may require clarification",)
    if not reasons:
        reasons = ("no high-impact signal detected",)

    return Assessment(
        risk_level=level.name.lower(),
        workflow=workflow,
        task_type=task_type,
        reversible=reversible,
        external_side_effects=external_side_effects,
        sensitive_data=sensitive_data,
        production_scope=production_scope,
        authorization_impact=authorization_impact,
        ambiguity=ambiguity,
        reasons=reasons,
    )
