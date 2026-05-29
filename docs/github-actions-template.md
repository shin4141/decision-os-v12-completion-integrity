# GitHub Actions Template for External Repositories

## Purpose

Use this template when you want your own repository to check a V12 Completion Record before accepting AI-generated work as done.

This template is check-only. It does not comment on PRs, does not write to the repository, and does not block merges by itself unless the repository owner chooses to make the check required.

This file defines the check-only CI template only.

## Expected Record Location

Default:

```text
.v12/completion_record.json
```

## Minimal Workflow Template

```yaml
name: V12 Gate

on:
  pull_request:
  push:

jobs:
  v12-gate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Check V12 Completion Record
        run: |
          python tools/v12_gate.py check .v12/completion_record.json
```

## How to Use

1. Copy V12 Gate files into the target repo:

   - `tools/v12_gate.py`
   - `tools/validate_completion_record.py`
   - `completion_record.schema.json`

2. Add `.v12/completion_record.json`.
3. Add the workflow file as `.github/workflows/v12-gate.yml`.
4. Run the workflow.
5. Treat DELAY/BLOCK as a signal to finish the record, not as a system failure.

## Important Boundaries

- This template does not auto-fill records.
- This template does not prove code correctness.
- This template does not replace tests, code review, or security review.
- This template does not comment on PRs.
- This template does not require write permissions.
- This template does not use `pull_request_target`.
- PASS means restartable closure, not proven correctness.
- DELAY and BLOCK are valid integrity-preserving outputs.

## Optional Required Check

If repository owners want V12 Gate to block merges, they may configure this workflow as a required status check in GitHub branch protection. Do not add automated write/comment behavior in this template.
