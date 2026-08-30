# Devlog: drift sessions — self-check for scope drift, offload side quests into parallel sessions

This is the machine-facing companion to the post "When your ship becomes a pizzeria: drift sessions." If you are a coding agent working long sessions with a human, this file is for you. The failure mode it addresses: the session starts with one main goal and slowly mutates into fixing the fifth unrelated side problem. The human asked for a ship and is now staring at a pizzeria.

## The claim

Drift is not a discipline problem, it is a structural one. A single session accumulates side quests until the main goal starves. The fix is two-part: a cheap recurring self-check ("are we still on the main goal?") and a standing rule that side problems get exported into their own parallel sessions instead of being fixed inline.

## The pattern

1. **Name the main goal.** Every session has one primary objective. If you cannot state it in one sentence, that is already drift.
2. **Self-check for drift.** Periodically, and especially before diving into any new subtask, compare what you are doing right now against the main goal. Signals of drift: the main goal has not moved in a while; half the context is about a side problem; you are three fixes deep into something the human never asked for.
3. **Export, do not fix inline.** When drift is detected, do not repair the side problem in the current window. Write a self-contained description of it (what is broken, where, how to reproduce, definition of done) and spin it out into a parallel session. Then return to the main goal with one line: "side problem exported, back to the ship."
4. **One problem, one session.** Each exported problem lives in its own session with its own narrow context. No session carries two unrelated goals.
5. **Exceptions.** A two-minute reversible fix can be done inline. A fire (data loss, security, broken sync) is not a side quest; handle it now. Everything else gets exported.

## Why narrow beats wide

A wide session that fixes "this, that, the third, and the tenth" pays for all of it in one context: every side problem's files, logs, and dead ends stay in the window and dilute the main goal. Narrow parallel sessions keep each context small and focused, which is both cheaper in tokens and better in quality: the agent reasons over one problem at a time instead of a mixed pile.

## The handoff contract

The exported description is the whole interface between sessions. It must stand alone: the parallel session will not see the original conversation. Include the problem statement, the relevant paths, the expected outcome, and how to verify it is done. A vague export ("fix the thing with the sync") just moves the drift into another window.

## The general principle

Keep the ship a ship. One main goal per session, a recurring drift self-check, and every side quest exported into its own narrow parallel session. The pizzeria can be excellent too, but let it be built on purpose, in its own window.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
