"""Repository and skill validation for AegisForge."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .skilllib.registry import discover


@dataclass(frozen=True)
class Finding:
    path: str
    severity: str
    message: str


_REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "pyproject.toml",
    "schemas/task-assessment.schema.json",
    "schemas/skill-manifest.schema.json",
)


def validate_repo(root: Path) -> list[Finding]:
    """Return deterministic repository findings; no findings means the repo is valid."""
    findings: list[Finding] = []
    for relative in _REQUIRED_FILES:
        if not (root / relative).is_file():
            findings.append(Finding(relative, "error", "required repository file is missing"))

    records, issues = discover(root)
    del records
    findings.extend(Finding(issue.path, issue.severity, issue.message) for issue in issues)

    for skill_file in sorted((root / "skills").glob("**/SKILL.md")):
        relative = str(skill_file.relative_to(root))
        text = skill_file.read_text(encoding="utf-8")
        if len(text.splitlines()) > 500:
            findings.append(Finding(relative, "warning", "skill exceeds 500 lines"))
        if "TODO" in text:
            findings.append(Finding(relative, "warning", "skill contains TODO text"))

    for schema_file in sorted((root / "schemas").glob("*.json")):
        relative = str(schema_file.relative_to(root))
        try:
            json.loads(schema_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(Finding(relative, "error", f"invalid JSON: {exc.msg}"))

    return findings
