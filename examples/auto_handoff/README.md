# Auto-Handoff Gate Examples

These examples demonstrate the deterministic Auto-Handoff Gate MVP.

The tool audits a long-running agent handoff note and suggests whether the workflow should:

- `CONTINUE`
- `PREPARE_HANDOFF`
- `HANDOFF_NOW`

It is not code correctness validation. It does not review code, approve work, replace tests, replace CI/CD, or control an autonomous workflow.

## Why Not A Fixed Context Threshold?

Fixed context-length thresholds are not enough.

Different models compress and summarize differently. Different tasks also degrade at different speeds. A short but vague final message may be less restartable than a longer structured handoff.

The MVP therefore uses deterministic self-assessment-style heuristics. It checks whether concrete restart handles are visible in the input.

## What The Tool Checks

The tool scores five dimensions from 0 to 5:

- `compression_fidelity`
- `restartability`
- `evidence_traceability`
- `rollback_clarity`
- `next_agent_safety`

The thresholds are initial operational defaults:

- 20-25: `CONTINUE`
- 14-19: `PREPARE_HANDOFF`
- 0-13: `HANDOFF_NOW`

These thresholds are not universal truth. Future versions may allow calibration per model, project, or workflow.

## Run The Examples

```bash
python tools/auto_handoff_gate.py examples/auto_handoff/long_run_bad.txt
python tools/auto_handoff_gate.py examples/auto_handoff/long_run_good.txt
```

`long_run_bad.txt` is intentionally vague and should return `HANDOFF_NOW` or `PREPARE_HANDOFF`.

`long_run_good.txt` includes what changed, untouched scope, verification, rollback, unresolved items, next step, and next-self constraints. It should not return `HANDOFF_NOW`.
