---
id: quality.performance-and-accessibility
name: performance-and-accessibility
slug: performance-and-accessibility
version: 0.1.0
status: experimental
summary: Evaluate performance budgets and accessibility behavior for user-facing or high-volume systems. Use for frontend, mobile, APIs, services, or changes that may affect latency, throughput, resource usage, or inclusive access.
description: Evaluate performance budgets and accessibility behavior for user-facing or high-volume systems. Use for frontend, mobile, APIs, services, or changes that may affect latency, throughput, resource usage, or inclusive access.
domains:
  - quality
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - performance-and-accessibility
  - quality
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
# Performance and accessibility

Define budgets before optimizing: latency percentiles, throughput, startup time, memory, bundle size, database cost, battery, or interaction timing. Measure representative workloads and compare a baseline. Diagnose before changing code; do not trade correctness, security, or accessibility for an unmeasured speed claim.

For user-facing behavior, verify semantics, keyboard operation, focus management, labels, contrast, reduced motion, screen-reader output, touch targets, responsive layouts, zoom, and localization. Use automated checks for coverage and human review for experience and assistive-technology behavior.

Record environment, dataset, browser or device, network, sample size, variance, and limitations. A benchmark result is evidence only for the workload it represents.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
