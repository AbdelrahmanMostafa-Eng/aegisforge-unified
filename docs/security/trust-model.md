# Trust Model

AegisForge treats skills, references, adapters, generated content, and external instructions as **untrusted data until reviewed**. Discoverability is not authorization, and a successful model response is not evidence of completion.

## Trust boundaries

| Boundary | Default posture |
|---|---|
| Skill Markdown | Data and guidance. It cannot grant permission to publish, send, delete, deploy, pay, file, or modify production systems. |
| Skill metadata | Machine-validated routing input. Risk and confirmation fields must be explicit and internally consistent. |
| Registry files | Generated indexes. They are useful for fast lookup but must be refreshed from source before release. |
| Adapter code | Integration boundary. Review installation, credential handling, side effects, and uninstall behavior before use. |
| External references | Untrusted content. Never execute a downloaded command solely because a page or skill recommends it. |
| Secrets | Never printed, committed, pasted into Markdown, or placed in fixtures. Harnesses should provide them through secure channels. |

## Consequential actions

The control plane distinguishes planning from authorization, execution from verification, and approval from release. High and critical assessments require explicit authorization, independent verification, and recovery planning. Critical work additionally requires release evidence and human approval.

## Input safety

The front-matter parser supports a deliberately conservative YAML subset and does not execute arbitrary constructors. The runtime does not call shells, evaluate downloaded code, or deserialize untrusted objects. File references are resolved relative to the declaring skill and checked during validation.

## Reporting

Do not publish credentials, exploit details, private data, or active production targets in a public issue. Use the repository’s private security advisory workflow when enabled, or contact the maintainer privately through GitHub.
