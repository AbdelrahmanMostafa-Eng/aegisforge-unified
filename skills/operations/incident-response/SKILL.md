---
id: operations.incident-response
name: incident-response
slug: incident-response
version: 0.1.0
status: experimental
summary: Coordinate safe response to production incidents, regressions, security events, and failed deployments. Use when customer impact or service degradation is suspected.
description: Coordinate safe response to production incidents, regressions, security events, and failed deployments. Use when customer impact or service degradation is suspected.
domains:
  - operations
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - incident-response
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
# Incident response

Prioritize human safety, customer impact, containment, and evidence preservation. Establish an incident owner, severity, timeline, affected systems, current symptoms, and communication channel. Prefer reversible containment such as rollback, feature disablement, rate limiting, or isolation over speculative fixes.

Separate observed facts from hypotheses. Record commands, timestamps, changes, logs, and decisions. Protect private data while preserving enough evidence for diagnosis. After recovery, verify customer impact, data integrity, monitoring, and follow-up ownership.

Write a blameless review that explains contributing conditions, detection gaps, response quality, corrective actions, and prevention work. Do not close the incident merely because the error rate returned to normal.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
