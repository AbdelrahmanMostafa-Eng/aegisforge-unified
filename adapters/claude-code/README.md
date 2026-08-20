# Claude Code Adapter

This adapter is a packaging target for the canonical SKILL.md library. It should expose `skills/` through the harness-supported plugin or project mechanism and include the foundation bootstrap only through the documented installation surface.

The adapter must preserve canonical paths, skill IDs, metadata, and confirmation policies. It must be tested in a clean temporary project and must provide a reversible uninstall path. The adapter should be generated from the canonical registry rather than maintained as a second hand-written skill collection.
