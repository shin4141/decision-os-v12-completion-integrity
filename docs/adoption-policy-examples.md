# Adoption Policy Examples

These are human/team operating policies, not machine-enforced policy files.

V12 Gate does not implement a policy engine. These examples introduce no scoring, weights, thresholds, domain tuning, policy YAML, or strict mode CLI flags.

PASS / DELAY / BLOCK remain the only outputs. DELAY and BLOCK are valid integrity-preserving outputs. PASS is not a truth guarantee.

## Solo Developer Policy

When to use it: before accepting an AI coding agent's "done" in a local branch or personal project.

PASS: you may close the local handoff as restartable, while still relying on tests and review for correctness.

DELAY: fill missing evidence, restart point, stop condition, unresolved item, or next-self prohibition before calling the task done.

BLOCK: stop closure and restore control before continuing.

Do not automate: do not let an AI autofill uncertainty away to reach PASS.

## Small Team Policy

When to use it: before merging AI-assisted work that another person may need to review or resume.

PASS: the handoff is restartable enough for team review; it is not approval of the code itself.

DELAY: keep the work open until the decision owner or reviewer can see the missing restart handles.

BLOCK: do not merge until rollback, restart, or owner review restores control.

Do not automate: do not replace reviewer responsibility with the gate result.

## Public Release Policy

When to use it: before publishing, deploying, or announcing a public-facing AI-assisted change.

PASS: the release handoff has enough restart and rollback context to be reviewed.

DELAY: pause release acceptance until evidence, stop conditions, and unresolved assumptions are explicit.

BLOCK: do not publish as complete when rollback or restart control is missing.

Do not automate: do not treat a public-facing summary as sufficient evidence.

## CI Check-Only Policy

When to use it: when a repository wants CI to surface incomplete Completion Records.

PASS: the record check passed; this does not prove the code is correct, secure, reviewed, or tested.

DELAY: the CI result is a signal to finish the handoff record, not a system failure.

BLOCK: the record says closure should not be accepted yet.

Do not automate: do not add PR comments, write permissions, or `pull_request_target`.

## Strict-But-Manual Policy

When to use it: when a team wants a stricter operating rule without changing V12 Gate behavior.

PASS: accept only when the team agrees that evidence, restart point, stop conditions, and prohibitions are actionable.

DELAY: require repair before merge when evidence anchors or stop conditions are missing.

BLOCK: require owner review, rollback, or re-anchoring before closure.

Do not automate: do not turn strictness into scoring, numeric thresholds, domain tuning, or a policy engine.
