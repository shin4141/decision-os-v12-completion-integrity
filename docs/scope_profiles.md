# Scope Profiles

Scope profiles describe the declared reuse surface for a Completion Record. They do not create scores, weights, or domain-specific rules.

## Temporary

A short-lived closure for a narrow context. Missing critical fields may warn because the record is expected to be rechecked before reuse.

## Reusable

A closure intended to be used again in a similar context. Missing critical fields should infer `DELAY` because future restartability is not yet sufficiently anchored.

## Shared

A closure intended to be read or used by more than one person, team, or workflow. Missing critical fields should infer `DELAY` because shared restartability needs clear control handles.

## Irreversible

A closure connected to an action that cannot be easily undone. Missing critical fields should infer `BLOCK` because closure would create serious False Completion risk.
