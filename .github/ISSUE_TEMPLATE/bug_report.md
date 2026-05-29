---
name: Bug report
about: Report validator, CLI, schema, or docs behavior that appears incorrect.
title: "[Bug] "
labels: bug
assignees: ""
---

## What happened?

Describe the behavior that appears incorrect.

## Where did it happen?

- Validator
- CLI
- Schema
- Docs
- Examples
- Other:

## Expected behavior

What did you expect V12 Gate to do?

## Actual behavior

What did V12 Gate do instead?

## Reproduction

```bash
python tools/v12_gate.py check <record.json>
```

## Boundary check

- PASS is not a truth guarantee.
- DELAY and BLOCK are valid integrity-preserving outputs.
- This issue is not asking V12 Gate to become a correctness checker, code reviewer, scoring system, or CI replacement.
