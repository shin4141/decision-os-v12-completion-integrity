# AI Coding Workflow with V12 Gate

## Purpose

Use V12 Gate before an AI coding agent calls work "done." The gate checks whether the next human, AI session, or coding agent can safely restart from the Completion Record.

## Minimal Workflow

- Start a bounded task.
- Keep Mission / Base / Keep / Rollback / Verify visible.
- Let the coding agent make the bounded change.
- Before accepting "done," create or update a Completion Record.
- Run `python tools/v12_gate.py check <completion-record.json>`.
- If PASS: closure may be accepted as restartable, not proven correct.
- If DELAY: do not claim completion yet; fill missing evidence, stop conditions, rollback or restart point, or prohibited next actions.
- If BLOCK: do not accept closure; restore control or rollback.

## Prompt to Give a Coding Agent

```text
Use V12 Gate before calling this task done.

Do not call the task done until a Completion Record exists.
Preserve evidence anchors.
Preserve rollback or restart point.
Preserve stop or recheck conditions.
Preserve prohibited next actions.
Do not optimize for PASS.

Run:
python tools/v12_gate.py check <completion-record.json>

Report the PASS / DELAY / BLOCK result from V12 Gate.
If the result is DELAY or BLOCK, report the missing fields and stop.
```

## Example Commands

```bash
python tools/v12_gate.py init > completion_record.json
python tools/v12_gate.py check completion_record.json
python tools/v12_gate.py check examples/delay.missing_stop_conditions.json
python tools/v12_gate.py check examples/block.public_missing_rollback.json
```

## Non-Goals

- V12 Gate is not a code reviewer.
- It is not a correctness proof.
- It is not a scoring system.
- It does not auto-fill records.
- It does not replace tests, human review, or security review.

## Recommended First Use

Start by checking the DELAY and BLOCK examples first. They show what V12 Gate is designed to prevent.
