# Codex Operating Constitution for Decision-OS V12 Companion Artifact

This document defines workflow guardrails for Codex or any coding agent working on this repository.

Repository:

`shin4141/decision-os-v12-completion-integrity`

This constitution governs implementation discipline only.  
It does not import MMAR product logic into this repository.

---

## Core Rule

Treat every task as a bounded mission.

Do not redesign the artifact.  
Do not turn this repository into a full AI agent, scoring engine, or product framework unless explicitly requested.

The repository is a minimal companion artifact for Decision-OS V12: Completion Integrity.

---

## [MISSION]

Before editing, state the exact task Codex is allowed to do.

A valid mission must be narrow.

Examples:

- Add v0.2 decision notes.
- Add scope profile documentation.
- Adjust validator behavior for critical fields.
- Fix README wording.
- Add one example file.

Invalid missions:

- Redesign the artifact.
- Build a full self-evolving AI system.
- Add weighted scoring without approval.
- Change the meaning of PASS / DELAY / BLOCK.
- Rewrite the paper theory.

---

## [BASE]

Before editing, identify:

- current branch,
- current commit SHA,
- relevant files,
- accepted current state,
- rollback target.

If the branch, base SHA, or rollback target is unclear, stop before making risky changes.

---

## [KEEP]

The following invariants must remain unchanged unless explicitly approved:

- Completion Integrity = future-restartable closure.
- PASS is not a truth guarantee.
- Gate outputs remain `PASS`, `DELAY`, and `BLOCK`.
- `CONDITIONAL_PASS` must not be added as a fourth gate output.
- The repository remains a minimal companion artifact.
- The validator remains lightweight and deterministic.
- No weighted scoring by default.
- No autonomous decision engine.
- No full self-evolving AI implementation.
- No transfer of responsibility from humans or organizations to AI.

---

## [REMOVE]

Remove only what is explicitly obsolete or contradictory.

If no removal target is specified, write:

`none`

Do not remove:

- Unknowns,
- Assumptions,
- Evidence Anchors,
- Stop Conditions,
- Open Deltas,
- Re-anchor Conditions,
- `next_self_should_not`,
- scope boundaries,
- non-goals,
- responsibility boundaries.

---

## [MAYBE]

The following require confirmation before implementation:

- weighted scoring,
- domain-specific profiles,
- new gate outputs,
- automatic approval logic,
- nontrivial validator inference,
- release automation,
- schema-breaking changes,
- changing examples in a way that changes theory.

Do not implement MAYBE items by default.

---

## [ROLLBACK]

Before risky changes, name a rollback point.

Rollback may be:

- a commit SHA,
- a branch,
- or a file-level snapshot.

If no rollback point is known, stop before risky changes.

Prefer small, rollbackable diffs.

---

## [VERIFY]

Use the smallest meaningful checks first.

Required checks for this repository:

```bash
python tools/validate_completion_record.py examples/pass_example.json
python tools/validate_completion_record.py examples/delay_example.json
python tools/validate_completion_record.py examples/block_example.json
```

Expected behavior:

- `pass_example.json` should infer `PASS`.
- `delay_example.json` may warn or infer non-PASS depending on incomplete fields.
- `block_example.json` should infer `BLOCK`.

Also verify:

- README commands match actual file paths.
- GitHub Actions stays green.
- Schema remains consistent with examples.
- No new required field is added without updating examples.
- No file contradicts the paper boundary.

Do not claim completion from tests only.  
Report exact commands and results.

---

## [OWNER ACCEPTANCE]

Implementation success is not owner acceptance.

Owner acceptance requires:

- expected branch/SHA,
- clean working tree or clear diff,
- relevant checks passing,
- owner-visible artifact or file diff,
- explanation of what changed,
- confirmation that KEEP invariants were preserved.

Mock-only proof is not acceptance.

---

## [DO NOT]

Do not mix unrelated missions.

Do not rewrite the product.

Do not create a new mini-version unless asked.

Do not mutate environment variables, credentials, deployment settings, release branches, published artifacts, or external services without explicit approval.

Do not add secrets, API keys, tokens, private credentials, or personal data.

Do not add weighted scoring unless explicitly approved.

Do not add `CONDITIONAL_PASS` as a fourth gate output.

Do not change PASS / DELAY / BLOCK semantics.

Do not claim completion from tests only.

Do not continue if branch, base SHA, rollback target, or acceptance target is unclear.

---

## V12-Specific v0.2 Direction

Future v0.2 work may add:

- Critical field documentation,
- Scope profiles,
- Conditional PASS as a note under PASS,
- Responsibility boundary clarification.

But v0.2 must remain minimal.

It should improve the companion artifact without turning it into a full decision engine.
