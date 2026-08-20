---
id: software-engineering.test-driven-development
name: Test-Driven Development
slug: test-driven-development
version: 1.0.0
status: stable
summary: Implement behavior by specifying it with a failing test before writing the smallest passing code.
description: Use when implementing or changing software behavior that can be expressed through automated tests and should be protected against regressions.
domains:
  - software-engineering
  - coding-and-programming
capabilities:
  - requirements-analysis
  - implementation
  - testing
  - refactoring
skill_type: procedure
keywords:
  - tdd
  - test first
  - red green refactor
  - unit testing
  - regression prevention
inputs:
  - behavior-requirement
  - source-code
  - test-framework
outputs:
  - failing-test
  - passing-implementation
  - regression-suite
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
related_skills:
  - _core.verification-before-completion
  - software-engineering.systematic-debugging
quality:
  maturity: production
  test_status: scenario-tested
---
# Test-Driven Development

## When to Use

Use when implementing a new behavior, fixing a reproducible defect, or changing an existing contract that can be checked by automated tests.

## Preconditions

Identify the expected behavior, the relevant test command, the smallest testable boundary, and any existing conventions. If the requirement is ambiguous, use `_core.task-framing` before coding.

## Procedure

1. Express one observable behavior as a focused test.
2. Run the test before implementation and confirm that it fails for the intended reason.
3. Implement the smallest change that makes the test pass.
4. Run the focused test again and inspect the result.
5. Refactor for clarity without changing behavior.
6. Run the relevant broader test suite and inspect the diff.
7. Report what the tests prove and what they do not prove.

## Verification

The red phase must fail because the behavior is absent or incorrect, not because of a syntax error, missing fixture, or broken test setup. The green phase must pass the new test and the relevant regression suite. The final diff should contain only changes necessary for the stated behavior.

## Failure Handling

If the baseline test fails for an unrelated reason, isolate the environment or test defect before proceeding. If the expected behavior cannot be observed at the current boundary, redesign the test around a stable public contract rather than asserting implementation details.

## Safety and Boundaries

Do not weaken, delete, skip, or overfit tests merely to obtain a passing result. Do not claim broad correctness from a single passing test. Do not modify production systems or publish changes without the confirmation policy of the surrounding task.
