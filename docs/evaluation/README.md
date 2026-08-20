# AegisForge evaluation

AegisForge should be judged by outcomes, not by the number of skills or the confidence of its prompts. Evaluation compares a baseline workflow with the candidate workflow on representative tasks under comparable model, tool, repository, and time conditions.

## Evaluation dimensions

| Dimension | Example measure |
|---|---|
| Task success | Requirements satisfied and accepted by a human or gold evaluator |
| Correctness | Defects, regressions, and hidden-test performance |
| Safety | Security findings, permission violations, data leakage, unsafe side effects |
| Delivery | Time to completion, rework, review cycles, and human correction time |
| Efficiency | Model calls, tokens, cost, latency, and unnecessary exploration |
| Maintainability | Review findings, complexity, documentation, test quality, and future change cost |
| Product value | User acceptance, success metric movement, and guardrail metrics |
| Reliability | Recovery quality, reproducibility, and performance across repeated runs |

## Scenario design

Each scenario should include a task statement, repository snapshot, risk classification, permitted tools, hidden requirements, expected evidence, evaluator rubric, and stop conditions. Include ordinary, ambiguous, adversarial, security-sensitive, production-like, and failure-recovery scenarios. Keep a locked evaluation set separate from the examples used to tune prompts.

## Reporting

Report the baseline, candidate, model and version, harness, run count, failures, cost, latency, human interventions, reviewer disagreement, confidence limitations, and representative examples. A result that improves speed while increasing unsafe changes is a regression, not a win.

## Anti-gaming rules

Do not tune the workflow against the locked test set. Do not count generated plans or tests as success without checking behavior. Do not permit the evaluator to reward unsupported certainty. Preserve failed runs and negative findings so the project learns from them.

## Repository benchmark

The repository includes a small deterministic regression suite at `evaluation/scenarios.json`. It covers safe documentation, ambiguity, dependency changes, authentication, migrations, production deployment, secret handling, external side effects, and destructive production actions.

Run it with:

```bash
aegisforge evaluate evaluation/scenarios.json
aegisforge evaluate evaluation/scenarios.json --json
```

The fixture tests the control-plane boundary only. It does not claim to measure model quality, end-to-end software delivery, or domain expertise. Larger locked suites should be added as the project gains reviewed scenarios.
