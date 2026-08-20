---
id: security.threat-modeling
name: threat-modeling
slug: threat-modeling
version: 0.1.0
status: experimental
summary: Analyze assets, actors, trust boundaries, abuse cases, and mitigations for a feature or architecture. Use before security-sensitive, identity, privacy, internet-facing, payment, or high-blast-radius work.
description: Analyze assets, actors, trust boundaries, abuse cases, and mitigations for a feature or architecture. Use before security-sensitive, identity, privacy, internet-facing, payment, or high-blast-radius work.
domains:
  - security
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - threat-modeling
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
# Threat modeling

Define the assets that must be protected, legitimate actors, attacker capabilities, trust boundaries, entry points, sensitive flows, and security objectives. Inspect the design and implementation for spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation.

For each credible abuse case, document preconditions, impact, likelihood, prevention, detection, response, and residual risk. Do not assume authentication means authorization is correct. Test tenant isolation, object ownership, privilege changes, replay, rate limits, logging, and failure behavior where applicable.

Threat modeling is a decision aid, not a security certificate. Escalate unresolved high-impact findings to a qualified human reviewer and preserve the model with the feature evidence.

## Required output

Produce `assets`, `trust_boundaries`, `abuse_cases`, `mitigations`, `security_tests`, `residual_risks`, and `approval_requirements`.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
