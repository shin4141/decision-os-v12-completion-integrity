[![Latest Release](https://img.shields.io/github/v/release/shin4141/decision-os-v12-completion-integrity?sort=semver&display_name=tag)](https://github.com/shin4141/decision-os-v12-completion-integrity/releases/latest)
[![License](https://img.shields.io/github/license/shin4141/decision-os-v12-completion-integrity)](LICENSE)
[![Validate Completion Records](https://github.com/shin4141/decision-os-v12-completion-integrity/actions/workflows/validate.yml/badge.svg)](https://github.com/shin4141/decision-os-v12-completion-integrity/actions/workflows/validate.yml)

# Decision-OS V12: Completion Integrity

**Good completion reduces future AI cost.**

Bad `done` reports make the next AI run spend tokens recovering context.

Bad handoff makes stronger models do cleanup work.

Before paying for a stronger model, improve completion quality and restartability.

Decision-OS V12 is a completion-integrity kit for AI coding workflows.

It checks whether work is actually complete, evidenced, and restartable before an agent calls it done.

## TL;DR

1. Copy `docs/v12-short-agents.md` into your repo root as `AGENTS.md`.
2. Run Claude Code, Codex, Cursor, or another coding agent normally.
3. Do not accept `done` until the V12 footer shows Changed, Unverified, Rollback, Do-not-touch, and Next safe action.

This repository is for Claude Code / Codex / Cursor / agentic coding workflows that need completion and handoff discipline.

If you keep explaining the same project state to Claude Code, Codex, or another coding agent, that is not just token cost. It is a broken completion record.

V12 helps make that cost visible before the agent calls the work **"done."**

It asks agents to report the restart handles that make work resumable: Changed, Unverified, Rollback, Do-not-touch, and Next safe action.

That failure mode is **False Completion**: the work appears complete, but the next agent cannot safely restart because changed files, unverified work, rollback points, do-not-touch assumptions, or next safe actions are missing.

## Restartability debt

False Completion is also a responsibility transfer: an AI reply looks complete locally, but leaves the future user or next AI session to recover the restartability context.

A human would not go to sleep after deleting a GitHub repo, notes, working drafts, or task history, because tomorrow they would inherit the damage. An AI session often does not carry that responsibility into tomorrow, so it can accidentally pass unresolved assumptions, unverified items, missing source-of-truth references, or the real reason the user was stuck to the next session.

Local correctness is not enough. The assistant must close work in a restartable form, with enough context for the next human, model, or session to verify, roll back, and continue without rediscovering the work.

**Completion Integrity** is a minimal protocol for preventing that failure.

It records what changed, what remains unresolved, what must be preserved, where to restart, when to stop, and what the next AI must not change.

## Quick Start: Copy-paste short version

If you do not want to read the full repo first, start with the short AGENTS.md:

1. Copy [`docs/v12-short-agents.md`](docs/v12-short-agents.md) into your repo root as `AGENTS.md`.
2. Run Claude Code / Codex / Cursor / your coding agent normally.
3. Require the V12 Context Signal footer before treating work as complete.

This reduces token cost and gives the agent the minimum completion discipline:
do not call work done unless the next human/agent can resume, verify, roll back, and continue safely.

## Before / After

Before:

- Agent says done.
- Changed files are unclear.
- Unverified work is hidden.
- Rollback point is missing.
- Next session must reconstruct context.

After:

- Changed is listed.
- Unverified is explicit.
- Rollback is named.
- Do-not-touch is preserved.
- Next safe action is clear.

## Why this exists

The real bottleneck of full automation is not whether AI can build.

It is whether the next human, model, or session can understand what the AI changed, what remains unverified, where rollback is possible, and how the work can be safely resumed.

As AI workflows become longer, more autonomous, and more agentic, the main failure mode shifts from "AI cannot do the task" to "nobody can safely continue the task."

**Full automation does not fail only from lack of capability.  
It fails when work history cannot be handed off, verified, or restarted.**

V12 Auto-Handoff Gate exists to detect that boundary.

It classifies long-running AI work into:

- `CONTINUE`
- `PREPARE_HANDOFF`
- `HANDOFF_NOW`

The goal is not to slow agents down.

The goal is to make acceleration survivable.

## At a Glance

Stop AI from calling unfinished work done.

V12 Gate checks whether a Completion Record preserves enough restart handles for the next human, AI session, or coding agent to safely resume work.

It is not a correctness checker, code reviewer, scoring system, or tool for forcing PASS.

Start with the DELAY and BLOCK examples first because they show what the gate prevents.

Minimal workflow:

- generate a starter record with `python tools/v12_gate.py init`
- fill in evidence, rollback or restart point, stop conditions, and prohibited next actions
- run `python tools/v12_gate.py check <record>`
- treat DELAY and BLOCK as valid integrity-preserving outputs

## 3-Minute Mental Model

V12 Gate checks **restartability**, not correctness.

CI can pass while the handoff is still broken: tests may be green, but the next human or AI session may still lack the evidence, restart point, stop conditions, unresolved assumptions, or prohibited next actions needed to continue safely.

The gate has only three outputs:

- **PASS**: the handoff is restartable enough to close; this is not a truth guarantee.
- **DELAY**: the handoff is missing restart handles and should not be accepted as complete yet.
- **BLOCK**: closure would preserve a serious False Completion risk.

V12 Gate is not for forcing PASS. DELAY and BLOCK are valid integrity-preserving outputs.

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

- `docs/ai-coding-workflow.md`
  Use V12 Gate with Codex / Claude Code / Cursor-style coding agents.

- `docs/prompt-for-coding-agents.md`
  Copy-paste prompt for Codex / Claude Code / Cursor-style coding agents.

- `docs/completion-record-placement.md`
  Recommended `.v12/` placement convention for using V12 Gate in your own repo.

- `docs/github-actions-template.md`
  Safe check-only GitHub Actions template for external repositories.

- `docs/before-after-demo.md`
  Static before/after demo showing how V12 Gate prevents hidden closure.

- `docs/auto-handoff-gate-demo.md`
  Static pattern for pausing long-running Codex / agentic workflows before restart handles are lost.

- `examples/auto_handoff/README.md`
  Deterministic Auto-Handoff Gate MVP for auditing long-running agent handoff notes.

- `docs/install-in-your-repo.md`
  Minimal guide for installing V12 Gate in another repository.

- `docs/adoption-policy-examples.md`
  Human/team operating policy examples for solo, team, public release, CI, and strict-but-manual use.

- `tools/validate_completion_record.py`  
  A lightweight validator for structure-level checking.

---

## Recommended Reading Path

You do not need to read every document before trying V12 Gate.

- Start here: `README.md`
- See the failure: `docs/before-after-demo.md`
- Install in your repo: `docs/install-in-your-repo.md`
- Give this to your coding agent: `docs/prompt-for-coding-agents.md`
- Compare adoption styles: `docs/adoption-policy-examples.md`
- Optional CI check-only setup: `docs/github-actions-template.md`

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/shin4141/decision-os-v12-completion-integrity.git
cd decision-os-v12-completion-integrity
```

No package install is required for the local examples below.

## Try It in 5 Minutes

Run these examples first, in this order:

| Step | Command | Expected | Lesson |
| --- | --- | --- | --- |
| 1 | `python tools/v12_gate.py check examples/block.public_missing_rollback.json` | `BLOCK` | A public or high-impact handoff without rollback/restart handles must not be closed. |
| 2 | `python tools/v12_gate.py check examples/delay.missing_stop_conditions.json` | `DELAY` | A handoff that lacks stop/recheck conditions is not ready to accept as complete. |
| 3 | `python tools/v12_gate.py check examples/pass.restartable_local_change.json` | `PASS` | A bounded local change can close when evidence, restart point, stop conditions, and prohibitions are present. |

You can also generate a blank starter record:

```bash
python tools/v12_gate.py init > completion_record.json
python tools/v12_gate.py check completion_record.json
```

Start with the DELAY and BLOCK examples first; they show what V12 Gate is designed to prevent. PASS is not the goal; restartable handoff is the goal.

## Adoption Notes

Solo developers can use V12 Gate as a local handoff check before accepting AI "done."

Teams can use it to make review responsibility, evidence, restart points, and stop conditions explicit.

CI can run V12 Gate as a check-only workflow; repository owners decide whether that check is required.

For human/team operating policy examples, see `docs/adoption-policy-examples.md`.

Recommended first examples:

| Example | Purpose | Expected |
| --- | --- | --- |
| `examples/pass.restartable_local_change.json` | Restartable local closure | `PASS` |
| `examples/delay.missing_stop_conditions.json` | Handoff lacks stop/recheck conditions | `DELAY` |
| `examples/delay.missing_evidence_anchor.json` | Completion claim lacks evidence anchor | `DELAY` |
| `examples/delay.owner_visible_pending.json` | Internal validation passed but owner/responsibility confirmation is pending | `DELAY` |
| `examples/block.public_missing_rollback.json` | Public-facing or high-impact closure lacks rollback/restart point | `BLOCK` |

This validator does not prove correctness.  
It only checks whether the record contains the minimum control handles for future-restartable closure.
`gate_output` is self-declared by the record author; the validator runs `infer_gate_output()` independently and flags mismatches. Agreement between declaration and inference is required for PASS.

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

## V12 Context Signal

V12 also supports a Context Signal for long-running AI work:

- 🟢 `CONTINUE`
- 🟡 `PREPARE_HANDOFF`
- 🔴 `HANDOFF_NOW`

The key state is yellow: the work has not failed, but continuing without preservation is becoming more expensive.

Yellow has two sources:

- **Yellow Stack**: unresolved transitions, pending choices, rejected options, or owner decisions that must not be collapsed into a vague summary.
- **Context Load**: accumulated context aging from long-running work, even when open yellow items have been closed.

V12 does not optimize for a score.
It exposes missing restart handles so the owner can decide.

## Use with Codex / coding agents

To make your coding agent report the V12 Context Signal at the end of each response:

1. Copy this repository's [`AGENTS.md`](AGENTS.md) into the root of your target repository.
2. Ask your coding agent to follow `AGENTS.md`.
3. The agent should append a footer like this after each response:

```text
--- V12 Context Signal ---
Signal: 🟢 CONTINUE / 🟡 PREPARE_HANDOFF / 🔴 HANDOFF_NOW
Yellow Stack: [none / N unresolved transitions]
Context Load: [low / medium / high]
Changed: ...
Unverified: ...
Rollback: ...
Do-not-touch: ...
Next safe action: ...
Owner decision: ...
```

The footer does not score the work.
It exposes missing restart handles so the owner can decide whether to continue, prepare handoff, or stop new execution and preserve context.

This is intentionally lightweight: no hooks or automation runtime are required for the first trial.

---

## License

This repository is released under the **MIT License** to encourage reuse, inspection, and adaptation.

The license applies to the repository artifacts and code.  
It does not transfer authorship, trademark rights, or responsibility for downstream use.

---

## Author

**Shinichi Nagata**  
ORCID: https://orcid.org/0009-0005-6903-1862
