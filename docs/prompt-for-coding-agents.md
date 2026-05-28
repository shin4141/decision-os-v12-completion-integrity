# Prompt for Coding Agents

## Purpose

This prompt is for developers using Codex / Claude Code / Cursor-style coding agents who want the agent to stop before calling work done unless a V12 Completion Record exists and passes the gate.

## Copy-Paste Prompt

```text
You are working inside a repository that uses V12 Gate.

Before calling any task "done", you must create or update a Completion Record and run:

python tools/v12_gate.py check <completion-record.json>

Rules:

* Do not call the task done until the V12 Gate result is reported.
* Do not optimize the record for PASS.
* PASS means restartable closure, not proven correctness.
* DELAY and BLOCK are valid integrity-preserving outputs.
* Preserve evidence anchors.
* Preserve rollback or restart point.
* Preserve stop or recheck conditions.
* Preserve prohibited next actions.
* Preserve unresolved items and assumptions.
* Do not convert assumptions into facts.
* Do not delete uncertainty to make the record pass.
* Do not add scoring, weights, thresholds, decision-engine behavior, or AI autofill.

If V12 Gate returns PASS:

* Report the PASS result.
* Summarize what changed.
* Summarize the evidence anchor.
* Summarize rollback/restart point.
* Summarize remaining constraints, if any.

If V12 Gate returns DELAY:

* Do not call the task done.
* Report the missing or incomplete fields.
* State the next smallest fix needed.

If V12 Gate returns BLOCK:

* Do not call the task done.
* Stop.
* Report the BLOCK reason.
* Recommend rollback, re-anchoring, or owner review.

Do not modify files after reporting PASS / DELAY / BLOCK unless the user explicitly approves the next bounded change.
```

## When to Use This Prompt

- Before accepting AI-coded changes.
- Before handoff to another session.
- Before merging AI-generated work.
- Before summarizing a long coding session.

## What This Prompt Does Not Do

- It does not replace tests.
- It does not replace human review.
- It does not replace security review.
- It does not prove correctness.
- It does not make PASS the goal.

## Minimal Command Sequence

```bash
python tools/v12_gate.py init > completion_record.json
python tools/v12_gate.py check completion_record.json
```
