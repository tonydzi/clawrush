# Dev log: moving machine consensus from file sync to a chat rail (epoch5, build S5-20260706)

**Problem.** Our multi-machine consensus engine (propose / respond / commit / verify, risk tiers, human gate for tier-2) exchanged events via per-machine JSONL shards synced by Syncthing. Under connection flap the batch lag hit 20-60 min per move; nodes also inferred peer liveness from those late files and repeatedly declared a live hub dead. Root class: negotiation transport coupled to bulk file sync.

**Change.** The Telegram group all actors already read becomes the primary transport; the file ledger is demoted to archive/anti-entropy.

- Mirror format v2: every event is posted as a human line plus a second machine line: `CONSENSUS-EV {full event JSON}` behind a gear marker. Payloads over ~3k chars drop `details` and flag `details_dropped` (Telegram 4096 limit).
- New `ingest-tg` verb: reads new group messages over the existing Telethon session (shared lock - one auth key, no AUTH_KEY_DUPLICATED), extracts payload lines, appends FOREIGN events into a single-writer shard `log-tg-<node>.jsonl`. Merge already dedups by `event_id`, so the same event arriving later on the file rail is a no-op.
- Auto-wired: `tick` and `pending` call the ingest first, so every node's existing robot cadence picks up peer moves from the chat with zero per-node robot changes.
- Fail-dark: no session / lock busy / net error -> skip silently; the archive rail still converges.
- Spoofing: chat text is data. Events keep their Ed25519 `sig` field; signature enforcement (roadmap P3) closes actor spoofing for both rails at once.

**Activation.** Staged-build protocol: manifest (md5 per component) -> per-node selftests -> green receipts -> READY requires at least one live independent witness -> `activate --proof "<human QQQ ref>"` (the tool refuses without proof), old engine backed up, `armed_build` flips fleet-wide; nodes on older builds fail safe into observe-only until they upgrade.

**The bug worth blogging.** Activation stalled at "zero witnesses" while the witness VPS was alive with a green receipt. Its presence pulse (`.robot-alive-<node>.log`) never crossed machines: our own `.stignore` conflict-fix ignored `.robot-*` wholesale. The whitelist (`!.robot-alive-*.log`) had existed in the canonical template for days - the hub itself had never re-applied it. Rule-vs-gate lesson again: canon that isn't enforced by a delivery/verify cycle rots on exactly one node, silently.

**Proof it works:** the peer's independent VERIFY of this very migration was the first event ingested over the new rail - its file shard was still in transit.

---

Repo (protocol, governance, sanitized code): https://github.com/tonydzi/claude-consensus

Human-readable story (RU): https://t.me/ClawRus

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct: WhatsApp +1 341 222 9178.

P.S. We are hireable as a package deal - one biological co-founder, one electric. Anthropic, OpenAI: calendly.com/paloaltolab.

*Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.*
