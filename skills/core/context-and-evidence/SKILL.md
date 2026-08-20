---
id: core.context-and-evidence
name: context-and-evidence
slug: context-and-evidence
version: 0.1.0
status: experimental
summary: Preserve the minimum useful context and a verifiable evidence ledger across agent sessions and handoffs. Use when work spans multiple tasks, subagents, tools, or review rounds.
description: Preserve the minimum useful context and a verifiable evidence ledger across agent sessions and handoffs. Use when work spans multiple tasks, subagents, tools, or review rounds.
domains:
  - core
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - context-and-evidence
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
# Context and evidence

Keep the active context small and durable. Store the task statement, approved plan, decisions, assumptions, changed files, commands run, test results, unresolved findings, and next action in a ledger. Prefer file references over pasting large diffs into prompts.

Every evidence item must include what was checked, the command or artifact used, the result, the time or commit when relevant, and any limitation. Distinguish **verified**, **partially verified**, **unverified**, and **blocked**. Never upgrade an unverified claim merely because another agent repeats it.

Before handing work to another agent, provide only the context needed for the next decision plus links to the authoritative artifacts. After the handoff, reconcile the returned work against the plan and ledger. Preserve dissenting findings and record who resolved them and why.

## Required output

Maintain an evidence ledger with `requirement`, `evidence`, `status`, `owner`, `commit_or_artifact`, `limitations`, and `next_action` fields.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
