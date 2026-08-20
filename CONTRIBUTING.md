# Contributing to AegisForge

Thank you for helping improve AegisForge. Contributions should make software-engineering agents more reliable, safer, more useful, or easier to evaluate. Prefer focused changes with clear evidence over large collections of speculative instructions.

## Before contributing

Read the [README](README.md), [AGENTS.md](AGENTS.md), and relevant skill files. Check whether the proposed capability already exists. If it is a new skill, define its trigger, scope, risk level, outputs, and references before writing the body.

## Skill standards

Every skill must have a concise `SKILL.md` with valid frontmatter containing `name` and `description`. The description must explain both what the skill does and when it should trigger. Keep the body under 500 lines and use progressive disclosure for large references. Avoid duplicating information between the skill and its references.

Skills should state assumptions, escalation conditions, evidence requirements, and failure handling. They must not encourage secret disclosure, unsafe execution, silent permission escalation, or unsupported claims. Domain-specific guidance should identify where qualified human review is required.

## Code standards

The reference CLI uses Python 3.11 and the standard library by default. Keep policy decisions deterministic and explainable. Add tests for new behavior, especially risk classification, validation, parsing, and failure cases. Do not add dependencies unless they have a clear need, a compatible license, and a documented supply-chain review.

## Pull requests

A pull request should explain the user problem, scope, non-goals, risk level, implementation, evidence, limitations, and follow-up work. Run the following commands before submitting:

```bash
python -m aegisforge validate .
python -m unittest discover -s tests -v
```

For changes to workflow behavior, add or update an evaluation scenario in `docs/evaluation/`. For high-risk changes, include a threat model or explain why it is not applicable. Do not include secrets, proprietary data, or generated artifacts that cannot be redistributed.

Maintainers may request a narrower change, independent verification, documentation improvements, or a rollback plan before merging.
