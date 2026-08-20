---
id: engineering.data-migration
name: data-migration
slug: data-migration
version: 0.1.0
status: experimental
summary: Plan and verify database schema, data backfill, retention, or indexing changes with compatibility, backup, rollout, validation, and recovery controls. Use for any persistent-data change.
description: Plan and verify database schema, data backfill, retention, or indexing changes with compatibility, backup, rollout, validation, and recovery controls. Use for any persistent-data change.
domains:
  - engineering
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - data-migration
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
# Data migration

Inventory readers, writers, historical data, indexes, constraints, jobs, reports, replicas, and external consumers before changing persistence. Define the old and new schemas, compatibility window, rollout order, backfill strategy, idempotency, throttling, observability, and recovery plan.

Prefer expand-and-contract migrations: add compatible structures, deploy dual-read or dual-write only when justified, backfill safely, verify counts and invariants, migrate readers, then remove obsolete structures in a later change. Never assume rollback is safe after destructive transformation; document roll-forward recovery when necessary.

Test empty, partial, duplicate, malformed, large, and legacy records. Prove backup and restore procedures for high-impact data. Do not use production personal data in tests or local development.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
