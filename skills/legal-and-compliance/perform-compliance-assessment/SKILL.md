---
id: legal-and-compliance.perform-compliance-assessment
name: Perform Compliance Assessment
slug: perform-compliance-assessment
version: 0.1.0
status: experimental
summary: Apply the perform compliance assessment capability in a controlled, verifiable way.
description: Use when the request requires perform compliance assessment and the task can be completed within the declared boundaries.
domains:
  - legal-and-compliance
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - perform-compliance-assessment
  - perform compliance assessment
inputs:
  - task-description
outputs:
  - completed-result
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
quality:
  maturity: scaffold
  test_status: pending
  catalog_source: legal-and-compliance
---
# Perform Compliance Assessment

> This is an **experimental catalog scaffold** generated from the SKILL.md capability inventory. It is discoverable, but it must be reviewed and specialized before being promoted to `stable`.

## When to Use

Use this skill when the user's request clearly requires **perform compliance assessment**. Confirm the actual objective, inputs, output format, constraints, and any domain-specific requirements before acting.

## Procedure

1. Clarify the intended outcome and identify the information or files required.
2. Choose the smallest safe method that satisfies the request.
3. Perform the work in observable steps and preserve relevant assumptions.
4. Check the result against the user's requested format and quality criteria.
5. Report what was completed, what remains uncertain, and what should be reviewed by a subject-matter expert.

## Verification

Verify that the requested output exists, is internally consistent, and does not claim work or evidence that was not actually produced. For high-impact domains, add domain-specific review and confirmation rules before changing this scaffold to `stable`.

## Safety and Boundaries

This scaffold does not authorize publishing, sending communications, changing production systems, making payments, filing legal documents, giving individualized medical or financial decisions, or handling sensitive information beyond the user's explicit request. Add precise side-effect and confirmation rules when specializing the skill.

## Specialization Checklist

- Replace the generic procedure with domain-expert instructions.
- Add positive and negative trigger scenarios.
- Add references, examples, and supported file types where relevant.
- Declare tools, credentials, dependencies, and side effects.
- Add tests before changing `status` from `experimental` to `stable`.

## Catalog Provenance

Generated from the canonical filename inventory section `legal-and-compliance`.
