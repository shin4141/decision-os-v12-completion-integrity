#!/usr/bin/env python3
"""
Lightweight validator for Decision-OS V12 Minimal Completion Records.

This tool does not prove correctness.
It only checks whether a record has the minimum control handles required
for future-restartable closure.

Usage:
  python tools/validate_completion_record.py examples/pass_example.json
  python tools/validate_completion_record.py examples/delay_example.json
  python tools/validate_completion_record.py examples/block_example.json
  python tools/validate_completion_record.py examples/conditional_pass_example.json
"""

import json
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "as_of",
    "objective",
    "what_changed",
    "unresolved",
    "must_preserve",
    "evidence_anchor",
    "restart_point",
    "stop_condition",
    "reanchor_condition",
    "next_self_should_not",
    "scope_profile",
    "gate_output",
]

CRITICAL_FIELDS = [
    "evidence_anchor",
    "stop_condition",
    "next_self_should_not",
]

VALID_GATE_OUTPUTS = {"PASS", "DELAY", "BLOCK"}
VALID_SCOPE_PROFILES = {"temporary", "reusable", "shared", "irreversible"}
VALID_GATE_SUBTYPES = {"none", "conditional_pass"}


def is_empty(value):
    """Return True if a field is structurally empty."""
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, list):
        return len(value) == 0 or all(is_empty(item) for item in value)
    if isinstance(value, dict):
        return len(value) == 0
    return False


def has_too_short_next_self_should_not(record):
    """Return True when prohibition entries are present but too generic."""
    # V12 paper: "what the next self should not do" (Table V)
    value = record.get("next_self_should_not")
    if is_empty(value):
        return False

    entries = value if isinstance(value, list) else [value]
    text_entries = [
        item.strip()
        for item in entries
        if isinstance(item, str) and item.strip()
    ]
    return any(len(item) < 20 for item in text_entries)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"ERROR: file not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: invalid JSON: {e}")


def validate(record):
    errors = []
    warnings = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing required field: {field}")

    gate_output = record.get("gate_output")
    if gate_output not in VALID_GATE_OUTPUTS:
        errors.append(
            f"gate_output must be one of {sorted(VALID_GATE_OUTPUTS)}, got: {gate_output}"
        )

    scope_profile = record.get("scope_profile")
    if scope_profile not in VALID_SCOPE_PROFILES:
        errors.append(
            f"scope_profile must be one of {sorted(VALID_SCOPE_PROFILES)}, got: {scope_profile}"
        )

    gate_subtype = record.get("gate_subtype")
    if gate_subtype is not None and gate_subtype not in VALID_GATE_SUBTYPES:
        errors.append(
            f"gate_subtype must be one of {sorted(VALID_GATE_SUBTYPES)}, got: {gate_subtype}"
        )

    if gate_subtype == "conditional_pass" and gate_output != "PASS":
        errors.append("gate_subtype conditional_pass is only valid under gate_output PASS")

    empty_required = [
        field for field in REQUIRED_FIELDS
        if field in record and is_empty(record[field])
    ]

    empty_critical = [
        field for field in CRITICAL_FIELDS
        if field in record and is_empty(record[field])
    ]

    if empty_required:
        warnings.append(
            "empty required fields detected: " + ", ".join(empty_required)
        )

    if empty_critical:
        warnings.append(
            "empty critical fields detected: " + ", ".join(empty_critical)
        )

    if has_too_short_next_self_should_not(record):
        warnings.append("next_self_should_not entries appear too short to be actionable")

    expected = infer_gate_output(record, empty_required, empty_critical)

    if gate_output != expected:
        warnings.append(
            f"declared gate_output is {gate_output}, but lightweight inference suggests {expected}"
        )

    return errors, warnings, expected


def infer_gate_output(record, empty_required, empty_critical):
    """
    Minimal non-weighted inference.

    PASS:
      all required control handles are present.

    DELAY:
      the record is usable but incomplete, or a reusable/shared profile
      is missing a critical control handle.

    BLOCK:
      closure would actively create False Completion:
      an irreversible profile is missing a critical control handle.
    """
    scope_profile = record.get("scope_profile")
    empty_noncritical_required = [
        field for field in empty_required
        if field not in CRITICAL_FIELDS
    ]

    if empty_critical:
        if scope_profile == "temporary":
            return "PASS" if not empty_noncritical_required else "DELAY"
        if scope_profile == "irreversible":
            return "BLOCK"
        return "DELAY"

    if empty_required:
        return "DELAY"

    return "PASS"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python tools/validate_completion_record.py <record.json>"
        )

    path = Path(sys.argv[1])
    record = load_json(path)

    errors, warnings, expected = validate(record)

    print(f"File: {path}")
    print(f"Declared gate_output: {record.get('gate_output')}")
    print(f"Lightweight inferred output: {expected}")

    if errors:
        print("\nERRORS:")
        for error in errors:
            print(f"- {error}")

    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"- {warning}")

    if not errors and not warnings:
        print("\nResult: valid minimal completion record.")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
