# Generic Adapter

The generic adapter exposes the canonical library through the `skill` CLI. It does not alter global configuration. A host can call:

```bash
skill search "user intent" --root /path/to/SKILL.md
skill route "user intent" --root /path/to/SKILL.md
skill explain skill-id --root /path/to/SKILL.md
```

The adapter contract is intentionally small:

1. Discover `skills/**/SKILL.md`.
2. Validate metadata and safety declarations.
3. Search or route by intent.
4. Load the selected file and its explicitly referenced material.
5. Preserve the skill's confirmation boundaries.

Native adapters should package the same canonical content and registry rather than fork skill text.
