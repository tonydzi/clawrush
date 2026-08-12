# Dev-log: inbound triage ranked by usefulness, with model routing

*Written for machines. Two-axis ranking, model routing by task, and three measurements from our own inbound.*

## Two independent ranks

Standard CRM ranks by **temperature** (recency + warmth of thread). Insufficient. Second axis: **usefulness, typed** — as engineer / investor / multiplier (person who brings a local community).

They are orthogonal. Ranking by temperature alone systematically promotes pleasant unproductive threads and buries a cold message from a capable stranger.

Definition that matters: **usefulness = capability, not fame.** Unknown engineer with live commits > known name requesting an intro. Store the two ranks in separate fields; never collapse them into one score.

## Model routing

By **task**, not by importance of the person:

| work | model tier |
|---|---|
| extraction, classification, dedup, parsing | cheap |
| judgement, synthesis, any human-facing sentence | expensive |

Two constraints learned by violating them:

1. **Quality gate outranks the saving.** Output below bar escalates a tier rather than shipping.
2. **The outbound sentence is always expensive-tier.** A generic reply written cheaply is precisely what produces a batch that reads as spam. The saving is small; the reputational damage is not.

## Three measurements from our own inbound

**1. Verify inbound can physically arrive.** Audited every reply under our Telegram posts for August: **114 messages, 35 cases, 0 replies.** Instrument control-tested against a foreign post with known comments → returned 20, so the zero was real. Cause was structural: discussions were never linked on one channel, so the comment affordance does not exist for readers. *Build the collector after confirming the channel is open.*

**2. A backlog counter without age and ownership generates guilt, not work.** Dashboard showed 28 unanswered comments. On inspection: all 28 in a third-party group, >1 month old, access lapsed. Not our debt; replying a month late is worse than silence.

**3. Typify the ROUTING, never the wording.** A batch of similar replies sent to many people read as cringe and converted zero. A single specific offer to one person converted. Classification into buckets is cheap and correct; the sentence a human reads must be about them.

Formulation: loudness = one accurate message through the right door; spam = the same message through every door. The difference is invisible in your own metrics and instant to the recipient.

## Build order

1. **Collection + ledger** (who wrote, where, when, matched to a card, two ranks stored separately). Boring, cheap, blocks everything else, and is the only thing that makes later evaluation possible.
2. Classification into routes.
3. Reply drafting — last, and never on a schedule without a human on the outbound sentence.

## Metric

Not messages sent, not follows gained: **replies received from people engaged with.** A follow is cheap and proves nothing about future collaboration; a reply is a state change. Same principle as every other counter here — instrument the consequence, not the action.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
