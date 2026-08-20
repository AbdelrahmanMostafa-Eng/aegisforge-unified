---
id: platform.ai-system-engineering
name: ai-system-engineering
slug: ai-system-engineering
version: 0.1.0
status: experimental
summary: Design, implement, or review AI features with explicit model contracts, tool permissions, retrieval quality, privacy, evaluation, and failure handling. Use for LLM, RAG, agent, prompt, embedding, or multimodal systems.
description: Design, implement, or review AI features with explicit model contracts, tool permissions, retrieval quality, privacy, evaluation, and failure handling. Use for LLM, RAG, agent, prompt, embedding, or multimodal systems.
domains:
  - platform
capabilities:
  - analysis
  - execution
skill_type: procedure
keywords:
  - ai-system-engineering
  - platform
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
# AI-system engineering

Define the task contract, model inputs and outputs, structured schemas, allowed tools, trust boundaries, fallback behavior, latency and cost budgets, and data-retention rules. Treat model output as untrusted until validated. Constrain tool calls with least privilege, argument validation, timeouts, rate limits, and audit logs.

Evaluate normal, ambiguous, adversarial, multilingual, prompt-injection, data-leakage, tool-failure, and refusal cases. Measure groundedness or task correctness using an independent rubric, not only model self-evaluation. Test retrieval freshness, chunking, ranking, citation behavior, and access-control filtering for RAG systems.

Document model/version changes, prompt changes, evaluation deltas, rollback, and user-visible limitations. Never promise deterministic behavior when the system is probabilistic.

## When to Use

Use this skill when the request matches the declared capability and its risk boundaries.

## Verification

Confirm that the requested output exists, record assumptions, and report unresolved uncertainty before completion.
