---
id: _core.task-framing
name: Task Framing
slug: task-framing
version: 1.0.0
status: stable
summary: Convert an ambiguous request into a precise, actionable task contract.
description: Use at the beginning of a task when the desired outcome, constraints, inputs, audience, or success criteria are unclear or distributed across the conversation.
domains:
  - _core
capabilities:
  - clarification
  - requirements-analysis
  - acceptance-criteria
skill_type: procedure
keywords:
  - clarify
  - requirements
  - scope
  - goal
  - constraints
  - acceptance criteria
inputs:
  - conversation
  - user-request
  - available-context
outputs:
  - task-contract
  - clarified-assumptions
  - acceptance-criteria
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
# Task Framing

## When to Use

Use this skill before substantial work when the request has multiple interpretations, meaningful constraints, external dependencies, or a high cost of rework.

## Procedure

1. State the requested outcome in one sentence.
2. Identify the intended audience, output format, scope, deadline, and quality bar.
3. Separate known facts from assumptions and unknowns.
4. Identify inputs, permissions, tools, external services, and side effects.
5. Ask only the smallest questions that block safe progress.
6. Convert the result into observable acceptance criteria.
7. Begin execution only after the task is sufficiently precise, while recording residual assumptions.

## Verification

A task is framed when another capable person could understand what to produce, what not to produce, how to judge completion, and which actions require confirmation.

## Boundaries

Do not invent missing requirements as facts. Do not ask questions whose answers do not affect the work. For high-impact decisions, preserve uncertainty and require appropriate human ownership.
