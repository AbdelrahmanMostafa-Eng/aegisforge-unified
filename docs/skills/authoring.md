# Skill authoring guide

A skill is a focused, reusable decision procedure for a coding agent. It should make a recurring task safer or more reliable, not merely restate general advice. A skill must be narrow enough to trigger correctly and complete enough to guide action under uncertainty.

## Required structure

```text
skills/<family>/<skill-name>/SKILL.md
```

The file begins with frontmatter:

```yaml
---
name: kebab-case-name
description: What the skill does and when it should trigger.
---
```

The body should explain the purpose, decision procedure, constraints, evidence requirements, escalation conditions, and required output. Keep it under 500 lines. Put large examples or domain references in adjacent files and link them from the skill.

## Quality checklist

| Check | Question |
|---|---|
| Trigger | Would an agent know when to load this skill? |
| Scope | Is the skill focused rather than a grab bag? |
| Safety | Does it prevent secret leakage, permission escalation, and unsafe side effects? |
| Evidence | Does it say how to verify claims and label uncertainty? |
| Failure | Does it explain what to do when evidence is missing or the plan fails? |
| Human control | Does it identify decisions requiring an authorized human? |
| Interoperability | Does it avoid assumptions about one harness or vendor? |
| Maintainability | Is it concise, non-duplicative, and easy to review? |
| Testability | Can examples or evaluation scenarios detect regressions? |

Avoid absolute claims such as “this guarantees security” or “tests prove correctness.” State the control, its evidence, and its limitations. Prefer explicit outputs over vague instructions to “be careful.”
