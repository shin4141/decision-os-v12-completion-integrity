# V12 Short AGENTS.md

A copy-paste short version for Codex / Claude Code / Cursor / agent projects.

```md
# V12 Short AGENTS.md

Before saying "done", leave restart handles.

Do not claim completion unless the next human/agent can resume, verify, roll back, and continue safely.

Always include:

- what_changed
- what_was_not_touched
- unresolved_items
- evidence_anchors
- verification
- rollback
- next_step
- next_self_should_not

If restart handles are missing, output:

HANDOFF_NOW

If handles are weakening, output:

PREPARE_HANDOFF

If the state is still restartable, output:

CONTINUE

V12 is not a code quality checker, code reviewer, security scanner, or CI replacement.

It is a completion discipline layer for restartable AI work.
```

Use the short version when you want a lightweight instruction that reduces token cost.
Use the canonical repo when you need the full schema, examples, tools, and release history.

Canonical repo:
`https://github.com/shin4141/decision-os-v12-completion-integrity`
