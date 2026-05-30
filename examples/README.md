# Examples

Start with these examples when trying V12 Gate for the first time.

| Example | Expected | Purpose |
| --- | --- | --- |
| `block.public_missing_rollback.json` | `BLOCK` | Public or high-impact closure without rollback/restart handles. |
| `delay.missing_stop_conditions.json` | `DELAY` | Handoff lacks explicit stop or recheck conditions. |
| `pass.restartable_local_change.json` | `PASS` | Bounded local change with enough restart handles to close. |
| `delay.missing_evidence_anchor.json` | `DELAY` | Completion claim lacks an evidence anchor. |
| `delay.owner_visible_pending.json` | `DELAY` | Owner or responsibility confirmation is still pending. |
| `conditional_pass_example.json` | `PASS` | Conditional PASS subtype under `PASS`, not a fourth gate output. |

DELAY and BLOCK are valid integrity-preserving outputs. PASS is not a truth guarantee and should not be treated as the goal.
