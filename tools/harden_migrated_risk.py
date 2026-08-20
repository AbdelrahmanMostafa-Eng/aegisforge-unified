from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIGH_RISK = re.compile(
    r"(migration|production|delivery-pipeline|identity|privacy|secret|supply-chain|threat|deploy|payment|authorization|incident)",
    re.IGNORECASE,
)

for path in sorted((ROOT / "skills").rglob("SKILL.md")):
    text = path.read_text(encoding="utf-8")
    if "migration_source: aegisforge-v0.1" not in text:
        continue
    if not HIGH_RISK.search(path.as_posix() + "\n" + text):
        continue
    text = re.sub(r"(?m)^(  level:) low$", r"\1 high", text, count=1)
    text = re.sub(r"(?m)^(  confirmation:) never$", r"\1 explicit", text, count=1)
    path.write_text(text, encoding="utf-8")

print("hardened migrated high-impact skills")
