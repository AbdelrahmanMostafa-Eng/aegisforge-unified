---
id: research-and-intelligence.evidence-synthesis
name: Evidence Synthesis
slug: evidence-synthesis
version: 1.0.0
status: stable
summary: Combine reliable evidence into a transparent, balanced answer while separating facts, inferences, and uncertainty.
description: Use when answering a research question requires multiple sources, conflicting evidence, time-sensitive facts, or an auditable explanation.
domains:
  - research-and-intelligence
  - writing-and-publishing
capabilities:
  - research
  - source-evaluation
  - synthesis
  - citation
  - uncertainty-analysis
skill_type: workflow
keywords:
  - research
  - evidence
  - sources
  - citations
  - literature review
  - compare evidence
inputs:
  - research-question
  - source-material
  - audience
  - date-boundary
outputs:
  - evidence-matrix
  - synthesized-answer
  - citations
  - limitations
risk:
  level: low
  confirmation: never
compatible_harnesses:
  - generic
  - claude-code
  - codex
  - cursor
related_skills:
  - _core.task-framing
  - _core.verification-before-completion
quality:
  maturity: production
  test_status: scenario-tested
---
# Evidence Synthesis

## When to Use

Use when the answer should be grounded in external evidence rather than memory or a single unverified source.

## Procedure

1. Define the question, scope, audience, date boundary, and required evidence standard.
2. Decompose the question into claims that can be independently checked.
3. Gather primary sources where available, then use reputable secondary sources for context.
4. Record source identity, publication date, claim supported, method, limitations, and confidence.
5. Compare sources for agreement, contradiction, scope mismatch, and potential bias.
6. Synthesize only claims supported by the evidence; label inference explicitly.
7. Cite claims close to the relevant statement and include a reference list.
8. State unresolved uncertainty, missing evidence, and conditions under which the conclusion could change.

## Verification

Every important factual claim should have a traceable source or be clearly labeled as analysis. Check that citations actually support the surrounding statement, that dates are appropriate, and that a source has not been stretched beyond its population, method, or time period.

## Failure Handling

If sources conflict, preserve the conflict and explain why. If primary evidence is unavailable, say so. Do not manufacture precision, consensus, quotations, statistics, or source access.

## Safety and Boundaries

Research synthesis is not permission to make individualized medical, legal, financial, or other high-impact decisions. In sensitive domains, present information and uncertainty while directing the user toward an appropriately qualified decision-maker.
