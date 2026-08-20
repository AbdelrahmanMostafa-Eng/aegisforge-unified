# Unified Runtime Architecture

AegisForge is organized as a layered control plane rather than a single monolithic prompt collection. Each layer has a narrow responsibility and can be tested independently.

## Runtime layers

| Layer | Responsibility | Primary location |
|---|---|---|
| Policy | Classify task risk and select a proportionate workflow. | `aegisforge/policy.py` |
| Contract | Parse and validate structured skill metadata. | `aegisforge/skilllib/frontmatter.py` and `registry.py` |
| Discovery | Find skill packages, detect duplicate IDs, and produce records. | `aegisforge/skilllib/registry.py` |
| Retrieval | Search skill metadata and explain why a result matched. | `aegisforge/skilllib/router.py` |
| Routing | Prefer the smallest useful set, stable status, and lower risk. | `aegisforge/skilllib/router.py` |
| Governance | Define approval, evidence, threat-model, and release expectations. | `AGENTS.md`, `templates/`, and `docs/governance/` |
| Integration | Expose one CLI and generated indexes for humans and harnesses. | `aegisforge/cli.py`, `registry/`, and `adapters/` |

## Request flow

```text
Natural-language request
        |
        v
  Risk assessment  ------->  Workflow mode and required controls
        |
        v
  Skill search  ----------->  Explainable candidate matches
        |
        v
  Conservative routing ---->  Smallest likely skill set
        |
        v
  Human/tool execution ---->  Evidence, verification, and release decision
```

Risk assessment and skill routing are intentionally separate. A search result identifies a capability; it does not grant permission to perform a side effect. A routed skill must still be constrained by its declared risk metadata, the project bootstrap rules, and explicit user confirmation when required.

## Lifecycle and generated content

The catalog generator creates discoverable experimental scaffolds from the canonical inventory. Generated entries are useful for coverage and discovery, but they are not treated as expert procedures. Promotion to `stable` requires a specific procedure, verification criteria, safety boundaries, and positive and negative scenarios.

## Extension boundary

New routing strategies should preserve the observable search and route interfaces. New adapters should consume the registry contract and preserve installation, discovery, loading, confirmation, and uninstall semantics. New policy signals should include deterministic tests and documented limitations because keyword heuristics are a first-pass control, not a substitute for domain review.
