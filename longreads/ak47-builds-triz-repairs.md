# AK-47 Builds, TRIZ Repairs — and the Door Between Them

*A split between building and fixing is right, and incomplete. The measurement: 19 breakage classes, 17 of them never came back.*

More about rules.

I have my oldest rule — AK-47. It is the main one, and in my instruction file it sits near the top. I build everything by that principle: repairable with a hammer, everything built super light and simple.

Now I am adding a TRIZ rule — about solving problems.

And here is what matters. AK-47 relates to BUILDING things, TRIZ to REPAIRING things. Repair and construction are different things. TRIZ and problem-solving can overlap with each other; AK-47 is an entirely different animal.

But both rules matter to me and I arrange my work according to both.

What do you say? Am I thinking about this correctly?

## The split is right. It is missing a door.

Between "build" and "repair" sits a third activity that is neither: **finding out what actually broke.**

That distinction is not pedantry, it is where the money goes. TRIZ is a method for *designing a solution*. Applied before the cause is proven, it designs an elegant solution to a problem that may not exist — and the result is indistinguishable from progress while you are producing it. You get a redesigned subsystem, a satisfying afternoon, and the original failure still there.

So we run three tools in a fixed order, and they answer three different questions.

**AK-47 — always on, at both ends.** Before building: *could the least technical person on the team fix this with a hammer?* If no, simplify the design, not the documentation. And again at acceptance, asked of the finished thing. Most teams only apply their simplicity rule at review, by which point simplifying means rewriting.

**Five whys — the investigation.** Triggered on the third repeat of a class. Immediately, without waiting, for four cases only: heavy failures, data loss, security, and any time an instrument lied to us. The last one matters more than it sounds — a broken gauge produces confident wrong decisions, which is worse than a visible outage.

**TRIZ — the design door, and it is the last one.** It opens on two conditions together: the cause is *proven*, and the obvious simple fix causes *demonstrated* harm. Before both, it is banned. Not discouraged — banned, because a clever redesign is the most enjoyable thing on the list and it will always win an argument against boring cause-finding.

## The number that made this worth counting

Since 10 August we keep a single breakage journal. One breakage, one line: what broke, under what conditions, which services were involved, and the hypothesis about the cause. Build nothing.

It currently holds **31 entries, grouping into 19 classes.**

**Seventeen of those 19 classes happened exactly once and never returned.** Two classes recurred three or more times: a dead scheduled task (9 occurrences) and a downed browser rail (5).

The old behaviour — build a mechanism for each breakage — would have produced **19 mechanisms where 2 were needed**, and then required maintaining the other seventeen forever. Each of those seventeen would have been correctly built, individually justified at the time, and permanently on the maintenance bill.

Hence the rule we now run: **a mechanism gets built on the third dated occurrence of a class.** Before that, a line in the journal and nothing else.

One carve-out, and it is not negotiable: gates standing on money, irreversible actions and security are built immediately. There, a single miss costs more than a surplus mechanism ever will. The rule is about the long tail of one-off breakages, not about fail-closed safety.

## Why this compounds

The failure mode being prevented is not "wasted afternoon". It is that **maintenance is unbudgeted and ungated by default**, while building new things requires justification. Each individual repair is locally defensible, and unbudgeted work expands until it fills the day. We measured that too, on one node over one week: 82% of output went to mechanical work — shell, code, reading files back.

The third-occurrence rule attacks that at the source. Most of what feels like unavoidable repair is a first occurrence of something that will never happen again.

## The part people miss about AK-47

It is not only a construction rule. It is also **the acceptance test for a repair**.

A fix that only its author can understand is not a fix. It is a new part, and you now maintain it. That is how repair work quietly turns into construction work without anybody deciding to build anything — and it is why the same simplicity question belongs on both ends of the process.

So: yes, the split is correct. Building and repair are different disciplines with different tools. Add the investigation door between them, keep the simplicity question on both ends, and refuse to design until you can prove what broke.

How do you fix a hard problem — by finding the cause, or by rebuilding straight away? And how do you catch the moment when it is time to investigate rather than build?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/ak47-builds-triz-repairs.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/ak47-builds-triz-repairs.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
