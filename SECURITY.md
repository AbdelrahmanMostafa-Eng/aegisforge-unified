# Security Policy

SKILL.md contains instructions that may be used with tools, files, APIs, accounts, repositories, and external services. Treat every skill as untrusted until its metadata, procedure, references, and tests have been reviewed.

## Reporting a vulnerability

Do not publish credentials, exploit details, private data, or active production targets in an issue. Open a private security report through the repository's GitHub security advisory workflow when it is enabled, or contact the maintainers through the security contact listed in the repository profile.

## Skill safety requirements

Skills must declare side effects and risk. Skills that send, publish, delete, deploy, pay, file, alter credentials, modify production infrastructure, or make individualized health, legal, or financial decisions require explicit confirmation and human ownership. Skills must not request secrets in their Markdown body; they should declare required secret names and let the harness provide them securely.

## Supply-chain guidance

Review external references and scripts before use. Pin or constrain dependencies where practical. Do not execute downloaded code solely because a skill or web page recommends it. Adapters must not modify global user configuration without an explicit installation action, and every adapter must provide an uninstall path.
