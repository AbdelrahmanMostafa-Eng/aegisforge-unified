---
id: engineering.architecture
name: architecture
slug: architecture
version: 0.1.0
status: experimental
summary: Design or review software architecture with explicit boundaries, trade-offs, data flows, failure modes, security boundaries, and operational constraints. Use before substantial features, integrations, migrations, or platform changes.
description: Design or review software architecture with explicit boundaries, trade-offs, data flows, failure modes, security boundaries, and operational constraints. Use before substantial features, integrations, migrations, or platform changes.
domains:
  - engineering
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - architecture
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
# Architecture

Start from system goals and constraints, not fashionable components. Define bounded contexts, responsibilities, interfaces, data ownership, trust boundaries, synchronous and asynchronous flows, failure modes, and recovery behavior. Prefer the simplest architecture that meets current requirements.

For each significant decision, compare at least two viable options and record the reason for the choice, the cost accepted, and the conditions that would justify revisiting it. Identify availability, consistency, latency, privacy, cost, and operability implications.

Produce an architecture note with a component diagram, data-flow diagram, dependency map, threat boundaries, migration or rollout approach, and explicit non-goals. Verify that the proposed design can be tested and operated by the intended team.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
