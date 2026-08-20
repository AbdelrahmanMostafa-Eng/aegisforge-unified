---
id: software-engineering.systematic-debugging
name: Systematic Debugging
slug: systematic-debugging
version: 1.0.0
status: stable
summary: Diagnose failures by reproducing, localizing, and verifying the root cause before applying a minimal fix.
description: Use when software behavior is failing, surprising, flaky, slow, or inconsistent and the cause is not already established.
domains:
  - software-engineering
  - coding-and-programming
capabilities:
  - debugging
  - diagnosis
  - root-cause-analysis
  - verification
skill_type: workflow
keywords:
  - debug
  - bug
  - failure
  - stack trace
  - flaky test
  - regression
inputs:
  - failure-report
  - source-code
  - logs
  - reproduction-steps
outputs:
  - root-cause
  - minimal-fix
  - regression-test
  - verification-report
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
related_skills:
  - software-engineering.test-driven-development
  - _core.verification-before-completion
quality:
  maturity: production
  test_status: scenario-tested
---
# Systematic Debugging

## When to Use

Use whenever a failure has an uncertain cause. Do not jump directly from a symptom to a patch.

## Procedure

1. Record the exact symptom, expected behavior, environment, inputs, and first known failing point.
2. Reproduce the failure with the smallest reliable command or scenario.
3. Read the complete error, stack trace, logs, and relevant recent changes.
4. Form a small set of competing hypotheses.
5. Add the narrowest observation or experiment that distinguishes those hypotheses.
6. Trace the failure backward from the symptom to the first incorrect state.
7. Apply the smallest fix at the root cause, not at a downstream symptom.
8. Add or strengthen a regression test.
9. Re-run the reproducer, relevant tests, and broader checks.
10. Report the cause, fix, evidence, and remaining uncertainty.

## Verification

A successful debugging result has a reproducible baseline failure, a documented root cause, a minimal corrective change, a regression test, and evidence that the original failure no longer occurs without introducing a new failure.

## Anti-Patterns

Do not guess-and-patch repeatedly, suppress the error, broaden permissions without evidence, delete a failing test, or stop after a single successful retry. A flaky pass is not a diagnosis.

## Safety and Boundaries

Use production logs and data according to their access policy. Avoid destructive experiments against production systems. Redact secrets and personal data from reports.
