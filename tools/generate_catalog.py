#!/usr/bin/env python3
"""Generate normalized SKILL.md packages from catalog/file-names.md.

The generator intentionally creates reviewable experimental scaffolds. It does
not claim that a generated placeholder is a completed production skill.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKIP_HEADINGS = {"recommended-file-layout", "filename-rules"}
DOMAIN_ALIASES = {
    "ai": "ai-and-agents",
    "cloud-and-devops": "cloud-and-infrastructure",
    "web-and-product": "web-and-product",
    "data": "data-and-analytics",
    "research-and-science": "research-and-intelligence",
    "education-and-training": "education-and-learning",
    "writing-and-communication": "writing-and-publishing",
    "graphic-design-and-branding": "design-and-creative",
    "image-creation-and-vision": "image-and-graphics",
    "video-and-animation": "video-and-film",
    "audio-and-music": "audio-and-music",
    "3d-and-spatial-computing": "3d-and-spatial-computing",
    "documents-and-knowledge": "documents-and-presentations",
    "productivity-and-personal-life": "personal-productivity",
    "repository-and-community-operations": "repository-and-community-operations",
    "cross-domain": "cross-domain",
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_catalog(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", raw)
        if heading:
            current = slugify(heading.group(1))
            sections.setdefault(current, [])
            in_fence = False
            continue
        if current is None:
            continue
        if raw.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        candidate = raw.strip().strip("`").strip()
        if candidate.startswith("-"):
            candidate = candidate[1:].strip()
        if SLUG_RE.fullmatch(candidate) and candidate not in {"skill-name", "domain", "name", "slug"}:
            sections[current].append(candidate)
    return {domain: sorted(set(skills)) for domain, skills in sections.items() if domain not in SKIP_HEADINGS and skills}


def render(domain: str, slug: str, canonical_source: str) -> str:
    title = slug.replace("-", " ").title()
    return f'''---
id: {domain}.{slug}
name: {title}
slug: {slug}
version: 0.1.0
status: experimental
summary: Apply the {title.lower()} capability in a controlled, verifiable way.
description: Use when the request requires {title.lower()} and the task can be completed within the declared boundaries.
domains:
  - {domain}
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - {slug}
  - {title.lower()}
inputs:
  - task-description
outputs:
  - completed-result
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
quality:
  maturity: scaffold
  test_status: pending
  catalog_source: {canonical_source}
---
# {title}

> This is an **experimental catalog scaffold** generated from the SKILL.md capability inventory. It is discoverable, but it must be reviewed and specialized before being promoted to `stable`.

## When to Use

Use this skill when the user's request clearly requires **{title.lower()}**. Confirm the actual objective, inputs, output format, constraints, and any domain-specific requirements before acting.

## Procedure

1. Clarify the intended outcome and identify the information or files required.
2. Choose the smallest safe method that satisfies the request.
3. Perform the work in observable steps and preserve relevant assumptions.
4. Check the result against the user's requested format and quality criteria.
5. Report what was completed, what remains uncertain, and what should be reviewed by a subject-matter expert.

## Verification

Verify that the requested output exists, is internally consistent, and does not claim work or evidence that was not actually produced. For high-impact domains, add domain-specific review and confirmation rules before changing this scaffold to `stable`.

## Safety and Boundaries

This scaffold does not authorize publishing, sending communications, changing production systems, making payments, filing legal documents, giving individualized medical or financial decisions, or handling sensitive information beyond the user's explicit request. Add precise side-effect and confirmation rules when specializing the skill.

## Specialization Checklist

- Replace the generic procedure with domain-expert instructions.
- Add positive and negative trigger scenarios.
- Add references, examples, and supported file types where relevant.
- Declare tools, credentials, dependencies, and side effects.
- Add tests before changing `status` from `experimental` to `stable`.

## Catalog Provenance

Generated from the canonical filename inventory section `{canonical_source}`.
'''


def generate(source: Path, output: Path) -> tuple[int, int]:
    sections = parse_catalog(source)
    created = 0
    skipped = 0
    for source_domain, skills in sections.items():
        domain = DOMAIN_ALIASES.get(source_domain, source_domain)
        for slug in skills:
            target = output / "skills" / domain / slug / "SKILL.md"
            if target.exists():
                skipped += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(domain, slug, source_domain), encoding="utf-8")
            created += 1
    return created, skipped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("catalog/file-names.md"))
    parser.add_argument("--output", type=Path, default=Path("."))
    args = parser.parse_args()
    created, skipped = generate(args.source, args.output)
    print(f"generated={created} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
