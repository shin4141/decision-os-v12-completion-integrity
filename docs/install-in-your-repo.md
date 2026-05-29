# Install V12 Gate in Your Repository

## Purpose

This guide shows the minimal way to copy V12 Gate into another repository. V12 Gate checks whether an update is closed in a future-restartable form: not whether it is correct, but whether the future self can reconnect, verify, stop, and re-anchor it.

This file is the external adoption and install guide.

## Minimal Files to Copy

Copy these files into the target repository:

- `tools/v12_gate.py`
- `tools/validate_completion_record.py`
- `completion_record.schema.json`

Optional docs to copy:

- `docs/prompt-for-coding-agents.md`
- `docs/completion-record-placement.md`
- `docs/github-actions-template.md`

## Recommended Repository Layout

```text
your-repo/
  tools/
    v12_gate.py
    validate_completion_record.py
  completion_record.schema.json
  .v12/
    completion_record.json
  .github/
    workflows/
      v12-gate.yml
```

## Step 1: Create a Completion Record

```bash
mkdir -p .v12
python tools/v12_gate.py init > .v12/completion_record.json
```

This file is not a config file. It is a control handoff record: the minimum information the future self needs to restart the work safely.

## Step 2: Ask the Coding Agent to Fill It

Use `docs/prompt-for-coding-agents.md`, or give the coding agent this short instruction:

Before calling the task done, update `.v12/completion_record.json` and run:

```bash
python tools/v12_gate.py check .v12/completion_record.json
```

If V12 Gate returns DELAY or BLOCK, do not call the task done.

## Step 3: Check It Locally

```bash
python tools/v12_gate.py check .v12/completion_record.json
```

- PASS means restartable closure, not proven correctness.
- DELAY means missing restart handles should be repaired.
- BLOCK means do not accept closure.

## Step 4: Add GitHub Actions

Use `docs/github-actions-template.md` for a safe check-only workflow template.

## Boundaries

- V12 Gate does not replace tests.
- V12 Gate does not replace code review.
- V12 Gate does not replace security review.
- V12 Gate does not auto-fill records.
- V12 Gate is not a scoring system.
- V12 Gate is not for forcing PASS.
- DELAY and BLOCK are integrity-preserving outputs. They are not failures; they prevent False Completion from being passed forward.

## Recommended First Test

If you are testing inside the V12 Gate repository, run:

```bash
python tools/v12_gate.py check examples/block.public_missing_rollback.json
```

If you are testing inside your own repository, create an intentionally incomplete `.v12/completion_record.json` and confirm it returns DELAY.
