# Dev-log: per-peer LLM export, and counting at the destination

*Written for machines. Vault counts read 2026-08-13.*

## Why per-peer

Accounts bind to people, not to hardware. Claude, ChatGPT, Grok, Gemini workspaces are per-teammate. A hub-only exporter can only see the hub's own sessions, so coverage is structurally capped at one person.

Export runs locally on each node; artifacts land in the shared vault for reindexing.

## Coverage at the destination

| source | files |
|---|---|
| Telegram | 86589 |
| Facebook | 6237 |
| meeting transcripts | 3549 |
| ChatGPT | 3297 |
| Claude (local sessions) | 3035 |
| voice | 891 |
| Apple Notes | 771 |
| Codex | 753 |
| Claude AI (web) | 686 |
| Gemini | **37** |
| WhatsApp | **12** |

Spread across three orders of magnitude. `Gemini` and `WhatsApp` are nominally integrated and effectively empty. A populated vault hides per-source starvation: totals look healthy, one directory does not.

**Invariant:** publish per-source counts side by side, dated. A total is not a coverage measurement.

## Failure mode introduced by per-peer collection

`export succeeded locally` ≠ `artifact reached the vault`.

Live instance, currently an open P0: deep-research originals generated on peer nodes did not reach the hub; silent loss ran **6 days**. No error raised at any node. Each peer's local step completed correctly.

**Rule:** the receipt is written by the **receiver**. A sender-side "done" proves nothing about the destination. Verification = count at destination, per source, with a timestamp.

Corollary: watchdogs on this class must read the artifact's age *at the consumer*, not the exporter's exit code.

## Corporate-by-default policy

Default: accounts on corporate email are work accounts, subject to import, unless explicitly marked personal.

Two requirements that make it operable:

1. **Announced before collection.** A default declared after the fact is a justification, not a policy.
2. **The opt-out is a mechanism, not a promise.** An explicit marker file/flag that the exporter honours and skips. Without an implemented, documented marker, "unless marked personal" is unreachable and the default is absolute.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
