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

## Release verification

The complete release gate is:

```bash
python -m unittest discover -s tests -v
python -m aegisforge validate . --json
python -m aegisforge doctor . --json
python -m aegisforge evaluate evaluation/scenarios.json --json
python -m aegisforge index .
git diff --exit-code -- registry/
python -m build
python -m pip check
python -m pip install pip-audit
python -m pip_audit --local
```

For packaging verification, install the generated wheel and a fresh source checkout into separate virtual environments, then run `aegisforge --version`, `aegisforge assess ... --json`, and `aegisforge doctor . --json`. The release-ready GitHub workflows repeat these checks on Python 3.11 and 3.12 and add repository secret-hygiene checks; they require workflow-write permission to activate.
