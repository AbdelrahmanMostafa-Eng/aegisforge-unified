---
id: security.identity-and-privacy
name: identity-and-privacy
slug: identity-and-privacy
version: 0.1.0
status: experimental
summary: Review authentication, authorization, tenant isolation, privacy, data minimization, retention, and user-control requirements. Use for accounts, permissions, personal data, analytics, integrations, or regulated workflows.
description: Review authentication, authorization, tenant isolation, privacy, data minimization, retention, and user-control requirements. Use for accounts, permissions, personal data, analytics, integrations, or regulated workflows.
domains:
  - security
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - identity-and-privacy
  - security
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
# Identity and privacy

Map actors to actions and resources. Verify authentication, session lifecycle, authorization at every server-side boundary, object ownership, tenant isolation, administrative actions, auditability, and safe failure behavior. Never rely on client-side checks for access control.

For personal or sensitive data, document purpose, collection, storage, access, retention, deletion, export, correction, masking, and third-party sharing. Minimize data and logs. Avoid copying real personal data into development or tests. Make consent, notice, and user controls explicit when applicable.

Test both allowed and denied paths, including stale sessions, privilege changes, cross-tenant identifiers, direct API access, replay, rate limits, and account recovery. Escalate jurisdiction-specific legal decisions rather than presenting generic guidance as legal advice.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
