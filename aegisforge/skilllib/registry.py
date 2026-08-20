"""Discovery and validation for the SKILL.md repository."""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from .frontmatter import FrontMatterError, read_skill_file

REQUIRED_FIELDS = {
    "id",
    "name",
    "slug",
    "version",
    "status",
    "summary",
    "description",
    "domains",
    "capabilities",
    "skill_type",
    "keywords",
    "inputs",
    "outputs",
    "risk",
    "compatible_harnesses",
}
ALLOWED_STATUS = {"draft", "experimental", "stable", "deprecated", "archived"}
ALLOWED_SKILL_TYPES = {
    "method",
    "procedure",
    "workflow",
    "pattern",
    "reference",
    "template",
    "tool",
    "policy",
    "evaluator",
    "agent",
    "adapter",
}
ALLOWED_RISK_LEVELS = {"none", "low", "moderate", "high", "critical"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


@dataclass(frozen=True)
class SkillRecord:
    id: str
    name: str
    slug: str
    version: str
    status: str
    summary: str
    description: str
    domains: tuple[str, ...]
    capabilities: tuple[str, ...]
    skill_type: str
    keywords: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    risk_level: str
    confirmation: str
    compatible_harnesses: tuple[str, ...]
    path: str
    metadata: dict[str, Any]

    def searchable_text(self) -> str:
        values = [
            self.id,
            self.name,
            self.slug,
            self.summary,
            self.description,
            *self.domains,
            *self.capabilities,
            *self.keywords,
            *self.inputs,
            *self.outputs,
        ]
        return " ".join(values).lower()


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    severity: str = "error"


def _as_string_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a non-empty list of strings")
    return tuple(item.strip() for item in value)


def record_from_metadata(metadata: dict[str, Any], path: Path) -> SkillRecord:
    missing = sorted(REQUIRED_FIELDS - metadata.keys())
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    risk = metadata.get("risk")
    if not isinstance(risk, dict):
        raise ValueError("risk must be a mapping with level and confirmation")
    risk_level = risk.get("level")
    confirmation = risk.get("confirmation")
    if risk_level not in ALLOWED_RISK_LEVELS:
        raise ValueError(f"risk.level must be one of {sorted(ALLOWED_RISK_LEVELS)}")
    if not isinstance(confirmation, str) or not confirmation:
        raise ValueError("risk.confirmation must be a non-empty string")

    fields = {
        "domains": _as_string_list(metadata["domains"], "domains"),
        "capabilities": _as_string_list(metadata["capabilities"], "capabilities"),
        "keywords": _as_string_list(metadata["keywords"], "keywords"),
        "inputs": _as_string_list(metadata["inputs"], "inputs"),
        "outputs": _as_string_list(metadata["outputs"], "outputs"),
        "compatible_harnesses": _as_string_list(metadata["compatible_harnesses"], "compatible_harnesses"),
    }
    scalar_fields = ["id", "name", "slug", "version", "status", "summary", "description", "skill_type"]
    for field in scalar_fields:
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    if not SLUG_RE.fullmatch(metadata["slug"]):
        raise ValueError("slug must use lowercase kebab-case")
    if not VERSION_RE.fullmatch(metadata["version"]):
        raise ValueError("version must use semantic versioning")
    if metadata["status"] not in ALLOWED_STATUS:
        raise ValueError(f"status must be one of {sorted(ALLOWED_STATUS)}")
    if metadata["skill_type"] not in ALLOWED_SKILL_TYPES:
        raise ValueError(f"skill_type must be one of {sorted(ALLOWED_SKILL_TYPES)}")
    id_segments = metadata["id"].split(".")
    if not id_segments or any(segment != "_core" and not SLUG_RE.fullmatch(segment) for segment in id_segments):
        raise ValueError("id must contain lowercase kebab-case segments separated by dots")

    return SkillRecord(
        id=metadata["id"],
        name=metadata["name"],
        slug=metadata["slug"],
        version=metadata["version"],
        status=metadata["status"],
        summary=metadata["summary"],
        description=metadata["description"],
        skill_type=metadata["skill_type"],
        risk_level=risk_level,
        confirmation=confirmation,
        path=str(path),
        metadata=metadata,
        **fields,
    )


def validate_skill(path: str | Path) -> list[ValidationIssue]:
    path = Path(path)
    issues: list[ValidationIssue] = []
    try:
        metadata, body = read_skill_file(path)
        record_from_metadata(metadata, path)
        if len(body.strip()) < 40:
            issues.append(ValidationIssue(str(path), "skill body is too short to be operational", "warning"))
        if "## Verification" not in body:
            issues.append(ValidationIssue(str(path), "skill should include a Verification section", "warning"))
        if "## When to Use" not in body:
            issues.append(ValidationIssue(str(path), "skill should include a When to Use section", "warning"))
    except (OSError, FrontMatterError, ValueError) as exc:
        issues.append(ValidationIssue(str(path), str(exc)))
    return issues


def discover(root: str | Path) -> tuple[list[SkillRecord], list[ValidationIssue]]:
    root = Path(root)
    records: list[SkillRecord] = []
    issues: list[ValidationIssue] = []
    seen_ids: dict[str, Path] = {}
    for path in sorted((root / "skills").rglob("SKILL.md")):
        try:
            metadata, _ = read_skill_file(path)
            record = record_from_metadata(metadata, path)
            if record.id in seen_ids:
                issues.append(ValidationIssue(str(path), f"duplicate id; first seen at {seen_ids[record.id]}"))
            else:
                seen_ids[record.id] = path
            records.append(record)
            issues.extend(validate_skill(path))
        except (OSError, FrontMatterError, ValueError) as exc:
            issues.append(ValidationIssue(str(path), str(exc)))
    return records, issues


def registry_document(records: Iterable[SkillRecord]) -> dict[str, Any]:
    items = []
    for record in records:
        data = asdict(record)
        data.pop("metadata", None)
        items.append(data)
    return {"schema_version": "1.0.0", "count": len(items), "skills": items}


def write_registry(root: str | Path, records: Iterable[SkillRecord]) -> Path:
    records = list(records)
    directory = Path(root) / "registry"
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "skills.json"
    output.write_text(json.dumps(registry_document(records), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    domains: dict[str, list[str]] = {}
    capabilities: dict[str, list[str]] = {}
    aliases: dict[str, str] = {}
    for record in records:
        for domain in record.domains:
            domains.setdefault(domain, []).append(record.id)
        for capability in record.capabilities:
            capabilities.setdefault(capability, []).append(record.id)
        for alias in record.metadata.get("aliases", []) if isinstance(record.metadata.get("aliases", []), list) else []:
            aliases[str(alias)] = record.id
    for mapping, filename in ((domains, "domains.json"), (capabilities, "capabilities.json"), (aliases, "aliases.json")):
        normalized = {key: sorted(value) if isinstance(value, list) else value for key, value in sorted(mapping.items())}
        (directory / filename).write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output
