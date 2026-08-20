# Devlog: Making Session Branches Visible

## Problem statement

A long-running AI conversation drifts into a second deliverable. The agent can suggest or create a branch, but an automatically created child may not appear in the operator's standard web or desktop session list. At scale, an invisible child is operationally equivalent to lost work.

The target behavior is narrow:

> When a task becomes independent, create a child session that is visible in the native interface, pass only the required context, and preserve a return path to the parent.

## Boundary of the solution

This design does not attempt to rebuild Claude's interface or maintain a second universal session dashboard. It treats native visibility as an acceptance requirement.

The routine is only a launcher. It must not become a permanently privileged worker that performs arbitrary tasks invisibly.

## Proposed record

Each branch should have a small durable record:

```json
{
  "branch_id": "session-drift-20260820-001",
  "parent_session": "visible-parent-id",
  "child_session": "visible-child-id",
  "objective": "One bounded deliverable",
  "created_at": "2026-08-20T00:00:00Z",
  "created_by": "routine",
  "visibility": "verified",
  "state": "running",
  "result_artifact": null
}
```

The schema is intentionally small. The transcript remains in the session system; the ledger stores identity, purpose, visibility, and outcome.

## Branching flow

1. Detect a possible change in deliverable.
2. Extract a minimal handoff from the parent.
3. Generate a descriptive child name.
4. Request creation through the mechanism that produces a native session.
5. Read the standard session list back.
6. Mark the branch `visible` only if the created id is present there.
7. If it is absent, fail closed and alert instead of claiming success.
8. On completion, attach the result artifact and send a compact return message.

## Minimal handoff contract

The child receives:

- one objective;
- relevant decisions and facts;
- artifact links instead of copied files;
- constraints and permissions;
- the required output format;
- the parent id.

It does not receive the complete parent transcript by default. That would carry the original drift into the new session and waste context.

## Drift signal

The first version should score changes in deliverable, target system, owner, deadline, permissions, and completion criteria. Topic similarity alone is not enough.

Recommended rollout:

- shadow mode: identify possible branches without creating them;
- compare suggestions with actual operator decisions;
- auto-create only the lowest-risk, highest-precision branch classes;
- keep ambiguous cases visible for one-click confirmation.

## Failure tests

The launcher is not accepted until these cases are tested:

- creation returns an id but the child is absent from the native list;
- the parent closes immediately after requesting a branch;
- two branch requests arrive concurrently;
- the same request is retried after a timeout;
- the child finishes but cannot write back to the parent;
- the routine lacks a dependency or credential;
- the context extractor produces an empty handoff.

The duplicate test requires an idempotency key derived from the parent id and branch objective. A retry must find the existing child instead of creating a second one.

## Visibility counter

Every launch should append one event:

```json
{"ts":"...","node":"session-branch-launcher","actor":"routine","event":"create-child","outcome":"visible|hidden|failed"}
```

Useful dashboard counters:

- branches requested;
- native sessions created;
- visibility verification failures;
- duplicate requests suppressed;
- branches completed;
- branches without a returned artifact after 24 hours.

The crucial metric is not spawn success. It is visible-and-recoverable success.

## Acceptance criteria

A branch is complete only when:

- the child is visible in the ordinary interface;
- the parent–child link is durable;
- the handoff contains one bounded objective;
- duplicate creation is prevented;
- the child can return an artifact or an explicit failure;
- a human can find the result without opening a custom dashboard.

## Related artifacts

- Longread: https://github.com/tonydzi/clawrush/blob/main/longreads/session-drift-lost-branches.md
- Routine launcher pattern: https://github.com/tonydzi/clawrush/blob/main/longreads/routine-session-starts-a-real-one.md
- Lost-session recovery: https://github.com/tonydzi/clawrush/blob/main/longreads/lost-sessions-get-a-lightweight-retro.md
- Repository: https://github.com/tonydzi/clawrush

Assisted-by: Mycroft (OpenAI Codex)
