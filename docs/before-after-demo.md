# Before / After Demo

## Purpose

V12 Gate makes the hidden failure in AI-generated "done" visible before the work is accepted as complete.

```text
AI: Done.
V12 Gate: DELAY.
Reason: evidence / rollback / stop condition missing.
Result: Do not accept completion yet.
```

## Before: AI says done

An AI coding agent says:

```text
"Done. I updated the workflow and everything should be ready."
```

But the handoff is missing:

- evidence anchor
- rollback or restart point
- stop/recheck condition
- unresolved assumptions
- prohibited next actions

This may look complete, but the next human, AI session, or coding agent cannot safely restart.

## After: V12 Gate checks the Completion Record

Run:

```bash
python tools/v12_gate.py check .v12/completion_record.json
```

Example output:

```text
V12 Gate: DELAY

WARNINGS:
- empty required fields detected: evidence_anchor, stop_condition, next_self_should_not
- empty critical fields detected: evidence_anchor, stop_condition, next_self_should_not
```

DELAY does not mean the work failed. It means the work should not be accepted as complete until the missing restart handles are restored.

## PR-comment-style example

This is a static example only. It does not implement PR comments.

```text
V12 Gate: DELAY

Do not accept completion yet.

Missing restart handles:
- evidence_anchor
- stop_condition
- next_self_should_not

Next smallest fix:
Update .v12/completion_record.json with evidence, stop/recheck conditions, and prohibited next actions.
```

## PASS example

```text
V12 Gate: PASS

Restartable closure accepted.
PASS is not a truth guarantee.
```

PASS means the record is restartable enough to close. It does not prove the code is correct.

## What This Demo Is Not

- This is not PR comment automation.
- This is not a code review.
- This is not a correctness proof.
- This is not a scoring system.
- This is a restartability gate.
