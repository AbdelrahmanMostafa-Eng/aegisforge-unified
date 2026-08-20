---
id: operations.delivery-pipeline
name: delivery-pipeline
slug: delivery-pipeline
version: 0.1.0
status: experimental
summary: Design or review CI/CD pipelines that lint, test, scan, build, publish, deploy, verify, and recover safely. Use when adding automation, changing release flow, or preparing production delivery.
description: Design or review CI/CD pipelines that lint, test, scan, build, publish, deploy, verify, and recover safely. Use when adding automation, changing release flow, or preparing production delivery.
domains:
  - operations
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - delivery-pipeline
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
# Delivery pipeline

Make the pipeline deterministic, least-privileged, observable, and easy to reproduce locally. Run formatting, type checks, unit and integration tests, dependency and secret scans, static analysis, build validation, artifact publication, deployment, smoke tests, and rollback verification as appropriate to the risk level.

Pin third-party actions and dependencies where practical. Separate build, deploy, and approval permissions. Protect environments and production credentials. Prefer promotion of the same immutable artifact rather than rebuilding per environment. Emit links to evidence and fail closed on missing required checks.

Do not add deployment automation without documenting ownership, environments, triggers, rollback, secrets, and cost. For high-risk releases, require explicit approval and progressive rollout.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
