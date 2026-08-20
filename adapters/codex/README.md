# Codex Adapter

This adapter packages the canonical skills for Codex-compatible skill discovery. It should prefer the harness's native skill mechanism and avoid adding a redundant session hook when native discovery already provides the required context.

Packaging must preserve IDs, metadata, references, and safety boundaries. Adapter tests should verify installation, discovery, loading, and clean removal in an isolated fixture.
