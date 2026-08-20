# Control Plane Concept

AegisForge is not a generic prompt collection. It is a control plane for agent work: it helps an agent understand what a request means, how risky it is, which capability is appropriate, what evidence is required, and whether the work may move to the next governance state.

```text
Request
  |
  v
Policy assessment ──> risk level, workflow, required controls
  |
  v
Skill registry ────> validated capabilities and compatibility
  |
  v
Explainable route ─> selected skills and rejected alternatives
  |
  v
Governance state ──> planned → authorized → executed → verified → approved → released
  |
  v
Evidence ledger ──> observable checks, outcomes, uncertainty, approval, verifier
  |
  v
Adapters / agents
```

The boundaries are intentionally explicit. A skill may explain how to perform work, but its Markdown cannot authorize a consequential action. A route may select a skill, but it cannot bypass approval. Evidence may demonstrate a check, but it cannot turn a failed check into success.
