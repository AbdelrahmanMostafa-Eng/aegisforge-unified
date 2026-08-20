# Cross-harness adapter contract

AegisForge skills are portable instructions, but each coding-agent harness exposes different names, hooks, context limits, permissions, and tool semantics. An adapter translates those differences without weakening the framework’s core contract.

## Adapter responsibilities

An adapter must load the bootstrap before implementation, expose skill discovery, map safe read and write operations, preserve evidence artifacts, surface approval gates, and report tool failures without hiding them. It should support a clean-session acceptance test and a minimal degraded mode when optional features are unavailable.

## Adapter metadata

Each adapter should document the harness name and version range, installation method, bootstrap file, skill search paths, tool mapping, permission model, context limits, subagent support, approval mechanism, evidence location, and known limitations.

## Safety rules

Adapters must not silently auto-approve destructive or externally visible operations. They must not place secrets into context merely because the harness can access them. They must preserve the distinction between a dry run and a side effect, and they must make blocked or unverified states visible to the user.

## Compatibility test

A compatible adapter must pass the following scenario in a clean project: intake a deliberately ambiguous feature, classify risk, load a relevant skill, produce a plan with acceptance criteria, refuse an unapproved destructive action, run verification, and emit an evidence ledger with limitations.
