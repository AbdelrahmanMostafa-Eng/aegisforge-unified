---
id: product.acceptance-and-ux
name: acceptance-and-ux
slug: acceptance-and-ux
version: 0.1.0
status: experimental
summary: Define and verify user-facing acceptance criteria across interaction design, accessibility, responsive behavior, localization, empty states, errors, and recovery. Use for frontend, mobile, workflow, and customer-facing changes.
description: Define and verify user-facing acceptance criteria across interaction design, accessibility, responsive behavior, localization, empty states, errors, and recovery. Use for frontend, mobile, workflow, and customer-facing changes.
domains:
  - product
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - acceptance-and-ux
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
# Acceptance and UX

Describe the critical user journeys from the user’s perspective, including first use, success, empty, loading, error, retry, permission-denied, offline, and recovery states. Make acceptance criteria observable and testable without depending on implementation details.

Review keyboard navigation, focus order, semantics, labels, contrast, reduced motion, screen-reader announcements, responsive layouts, touch targets, localization, time zones, right-to-left behavior, and content clarity when relevant. Use screenshots, browser automation, accessibility tooling, and human review as appropriate.

Do not treat passing unit tests as evidence of a usable interface. Record visual or accessibility limitations and escalate when a human with the relevant disability or domain expertise should review the result.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
