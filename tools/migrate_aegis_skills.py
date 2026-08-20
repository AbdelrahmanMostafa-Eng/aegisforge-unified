from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def parse_simple_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(?P<meta>.*?)\n---\n(?P<body>.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("skill does not contain simple front matter")
    metadata: dict[str, str] = {}
    for line in match.group("meta").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, match.group("body")


def yaml_scalar(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def migrate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_simple_frontmatter(text)
    relative = path.relative_to(SKILLS)
    domain = relative.parts[0]
    slug = relative.parent.name
    skill_id = f"{domain}.{slug}"
    description = metadata.get("description", "Apply this capability in a controlled, verifiable way.")
    risk_level = "high" if domain in {"security", "operations"} else "low"
    confirmation = "explicit" if risk_level == "high" else "never"
    capabilities = "analysis\n  - execution" if domain not in {"quality", "core"} else "analysis\n  - verification"
    frontmatter = f'''---
id: {skill_id}
name: {yaml_scalar(metadata.get("name", slug.replace("-", " ").title()))}
slug: {slug}
version: 0.1.0
status: experimental
summary: {yaml_scalar(description)}
description: {yaml_scalar(description)}
domains:
  - {domain}
capabilities:
  - {capabilities}
skill_type: procedure
keywords:
  - {slug}
  - {domain}
inputs:
  - task-description
outputs:
  - completed-result
risk:
  level: {risk_level}
  confirmation: {confirmation}
compatible_harnesses:
  - generic
  - claude-code
  - codex
quality:
  maturity: authored
  test_status: pending
  migration_source: aegisforge-v0.1
---
'''
    path.write_text(frontmatter + body.lstrip("\n"), encoding="utf-8")


if __name__ == "__main__":
    paths = sorted((SKILLS / "core").rglob("SKILL.md")) + sorted(
        p for domain in ("engineering", "operations", "platform", "product", "quality", "security")
        for p in (SKILLS / domain).rglob("SKILL.md")
        if "catalog_source:" not in p.read_text(encoding="utf-8", errors="ignore")
    )
    for path in paths:
        migrate(path)
    print(f"migrated={len(paths)}")
