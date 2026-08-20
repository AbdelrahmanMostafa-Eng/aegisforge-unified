"""Reproducible evaluation harness for AegisForge control-plane behavior."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable

from .policy import Assessment, assess


@dataclass(frozen=True)
class EvaluationScenario:
    id: str
    prompt: str
    expected_risk: str
    expected_workflow: str
    expected_confirmation: bool = False
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvaluationResult:
    scenario_id: str
    passed: bool
    actual_risk: str
    actual_workflow: str
    actual_confirmation: bool
    reasons: tuple[str, ...]
    failures: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationReport:
    total: int
    passed: int
    failed: int
    results: tuple[EvaluationResult, ...]

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 1.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["results"] = [asdict(result) for result in self.results]
        payload["pass_rate"] = self.pass_rate
        return payload


def requires_confirmation(assessment: Assessment) -> bool:
    """Return whether the assessment requires explicit human authorization."""
    return assessment.risk_level in {"high", "critical"} or not assessment.reversible or assessment.external_side_effects


def evaluate(scenario: EvaluationScenario) -> EvaluationResult:
    actual = assess(scenario.prompt)
    failures: list[str] = []
    confirmation = requires_confirmation(actual)
    if actual.risk_level != scenario.expected_risk:
        failures.append(f"risk expected {scenario.expected_risk}, got {actual.risk_level}")
    if actual.workflow != scenario.expected_workflow:
        failures.append(f"workflow expected {scenario.expected_workflow}, got {actual.workflow}")
    if confirmation != scenario.expected_confirmation:
        failures.append(f"confirmation expected {scenario.expected_confirmation}, got {confirmation}")
    return EvaluationResult(
        scenario_id=scenario.id,
        passed=not failures,
        actual_risk=actual.risk_level,
        actual_workflow=actual.workflow,
        actual_confirmation=confirmation,
        reasons=actual.reasons,
        failures=tuple(failures),
    )


def evaluate_all(scenarios: Iterable[EvaluationScenario]) -> EvaluationReport:
    results = tuple(evaluate(scenario) for scenario in scenarios)
    passed = sum(result.passed for result in results)
    return EvaluationReport(len(results), passed, len(results) - passed, results)


def load_scenarios(path: str | Path) -> tuple[EvaluationScenario, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("evaluation scenarios must be a JSON list")
    scenarios: list[EvaluationScenario] = []
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("each evaluation scenario must be an object")
        tags = tuple(item.get("tags", ()))
        scenarios.append(EvaluationScenario(tags=tags, **{key: value for key, value in item.items() if key != "tags"}))
    return tuple(scenarios)
