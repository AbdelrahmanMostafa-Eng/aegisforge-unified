---
id: quality.independent-review
name: independent-review
slug: independent-review
version: 0.1.0
status: experimental
summary: Review a change independently against requirements, risks, quality attributes, and evidence without modifying the working tree. Use after implementation and before merge or release.
description: Review a change independently against requirements, risks, quality attributes, and evidence without modifying the working tree. Use after implementation and before merge or release.
domains:
  - quality
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - independent-review
  - quality
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
# Independent review

Read the approved requirement, plan, risk assessment, diff, tests, and evidence ledger before forming findings. Review for requirement gaps, incorrect behavior, security and privacy issues, authorization failures, performance regressions, reliability risks, maintainability, observability, accessibility, documentation, and scope creep.

For every finding, provide severity, exact file and line or artifact, violated requirement or risk, impact, reproduction or reasoning, and a concrete fix. Do not suppress a finding because the implementer intended the behavior or because the plan contains it; flag the conflict and escalate the decision.

Reviewers should be read-only. They should not change branches, rewrite history, weaken tests, or perform unrelated cleanup. A review is complete only when findings are resolved, explicitly accepted by an authorized human, or documented as residual risk.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
