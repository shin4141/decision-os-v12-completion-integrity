---
name: Boundary misuse concern
about: Raise a concern that a change may blur V12 Gate boundaries.
title: "[Boundary] "
labels: boundary
assignees: ""
---

## Concern

Describe the change, wording, example, or workflow behavior that may blur the V12 Gate boundary.

## Which boundary may be affected?

- Scoring or weights
- Domain thresholds
- Correctness proof
- CI replacement
- AI autofill
- PR comment automation
- Write-permission workflow behavior
- PASS optimization
- Other:

## Why does this matter?

Explain how the concern could make V12 Gate look like something other than a restartability gate.

## Safer alternative

If possible, suggest a smaller boundary-preserving wording or behavior.

## Boundary reminder

- PASS is not a truth guarantee.
- DELAY and BLOCK are valid integrity-preserving outputs.
- V12 Gate does not replace tests, code review, CI, or security review.
- V12 Gate is not for making PASS the goal.
