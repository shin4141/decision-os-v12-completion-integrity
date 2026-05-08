# Completion Gate Checklist

Human-readable checklist for **Decision-OS V12: Completion Integrity**.

This checklist is a lightweight companion to `completion_record.schema.json`.

It does not prove correctness.  
It checks whether an update can be closed in a future-restartable form.

---

## Core Rule

> Completion is not proven correctness.  
> Completion is future-restartable closure.

Do not close an update unless the future self can reconnect, verify, stop, revise, and re-anchor it.

---

## Gate Inputs

Before closing an update, confirm that the following are present.

- [ ] `as_of`  
  Timestamp or As-of marker for when the update was produced.

- [ ] `objective`  
  The current objective of the update cycle.

- [ ] `what_changed`  
  Explicit delta from the prior state.

- [ ] `unresolved`  
  Open items, Unknowns, Assumptions, or incomplete structures.

- [ ] `must_preserve`  
  Canon, KEEP constraints, definitions, or structures that must not be overwritten.

- [ ] `evidence_anchor`  
  Source, log, file, hash, commit, version, URL, or reference.

- [ ] `restart_point`  
  Where the future self should resume.

- [ ] `stop_condition`  
  Conditions that should trigger DELAY or BLOCK.

- [ ] `reanchor_condition`  
  Conditions under which the update must be re-anchored.

- [ ] `next_self_should_not`  
  Explicit prohibitions for the future self.

---

## PASS

Use **PASS** only when all required control handles are present.

PASS means:

- the future self can reconnect,
- evidence can be checked,
- Unknowns and Assumptions remain visible,
- Stop Conditions exist,
- Re-anchor Conditions exist,
- and the next self knows what not to do.

PASS does **not** mean the update is true or final.

---

## DELAY

Use **DELAY** when the record is useful but not ready to close.

Typical DELAY conditions:

- Evidence Anchor is missing or incomplete.
- Stop Condition is vague.
- Re-anchor Condition is unclear.
- Open Delta exists but is not recorded.
- Unknowns or Assumptions need review.
- The future self can continue only after additional checking.

DELAY is not failure.  
It means the update should not yet be closed as complete.

---

## BLOCK

Use **BLOCK** when closing the update would actively create False Completion.

Typical BLOCK conditions:

- Past Fidelity is violated.
- Canon or KEEP constraints were removed.
- Evidence Anchor is missing for an irreversible claim.
- The future self cannot restart.
- No Stop Condition exists for a known risk.
- Unknowns were converted into facts.
- A fluent summary replaced the original evidence path.
- The next self would be unable to stop or re-anchor.

BLOCK means the update must not be closed as complete.

---

## Minimal Closure Question

Before closing, ask:

> Can the future self safely restart from what the current self is about to call complete?

If the answer is unclear, choose DELAY.  
If closure would hide risk or break reconnection, choose BLOCK.

---

## Non-Goals

This checklist does not:

- verify truth,
- replace CI/CD,
- replace human review,
- replace formal verification,
- define weighted scoring,
- or implement a self-evolving AI system.

It only checks whether a closure record is future-restartable.
