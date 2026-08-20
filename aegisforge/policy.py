"""Deterministic, explainable risk assessment for agent work.

The policy engine is intentionally conservative and dependency-free. It is a
first-pass control plane: domain experts and human reviewers remain the final
authority when context contradicts a keyword signal.
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


_HIGH_ASSURANCE_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b(prod|production|live)\b", "production scope"),
    (r"\b(delete|destroy|drop|purge|wipe|revoke|erase)\b", "destructive action"),
    (r"\b(migrat|backfill|schema change|database|customer records)\b", "data or schema change"),
    (r"\b(password|secret|credential|token|private key|api key)\b", "secret handling"),
    (r"\b(oauth|sso|authentication|authorization|rbac|permission|access control)\b", "identity or authorization"),
    (r"\b(payment|billing|transfer|purchase|financial|invoice)\b", "financial impact"),
    (r"\b(health|medical|patient|hipaa|personal data|personal information|pii|privacy|user data|customer data)\b", "sensitive or regulated data"),
    (r"\b(deploy|release|rollout|infrastructure|terraform|kubernetes|cloud)\b", "operational or infrastructure impact"),
    (r"\b(external api|third-party api|external service|webhook|notify customer|notify|send (?:an? )?email|publish|post)\b", "external side effect"),
    (r"\b(public release|release publicly|make public)\b", "public release"),
)

_MEDIUM_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b(feature|endpoint|api|service|integration|refactor|dependency|package)\b", "cross-file or integration change"),
    (r"\b(ui|frontend|mobile|browser|workflow|user-facing)\b", "user-facing behavior"),
    (r"\b(test|bug|fix|regression|performance|benchmark)\b", "behavior requiring verification"),
)

_AMBIGUITY_PATTERNS: tuple[str, ...] = (
    r"\b(make|build|improve|update|optimize|change)\b",
    r"\b(better|best|everything|all|as needed)\b",
)


def _matches(text: str, patterns: Iterable[tuple[str, str]]) -> list[str]:
    return [reason for pattern, reason in patterns if re.search(pattern, text, re.IGNORECASE)]


def _controls(level: RiskLevel) -> tuple[str, ...]:
    controls = ["task framing", "targeted verification"]
    if level >= RiskLevel.MEDIUM:
        controls.extend(("additional verification", "review change surface"))
    if level >= RiskLevel.HIGH:
        controls.extend(("threat model or security review", "explicit authorization", "independent verification", "rollback or recovery plan"))
    if level >= RiskLevel.CRITICAL:
        controls.extend(("human approval", "release evidence", "post-change observation"))
    return tuple(controls)


@dataclass(frozen=True)
class Assessment:
    """Structured, explainable assessment returned by the policy engine."""

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
    required_controls: tuple[str, ...] = ()
    requires_confirmation: bool = False

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["reasons"] = list(self.reasons)
        result["required_controls"] = list(self.required_controls)
        return result


def assess(text: str) -> Assessment:
    """Classify a natural-language task using conservative, explainable rules."""
    normalized = " ".join(text.split())
    if not normalized:
        level = RiskLevel.MEDIUM
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
            required_controls=_controls(level),
            requires_confirmation=False,
        )

    lower = normalized.lower()
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

    production_scope = bool(re.search(r"\b(prod|production|live)\b", lower))
    external_side_effects = bool(re.search(r"\b(external api|external service|webhook|notify customer|notify|send (?:an? )?email|publish|post)\b", lower))
    sensitive_data = bool(re.search(r"\b(secret|credential|token|personal data|personal information|pii|patient|medical|user data|customer data)\b", lower))
    authorization_impact = bool(re.search(r"\b(oauth|sso|authentication|authorization|rbac|permission|access control)\b", lower))
    reversible = not bool(re.search(r"\b(delete|destroy|drop|purge|wipe|revoke|erase|irreversible|cannot be undone)\b", lower))

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
        required_controls=_controls(level),
        requires_confirmation=level >= RiskLevel.HIGH or external_side_effects or not reversible,
    )
