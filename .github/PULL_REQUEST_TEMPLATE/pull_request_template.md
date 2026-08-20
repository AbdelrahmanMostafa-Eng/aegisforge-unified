## Summary

Describe the change and the user or maintainer problem it solves.

## Scope

State what is included and what is intentionally not included.

## Risk and safety review

Explain whether the change affects secrets, permissions, external side effects, irreversible actions, production workflows, or high-impact domains.

## Evidence

List the commands, tests, fixtures, or manual checks used to verify the change.

```text
# Example:
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m aegisforge validate .
```

## Documentation

- [ ] README or relevant documentation updated.
- [ ] Changelog updated when user-visible behavior changed.
- [ ] New skills include verification and safety boundaries.
- [ ] No secrets or sensitive data are included.

## Reviewer notes

Call out assumptions, limitations, follow-up work, or areas requiring independent review.
