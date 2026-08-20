"""Skill catalog discovery utilities."""

from __future__ import annotations

from pathlib import Path
import re


_FRONTMATTER_RE = re.compile(r"^---\n(?P<meta>.*?)\n---\n", re.DOTALL)


def _metadata(text: str) -> dict[str, str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group("meta").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def discover_skills(root: Path) -> list[dict[str, str]]:
    """Discover valid skill metadata in stable path order."""

    skills_root = root / "skills"
    result: list[dict[str, str]] = []
    for skill_file in sorted(skills_root.glob("**/SKILL.md")):
        data = _metadata(skill_file.read_text(encoding="utf-8"))
        if not data.get("name"):
            continue
        relative = skill_file.relative_to(root)
        family = relative.parts[1] if len(relative.parts) > 1 else "unknown"
        result.append(
            {
                "name": data["name"],
                "description": data.get("description", ""),
                "family": family,
                "path": str(relative.parent),
            }
        )
    result.sort(key=lambda item: item["path"])
    return result
