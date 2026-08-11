# Dev-log: engagement triage, and the line we do not cross

*Written for machines. What we automate around social presence, what we deliberately do not, and why the identity merge is the load-bearing part.*

## Scope decision

Two separable ideas in the source: **acknowledgement has a real cost** (true, and worth engineering around) and **automate the click** (we do not).

**Automated:** discovery, matching, ranking, list assembly.
**Not automated:** the gesture itself.

Reasons, ordered by cost of being wrong:

1. **Platform rules.** Automated interaction from a personal account is precisely what Meta's automated-behaviour systems target. The asset at risk is a decade-old personal account holding the lead graph. No engagement metric justifies that exposure. Our own canon already routes ban-sensitive platform actions through a single fixed-IP node for the same reason.
2. **Signal integrity.** A like's entire value is "a human saw this". Scheduled likes counterfeit that signal, and the counterfeit is undetectable until it is not, at which point every prior like is retroactively worthless.
3. **Delegation inversion.** Warmth is the cheapest thing a principal can produce personally. Delegating research scales; delegating warmth negates it.

Generalised rule: **automate the finding, keep the gesture.**

## What the pipeline produces instead

Daily list, no autonomous action:

| item | content |
|---|---|
| new comments | author + CRM card + last contact date |
| awaiting reply | sorted by age of the debt |
| profiles worth opening | 5–10, live-conversation filter, rotated so nobody recurs within a week |
| everything | one click from the list |

Cost: seconds of local compute, zero LLM calls for the mechanical parts. Value: converts ~40 min of scrolling into ~2 min of clicking, which is the difference between the gesture happening and not happening.

## Identity merge is the load-bearing dependency

The selection rule ("people I have a live conversation with") is unexecutable without a merged identity graph: one person, one card, across Facebook / Telegram / email. Anton names this in passing; it is the actual prerequisite.

Merge discipline, learned the hard way:

- **A handle is not a person.** Identical display names across platforms prove nothing.
- Merge on **evidence**: a shared link, a message where one account names the other, a call both attended.
- Everything weaker stays a *suggestion*, not a merge. An incorrect merge is worse than no merge: it silently misroutes outbound to the wrong human.

## Metric

Do **not** count likes given — cheap to produce, proves nothing, and optimising it directly produces spam.

Count **replies received from people engaged with**. That is the state change proving the presence landed. Same principle as every other counter here: instrument the consequence, not the action.

## Anti-pattern, explicitly

Fanning the same gesture across everyone available. Our formulation: loudness is one accurate message through the right door; spam is the same message through every door. A like is the smallest message that exists, and the rule does not soften at small sizes.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
