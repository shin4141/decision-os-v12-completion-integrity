# Auto-Handoff Gate with Dynamic Workflow Artifacts

## Purpose

This note explains how to use V12 Auto-Handoff Gate as a post-run / pre-done audit for long-running Codex or skill-based agent workflows.

The intended use is simple: before declaring a workflow done, write or update a final report, handoff note, integration checklist, or completion note, then run that text through Auto-Handoff Gate. The gate checks whether enough restart handles are visible for the next human or agent to resume the work.

## What this is not

This is not:

- direct `/dynamic` integration
- direct `/goal` integration
- a subagent runner
- a code quality checker
- a security scanner
- an autonomous approval system
- a CI/CD replacement

V12 does not control dynamic workflows or run subagents. It only audits whether the workflow has left enough restart information before the final answer.

## Workflow artifact model

Some skill-based dynamic workflows use local workflow artifacts such as:

```text
.workflow/<slug>/plan.md
.workflow/<slug>/state.json
.workflow/<slug>/orchestration.md
.workflow/<slug>/packets/
.workflow/<slug>/results/
.workflow/<slug>/final-report.md
```

These are external workflow artifacts and may vary by implementation. Auto-Handoff Gate does not require this exact structure. It only needs a text file that summarizes the workflow state clearly enough to audit for restart handles.

Good candidate inputs include:

- `.workflow/<slug>/final-report.md`
- an integration checklist
- a handoff note
- a final agent completion note

## Best insertion points

Auto-Handoff Gate fits best at workflow boundaries where context may be lost:

- before final "done"
- after result aggregation
- before final report acceptance
- after multiple sub-agent / packet results are merged
- when verification is missing
- when rollback is unclear
- when the workflow becomes hard to resume

The strongest default insertion point is before the parent agent declares the workflow complete.

## Recommended MVP pattern

1. Write or update a final report or handoff note.
2. Run Auto-Handoff Gate against it:

```bash
python tools/auto_handoff_gate.py .workflow/<slug>/final-report.md
```

3. Respond to the returned stage:

- `CONTINUE`: continue while keeping restart handles visible.
- `PREPARE_HANDOFF`: checkpoint before continuing.
- `HANDOFF_NOW`: stop and write a V12 Completion Record before continuing.

This pattern keeps V12 at the completion-discipline layer. It does not make V12 responsible for judging implementation quality or approving the workflow.

## Sample handoff note fields

A useful handoff note should cover:

- what changed
- what was not touched
- unresolved items
- evidence anchors
- verification
- rollback
- next step
- next agent must not change

The details should be concrete enough that the next human or agent can restart without reconstructing the whole session from scratch.

## Sample prompt for Codex / skill workflows

```text
Before declaring this workflow done, write a final-report / handoff note and run it through V12 Auto-Handoff Gate. If the gate returns HANDOFF_NOW, do not continue until a V12-style Completion Record is written.
```

## Why this matters

Dynamic workflows and subagents can accelerate work, but acceleration also increases the risk that restart handles are lost.

V12 does not slow the workflow for its own sake. It marks the handoff boundary before completion becomes unrestartable.

## Non-goals and boundaries

V12 does not approve code.

V12 does not prove correctness.

V12 does not replace tests.

V12 only checks whether the workflow leaves enough restart information for the next human or agent.
