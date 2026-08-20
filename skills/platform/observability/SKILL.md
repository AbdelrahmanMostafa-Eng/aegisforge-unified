---
id: platform.observability
name: observability
slug: observability
version: 0.1.0
status: experimental
summary: Design or review logs, metrics, traces, health checks, alerts, dashboards, and privacy-safe telemetry. Use for services, agents, integrations, production changes, performance issues, or incident readiness.
description: Design or review logs, metrics, traces, health checks, alerts, dashboards, and privacy-safe telemetry. Use for services, agents, integrations, production changes, performance issues, or incident readiness.
domains:
  - platform
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - observability
  - platform
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
# Observability

Start from user-impacting failure modes and operational questions. Define structured events, useful dimensions, latency and error metrics, traces across service and tool boundaries, health and readiness checks, dashboards, alert thresholds, ownership, and retention.

Do not log secrets, tokens, raw personal data, prompts containing confidential information, or unbounded payloads. Make correlation identifiers safe and useful. Verify that alerts are actionable, noise is bounded, and a responder can diagnose the documented failure from the available evidence.

For agent systems, record model and tool versions, policy decisions, retries, latency, cost, refusals, and outcome signals without exposing sensitive content. Document sampling and redaction so telemetry remains safe and useful.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
