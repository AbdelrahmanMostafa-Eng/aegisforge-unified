"""Repository, schema, and skill validation for AegisForge."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .policy import assess
from .schema import load_schema, validate_payload, validate_schema_document
from .skilllib.registry import discover, registry_is_fresh


@dataclass(frozen=True)
class Finding:
    path: str
    severity: str
    message: str
    code: str = "invalid"


_REQUIRED_FILES = (
    "README.md", "AGENTS.md", "LICENSE", "CONTRIBUTING.md", "pyproject.toml",
    "schemas/task-assessment.schema.json", "schemas/skill-manifest.schema.json",
)


def validate_repo(root: Path) -> list[Finding]:
    """Return deterministic repository findings; no errors means the repo is valid."""
    root = root.resolve()
    findings: list[Finding] = []
    for relative in _REQUIRED_FILES:
        if not (root / relative).is_file():
            findings.append(Finding(relative, "error", "required repository file is missing", "missing-file"))

    records, issues = discover(root)
    del records
    findings.extend(Finding(issue.path, issue.severity, issue.message, issue.code) for issue in issues)

    registry_path = root / "registry" / "skills.json"
    if registry_path.is_file() and not registry_is_fresh(root):
        findings.append(Finding("registry/skills.json", "warning", "generated registry is older than a skill source; run `aegisforge index`", "stale-index"))

    for schema_file in sorted((root / "schemas").glob("*.json")):
        relative = str(schema_file.relative_to(root))
        try:
            schema = load_schema(schema_file)
            for message in validate_schema_document(schema):
                findings.append(Finding(relative, "error", message, "invalid-schema"))
            if schema_file.name == "task-assessment.schema.json":
                payload = assess("Add OAuth login and deploy it to production").to_dict()
                for message in validate_payload(payload, schema):
                    findings.append(Finding(relative, "error", f"assessment payload contract failure: {message}", "schema-mismatch"))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            findings.append(Finding(relative, "error", str(exc), "invalid-schema"))

    return findings
