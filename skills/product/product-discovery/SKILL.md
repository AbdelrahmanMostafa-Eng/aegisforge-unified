---
id: product.product-discovery
name: product-discovery
slug: product-discovery
version: 0.1.0
status: experimental
summary: Validate the user problem, desired outcome, assumptions, success metrics, and non-goals before building a feature. Use when a request describes a solution but not the underlying need or measurable outcome.
description: Validate the user problem, desired outcome, assumptions, success metrics, and non-goals before building a feature. Use when a request describes a solution but not the underlying need or measurable outcome.
domains:
  - product
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - product-discovery
  - product
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
# Product discovery

Separate the proposed solution from the problem it is meant to solve. Identify target users, context, current behavior, pain, desired behavior, constraints, and the smallest experiment that can test the riskiest assumption.

Define a measurable outcome and guardrail metrics. State what would count as evidence that the feature is useful, what would disprove the assumption, and what the team will deliberately not build. Prefer a narrow experiment or prototype when uncertainty is high.

Do not invent user research, market data, or business metrics. Label assumptions and ask for evidence when the decision depends on them. A technically correct implementation is not a successful delivery if it does not improve the intended outcome.

## Required output

Produce a problem statement, target user, current and desired behavior, assumptions, success metrics, guardrails, non-goals, experiment or acceptance plan, and decision.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
