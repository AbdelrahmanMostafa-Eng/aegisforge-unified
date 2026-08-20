---
id: core.risk-assessment
name: risk-assessment
slug: risk-assessment
version: 0.1.0
status: experimental
summary: Classify task risk and select proportionate controls before an agent acts. Use for production changes, secrets, identity, privacy, payments, data, infrastructure, external side effects, or uncertain blast radius.
description: Classify task risk and select proportionate controls before an agent acts. Use for production changes, secrets, identity, privacy, payments, data, infrastructure, external side effects, or uncertain blast radius.
domains:
  - core
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - risk-assessment
  - core
inputs:
  - task-description
outputs:
  - completed-result
risk:
  level: high
  confirmation: explicit
compatible_harnesses:
  - generic
  - claude-code
  - codex
quality:
  maturity: authored
  test_status: pending
  migration_source: aegisforge-v0.1
---
# Risk assessment

Assess the request across six dimensions: reversibility, data sensitivity, authorization impact, external side effects, production scope, and ambiguity. Record evidence for each dimension rather than assigning an unexplained score.

Use the highest applicable level:

- **Low:** reversible, local, well understood, no sensitive data, no external side effect.
- **Medium:** cross-file, user-facing, integration, or behavior-changing work.
- **High:** security, identity, privacy, infrastructure, production, or externally visible work.
- **Critical:** destructive, irreversible, financially consequential, regulated, or high-blast-radius work.

For high and critical work, require a threat model, explicit approvals, a rollback or recovery plan, independent verification, and a release evidence record. Never treat a keyword score as final authority: escalate when context contradicts the heuristic.

## Required output

Return `risk_level`, `workflow`, `reversibility`, `data_sensitivity`, `authorization_impact`, `external_side_effects`, `production_scope`, `assumptions`, `required_controls`, and `escalation_conditions`.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
