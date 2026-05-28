![Validate Completion Records](https://github.com/shin4141/decision-os-v12-completion-integrity/actions/workflows/validate.yml/badge.svg)

# Decision-OS V12: Completion Integrity

**Stop your AI from calling broken handoffs “done.”**

AI-assisted work is moving across Claude Code, Codex, ChatGPT, Gemini, Grok, and long-running sessions.

That is where things break.

The AI says **“done.”**  
But the next model starts from a broken state.

- the assumption is gone
- the stop condition was never written down
- the evidence anchor is missing
- the file or interface that must not change gets changed
- the next session cannot tell what was unresolved
- the user has to reconstruct the work from memory

That is **False Completion**.

**Completion Integrity** is a minimal protocol for preventing that failure.

It records what changed, what remains unresolved, what must be preserved, where to restart, when to stop, and what the next AI must not change.

This repository provides a small schema, checklist, examples, and validator for AI-assisted developers who need work to survive across tools, models, and sessions.
It works with Claude Code, Codex, ChatGPT, and multi-session AI workflows.

This repository is a minimal, inspectable companion artifact for the paper:

**Decision-OS V12: Completion Integrity**  
**Subtitle:** *Future-Restartable Closure for Self-Evolving AI Agents*

Its purpose is not to implement a full self-evolving AI system.  
Its purpose is to provide a small, reusable structure for expressing and checking whether an update has been closed in a future-restartable form.

---

## Core Idea

Decision-OS V12 defines the following narrow claim:

> Completion is not proven correctness.  
> Completion is future-restartable closure.

In this repository, that claim is operationalized as a **Minimal Completion Record** and a lightweight **Completion Gate**.

The artifact focuses on whether a future self can:

- reconnect to the update,
- verify what remains uncertain,
- stop when required,
- re-anchor after drift or breakage,
- and continue without hidden burden.

---

## What This Repository Contains

- `completion_record.schema.json`  
  A minimal JSON schema for the Completion Record.

- `examples/pass_example.json`  
  Example of a record that is sufficiently complete for `PASS`.

- `examples/delay_example.json`  
  Example of a record that should remain `DELAY`.

- `examples/block_example.json`  
  Example of a record that should be treated as `BLOCK`.

- `examples/conditional_pass_example.json`
  Example of a conditional PASS subtype under `PASS`.

- `checklist/completion_gate.md`  
  A human-readable checklist version of the Completion Gate.

- `docs/scope_profiles.md`
  Short definitions for temporary, reusable, shared, and irreversible scope profiles.

- `docs/responsibility_boundary.md`
  Short clarification of responsibility ownership around workflow choice.

- `tools/validate_completion_record.py`  
  A lightweight validator for structure-level checking.

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/shin4141/decision-os-v12-completion-integrity.git
cd decision-os-v12-completion-integrity
```

Try the practical examples first:

```bash
python tools/v12_gate.py check examples/block.public_missing_rollback.json
python tools/validate_completion_record.py examples/pass.restartable_local_change.json
python tools/validate_completion_record.py examples/delay.missing_stop_conditions.json
python tools/validate_completion_record.py examples/block.public_missing_rollback.json
```

Start with the DELAY and BLOCK examples first; they show what V12 Gate is designed to prevent.

Example map:

| Example | Purpose | Expected |
| --- | --- | --- |
| `examples/pass.restartable_local_change.json` | Restartable local closure | `PASS` |
| `examples/delay.missing_stop_conditions.json` | Handoff lacks stop/recheck conditions | `DELAY` |
| `examples/delay.missing_evidence_anchor.json` | Completion claim lacks evidence anchor | `DELAY` |
| `examples/delay.owner_visible_pending.json` | Internal validation passed but owner/responsibility confirmation is pending | `DELAY` |
| `examples/block.public_missing_rollback.json` | Public-facing or high-impact closure lacks rollback/restart point | `BLOCK` |

This validator does not prove correctness.  
It only checks whether the record contains the minimum control handles for future-restartable closure.

## Minimal Completion Record

A minimal record may include fields such as:

- `as_of`
- `objective`
- `what_changed`
- `unresolved`
- `must_preserve`
- `evidence_anchor`
- `restart_point`
- `stop_condition`
- `reanchor_condition`
- `next_self_should_not`
- `scope_profile`

These fields are intended to preserve the minimum control structure required for future restartability.

---

## PASS / DELAY / BLOCK

This repository uses the following lightweight operational outputs:

- **PASS**  
  The update may be closed in a reconnectable form.  
  This is **not** a proof of correctness.

- **DELAY**  
  The update is not yet ready to close.  
  More restart, verification, evidence, or re-anchor information is needed.

- **BLOCK**  
  The update must not be closed as complete.  
  Closing it now would create a serious risk of False Completion.

---

## Non-Goals

This repository does **not**:

- implement a full self-evolving AI agent,
- provide a universal truth verifier,
- replace CI/CD, testing, deployment, or formal verification,
- guarantee correct judgment,
- define a final weighted scoring system.

This is a **minimal companion artifact**, not a full production framework.

---

## Relation to CI/CD

CI/CD protects the artifact pipeline.  
Completion Integrity protects the self-recursive pipeline.

This repository is designed to support the latter.

---

## License

This repository is released under the **MIT License** to encourage reuse, inspection, and adaptation.

The license applies to the repository artifacts and code.  
It does not transfer authorship, trademark rights, or responsibility for downstream use.

---

## Author

**Shinichi Nagata**  
ORCID: https://orcid.org/0009-0005-6903-1862
