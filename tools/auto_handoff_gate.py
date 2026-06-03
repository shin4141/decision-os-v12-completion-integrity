#!/usr/bin/env python3
"""
Deterministic Auto-Handoff Gate MVP.

This tool is a handoff timing assistant for long-running Codex / agentic
workflows. It does not prove code correctness, review code, approve work,
control a workflow, or replace CI/CD.

The thresholds below are initial operational defaults, not universal truth.
Future versions may allow calibration per model, project, or workflow.
"""

import argparse
import re
import sys
from pathlib import Path


STAGE_CONTINUE = "CONTINUE"
STAGE_PREPARE = "PREPARE_HANDOFF"
STAGE_NOW = "HANDOFF_NOW"

DIMENSIONS = [
    "compression_fidelity",
    "restartability",
    "evidence_traceability",
    "rollback_clarity",
    "next_agent_safety",
]

HANDLE_PATTERNS = {
    "what_changed": [
        r"\bwhat_changed\b",
        r"\bwhat changed\b",
        r"\bchanged\b",
        r"\badded\b",
        r"\bupdated\b",
        r"\bmodified\b",
        r"\bimplemented\b",
        r"\bfiles?\b",
    ],
    "what_was_not_touched": [
        r"\bwhat_was_not_touched\b",
        r"\bnot touched\b",
        r"\buntouched\b",
        r"\bdid not change\b",
        r"\bunchanged\b",
        r"\bwas not changed\b",
        r"\bwere not changed\b",
    ],
    "unresolved_items": [
        r"\bunresolved_items\b",
        r"\bunresolved\b",
        r"\bpending\b",
        r"\bunknown\b",
        r"\bassumption",
        r"\bTODO\b",
        r"\bneeds? review\b",
        r"\bnot yet\b",
    ],
    "evidence_anchors": [
        r"\bevidence_anchors\b",
        r"\bevidence\b",
        r"\blog\b",
        r"\bdiff\b",
        r"\bcommit\b",
        r"\bhash\b",
        r"\bfile path\b",
        r"\bworkflow run\b",
        r"[\w./-]+\.(py|js|ts|json|md|yml|yaml|html|css|txt)\b",
    ],
    "verification": [
        r"\bverification\b",
        r"\bverified\b",
        r"\btest",
        r"\bpassed\b",
        r"\bfailed\b",
        r"\bsmoke\b",
        r"\bcheck\b",
        r"\bcommand output\b",
    ],
    "rollback": [
        r"\brollback\b",
        r"\brevert\b",
        r"\brestore\b",
        r"\bback out\b",
        r"\bprevious commit\b",
        r"\brollback path\b",
    ],
    "next_step": [
        r"\bnext_step\b",
        r"\bnext step\b",
        r"\bnext action\b",
        r"\bfollow[- ]?up\b",
        r"\bcontinue by\b",
        r"\bresume\b",
        r"\brun the\b",
    ],
    "next_self_should_not": [
        r"\bnext_self_should_not\b",
        r"\bshould not\b",
        r"\bdo not\b",
        r"\bmust not\b",
        r"\bdo-not\b",
        r"\bconstraint",
        r"\bavoid\b",
        r"\bnot change\b",
    ],
}

VAGUE_PATTERNS = [
    r"\bdone\b",
    r"\beverything should work\b",
    r"\bcleaned up\b",
    r"\bshould be ready\b",
    r"\ball set\b",
    r"\bfixed it\b",
]


def count_matches(text, patterns):
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))


def clamp(value):
    return max(0, min(5, value))


def detect_handles(text):
    return {
        handle: count_matches(text, patterns) > 0
        for handle, patterns in HANDLE_PATTERNS.items()
    }


