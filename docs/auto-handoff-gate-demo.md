# Auto-Handoff Gate Demo

For long-running Codex or agentic workflows, "keep going" can become less safe than pausing to create a restartable completion record.

## What This Demo Is

This is a static operating pattern, not a tool.

It demonstrates when a long-running AI coding workflow should pause and write a V12-style Completion Record before restart handles are lost.

## Why This Matters

Dynamic workflows and sub-agents can run longer than ordinary one-task sessions.

Longer runs increase the chance that restart handles are lost:

- what changed
- what was not touched
- unresolved items
- evidence or verification
- rollback path
- next step
- what the next agent must not change

Summaries are not necessarily handoffs. A workflow can appear productive while becoming hard for the next human, AI session, or coding agent to resume.

## Trigger Moments

Pause and create a handoff boundary when:

- the task has grown beyond the original scope
- multiple sub-agents produced partial outputs
- many files were changed
- verification is incomplete
- rollback is unclear
- the next step depends on unstated assumptions
- the agent is about to say "done" without evidence anchors
- continuing would make the state harder to summarize or restart

## Bad Pattern

```text
Done. I implemented the feature and cleaned up the code.
```

This is not restartable because it leaves out:

- changed file list
- untouched scope
- verification evidence
- rollback path
- unresolved items
- next-agent constraints

The message sounds complete, but the next agent cannot safely reconnect to the work.

## V12 Auto-Handoff Boundary

Instead of continuing or claiming done, the agent pauses and emits:

```text
Completion state: DELAY
Reason: restart handles are missing.
Action: write a Completion Record before continuing.
```

This preserves Completion Integrity. DELAY is not failure; it is a signal that the handoff is not restartable enough yet.

## Good Pattern

```text
Completion state: DELAY

what_changed:
- Added the first implementation pass for the feature.
- Updated the local wiring needed for the feature to run.

what_was_not_touched:
- Did not change public API contracts.
- Did not change deployment or permissions.

unresolved_items:
- Edge-case behavior still needs owner review.
- One integration path has not been verified.

evidence_anchors:
- Local diff
- Test command output
- Relevant file paths

verification:
- Unit tests passed locally.
- Manual smoke check not yet complete.

rollback:
- Revert this feature commit or restore the pre-change branch.

next_step:
- Run the missing smoke check and resolve the owner-review question.

next_self_should_not:
- Do not widen scope into unrelated refactors.
- Do not change public API contracts without a new mission.
```

This is a V12-style handoff shape. It is not a full schema replacement; it is a compact demo of the restart handles the next agent needs.

## Boundary / Non-Goals

This demo does not approve code.

It does not prove correctness.

It does not replace tests.

It does not decide whether a PR should merge.

It does not add automation, scoring, PR comments, CI/CD replacement behavior, or autonomous approval.

It only demonstrates when a long-running workflow should create restartable handoff information.

## Suggested Prompt

```text
When this task becomes long-running, before saying done, pause and apply V12 Completion Integrity.

If restart handles are missing, output DELAY and write a Completion Record with what_changed, what_was_not_touched, unresolved_items, evidence_anchors, verification, rollback, next_step, and next_self_should_not.
```
