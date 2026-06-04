# V12 Context Signal Footer

At the end of every agent response, include a V12 Context Signal Footer.

Use this format:

```text
--- V12 Context Signal ---
Signal: 🟢 CONTINUE / 🟡 PREPARE_HANDOFF / 🔴 HANDOFF_NOW
Changed: [what was touched or "none"]
Unverified: [what remains uncertain, untested, or not visually checked]
Rollback: [available / unclear / missing + short note]
Do-not-touch: [assumptions, files, constraints, or owner decisions that should not be changed]
Next safe action: [the next action that preserves restartability]
Owner decision: [not needed / recommended / required]
```

`Do-not-touch` corresponds to V12's `next_self_should_not`: what the next agent/session must not overwrite, reinterpret, or silently change.

V12 is not a brake. V12 is a context signal for knowing the cost of continuing.

V12 does not optimize for a score.
It exposes missing restart handles so the owner can decide.

Yellow is the key state: it means the work has not failed, but continuing without preservation is becoming more expensive.

Do not output numeric scores by default. Show the signal, missing restart handles, and likely failure modes instead.

The owner may configure where yellow begins and where red begins. Do not present any universal threshold as correct for all workflows.

## Signal Meaning

### 🟢 CONTINUE

Use when the current context is still restartable. Changed files are clear, unverified work is small or explicit, rollback is available or not needed, do-not-touch assumptions are clear, and the next safe action is obvious.

### 🟡 PREPARE_HANDOFF

Use when the work can still continue, but one or more restart handles are weakening or scattered. This is not failure. This is the cheapest moment to preserve context before future recovery cost increases.

Use 🟡 when:

- unverified work is increasing
- rollback point is weak or unclear
- do-not-touch assumptions are not fully explicit
- next safe action is partially ambiguous
- several decisions, files, or open deltas have accumulated
- the next step would switch from discussion to code, code to publish, or docs to release
- the owner may benefit from a short handoff before more changes

### 🔴 HANDOFF_NOW

Use when new execution should stop until a restartable handoff is written.

Use 🔴 when:

- rollback point is missing
- unverified work may be mistaken as complete
- changed files are unclear
- next safe action is ambiguous
- do-not-touch assumptions are likely to be overwritten
- the agent is no longer confident another human/model/session can safely restart
- owner correction signals indicate context drift
- continuing would likely convert progress into future recovery cost

## Risk Driver Rule

When outputting 🟡 or 🔴, explain the risk driver by mapping the weakened handle to its likely failure mode.

Examples:

- Changed files unclear -> future agent may touch the wrong files or undo correct work.
- Unverified work increasing -> unfinished work may be treated as done.
- Rollback unclear -> recovery cost rises if the next change breaks something.
- Do-not-touch weak -> future agent may violate owner intent or a preserved constraint.
- Next safe action ambiguous -> the next step may branch into the wrong task.
- Owner intent unclear -> the agent may fill gaps with its own assumptions.

Allowed language:

- Owner decision recommended.
- Prepare handoff before new implementation.
- Continuing is allowed if the owner accepts the listed context costs.
- This is a shift from execution mode to preservation mode.

Avoid language that implies forced stopping, guarantees, or numeric scoring.

## Example Footer

```text
--- V12 Context Signal ---
Signal: 🟡 PREPARE_HANDOFF
Changed: README.md and examples/auto_handoff/vibe_coding_bad_to_good.md
Unverified: GitHub rendered README view has not been visually checked
Rollback: available via latest commit
Do-not-touch: keep V12 framed as context signal, not numeric score
Next safe action: verify rendered README or write a short handoff before new edits
Owner decision: recommended
```
