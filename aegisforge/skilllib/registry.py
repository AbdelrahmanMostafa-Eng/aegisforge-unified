from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import re
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
    "method", "procedure", "workflow", "pattern", "reference", "template", "tool", "policy", "evaluator", "agent", "adapter"
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
            self.id, self.name, self.slug, self.summary, self.description,
            *self.domains, *self.capabilities, *self.keywords, *self.inputs, *self.outputs,
        ]
        return " ".join(values).lower()


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    severity: str = "error"
    code: str = "invalid"


def _as_string_list(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a non-empty list of strings")
    return tuple(item.strip() for item in value)


def _relative_path(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def record_from_metadata(metadata: dict[str, Any], path: Path, *, root: Path | None = None) -> SkillRecord:
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
    if not isinstance(confirmation, str) or not confirmation.strip():
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
    if risk_level in {"high", "critical"} and confirmation in {"never", "recommended"}:
        raise ValueError("high and critical skills require explicit or always confirmation")

    return SkillRecord(
        id=metadata["id"], name=metadata["name"], slug=metadata["slug"], version=metadata["version"],
        status=metadata["status"], summary=metadata["summary"], description=metadata["description"],
        skill_type=metadata["skill_type"], risk_level=risk_level, confirmation=confirmation,
        path=_relative_path(path, root), metadata=metadata, **fields,
    )


def validate_skill(path: str | Path, *, root: str | Path | None = None) -> list[ValidationIssue]:
    path = Path(path)
    root_path = Path(root) if root is not None else None
    issues: list[ValidationIssue] = []
    display_path = _relative_path(path, root_path)
    try:
        metadata, body = read_skill_file(path)
        record = record_from_metadata(metadata, path, root=root_path)
        if len(body.strip()) < 40:
            issues.append(ValidationIssue(display_path, "skill body is too short to be operational", "warning", "short-body"))
        if "## Verification" not in body:
            issues.append(ValidationIssue(display_path, "skill should include a Verification section", "warning", "missing-verification"))
        if "## When to Use" not in body:
            issues.append(ValidationIssue(display_path, "skill should include a When to Use section", "warning", "missing-trigger"))
        if record.status == "stable" and "experimental catalog scaffold" in body.lower():
            issues.append(ValidationIssue(display_path, "stable skill contains experimental scaffold language", "error", "stable-scaffold"))
        if re.search(r"\b(TODO|TBD|coming soon)\b", body, re.IGNORECASE):
            issues.append(ValidationIssue(display_path, "skill contains unresolved placeholder language", "warning", "placeholder-text"))
        for reference in metadata.get("references", []) if isinstance(metadata.get("references"), list) else []:
            if isinstance(reference, str) and reference.startswith("file:"):
                target = path.parent / reference[5:]
                if not target.exists():
                    issues.append(ValidationIssue(display_path, f"referenced file does not exist: {reference}", "error", "broken-reference"))
    except (OSError, FrontMatterError, ValueError, AttributeError) as exc:
        issues.append(ValidationIssue(display_path, str(exc), "error", "invalid-skill"))
    return issues


def discover(root: str | Path) -> tuple[list[SkillRecord], list[ValidationIssue]]:
    root = Path(root).resolve()
    records: list[SkillRecord] = []
    issues: list[ValidationIssue] = []
    seen_ids: dict[str, Path] = {}
    skills_root = root / "skills"
    for path in sorted(skills_root.rglob("SKILL.md")):
        display_path = _relative_path(path, root)
        try:
            metadata, _ = read_skill_file(path)
            record = record_from_metadata(metadata, path, root=root)
            if record.id in seen_ids:
                issues.append(ValidationIssue(display_path, f"duplicate id; first seen at {_relative_path(seen_ids[record.id], root)}", "error", "duplicate-id"))
            else:
                seen_ids[record.id] = path
            records.append(record)
            issues.extend(validate_skill(path, root=root))
        except (OSError, FrontMatterError, ValueError, AttributeError) as exc:
            issues.append(ValidationIssue(display_path, str(exc), "error", "invalid-skill"))
    return records, issues


def registry_document(records: Iterable[SkillRecord]) -> dict[str, Any]:
    items = []
    for record in records:
        data = asdict(record)
        data.pop("metadata", None)
        items.append(data)
    return {"schema_version": "1.1.0", "count": len(items), "skills": items}


def write_registry(root: str | Path, records: Iterable[SkillRecord]) -> Path:
    root = Path(root).resolve()
    records = list(records)
    directory = root / "registry"
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
        raw_aliases = record.metadata.get("aliases", [])
        for alias in raw_aliases if isinstance(raw_aliases, list) else []:
            aliases[str(alias)] = record.id
    for mapping, filename in ((domains, "domains.json"), (capabilities, "capabilities.json"), (aliases, "aliases.json")):
        normalized = {key: sorted(value) if isinstance(value, list) else value for key, value in sorted(mapping.items())}
        (directory / filename).write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def registry_is_fresh(root: str | Path) -> bool:
    """Return whether the generated registry is newer than every skill source."""
    root = Path(root).resolve()
    registry = root / "registry" / "skills.json"
    if not registry.is_file():
        return False
    registry_time = registry.stat().st_mtime_ns
    return all(path.stat().st_mtime_ns <= registry_time for path in (root / "skills").rglob("SKILL.md"))


def load_registry(root: str | Path) -> list[SkillRecord]:
    """Load a generated registry as records for fast search without a filesystem scan."""
    root = Path(root).resolve()
    payload = json.loads((root / "registry" / "skills.json").read_text(encoding="utf-8"))
    if payload.get("schema_version") not in {"1.0.0", "1.1.0"}:
        raise ValueError("unsupported registry schema version")
    records: list[SkillRecord] = []
    for item in payload.get("skills", []):
        records.append(SkillRecord(
            id=item["id"], name=item["name"], slug=item["slug"], version=item["version"], status=item["status"],
            summary=item["summary"], description=item["description"], domains=tuple(item["domains"]),
            capabilities=tuple(item["capabilities"]), skill_type=item["skill_type"], keywords=tuple(item["keywords"]),
            inputs=tuple(item["inputs"]), outputs=tuple(item["outputs"]), risk_level=item["risk_level"],
            confirmation=item["confirmation"], compatible_harnesses=tuple(item["compatible_harnesses"]),
            path=item["path"], metadata={},
        ))
    return records
