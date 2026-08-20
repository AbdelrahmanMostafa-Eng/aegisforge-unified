# Architecture

SKILL.md is organized as a **content layer plus a control layer**. The content layer contains canonical skills and references. The control layer indexes, validates, routes, packages, and audits those skills.

## Request lifecycle

```text
user request
    ↓
task framing and risk extraction
    ↓
registry search and alias expansion
    ↓
compatibility, dependency, and conflict filtering
    ↓
explainable ranking
    ↓
foundation + selected skill loading
    ↓
execution or confirmation gate
    ↓
verification and completion report
```

The first implementation uses deterministic keyword search so it remains predictable and dependency-free. Semantic retrieval can be added later as an optional index, but it must preserve explainability and must never bypass risk metadata or compatibility constraints.

## Canonical source of truth

A skill's canonical source is its directory under `skills/`. `registry/skills.json` is generated and should not be hand-edited. Adapters package canonical content for the target harness; they should not fork or silently rewrite the skill body.

## Progressive disclosure

The registry contains enough metadata to decide whether a skill is relevant. The runtime loads the full `SKILL.md` only after selection and follows only explicit references. This keeps the default context small even as the repository grows to tens of thousands of skills.

## Catalog generation

`tools/generate_catalog.py` converts the current inventory in `catalog/file-names.md` into experimental packages. This preserves a broad map of intended coverage while making the quality state visible. A generated scaffold is not considered production guidance until a contributor specializes and tests it.

## Extending the runtime

New routing strategies should implement the same observable interface as `skill search` and `skill route`. New adapters should consume the registry contract and provide installation, discovery, loading, confirmation preservation, and uninstall behavior. Every new runtime feature requires unit tests and at least one integration fixture.
