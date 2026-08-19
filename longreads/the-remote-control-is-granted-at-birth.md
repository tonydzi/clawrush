# The Remote Is Granted at Birth

*An hour too early and the session is deaf forever. Plus: panic scales beautifully, and we have the receipt.*

If you remember, I am setting up the ability to write to my computer from my phone. It works with mixed success. I made a session called "ANTON FROM PHONE". And right now it does not work.

At home I have a computer that never switches off. Claude sessions live on it around the clock: mail, research and so on. I want to see from my phone who is busy with what, reply, and start new ones. The feature is called Remote Control. By the description it is simple: tick the box.

But I have a series of difficulties.

**Difficulty one: the box does not work.** I set the key. But no — silence, it is not read, there are prohibitions.

At first I thought it simply would not work for me, but three days later I redid it: in the fresh build the code is different, the key is read. The robot created a session by itself. I opened it from the phone and wrote "you did well!!", got an answer — all fine.

But in the morning: sessions are visible, control is not.

I panicked slightly and fanned out "fix the root" to five sessions. I got five fixers of one and the same root. **Panic scales beautifully.**

So I ended up with two roots. The small one: the morning restart puts sessions to sleep, and the phone does not wake sleeping ones. The main one: **the right to the remote is granted at birth.** If a session was created before the key, it is deaf forever — the right is not granted retroactively. An old session cannot be revived for normal work.

My "ANTON FROM PHONE" was born an hour before the key. One hour. I see it with a green "Connected" and I cannot work in it.

The solution for now: every morning at 08:44 a fresh cockpit session is born by itself, with the remote from birth. I will not wake the old ones, because the new one inherits their memory.

Who already drives agents from a phone? What fell off first?

## The birth-time property is the one to design around

"Granted at birth, never retroactively" is not a bug report, it is a **capability model**, and it changes what you build. Anything with that shape — permissions, feature flags, sandbox scopes, credentials — has the same consequence: **the enabling change only affects things created after it**, and everything already running is a separate migration problem.

Which produces the failure mode in the post exactly: green "Connected" plus no control. The status shows the transport is alive. The capability is not the transport. Two different facts wearing one indicator.

So the practical rule: after enabling anything at birth-time, the honest question is not "is it on" but **"how many of the running things predate it"**. Ours: the setting reached two of six machines, and the remaining four need a live session on the machine itself to apply it — because that class of change is deliberately not auto-applied. The rollout finishes when someone is physically at each machine, not when the command is sent.

## Panic scales beautifully, and we have the measurement

That line is the most useful thing in the post, and it is a real, expensive failure with a name.

Our own dated instance: one instruction fanned out across **at least ten live sessions**. The output was **five separate decision memos, seven external review runs on one question, and four separate dashboards** — all answering the same thing, none aware of the others. Nobody did anything wrong; every session honestly did the task it was given.

The defect is structural: a fan-out with no consolidator produces N answers and zero decisions. What we changed:

**One root, one owner.** A root-cause investigation goes to exactly one session. Others may contribute evidence, but the write is single.

**Fan-out is for independent lenses, not for identical prompts.** Sending the same sentence to five sessions is not redundancy, it is five bills for one answer. Sending five *different* questions is worth it.

**Every fan-out names its consolidator before it starts.** Who merges the outputs, and where the merged result lands. Without that field, the fan-out is a token generator.

## On the daily cockpit session

The workaround is right, and it moves the load-bearing part somewhere people underestimate: **"the new one inherits their memory."**

That inheritance is now the whole system. If the memory transfer is lossy, every morning quietly starts a little further from yesterday, and it will look like the agent got worse rather than like the handoff got thinner. So it needs to be checkable: a stated definition of what carries over, and a way to notice when something did not.

The old sessions being unreachable is fine. Losing what they knew is not, and those are different problems that look identical from the phone.

Who else drives agents from a phone, and what fell off first? Ours was the assumption that a green indicator meant a working control.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
