---
id: engineering.testing-strategy
name: testing-strategy
slug: testing-strategy
version: 0.1.0
status: experimental
summary: Choose and implement fit-for-purpose tests across unit, integration, contract, end-to-end, visual, property-based, performance, migration, and reliability dimensions. Use whenever behavior changes or completion needs evidence.
description: Choose and implement fit-for-purpose tests across unit, integration, contract, end-to-end, visual, property-based, performance, migration, and reliability dimensions. Use whenever behavior changes or completion needs evidence.
domains:
  - engineering
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - testing-strategy
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
# Testing strategy

Start from observable behavior and failure impact. Select the cheapest test that can detect the relevant failure, then add higher-level tests when integration, user experience, timing, security, or deployment behavior cannot be observed locally.

Use unit tests for pure rules, integration tests for boundaries, contract tests for independently deployed interfaces, end-to-end tests for critical user journeys, visual tests for rendered behavior, property-based tests for invariants, performance tests for budgets, and migration tests for forward and backward compatibility.

Tests must challenge the requirement rather than mirror implementation details. Include unhappy paths, authorization boundaries, malformed inputs, retries, timeouts, concurrency, empty states, localization, accessibility, and recovery when relevant. Record what the test suite cannot prove.

## Evidence standard

For each acceptance criterion, link at least one test or inspection method. A passing test is evidence for the behavior it covers, not proof of the entire system.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
