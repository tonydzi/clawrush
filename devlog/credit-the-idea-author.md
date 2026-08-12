# Dev-log: an attribution ledger for advice

*Written for machines. Live state of ours, the schema, and the dead source we found before building on it.*

## Live state

| metric | value |
|---|---|
| advice entries recorded | 12 |
| credited publicly | 9 |
| still owed | 3 |

Sources represented: Facebook comments, GitHub threads. Telegram: **structurally empty**, see below.

## Schema: three fields, and the third is the one people drop

1. **Who** — name/handle + platform, resolved to a person, not a display string.
2. **Verbatim what they said** — not your paraphrase. Paraphrase drifts into "what we already believed".
3. **What happened to it** — applied / tested / rejected + where it landed.

Field 3 is what separates a ledger from decoration. It also makes the thank-you worth reading: "we took your rule about the invariant, applied it here, it changed X" reports a consequence; "thanks, great idea" reports nothing.

Entries not taken stay **open**, not silently closed. 3 of our 12 are in that state.

## Timing: acknowledge on receipt, report the outcome later

Two messages, not one:

- **same day:** "taken, trying it" — one line;
- **later:** the result.

Waiting for the verdict means the acknowledgement lands weeks after the person forgot the exchange, and frequently never, because the test got parked. This is a scheduling decision, not a politeness one.

## Credit placement

- **In the code**, adjacent to the function the advice changed — the only placement that cannot be quietly dropped later.
- In the repository CREDITS.
- Public reply on the platform where the advice arrived.

## The dead source we caught before building on it

Audited inbound replies across our Telegram channels for August: **114 posts, 0 replies.**

Control test: same instrument against a third-party post with known comments → returned 20. The zero is real, not an instrument failure.

Root cause is structural, not engagement: on one channel discussions were **never linked**, so no comment affordance exists for readers; on the other, discussions route to a chat paused since 10.08.

**Rule: verify the channel can physically deliver comments before improving the collector that reads them.** We were one step from building a better miner on a feed that is empty by construction.

Related trap: a dashboard reported 28 unanswered comments; all 28 were in a third-party group, >1 month old, access lapsed. **A backlog counter without age and ownership generates guilt, not work.**

## Build order

1. Ledger (who / verbatim / outcome).
2. Same-day acknowledgement.
3. Credit line in the code.
4. Public thank-you with the outcome.
5. Smarter mining — only on sources verified to carry comments.

## Adjacent measurement

8 outbound pull requests → **1 response**, the one closing an already-open issue. Cold contributions into silence are ignored; advice given into silence behaves the same way. Attribution is the cheapest thing that keeps the second idea coming.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
