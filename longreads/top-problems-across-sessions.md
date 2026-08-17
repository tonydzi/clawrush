# Looking for the Top 10 Problems Across 300 Sessions

*We ran it. There are not ten. Two classes account for more than half of everything that broke.*

Another thing I am doing: analysing all my sessions from the last month — 100, 200, 300 sessions. Particular attention to sessions where I was building something, retro sessions, sessions from all my computers.

The task: find the top 10 problems worth fixing. Meaning, find the problems that show up often and that may be stopping my project from working properly.

I will give it a go.

## First, the size of the haystack

One node, last 30 days: **676 sessions, 592 MB of transcripts, median transcript 76 KB.**

That number decides the method before you touch the content. Feeding 592 MB to a model to ask "what keeps going wrong" costs a great deal and returns a summary nobody can act on — because a model reading transcripts sees what was *discussed*, not what actually broke. Most discussion of a problem happens in the session where it was already understood.

## The result: it is not a top 10, it is a top 2

We keep a breakage journal — one line per incident: what broke, under what conditions, which parts were involved, hypothesis of cause. Read today:

**39 incidents. 19 distinct classes.**

| class | incidents |
|---|---|
| a scheduled task silently dead | **14** |
| the browser rail down | **8** |
| the other 17 classes | 1 each |

**Two classes are 22 of 39 incidents — 56% of everything that broke.** Seventeen classes happened exactly once and never returned.

So the honest answer to "find the top 10 problems" is: there is no meaningful tenth. Ranking a list of one-offs by frequency produces ten items of which eight are noise, and then you build ten fixes and maintain them forever.

This is why our rule is that a mechanism gets built on the **third** dated occurrence of a class, not the first. Applied to this data: 2 mechanisms deserved building, 17 did not.

## The two that do matter, and what they have in common

**A scheduled task silently dead** — 14 incidents. The job is disabled or fails to launch, and nothing anywhere goes red. The output simply stops existing, and an absent report looks exactly like a quiet day.

**The browser rail down** — 8 incidents. Authentication expires, a driver dies, an extension disconnects; work that needs a live browser stalls, and the same silence follows.

They are one failure, twice. **A component that stops does not announce it; only its output is missing, and missing output is indistinguishable from nothing-to-report.** Everything else in the journal was a genuine one-off.

Which is why the fix for both is the same and is not "fix the task" or "fix the browser": watch the **age of the output at the consumer**. Not "did the process start", not "exit code zero" — the timestamp inside the artifact somebody actually reads. That watcher must live outside the thing it watches, or it dies with it.

## Method notes, since this is the part that transfers

**Write the journal as you go; do not reconstruct it afterwards.** Reconstruction from transcripts is archaeology: expensive, incomplete, and biased toward the incidents that generated the most conversation rather than the most damage. One line at the moment of breakage costs seconds and is a fact rather than a recollection.

**Count classes, not incidents.** Fourteen occurrences of one class is one problem, not fourteen. A list sorted by raw incident count will put a single noisy component above a rare failure that eats your data.

**Deterministic first, model last.** Grouping, counting and deduplicating are code, not judgement. Use the model where judgement is needed — deciding whether two differently-worded incidents are the same class — and on a few dozen candidates, not on 592 MB.

**A frequency ranking is not a priority ranking.** The most frequent thing is often the most visible and least harmful. One silent data loss outranks fourteen annoyances. Frequency tells you what to automate away; damage tells you what to fix first.

If you have run this on your own history: how many distinct classes did you end up with, and how many were one-offs? Our ratio was 17 of 19.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/top-problems-across-sessions.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/top-problems-across-sessions.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
