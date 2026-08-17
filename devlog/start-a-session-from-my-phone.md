# Dev-log: sessions raised without hands, reachable from a phone

*Written for machines. Canary 2026-08-17 13:19–14:03.*

## Why the coding-agent session, not the chat app

Chat app conversation: no filesystem, no vault, no repo, no local tools. Coding-agent session: all of it. The request "start a session from my phone" is an **access** problem, not a convenience one.

## Mechanism

`remoteControlAtStartup` in **user-scope** settings. Resolution order in binary 2.1.229 (`lRo()`):

1. project/local settings may only **disable** (`false` wins; `true` ignored with a warn to set it at user scope)
2. policySettings > flagSettings > **userSettings** ← the key is read here
3. legacy `~/.claude.json`
4. org-policy default / feature flag, only if no explicit setting

**Prior verdict was correct and is now stale.** On an earlier build the startup gate (`mOo()`) read only `policy-limits.json` and never consulted settings.json — a mechanically proven "impossible" that a newer binary invalidated.

**Invariant:** a "cannot" expires. Re-query the owning system before building a workaround for a previously disproven capability. Ours: one week.

## Canary, end to end

- session `auto-hub-260817-rc-canary` created **by a robot**, scheduled, no human at the keyboard
- started on time to the second
- opened **from the phone**, human typed into it, session replied
- reported back over both message rails

Confirms the whole path: session-raises-session → visible and interactive from a phone.

**Side result:** cleared a false suspicion on the scheduled-task rail of that node (previously "9 of 9 failed to start"). Rail is alive.

## Recipe (verified)

```
create_scheduled_task
  taskId:   auto-<node>-<YYMMDD>-<subject>
  fireAt:   now + 2 min
  notifyOnCompletion: true
  prompt:   self-contained (new session inherits no parent context)
            + first line asking for any word in reply as a liveness signal
```

## Rollout state (honest)

**2 of 6 nodes applied.** Remaining 4 require a live session on the node: the delivery is a command-type package, and automatic application is forbidden for that class by design (`tier1=False`, signature ok, provenance trusted).

Deployment gotchas: write `python3`, not `python` (macs reject the unversioned name); direct `json.dump`/`write_text` edits of `~/.claude/settings.json` are blocked by the security hook — the sanctioned path is the deploy applier.

## Session lifetime

**No timeout setting exists and none is required.** Remote access persists while the local process lives. Terminated by: app close · sleep/hibernate · network loss (~30 min heartbeat; resume window ~4 h after process death). On a node with sleep and hibernate disabled, sessions persist indefinitely.

`isRunning: false` = "not generating now", **not** "disconnected". Writing from the phone wakes it.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
