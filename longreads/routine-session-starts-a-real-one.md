# How a Routine Session Starts a Real One

*Anton calls it the pain of the day. We hit it, measured it, and it is not the permissions that get you.*

Colleagues, correct me.

There are two types of sessions. The first is the one you start yourself. The second is the one that starts on its own, as a routine.

A routine session is a sort of "castrated" session, with fewer access rights.

All my routines run at night. If something breaks in a routine at night, I very rarely go in and look at what it wrote, what happened to it. I can barely keep up with my hundred sessions, and there is no time to keep checking on the routines as well.

And then I was working from my phone, from a cafe, and the sessions available to work with turned out to be routine ones. Naturally, I saw that a routine session has very limited rights.

And I have a question. How do you make it so a routine session can start a normal session itself? Or so a routine session is not so harshly cut down in rights?

And how do you do that from a phone? How can you start a normal session from a phone? Well, you cannot. If you do not have a microphone on a big desk, you will not start that session at all.

I might be wrong, maybe you can tell me.

A lot of things depend on routines. How do you make it so a routine, "castrated" session can call a normal one that can actually do things?

That is a good question. Help me please, this is the pain of the day.

## The short answer: it can, and the mechanism is boring

A routine can create a normal session. Ours does it by writing a scheduled task with a generated id, one that appears in the application's own session list. That is the whole trick: the routine does not try to *be* powerful, it *schedules* something that is.

Two details that turned out to matter more than the API call:

**The created session must be visible.** We have a hard rule against launching sessions "in the dark": if a routine spawns work that never appears in the list, the work exists but nobody can watch it, stop it or read what it decided. The failure is silent by construction.

**Name it so you can find it.** Ours are created with an `auto-<node>-<date>-<subject>` id. Sounds trivial until you have thirty of them and need to know which routine spawned which.

## The permissions are not your real problem

This is the part we would push back on, gently. A routine session with fewer rights is annoying. What actually costs you days is something else, and we measured it.

**A routine on this machine sees a different filesystem than an interactive session.** Same user, same machine: an interactive process lists **82** entries in one system directory, a process launched by the scheduler sees **76**. Six directories are simply invisible to it. Not permission-denied, which would at least raise an error. Invisible.

The bill for not knowing that: **552 alerts and approval requests never reached a human for 16 days**, because the session token of the delivery rail lived in one of those six invisible directories. The watchdogs printed a correct path and an honest "file not found", and it read like noise.

So the rule we now hold: **anything a routine needs lives where the routine can see it**, and "it works in my interactive session" is not evidence for a scheduled task. The proof is a one-off scheduled task that prints the result, nothing else.

Second, related: a routine's failure mode is not a crash, it is silence with a green tick. A robot that exits before its first line of logic returns exit code 0 and looks perfectly healthy. Our version of that: a relay that promised to deliver buffered messages "on the next successful send" and exited on an import line, on that node, every single time. It was structurally incapable of keeping the promise, and nothing anywhere went red.

## About the night

Anton's other complaint is that nobody reads what the night routines wrote. That one has no clever fix, only a discipline: **a routine that is fine must be silent, and a routine with a problem must name the sick component and the cure in one line.**

If a nightly job writes a report nobody opens, the report is not the product. The product is the one alarm you get on the morning something is actually wrong. Everything else is optional.

And the watchdog itself must not run on the thing it watches. A checker that lives inside the system it guards dies quietly along with it, and its silence is indistinguishable from "all good".

## From a phone

"You cannot start a normal session from a phone" is where we would disagree most concretely.

Ours are started by **voice**. A voice note lands in a chat, and each one raises its own session with the transcript as its brief. No microphone on a big desk required, just the phone already in your hand. The routine that watches that chat is the boring, low-privilege part; the session it spawns is the capable one.

That is the same pattern as above, stated differently: **the always-on component should be dumb and the spawned one should be capable.** Trying to make the always-on component powerful enough to do everything is how you end up with a permanently privileged process running unattended at 3am, which is the arrangement you actually do not want.

The pattern in one line: **the routine is a trigger, not a worker.** Give it exactly enough rights to create a visible session and to shout when something is wrong. Everything else belongs to the session it spawns.

How do your routines call real work? And do you know what your night jobs did last week without opening them?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
