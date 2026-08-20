# Changelog

All notable changes to AegisForge are documented here.

## 0.3.0 - Trustworthy control plane

- Added explicit governance states and transition gates for authorization, execution, verification, approval, and release.
- Added structured evidence ledgers with validation, uncertainty tracking, approval metadata, and independent-verification fields.
- Expanded risk assessment with deterministic control consequences, confirmation requirements, migration semantics, user-data signals, external-side-effect signals, and public-release signals.
- Added a reproducible nine-scenario evaluation suite and `evaluate`, `doctor`, `inspect`, and `evidence` CLI commands.
- Hardened front matter and registry validation with duplicate-key detection, portable relative paths, quality checks, schema checks, broken-reference checks, and registry freshness diagnostics.
- Added compatibility-aware routing with selected and rejected alternatives.
- Added packaged schema resources, clean-install verification, expanded regression coverage, richer documentation, and a comprehensive CI template.

## 0.2.1 - Repository polish

- Added GitHub Actions CI, issue forms, pull-request guidance, CODEOWNERS, EditorConfig, and citation metadata.
- Added unified runtime architecture documentation and improved the public README positioning, badges, and project links.
- Updated package metadata, security guidance, and contributor-facing repository conventions.

## [Unreleased]

### Added

- Portable `AGENTS.md` bootstrap with adaptive workflow, evidence, escalation, and human-control rules.
- Deterministic Python reference CLI with `assess`, `validate`, and `skills` commands.
- Explainable risk classification for reversibility, production scope, identity, data, secrets, infrastructure, financial, and external-side-effect signals.
- Skill catalog covering core workflow, engineering, security, product, quality, operations, and AI/platform concerns.
- Machine-readable task-assessment and skill-manifest schemas.
- Plan, evidence-ledger, threat-model, and release-readiness templates.
- Architecture, governance, adapter, evaluation, skill-authoring, and roadmap documentation.
- GitHub Actions validation workflow and unit tests.

### Known limitations

- The classifier is a deterministic first-pass heuristic and requires human judgment for hidden context.
- Harness adapters are documented but not yet packaged for every supported coding-agent environment.
- Evaluation scenarios and outcome benchmarks are planned, not yet a published statistical claim.
- Security scans, deployment integrations, observability backends, and domain packs are not yet bundled into the foundation release.

## 0.2.0 - Unified runtime

- Combined AegisForge risk assessment and policy workflows with the SKILL.md registry, rich metadata contract, explainable search, conservative routing, and index generation.
- Added the unified `aegisforge` CLI with `assess`, `validate`, `skills`, `search`, `route`, and `index` commands.
- Added `skill` and `skill-md` command aliases for compatibility.
- Migrated the original AegisForge skill packages to explicit experimental metadata with risk and confirmation declarations.
- Expanded tests to cover policy assessment, catalog discovery, registry validation, search, routing, and repository validation.
