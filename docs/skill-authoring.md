# Skill Authoring Guide

A skill is a bounded capability, not a general personality prompt. It should activate for a recognizable user intent, perform a useful procedure, and stop at a clear verification boundary.

## Front matter

Use the contract in [`schema/skill-frontmatter.schema.json`](../schema/skill-frontmatter.schema.json). Keep `summary` short enough for a registry result. Write `description` as a trigger condition: start with “Use when” or equivalent language and describe the problem, not the entire procedure.

## Progressive disclosure

Keep the frequently loaded `SKILL.md` concise. Put long API references, vendor flags, extensive examples, large schemas, and background material in `references/`. Link to those files from the procedure. An agent should be able to understand whether the skill applies without reading every reference.

## Skill anatomy

A strong skill answers these questions:

| Question | Required content |
|---|---|
| When does it apply? | Positive triggers and, where useful, anti-triggers. |
| What does it need? | Inputs, tools, permissions, credentials, and assumptions. |
| What does it do? | Ordered procedure with decision points. |
| What does it produce? | Output artifacts and expected format. |
| How is it checked? | Verification criteria and failure handling. |
| What must it not do? | Safety boundaries, side effects, and confirmation requirements. |
| What does it connect to? | Related skills and dependencies. |

## Promotion lifecycle

New skills begin as `draft` or `experimental`. Promote a skill to `stable` only after its triggers, procedure, outputs, verification, safety boundaries, and scenario tests have been reviewed. Deprecate a skill when a replacement exists or its source material is no longer reliable; do not silently delete historical IDs.

## Avoiding overlap

Search the registry before authoring. Use aliases and `related_skills` for synonyms. Keep the canonical skill focused on one capability, and create a workflow skill only when it coordinates multiple capabilities into a repeatable outcome.
