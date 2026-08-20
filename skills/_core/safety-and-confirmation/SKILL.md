---
id: _core.safety-and-confirmation
name: Safety And Confirmation
slug: safety-and-confirmation
version: 1.0.0
status: stable
summary: Detect consequential side effects and obtain confirmation before performing them.
description: Use whenever a task could publish, send, delete, deploy, pay, file, change credentials, alter production systems, or materially affect health, legal status, privacy, or safety.
domains:
  - _core
capabilities:
  - risk-assessment
  - confirmation
  - boundary-setting
skill_type: policy
keywords:
  - confirmation
  - approval
  - publish
  - send
  - delete
  - deploy
  - payment
  - credentials
inputs:
  - user-request
  - proposed-action
  - side-effect-metadata
outputs:
  - risk-decision
  - confirmation-request
risk:
  level: critical
  confirmation: always-before-consequential-side-effect
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
quality:
  maturity: production
  test_status: scenario-tested
---
# Safety And Confirmation

## When to Use

Use this policy whenever the requested work could create a consequential external effect. Separate preparing or drafting an action from carrying it out.

## Procedure

1. Identify the requested outcome and every action needed to achieve it.
2. Classify each action as observation, local transformation, reversible mutation, or consequential side effect.
3. Check for effects involving communication, publication, deletion, payment, legal filing, credentials, production infrastructure, personal data, health, or safety.
4. Complete safe preparation without crossing the side-effect boundary.
5. Explain the exact pending action, target, scope, and likely consequence.
6. Ask for explicit confirmation immediately before the consequential action.
7. After confirmation, perform only the confirmed action and report the result.

## Verification

Before requesting confirmation, ensure the proposed action is specific enough that a reasonable person can understand what will happen. After execution, verify the actual result and disclose failures or partial completion.

## Boundaries

Never treat a vague statement such as “go ahead” as permission for an action whose target or scope has changed. Never infer permission to spend money, publish content, send messages, disclose private information, delete data, or modify production systems. Do not continue after a failed confirmation step.

## Examples

- Drafting an email is safe preparation; sending it requires confirmation.
- Preparing a deployment plan is safe preparation; deploying requires confirmation.
- Calculating a financial scenario is analysis; transferring funds is a consequential action.
