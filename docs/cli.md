# CLI Reference

The `aegisforge` command is designed for both humans and automation. Existing discovery commands retain JSON as their default output for compatibility; add `--human` when readable terminal output is preferred. Commands return zero on success and non-zero when a requested validation or evaluation fails.

| Command | Purpose |
|---|---|
| `aegisforge assess <task>` | Classify risk, workflow, confirmation requirements, and required controls. |
| `aegisforge validate [path]` | Validate repository files, skill metadata, schemas, and generated-index freshness. |
| `aegisforge skills [path]` | List skills, optionally filtered by lifecycle status or domain. |
| `aegisforge search <query>` | Find matching skills and explain every positive match. |
| `aegisforge route <query>` | Select the smallest likely skill set and show rejected alternatives. |
| `aegisforge inspect <skill>` | Display a skill’s metadata and procedure. |
| `aegisforge evaluate [path]` | Run deterministic benchmark scenarios. |
| `aegisforge doctor [path]` | Diagnose Python, package import, validation, registry, and schema readiness. |
| `aegisforge index [path]` | Rebuild `registry/skills.json` and derived indexes. |
| `aegisforge evidence <path>` | Validate a structured evidence ledger, optionally requiring approval. |

## Automation examples

```bash
aegisforge assess --json "Delete customer records from the production database"
aegisforge validate . --json
aegisforge search "debug Python test" --root . --json
aegisforge route "deploy an authentication change" --root . --harness codex --json
aegisforge doctor . --json
aegisforge evaluate evaluation/scenarios.json --json
```

The `--json` output is stable enough for automation but should be treated as a versioned interface. The `--human` output is optimized for local review and may evolve without changing the underlying decision model.

## Compatibility aliases

The installed `skill` and `skill-md` commands point to the same unified CLI for compatibility with the original SKILL.md runtime. The canonical project command is `aegisforge`.
