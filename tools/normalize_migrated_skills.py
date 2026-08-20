from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in sorted((ROOT / "skills").rglob("SKILL.md")):
    text = path.read_text(encoding="utf-8")
    if "migration_source: aegisforge-v0.1" not in text:
        continue
    additions: list[str] = []
    if "## When to Use" not in text:
        additions.append("## When to Use\n\nUse this skill when the request matches the declared capability and its risk boundaries.\n")
    if "## Verification" not in text:
        additions.append("## Verification\n\nConfirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.\n")
    if additions:
        path.write_text(text.rstrip() + "\n\n" + "\n".join(additions), encoding="utf-8")

print("normalized migrated skills")
