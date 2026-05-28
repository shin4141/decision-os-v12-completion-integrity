#!/usr/bin/env python3
"""
Minimal CLI wrapper for the V12 Completion Gate.

Usage:
  python tools/v12_gate.py check <record.json>
"""

import sys
from pathlib import Path

from validate_completion_record import load_json, validate


def print_usage():
    print("Usage: python tools/v12_gate.py check <record.json>")


def check_record(path):
    record = load_json(path)
    errors, warnings, inferred_output = validate(record)

    print(f"V12 Gate: {inferred_output}")

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
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        print_usage()
        return 1

    return check_record(Path(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
