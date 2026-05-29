# Security Policy

## Supported Version

Security and boundary reports should target current `main` and the latest release.

## Reporting

Do not post private user data, secrets, tokens, exploit details, or sensitive workflow information in public issues.

For security-sensitive concerns, use a private reporting channel if one is available. If no private channel is available, open a minimal public issue without sensitive details.

Non-sensitive misuse or boundary concerns should use the existing "Boundary / misuse concern" issue template.

## Scope

V12 Gate does not execute user code.

V12 Gate does not replace security review, code review, tests, or CI.

V12 Gate checks restartable handoff structure, not correctness or security.

Reports about scoring, AI autofill, PR comment automation, write-permission workflows, or PASS optimization should be treated as boundary concerns.
