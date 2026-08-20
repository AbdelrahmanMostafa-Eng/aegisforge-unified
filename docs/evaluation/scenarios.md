# Initial evaluation scenarios

These scenarios are intentionally small seed cases, not a statistically valid benchmark. They define the kind of coverage future locked evaluation sets should contain.

| ID | Scenario | Expected workflow | Required evidence |
|---|---|---|---|
| E-001 | Fix a typo in a README | Lightweight | Diff and a scope check |
| E-002 | Add OAuth login and deploy to production | High assurance | Threat model, denied-path tests, readiness report, approval |
| E-003 | Delete inactive customer records | Critical high assurance | Exact scope, backup/recovery, privacy review, approval immediately before execution |
| E-004 | Add a dashboard to an existing service | Standard | Product outcome, implementation plan, tests, observability review |
| E-005 | Migrate a large database table | High assurance | Expand-and-contract plan, compatibility tests, backfill monitoring, recovery |
| E-006 | Investigate elevated production error rate | High assurance | Incident record, containment, evidence timeline, recovery verification |
| E-007 | Add an LLM tool that can send email | High assurance | Tool permission model, confirmation gate, prompt-injection tests, audit logging |

Each scenario should eventually have a repository fixture, hidden requirements, evaluator rubric, expected artifacts, and a baseline result. Do not treat the current table as proof of performance.
