---
id: quality.agent-evaluation
name: agent-evaluation
slug: agent-evaluation
version: 0.1.0
status: experimental
summary: Evaluate an agent workflow or skill with reproducible scenarios, evidence-based scoring, cost and latency measures, and human-correction analysis. Use when changing prompts, orchestration, model routing, or framework behavior.
description: Evaluate an agent workflow or skill with reproducible scenarios, evidence-based scoring, cost and latency measures, and human-correction analysis. Use when changing prompts, orchestration, model routing, or framework behavior.
domains:
  - quality
capabilities:
  - analysis
  - verification
skill_type: procedure
keywords:
  - agent-evaluation
  - quality
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
# Agent evaluation

Define a representative task set with clear gold requirements, permitted tools, risk labels, and expected evidence. Run a controlled baseline and the candidate workflow under comparable conditions. Preserve prompts, model identifiers, tool traces, artifacts, test results, reviewer findings, cost, latency, and human interventions.

Measure task success, requirement coverage, defect rate, regression rate, rework, time to completion, token or API cost, reviewer agreement, false-confidence rate, and human correction time. Include adversarial, ambiguous, security-sensitive, and failure-recovery scenarios. Report confidence limits and cases where the evaluator itself is uncertain.

Do not optimize for a single score. A faster workflow that increases security defects or hidden human correction is not an improvement. Store scenarios and result schemas so future releases can reproduce comparisons.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
