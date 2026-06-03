# Vibe Coding Handoff Example

## Why this example matters

A broken handoff is not acceleration. It is deferred cost.

The fastest workflow is not the one that moves fastest once. It is the one that can restart without paying the same context cost again.

Long-running vibe-coding and agent workflows can produce useful work quickly, but they can also leave the next human or AI session with no reliable way to continue.

## Bad long-running AI work log

```text
Implemented auth changes.
Updated some API files.
Tests mostly pass.
Need to clean up later.
Maybe rollback if broken.
```

## Why this is not restartable

The next AI or human cannot safely continue because the log does not say:

- which files changed
- which checks passed
- what work is still unverified
- where rollback is possible
- what assumptions must not be changed
- what the next safe action is

The next session has to reread files, revalidate assumptions, rerun checks, and rediscover what the previous session already knew. That cost was not removed. It was deferred.

## Gate result

Likely Auto-Handoff Gate result:

```text
HANDOFF_NOW
```

Reason: the log claims progress, but it does not preserve enough restart handles for the next session to resume safely.

## Restartable handoff version

```text
Changed files:
- src/auth/session.py
- src/auth/token_store.py
- src/api/login.py
- tests/auth/test_login.py

Verified:
- Ran python -m pytest tests/auth/test_login.py.
- Login success and invalid-password cases passed.
- Manual smoke test confirmed that expired sessions redirect to /login.

Unverified:
- Full test suite was not run.
- Password reset flow was not retested.
- Token refresh behavior was not checked in the browser.

Rollback point:
- Revert commit abc1234 or restore the four changed files above from main.

Do not touch:
- Do not rename the session_cookie field.
- Do not change the existing refresh-token lifetime assumption.
- Do not rewrite the auth middleware; only continue from the login/session patch.

Next safe action:
- Run the full auth test group.
- Recheck password reset and token refresh.
- If those pass, update the completion record with evidence and remaining risks.
```

## Cost saved

Making the handoff explicit can reduce restart cost by preserving:

- fewer rereads
- fewer repeated tests
- fewer duplicated tool calls
- less rediscovery
- lower chance of undoing correct work
- faster next session

This does not guarantee correctness. It makes the work easier to inspect, resume, verify, and roll back.
