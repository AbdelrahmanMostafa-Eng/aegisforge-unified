# AegisForge skill catalog

AegisForge skills are modular procedures loaded progressively by task and risk. The current foundation includes the following families.

| Family | Skills | Typical trigger |
|---|---|---|
| Core | `task-intake`, `risk-assessment`, `context-and-evidence`, `human-approval` | Any non-trivial request, handoff, or side-effecting action |
| Engineering | `architecture`, `implementation-planning`, `testing-strategy`, `data-migration` | Features, integrations, refactors, tests, or persistent-data changes |
| Security | `threat-modeling`, `secrets-and-supply-chain`, `identity-and-privacy` | Identity, secrets, internet-facing, dependency, privacy, or regulated work |
| Product | `product-discovery`, `acceptance-and-ux` | User-facing work or requests without measurable outcomes |
| Quality | `independent-review`, `agent-evaluation` | Pre-merge review, workflow changes, or framework releases |
| Operations | `production-readiness`, `incident-response`, `delivery-pipeline` | Deployment, release, incident, CI/CD, or day-two operations |
| Platform | `ai-system-engineering`, `observability` | LLM systems, tools, services, telemetry, or production diagnosis |

Each skill is intentionally concise. Load adjacent references only when required, and preserve the skill’s evidence and escalation requirements when adapting it to another harness.

## Planned families

The next skill packs should cover contract and API design, frontend and mobile testing, accessibility automation, performance engineering, infrastructure as code, container hardening, backup and disaster recovery, finance and healthcare controls, data science reproducibility, legal-document workflows, cost optimization, change management, and community operations.
