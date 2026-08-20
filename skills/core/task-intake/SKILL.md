---
id: core.task-intake
name: task-intake
slug: task-intake
version: 0.1.0
status: experimental
summary: Convert a natural-language request into an explicit outcome, constraints, non-goals, acceptance criteria, and an appropriate AegisForge workflow. Use before implementation whenever the request is ambiguous, multi-step, or user-facing.
description: Convert a natural-language request into an explicit outcome, constraints, non-goals, acceptance criteria, and an appropriate AegisForge workflow. Use before implementation whenever the request is ambiguous, multi-step, or user-facing.
domains:
  - core
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - task-intake
  - core
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
# Task intake

Establish what success means before proposing implementation. Restate the requested outcome in one sentence, then separate the user problem from the requested solution. Record actors, affected systems, constraints, non-goals, assumptions, and acceptance criteria.

Choose the smallest workflow that can produce trustworthy evidence:

- Use **lightweight** for narrow, reversible, well-understood changes.
- Use **standard** for normal feature, bugfix, refactor, integration, or documentation work.
- Use **high-assurance** for production, identity, privacy, payment, data migration, destructive, regulated, or externally visible work.

Do not invent product requirements. Mark unknowns explicitly and ask only the questions whose answers would change the solution or risk level. For each acceptance criterion, state how it will be verified. If the request contains a hidden trade-off, surface it before implementation.

## Required output

Produce an intake record containing `goal`, `user_problem`, `scope`, `non_goals`, `constraints`, `assumptions`, `acceptance_criteria`, `workflow`, `risk_level`, and `open_questions`. Keep it concise enough for a human to approve.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
