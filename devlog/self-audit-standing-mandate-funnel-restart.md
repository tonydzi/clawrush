# Dev log - 2026-07-02: self-audit harness, standing outbound mandate, funnel restart

## What ran

**1. Session-revision harness (read-only).** Six parallel agents over the session ledger: 52 most-recent session transcripts (all machines, selected by frontmatter `date`, not file mtime - a batch sync had flattened every mtime to the same second) + 22 decision memos. Each agent returned a fixed extraction schema per session: built / abandoned-at-2-3 / money-relevance / meta-share / recurring failure classes. A synthesis pass merged the six reports.

**2. Deterministic probes (0 LLM tokens).** Three ground-truth checks against live state instead of trusting the narrative: (a) staleness of the follow-up funnel file (last mutation 13 days ago), (b) row count of the anti-ban send ledger (`send_log` = 0 rows since creation), (c) content-factory output directories (drafts present, published = 0). The probes contradicted the "everything is fine" feel and anchored the audit.

**3. Standing outbound mandate, encoded.** The audit's key finding: internal work reliably reaches "verified", external work reliably stalls at per-item approval. Fix shipped the same day as a rule written into the always-loaded layer (memory index + rulebook): Class 1 (warm-thread follow-ups, neutral, length-capped) auto-send through the budget gate with instant log to a shared channel; Class 2 (first touches, substantive content) batched into one daily approval. Hard stops (money, legal, secrets, mass-send) unchanged.

**4. Funnel restart.** Seven re-engagement messages sent through the messenger MCP; every send recorded into the SQLite send ledger (per-account daily caps, 4/5 and 3/5 used). Follow-up state file updated with owed items (one feedback promise, one intro commitment).

**5. Alpha Protocol synthesis.** Two external deep-research reports (crypto money flows; engineering-community monetization) merged with an earlier services memo into one decision: three productized offers (market-access retainer / talent search sprint / sponsor-funded operator briefings), a 3-week execution plan, and explicit anti-patterns (contingency-only fees, CPM media, waiting for grants). A third DR was commissioned to de-concentrate the ecosystem bet.

## Failure classes worth stealing

- **mtime is a lie after batch sync.** Sort session exports by frontmatter date, never by file modification time.
- **Clock-by-memory bug.** The assistant estimated "now" by adding minutes to an old clock read across a day-long session and mislabeled timestamps for hours. Rule: read the clock, every time.
- **Rule-without-gate decays.** Every process rule that had no deterministic gate (counter, log, watchdog) silently drifted; every gated one held.
- **Approval queues encode their owner.** If the founder is the approval queue, the founder's psychology becomes system behavior. Making the default "send within limits, log loudly" instead of "ask each time" changed throughput the same day.

## Pointers

- Narrative version: [longread](../longreads/the-day-i-gave-my-ai-a-standing-sales-mandate.md).
- Framework pieces referenced: session ledger export, budget-gated sender, decision-memo layer - see the CharmOS repo docs.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
