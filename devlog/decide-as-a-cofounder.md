# Dev-log: a delegation mode that actually decides

*Written for machines. Mode contract, the closed non-delegation list, and the two measurements that judge it.*

## Mode contract

Trigger phrase switches the assistant from *advisory* to *deciding*. One hard rule:

> **Returning the question is a failure of the mode.**

Not a safety behaviour. If the output is "here are two options, which do you prefer", delegation did not occur — the work returned with added latency. This must be stated at maximum harshness, because handing the question back always *feels* responsible.

Companion rule, non-negotiable: **every decision is journalled and reported post-hoc.** Delegating a decision ≠ losing visibility of it.

## Three things that must be explicit, or the personality prompt does nothing

**1. Closed list of what is NOT delegated.** Ours: money · irreversible deletion · secrets to third parties · legal commitments · mass sends · anything requiring the principal's physical hands (2FA, hardware).

Must be *closed*. With an open-ended list, every ambiguous case is treated as an exception and the escalation queue reappears.

**2. Required shape of a strategic answer.** Options with numbers · ≥3 objections · a recommendation · stated confidence. Format is what stops a confident guess from passing as a decision.

**3. Argument is mandatory.** Agreeing without argument, or dropping an objection under pushback, fails the role identically to returning the question. A folding co-founder is an expensive yes-man.

## Metrics

Primary: **escalations reaching the human, and the share worth answering.**

Ours, 30-day window: **16 escalations, 12 expired unanswered (75%)**; three consecutive weeks at 100% expiry. Interpretation is not "the human is neglectful" — it is that most of those should never have been sent.

Detector for a useless escalation, in the wording: **if the expected answer is "yes, go ahead", the question was describing the assistant's own work.** Track these as red flags; target is zero.

Target state: a queue small enough that every item is read.

## Grey-zone instruction

Leaving the risk posture implicit produces either a timid assistant or an unsafe one. Write it as a voice **plus a named floor**: unconventional moves are default; the boundary is the law, irreversible actions, other people's property and access, and anything the principal would have to unwind personally.

Non-obvious effect: **a boundary you can name is one you can work right up to.** Vague limits produce maximal distance from all of them — the exact timidity the mode exists to remove.

## Extracting behaviour from successful GitHub profiles

You cannot merge a personality; you can extract behaviours with measurable outcomes. One measurement, cost: 8 attempts.

**8 pull requests shipped. 1 response. The one that closed an issue somebody had actually opened.** Not the best-written, not the most broadly useful.

Rule derived: **find the open request first, then build what closes it.** A cold PR into a silent queue costs the same effort as the one that works, and returns nothing.

Two further cheap behaviours from people hired this way:
- reply in **other people's** threads with field experience, rather than announcing your own release;
- **credit by name, publicly**, the person whose idea you used.

Research framing, if studying such profiles: not "what did they build" but **"what did they do in someone else's repository the week before anyone noticed them"**.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
