---
id: core.human-approval
name: human-approval
slug: human-approval
version: 0.1.0
status: experimental
summary: Define and enforce human confirmation gates for irreversible, destructive, privacy-sensitive, financially consequential, externally visible, or production actions. Use before an agent creates side effects outside the working tree.
description: Define and enforce human confirmation gates for irreversible, destructive, privacy-sensitive, financially consequential, externally visible, or production actions. Use before an agent creates side effects outside the working tree.
domains:
  - core
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - human-approval
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
# Human approval

Identify actions that change the world beyond a local draft: deleting or migrating data, changing permissions, handling secrets, deploying to production, sending messages, publishing content, purchasing resources, creating cloud infrastructure, or merging protected branches.

Before such an action, present the exact operation, scope, affected resources, expected consequence, rollback or recovery path, and unresolved uncertainty. Ask for confirmation at the last safe point before execution. Do not bundle unrelated actions into one approval.

Approval is not required for a harmless dry run, local read-only inspection, or reversible change that stays within the isolated workspace, unless project policy says otherwise. If authorization is unclear, stop rather than infer permission.

## Required output

Produce an approval record with `action`, `scope`, `risk`, `preconditions`, `rollback`, `evidence`, `approver`, `timestamp`, and `decision`. If declined, preserve the decision and propose a safe alternative.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
