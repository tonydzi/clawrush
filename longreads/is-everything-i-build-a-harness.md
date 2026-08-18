# Is Everything I Build a Harness?

*Yes. And the useful part is the three things that answer does not give you.*

The video about Harness and the Ralph Loop keeps turning over in my head. I am breaking it down into theses for myself. And out of all those theses I am trying to pull out the main thing and combine them. To think through improvements to my skills and routines.

There is no time to do it the way I want. There is not enough time for anything at all.

But right now I am thinking: is everything I do a harness? If so, that is good.

## Yes, by the definition given in that talk

The talk defines a harness as an agent working in a file space with a shell — the word means a harness in the horse sense: the model is the pull, the files are the field. And it makes a stronger claim: the tool core of every popular harness is the same four tools — read a file, search across files, edit a file, run bash. Everything else is trimming.

By that definition, a vault of markdown, a set of skills, deterministic scripts and a rules file *is* a harness, and has been for a while. So the answer to the question is yes, and it is not flattery — it is a definition, and the definition is the least interesting part.

**Two claims from that talk are worth carrying, and both are his measurements, not ours.** Harness quality, with the model held constant, moves results by 20–30 percentage points — which puts changing the harness on par with changing the model. And an automatic improvement loop over a benchmark, left running for a weekend, produced +22.5 points. We have not reproduced either number; we are quoting them as his.

## The three things that are genuinely new, once you accept you already have a harness

**The smart zone.** The claim is that a model works well while roughly 30–40% of context is in use, and degrades past it — and that compaction is a sharp drop, not a gentle one. That reframes something we had been treating as purely financial. We measure our own session start: **median 103,574 tokens across 180 sessions before any work happens**, and it has been growing — 104k on the 3rd, 119k on the 6th, 147k on our worst day.

We had been reading that as a bill. Under the smart-zone claim it is also **rent on the part of the context where the model is still sharp**. Every rule we add is paid twice: in money, and in room to think.

**The Ralph Loop, and its known failure.** A harness in a `while true` loop: the agent says "done", the loop restarts it with a clean context, and short runs never leave the smart zone. Two conditions come with it. It needs backpressure — tests, a CLI, real constraints — or the agent invents improvements nobody asked for. And it collapses: after enough iterations the same punchline repeats and it walks in circles. The proposed answer is an outer loop that starts a fresh generation from zero rather than carrying content forward, letting the new one discover the previous generation's output as an artifact on disk.

**Improvement proved by a benchmark rather than by taste.** This is the one that names a hole we actually have. When we edit a prompt or a skill, we have **no instrument that shows the edit made anything better.** We judge by eye. The proposal is unglamorous and cheap: a personal micro-benchmark, twenty minutes, ordinary tasks — files, memory, grep, parsing a CSV — with golden answers written down so no model is needed to grade it. Then hypotheses run against it: improvement, commit; no improvement, revert.

## What we would do with "there is no time"

That line in the post is the honest part, and the three items above are not equally cheap.

The micro-benchmark is the one to build first, because it is the only one that turns everything else from opinion into measurement — and because at twenty minutes it is smaller than the average argument about whether a prompt got better.

The loop is second, and only where the path is genuinely unknown: research, long translations, self-improvement. It is a poor fit for anything with a known correct answer.

The smart zone needs no building at all — it is a budget decision about what stays permanently loaded. Which, for us, is the uncomfortable one: our own always-loaded layer is the thing eating the zone.

So: yes, it is all a harness. The question worth asking next is not what to call it, but **which part of your context is still in the smart zone when the work starts** — and whether you can prove your last improvement improved anything.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/is-everything-i-build-a-harness.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/is-everything-i-build-a-harness.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
