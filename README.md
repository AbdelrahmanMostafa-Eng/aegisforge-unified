# AegisForge

[![CI](https://github.com/AbdelrahmanMostafa-Eng/aegisforge-unified/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdelrahmanMostafa-Eng/aegisforge-unified/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-2ea44f)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange)](CHANGELOG.md)

> **A risk-aware, searchable, and testable operating system for software-engineering agents.**

AegisForge is a compact control plane for trustworthy agent work. It combines two complementary ideas. It provides AegisForge’s focused workflow for classifying task risk and selecting proportionate engineering controls, while also providing SKILL.md’s portable skill contract, registry, validation, search, routing, and indexing runtime.

The result is intentionally conservative: a broad catalog may be discoverable, but a skill is not treated as production-ready merely because it exists. Skills declare their maturity, risk, confirmation requirements, inputs, outputs, and compatible harnesses. Experimental catalog scaffolds remain explicitly experimental until their procedures and scenario tests are specialized.

## Why AegisForge

Most agent frameworks optimize for code generation alone. AegisForge adds the missing operating discipline: classify risk before acting, discover the smallest suitable capability, preserve explainable evidence, and require stronger controls when a task touches production, identity, secrets, regulated data, money, or irreversible side effects.

## Core capabilities

| Capability | Implementation |
|---|---|
| Risk-aware workflow selection | `aegisforge assess` classifies production, security, identity, data, financial, destructive, and external-side-effect signals. |
| Rich skill contract | Each `skills/**/SKILL.md` declares identity, version, domains, capabilities, risk, inputs, outputs, and compatibility. |
| Explainable discovery | Search results include the keywords, domains, or metadata that caused a match. |
| Conservative routing | Routing prefers stable and lower-risk skills over experimental, deprecated, or archived skills. |
| Repository validation | Validation checks required repository files, structured skill metadata, duplicate IDs, semantic versions, required sections, and JSON syntax. |
| Registry generation | Indexing writes `registry/skills.json`, domain indexes, capability indexes, and aliases. |
| Portable authoring | Skills remain independent of any single agent harness and can be adapted to compatible environments. |

## Quick start

Run the commands from the repository root:

```bash
PYTHONPATH=. python3 -m aegisforge assess --text "Add OAuth login and deploy it to production"
PYTHONPATH=. python3 -m aegisforge validate .
PYTHONPATH=. python3 -m aegisforge skills . --status stable
PYTHONPATH=. python3 -m aegisforge search "debug a failing Python test" --root . --limit 5
PYTHONPATH=. python3 -m aegisforge route "create a safe research report with citations" --root . --limit 5
PYTHONPATH=. python3 -m aegisforge index .
```

After installation, the same entry point is available as `aegisforge`. The compatibility aliases `skill` and `skill-md` point to the same unified CLI.

## Risk assessment

The assessment engine is deterministic and explainable. It is a first-pass policy engine, not a replacement for human judgment or domain-specific review.

```text
Request → classify risk → select workflow → implement → independently verify → release with evidence
```

High-assurance tasks include production changes, identity and authorization work, secret handling, destructive operations, data or schema changes, payments, regulated data, infrastructure, and external side effects. The assessment output includes reasons, reversibility, sensitive-data signals, production scope, authorization impact, and ambiguity.

## Skill lifecycle

A skill follows the lifecycle below:

| Status | Meaning |
|---|---|
| `draft` | Incomplete and not ready for routine discovery. |
| `experimental` | Discoverable, but still requires specialization or additional testing. |
| `stable` | Reviewed and scenario-tested for its declared boundaries. |
| `deprecated` | Kept for migration compatibility and should not be newly selected. |
| `archived` | Retained for historical reference only. |

The generated catalog contains many experimental scaffolds by design. The catalog generator never promotes a generated placeholder to `stable` automatically.

## Repository layout

```text
AGENTS.md                 Project bootstrap and agent operating rules
skills/                   Canonical skill packages
schemas/                  Machine-readable task and skill contracts
registry/                 Generated skill, domain, capability, and alias indexes
aegisforge/               Risk engine, unified CLI, validator, and skill runtime
catalog/                  Canonical filename inventory for catalog generation
tools/                    Catalog and migration utilities
templates/                Plans, evidence ledgers, threat models, and readiness reports
docs/                     Architecture, authoring, testing, and governance guidance
tests/                    Policy, catalog, registry, routing, and validator tests
adapters/                 Harness integration placeholders
```

## Adding a skill

Add a package at `skills/<domain>/<skill-slug>/SKILL.md`. Include valid front matter, a focused `When to Use` section, a concrete procedure, verification criteria, safety boundaries, and at least one positive and one negative scenario. Use `status: experimental` until the skill has been reviewed and tested against its declared behavior.

Do not use generic low-risk metadata for a skill that can publish, send, delete, deploy, pay, file, modify credentials, change production systems, or make individualized medical, legal, or financial decisions. Those skills require precise side-effect and confirmation rules.

## Development checks

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m aegisforge validate .
python3 -m compileall -q aegisforge tools
```

## License

AegisForge is released under the MIT License. See [LICENSE](LICENSE). Contributed skill packages may include additional attribution or source requirements in their metadata.