def score_text(text, handles):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    structured_lines = sum(
        1
        for line in lines
        if line.startswith(("-", "*", "#")) or ":" in line
    )
    vague_hits = count_matches(text, VAGUE_PATTERNS)
    handle_count = sum(1 for present in handles.values() if present)

    compression_fidelity = clamp(
        (1 if len(lines) >= 4 else 0)
        + (2 if structured_lines >= 4 else 1 if structured_lines >= 2 else 0)
        + (2 if handle_count >= 6 else 1 if handle_count >= 3 else 0)
        - (1 if vague_hits >= 2 else 0)
    )

    restartability = clamp(
        (1 if handles["what_changed"] else 0)
        + (1 if handles["what_was_not_touched"] else 0)
        + (1 if handles["unresolved_items"] else 0)
        + (2 if handles["next_step"] else 0)
    )

    evidence_traceability = clamp(
        (3 if handles["verification"] else 0)
        + (2 if handles["evidence_anchors"] else 0)
    )

    rollback_clarity = 5 if handles["rollback"] else 0

    next_agent_safety = clamp(
        (3 if handles["next_self_should_not"] else 0)
        + (1 if handles["what_was_not_touched"] else 0)
        + (1 if handles["unresolved_items"] else 0)
    )

    return {
        "compression_fidelity": compression_fidelity,
        "restartability": restartability,
        "evidence_traceability": evidence_traceability,
        "rollback_clarity": rollback_clarity,
        "next_agent_safety": next_agent_safety,
    }


def stage_for_total(total):
    if total >= 20:
        return STAGE_CONTINUE
    if total >= 14:
        return STAGE_PREPARE
    return STAGE_NOW


def required_action(stage):
    if stage == STAGE_CONTINUE:
        return "Continue, while keeping restart handles visible."
    if stage == STAGE_PREPARE:
        return "Prepare a checkpoint soon before the workflow becomes hard to resume."
    return "Stop now and write a V12-style Completion Record before continuing."


def threshold_note():
    print("Threshold note: 20-25 => CONTINUE, 14-19 => PREPARE_HANDOFF, 0-13 => HANDOFF_NOW.")
    print("These thresholds are initial operational defaults, not universal truth.")


def print_scores(scores):
    print("| Dimension | Score |")
    print("| --- | ---: |")
    for dimension in DIMENSIONS:
        print(f"| {dimension} | {scores[dimension]}/5 |")


def print_missing(handles):
    missing = [handle for handle, present in handles.items() if not present]
    if not missing:
        print("- none detected")
        return
    for handle in missing:
        print(f"- {handle}")


def print_completion_record_draft(handles):
    fields = [
        "what_changed",
        "what_was_not_touched",
        "unresolved_items",
        "evidence_anchors",
        "verification",
        "rollback",
        "next_step",
        "next_self_should_not",
    ]

    for field in fields:
        print(f"{field}:")
        if handles[field]:
            print("- Present in input; copy the concrete detail into the record.")
        else:
            print(f"- TODO: add {field.replace('_', ' ')}.")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Auto-Handoff Gate MVP."
    )
    parser.add_argument("handoff_note", help="Path to a long-running workflow handoff note.")
    parser.add_argument(
        "--show-scores",
        "--verbose",
        action="store_true",
        help="Show internal dimension scores and threshold details.",
    )
    args = parser.parse_args()

    path = Path(args.handoff_note)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: could not read {path}: {exc}", file=sys.stderr)
        return 1

    handles = detect_handles(text)
    scores = score_text(text, handles)
    total = sum(scores.values())
    stage = stage_for_total(total)

    print(f"# Auto-Handoff Stage: {stage}")
    print()
    if args.show_scores:
        print_scores(scores)
        print()
        print(f"**Total score:** {total}/25")
        print()
        threshold_note()
        print()
    print("## Missing Restart Handles")
    print()
    print_missing(handles)
    print()
    print("## Required Action")
    print()
    print(required_action(stage))
    print()
    print("## Suggested V12 Completion Record Draft")
    print()
    print_completion_record_draft(handles)

    return 0


if __name__ == "__main__":
    sys.exit(main())
