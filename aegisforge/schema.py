"""Small, dependency-free checks for the repository's JSON Schema contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_schema(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("schema must be a JSON object")
    return payload


def validate_schema_document(payload: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for field in ("$schema", "$id", "title", "type", "required", "properties"):
        if field not in payload:
            findings.append(f"schema missing {field}")
    if payload.get("type") != "object":
        findings.append("schema root type must be object")
    required = payload.get("required", [])
    properties = payload.get("properties", {})
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        findings.append("schema required must be a list of strings")
    if not isinstance(properties, dict):
        findings.append("schema properties must be an object")
    elif isinstance(required, list):
        missing = sorted(set(required) - properties.keys())
        if missing:
            findings.append(f"schema required fields missing from properties: {', '.join(missing)}")
    return findings


def validate_payload(payload: Any, schema: dict[str, Any], *, path: str = "$") -> list[str]:
    """Validate the useful subset of JSON Schema used by project contracts."""
    findings: list[str] = []
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(payload, dict):
            return [f"{path} must be an object"]
        required = schema.get("required", [])
        for field in required:
            if field not in payload:
                findings.append(f"{path}.{field} is required")
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}))
            for field in sorted(set(payload) - allowed):
                findings.append(f"{path}.{field} is not allowed")
        for field, field_schema in schema.get("properties", {}).items():
            if field in payload and isinstance(field_schema, dict):
                findings.extend(validate_payload(payload[field], field_schema, path=f"{path}.{field}"))
    elif expected_type == "array":
        if not isinstance(payload, list):
            findings.append(f"{path} must be an array")
        else:
            minimum = schema.get("minItems")
            if isinstance(minimum, int) and len(payload) < minimum:
                findings.append(f"{path} must contain at least {minimum} item(s)")
            item_schema = schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(payload):
                    findings.extend(validate_payload(item, item_schema, path=f"{path}[{index}]"))
    elif expected_type == "string" and not isinstance(payload, str):
        findings.append(f"{path} must be a string")
    elif expected_type == "boolean" and not isinstance(payload, bool):
        findings.append(f"{path} must be a boolean")
    enum = schema.get("enum")
    if isinstance(enum, list) and payload not in enum:
        findings.append(f"{path} must be one of {enum}")
    if isinstance(payload, str) and isinstance(schema.get("minLength"), int) and len(payload) < schema["minLength"]:
        findings.append(f"{path} must contain at least {schema['minLength']} character(s)")
    return findings
