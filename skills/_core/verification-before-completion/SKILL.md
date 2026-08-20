---
id: _core.verification-before-completion
name: Verification Before Completion
slug: verification-before-completion
version: 1.0.0
status: stable
summary: Verify observable results before claiming that a task is complete.
description: Use before reporting completion of any task that produces files, code, data, analysis, media, external changes, or other inspectable results.
domains:
  - _core
capabilities:
  - verification
  - quality-control
  - evidence-reporting
skill_type: policy
keywords:
  - verify
  - check
  - test
  - validate
  - complete
  - evidence
inputs:
  - task-contract
  - produced-artifacts
  - acceptance-criteria
outputs:
  - verification-result
  - limitations
  - completion-report
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
quality:
  maturity: production
  test_status: scenario-tested
---
# Verification Before Completion

## When to Use

Use immediately before saying that work is complete or before handing over an artifact.

## Procedure

1. Re-read the task contract and acceptance criteria.
2. Inspect the actual files, output, state, or external result rather than relying on memory.
3. Run the narrowest meaningful tests, checks, renders, or comparisons.
4. Confirm that important negative cases and safety boundaries still hold.
5. Distinguish verified facts, reasonable inferences, and unverified assumptions.
6. Report completion only for the parts supported by evidence.

## Verification

The final report should identify what was checked, the result of each check, remaining limitations, and any user action still required.

## Boundaries

Never claim that a command ran, a file was created, a test passed, a source was consulted, or an external action succeeded unless the result was actually observed. A generated artifact is not automatically a correct artifact.
