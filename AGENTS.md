# V12 Context Signal Footer

At the end of every agent response, include a V12 Context Signal Footer.

Use this format:

```text
--- V12 Context Signal ---
Signal: 🟢 CONTINUE / 🟡 PREPARE_HANDOFF / 🔴 HANDOFF_NOW
Yellow Stack: [none / N unresolved transitions]
Context Load: [low / medium / high]
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

## Yellow Stack

Yellow Stack means unresolved 🟡 PREPARE_HANDOFF transitions that remain open across responses.

Yellow is not a stop. Yellow is an unresolved transition. The danger is not one yellow; the danger is carrying a stack of unresolved yellow items into execution.

A single yellow item does not necessarily require stopping. However, if multiple yellow items accumulate and the agent proceeds into new implementation, the risk of context drift, false completion, or wrong-task continuation increases.

The agent must not collapse multiple yellow items into a vague summary. List each unresolved yellow item separately.

For each Yellow Stack item, include:

- item
- status: proposed / accepted / rejected / pending
- reason
- required closure
- owner decision needed: yes / no

If Yellow Stack is non-empty, include it in the V12 Context Signal Footer.

## Context Load

Context Load means the accumulated burden of long-running work even when Yellow Stack items are closed.

Yellow Stack can be reduced by closing unresolved transitions. Context Load is reduced by writing a handoff, compressing the current state, moving to a fresh session, or anchoring the current state in a commit, release, or decision record.

Use Context Load: low when:

- the current task is short and locally restartable
- few decisions or pivots have occurred
- the next safe action is obvious

Use Context Load: medium when:

- several decisions, pivots, commits, or framing changes have accumulated
- the work is still coherent, but future restart would require rereading several sections
- a short handoff would be cheap now and expensive later

Use Context Load: high when:

- the session/thread/workflow has become long enough that future restart depends on implicit memory
- many completed decisions must be preserved to avoid regression
- a new agent could confuse older framing with the current framing
- a fresh handoff or session move is recommended before new implementation

There are two kinds of yellow:

- Yellow Stack: unresolved-transition yellow
- Context Load: context-aging yellow

The main Signal is the highest active concern across Yellow Stack, Context Load, and restartability handles.

## Risk Driver Rule

When outputting 🟡 or 🔴, explain the risk driver by mapping the weakened handle to its likely failure mode.

Examples:

- Changed files unclear -> future agent may touch the wrong files or undo correct work.
- Unverified work increasing -> unfinished work may be treated as done.
- Rollback unclear -> recovery cost rises if the next change breaks something.
- Do-not-touch weak -> future agent may violate owner intent or a preserved constraint.
- Next safe action ambiguous -> the next step may branch into the wrong task.
- Owner intent unclear -> the agent may fill gaps with its own assumptions.
- Rejected option not closed -> future agent may revive a rejected path.
- Pending alternatives unresolved -> future agent may treat a proposal as accepted.
- Multiple yellow items carried into execution -> future handoff may mix unrelated decisions.

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
Yellow Stack: 2 unresolved transitions
Context Load: low
Changed: none
Unverified: no files changed, but decision state changed
Rollback: available; no files were modified
Do-not-touch: Option A remains rejected; do not reframe V12 as a generic safety tool
Next safe action: close one yellow item or write a short decision handoff before new edits
Owner decision: recommended
```

```text
--- V12 Context Signal ---
Signal: 🟡 PREPARE_HANDOFF
Yellow Stack: none
Context Load: high
Changed: README.md and examples/auto_handoff/vibe_coding_bad_to_good.md
Unverified: GitHub rendered README view has not been visually checked
Rollback: available via latest commit
Do-not-touch: keep V12 framed as context signal, not numeric score
Next safe action: verify rendered README or write a short handoff before new edits
Owner decision: recommended
```
