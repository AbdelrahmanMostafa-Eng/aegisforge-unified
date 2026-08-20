---
id: operations.production-readiness
name: production-readiness
slug: production-readiness
version: 0.1.0
status: experimental
summary: Determine whether a change is safe to release and operate in production. Use before deployment, release, migration, rollout, or completion of a high-impact feature.
description: Determine whether a change is safe to release and operate in production. Use before deployment, release, migration, rollout, or completion of a high-impact feature.
domains:
  - operations
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - production-readiness
  - operations
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
# Production readiness

Confirm that the change has a release owner, environment strategy, configuration review, migration plan, rollback or recovery path, feature-flag or progressive-rollout option where useful, and post-deployment verification.

Check structured logs, metrics, traces, dashboards, alerts, SLO or performance budgets, capacity assumptions, cost impact, backups, restore procedures, and runbooks. Verify that sensitive data is not exposed through telemetry. For migrations, prove forward compatibility, failure recovery, and rollback or roll-forward behavior.

A release is not ready merely because CI passes. Mark each control as verified, partially verified, unverified, or not applicable, and escalate missing evidence for high-impact systems.

## Required output

Produce a readiness report with `release_scope`, `owner`, `dependencies`, `migrations`, `observability`, `performance`, `rollback`, `runbook`, `post_release_checks`, `open_risks`, and `decision`.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
