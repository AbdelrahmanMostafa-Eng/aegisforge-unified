# Testing Skills

SKILL.md treats instruction quality as testable behavior. A skill can be tested at several levels.

## Structural tests

The validator checks front matter, required fields, semantic versioning, lowercase kebab-case slugs, canonical IDs, risk metadata, and compatibility declarations.

## Trigger tests

A positive scenario should activate the intended skill for a representative request. A negative scenario should remain inactive for a nearby but different request. Include explicit requests and natural-language requests when the skill will be discovered implicitly.

## Procedure tests

Procedure tests use controlled fixtures to confirm that the skill produces the expected artifact or decision. They should state what is observable without requiring a particular model's exact wording.

## Safety tests

Test that drafting is not treated as sending, analysis is not treated as execution, and high-impact actions request confirmation. Include ambiguous requests, changed targets, missing credentials, and partial failures.

## Regression tests

When a skill is changed, preserve scenarios that previously exposed a defect. Registry changes should be rebuilt and reviewed rather than hand-edited.

Run the baseline suite with:

```bash
PYTHONPATH=. python3 -m aegisforge validate .
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## Current executable checks

Run the full local quality gate with:

```bash
make check
python3 -m compileall -q aegisforge tools
python3 -m pip wheel --no-deps . --wheel-dir dist
```

The unified suite covers policy decisions, negative parser cases, registry discovery, routing, CLI compatibility, governance state transitions, evidence-ledger completeness, and deterministic evaluation scenarios. `aegisforge doctor . --json` provides a machine-readable readiness summary.

A clean-room installation should be tested in a fresh virtual environment:

```bash
python3 -m venv /tmp/aegisforge-clean
/tmp/aegisforge-clean/bin/python -m pip install .
/tmp/aegisforge-clean/bin/aegisforge --version
/tmp/aegisforge-clean/bin/aegisforge doctor . --json
```
