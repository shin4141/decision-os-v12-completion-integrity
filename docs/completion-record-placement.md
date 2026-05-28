# Completion Record Placement

## Purpose

V12 Gate becomes more useful when Completion Records have a predictable location inside a repository. This is a placement convention only, not a schema change or workflow enforcement.

## Recommended Default

Use:

```text
.v12/completion_record.json
```

for the current active task or current handoff.

## Alternative for Multiple Records

Use:

```text
.v12/completion_records/<task-name>.json
```

or:

```text
.v12/completion_records/YYYY-MM-DD-<task-name>.json
```

## When to Create or Update a Record

- Before accepting an AI coding agent's "done".
- Before handing work to another session.
- Before tagging or releasing.
- Before merging AI-generated work.
- When the human feels the task has become heavy or hard to restart.

## Minimal Command Sequence

```bash
mkdir -p .v12
python tools/v12_gate.py init > .v12/completion_record.json
python tools/v12_gate.py check .v12/completion_record.json
```

## Important Boundaries

- Do not treat the placement convention as automatic completion.
- Do not optimize the record toward PASS.
- A blank starter record may return DELAY.
- PASS means restartable closure, not proven correctness.
- DELAY and BLOCK are valid outcomes.
- Placement does not replace tests, review, or security checks.

## Recommended AI Coding Agent Instruction

Before calling work done, update `.v12/completion_record.json` and run:

```bash
python tools/v12_gate.py check .v12/completion_record.json
```

If the result is DELAY or BLOCK, do not call the task done.
