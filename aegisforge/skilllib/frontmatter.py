"""Small YAML-subset parser for SKILL.md front matter.

The repository intentionally keeps the runtime dependency-free. The supported
front matter is deliberately conservative: mappings, scalar values, and lists
of scalar values. Complex YAML can be introduced later behind an optional
adapter without changing the skill contract.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any


class FrontMatterError(ValueError):
    """Raised when a SKILL.md front matter block cannot be parsed."""


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def _next_content(lines: list[str], start: int, end: int) -> str | None:
    for index in range(start, end):
        if lines[index].strip() and not lines[index].lstrip().startswith("#"):
            return lines[index].strip()
    return None


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Return ``(metadata, markdown_body)`` from a SKILL.md document."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontMatterError("SKILL.md must begin with YAML front matter")

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        raise FrontMatterError("front matter opening delimiter has no closing delimiter")

    metadata: dict[str, Any] = {}
    index = 1
    while index < end:
        line = lines[index]
        line_number = index + 1
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith(" "):
            raise FrontMatterError(f"line {line_number}: unexpected indentation")
        if ":" not in line:
            raise FrontMatterError(f"line {line_number}: expected key: value")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            raise FrontMatterError(f"line {line_number}: invalid metadata key")
        if value:
            metadata[key] = _scalar(value)
            index += 1
            continue

        next_content = _next_content(lines, index + 1, end)
        if next_content and next_content.startswith("-"):
            metadata[key] = []
            index += 1
            while index < end:
                child = lines[index]
                if not child.strip() or child.lstrip().startswith("#"):
                    index += 1
                    continue
                if not child.startswith(" "):
                    break
                child_value = child.strip()
                if not child_value.startswith("-"):
                    raise FrontMatterError(f"line {index + 1}: expected list item")
                metadata[key].append(_scalar(child_value[1:].strip()))
                index += 1
            continue

        metadata[key] = {}
        index += 1
        while index < end:
            child = lines[index]
            if not child.strip() or child.lstrip().startswith("#"):
                index += 1
                continue
            if not child.startswith(" "):
                break
            child_value = child.strip()
            if ":" not in child_value or child_value.startswith("-"):
                raise FrontMatterError(f"line {index + 1}: expected nested key: value")
            child_key, child_raw = child_value.split(":", 1)
            child_key = child_key.strip()
            child_value = child_raw.strip()
            if not child_key:
                raise FrontMatterError(f"line {index + 1}: invalid nested metadata key")
            metadata[key][child_key] = _scalar(child_value)
            index += 1

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return metadata, body


def read_skill_file(path: str | Path) -> tuple[dict[str, Any], str]:
    path = Path(path)
    return parse_front_matter(path.read_text(encoding="utf-8"))
