#!/usr/bin/env python3
"""
Minimal CLI wrapper for the V12 Completion Gate.

Usage:
  python tools/v12_gate.py init
  python tools/v12_gate.py check <record.json>
"""

import json
import sys
from pathlib import Path

from validate_completion_record import load_json, validate


def print_usage():
    print("Usage:")
    print("  python tools/v12_gate.py init")
    print("  python tools/v12_gate.py check <record.json>")


def blank_record_template():
    return {
        "as_of": "",
        "objective": "<what is being closed>",
        "what_changed": [
            "<what changed>"
        ],
        "unresolved": [
            "<what is unknown, assumed, or still pending>"
        ],
        "must_preserve": [
            "Completion Integrity = future-restartable closure.",
            "PASS is not a truth guarantee.",
            "V12 Gate is not for optimizing records toward PASS."
        ],
        "evidence_anchor": [],
        "restart_point": "<restart or rollback point>",
        "stop_condition": [],
        "reanchor_condition": [
            "<when this record must be re-anchored>"
        ],
        "next_self_should_not": [],
        "scope_profile": "reusable",
        "gate_output": "DELAY",
        "gate_subtype": "none",
        "notes": (
            "Blank starter template. Fill in <evidence anchor>, "
            "<stop or recheck condition>, and "
            "<what the next AI/human must not do> before closing."
        ),
    }


def print_blank_template():
    print(json.dumps(blank_record_template(), indent=2))
    return 0


def summarize_value(value):
    if value is None:
        return ""
    if isinstance(value, list):
        if not value:
            return ""
        preview = "; ".join(str(item) for item in value[:2])
        return preview + ("; ..." if len(value) > 2 else "")
    return str(value)


def print_closure_summary(record):
    print("\nClosure summary:")
    print(f"- objective: {summarize_value(record.get('objective'))}")
    print(f"- evidence_anchor: {summarize_value(record.get('evidence_anchor'))}")
    print(f"- restart_point: {summarize_value(record.get('restart_point'))}")
    print("- note: PASS is not a truth guarantee.")


def check_record(path):
    record = load_json(path)
    errors, warnings, inferred_output = validate(record)

    print(f"V12 Gate: {inferred_output}")

    if inferred_output == "PASS" and not errors:
        print_closure_summary(record)

    if errors:
        print("\nERRORS:")
        for error in errors:
            print(f"- {error}")

    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if errors else 0


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "init":
        return print_blank_template()

    if len(sys.argv) == 3 and sys.argv[1] == "check":
        return check_record(Path(sys.argv[2]))

    print_usage()
    return 1


if __name__ == "__main__":
    sys.exit(main())
