# Getting Started

AegisForge is dependency-light and requires Python 3.11 or newer. The repository keeps the canonical skill catalog in the source tree while packaging the runtime and CLI as a normal Python project.

## Clone and install

```bash
git clone https://github.com/AbdelrahmanMostafa-Eng/aegisforge-unified.git
cd aegisforge-unified
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For contributor work, use an editable install:

```bash
python -m pip install --editable .
```

## Verify the installation

```bash
aegisforge --version
aegisforge doctor .
aegisforge validate .
aegisforge evaluate evaluation/scenarios.json
```

A healthy checkout should report no validation errors, a fresh registry, valid schemas, and a passing evaluation report.

## Use the control plane

Assess a request before acting:

```bash
aegisforge assess "Rotate the production API key and deploy the release"
```

Search for a capability:

```bash
aegisforge search "debug a failing Python test" --root . --human
```

Route a request and inspect rejected alternatives:

```bash
aegisforge route "create a safe research report with citations" --root . --human
```

Inspect one skill:

```bash
aegisforge inspect software-engineering.systematic-debugging --root .
```

## Add a skill

Create `skills/<domain>/<slug>/SKILL.md` with rich front matter, a focused `When to Use` section, a concrete procedure, verification criteria, and safety boundaries. Start with `status: experimental`. Then run:

```bash
aegisforge validate .
aegisforge index .
```

Promotion to `stable` requires scenario tests and review. See [`docs/skill-authoring.md`](skill-authoring.md), [`docs/testing.md`](testing.md), and [`AGENTS.md`](../AGENTS.md).
