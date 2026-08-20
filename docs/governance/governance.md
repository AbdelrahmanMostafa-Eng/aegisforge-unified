# Governance and autonomy

AegisForge is designed for **bounded autonomy**. The agent may explore, draft, test, and make reversible local changes without interrupting the user unnecessarily. It must pause before actions whose consequences extend beyond the isolated workspace or whose risk cannot be independently verified.

## Approval matrix

| Action | Default approval | Required evidence |
|---|---|---|
| Read local source and run safe tests | No additional approval | Command and result in evidence ledger |
| Edit files in an isolated branch | No additional approval | Diff, tests, and scope check |
| Add a dependency | Review required | Purpose, license, audit, lockfile change |
| Change authentication or authorization | Human approval | Threat model, denied-path tests, reviewer sign-off |
| Handle secrets or personal data | Human approval | Redaction plan, access boundary, retention decision |
| Modify persistent data or schema | Human approval | Migration plan, backup/recovery, compatibility tests |
| Deploy or publish externally | Human approval | Release readiness, smoke test, rollback |
| Delete, revoke, transfer, or purchase | Explicit confirmation immediately before action | Exact scope, consequence, recovery, approval record |

## Evidence states

Every requirement and control should be marked **verified**, **partially verified**, **unverified**, **blocked**, or **not applicable**. The agent must explain the limitation of evidence. Passing tests do not prove untested behavior, and a reviewer’s confidence does not replace an independent check where the impact is high.

## Escalation rules

Escalate when the user’s intent is ambiguous in a way that changes the result, when a permission boundary is unclear, when an irreversible action lacks recovery, when security or privacy impact is unresolved, when reviewers disagree on a load-bearing decision, or when the plan has no evidence-based path forward.

## Human responsibility

AegisForge does not transfer accountability to a model. Human owners remain responsible for product decisions, legal and regulatory interpretations, access approvals, production changes, and acceptance of residual risk. The framework exists to make those decisions more explicit and better evidenced.
