# Starting a Session From My Phone

*Asked on Sunday. Working the same day, proved end to end — and four of six machines still do not have it.*

Sometimes I am on the road and I need to start a new session from my phone.

I can of course connect to the computer through AnyDesk, squint at the screen on my phone, press the "new" button and so on. But that is such a pain.

I am thinking maybe it is better to make a Telegram bot that can create a new session itself. I just say: "on this machine, raise a session, start a session" — and it starts a session on that machine.

Why do I want this? Because right now I talk to Claude and ChatGPT through the ordinary interface. Meaning I talk to ChatGPT, not to Codex; to Claude, not to Claude Code. And none of those conversations are glued to my personal knowledge. I want all my queries to be cross-linked somehow.

I want the LLM to use all my knowledge, all my vaults. For that I need to properly start a session inside Codex or Claude Code. And that is exactly the session where everything should begin — build them a robot that will start all my sessions.

Not sure I explained it clearly. Share examples of how to do this better?

## The second paragraph is the real reason, and it is worth separating

The request looks like a convenience problem — a button that is annoying to press on a phone. It is not. The line underneath is the substantive one: **the chat app and the coding agent are different products with different access.**

A conversation in the phone app has no filesystem, no vault, no repository, no local tools. A session in Claude Code or Codex has all of it. So "start a session from my phone" is not about avoiding a remote-desktop click — it is the difference between an assistant that guesses from memory and one that reads your actual notes before answering. Everything else in the post follows from that.

## It works. Proved today, end to end.

We did not need the Telegram bot in the end, because the capability already existed and was switched off by default.

**The mechanism:** a setting that makes every new session available for remote control from the phone. On the current binary it is read from the user-level config; earlier this month the same key genuinely did not work — the startup gate ignored it entirely — and a newer build changed the resolution order. That is worth saying plainly, because it means **a capability being absent last week is not evidence it is absent now.**

**The proof, and it is a real one:** at 13:19 today a session was created by a robot, on a schedule, with nobody at the keyboard. It started to the second. It was opened **from the phone**, a message was typed into it — "you did well!!" — the session answered and reported back over both message rails. The full path, from "a session is raised by another session" to "a human works with it from a phone", is confirmed by a live touch, not by a log line.

**The recipe, since it transfers:** create a scheduled task with a fire time of about two minutes out, a self-contained prompt (the new session inherits nothing from its parent), and a first line asking it to reply with any word so you know it is alive. That is the whole thing. It runs from session to session with no hands at the entrance.

**The side benefit:** it also cleared a suspicion. The scheduled-task rail on that machine had looked dead a few days earlier — nine of nine failed to start. This canary proved the rail is alive, which is a different problem than the one we thought we had.

## What is honestly not done

**Four of six machines still do not have it.** Two are done — the hub and one laptop. The remaining four need a live session on the machine itself to apply the change, because the delivery is a command-type package and automatic application is deliberately forbidden for that class. That is a design decision, not a bug, and it means the rollout finishes when someone is at each machine.

Also worth stating, because it comes up immediately: **there is no session timeout knob, and none is needed.** Remote access lives as long as the local process lives. Sessions die from exactly three things: closing the application, the machine sleeping or hibernating, and losing the network for long enough. On a machine set never to sleep, sessions survive indefinitely. A session showing as not running means "not generating right now", not "disconnected" — you write to it from the phone and it wakes.

## The general rule this cost us

The version of this we had written down two weeks ago said the feature could not be enabled by configuration, with a mechanical proof: the exact function in the binary that ignored the key. That was correct then and wrong now.

**A "cannot" has an expiry date.** Ours is a week: before building a workaround for something previously proven impossible, ask the owning system again. We nearly built a Telegram bot for a capability that had quietly started working.

Have you re-checked the thing you decided was impossible? Most of those verdicts are older than the software they describe.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/start-a-session-from-my-phone.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/start-a-session-from-my-phone.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
