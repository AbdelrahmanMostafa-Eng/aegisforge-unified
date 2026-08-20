---
id: engineering.implementation-planning
name: implementation-planning
slug: implementation-planning
version: 0.1.0
status: experimental
summary: Convert an approved design into small, ordered, independently verifiable implementation tasks. Use before multi-file feature work, migrations, refactors, or delegated agent execution.
description: Convert an approved design into small, ordered, independently verifiable implementation tasks. Use before multi-file feature work, migrations, refactors, or delegated agent execution.
domains:
  - engineering
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - implementation-planning
  - engineering
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
# Implementation planning

Create a plan that an engineer with no hidden context can execute. Each task must state its purpose, exact files or symbols, dependencies, expected behavior, tests to add or update, verification commands, and completion evidence.

Sequence work so that contracts and characterization tests precede implementations, data changes have recovery paths, and risky changes remain isolated. Include assumptions, non-goals, open questions, and a rollback strategy. Keep tasks small enough to review without reconstructing the entire project.

Before execution, perform a pre-flight review for contradictions, missing dependencies, untestable requirements, unsafe permissions, and plan steps that would violate the risk assessment. Update the plan when evidence changes; do not silently drift.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
