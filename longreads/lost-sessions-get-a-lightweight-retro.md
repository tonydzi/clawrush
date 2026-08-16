# Lost Sessions Get a Lightweight Retro

*Work that leaves no trace did not happen. The interesting part is not the retro, it is which machine runs it.*

I keep accumulating orphaned sessions.

I sit down with an agent, get absorbed in the work, close the window, and that is it. The result is written down nowhere, what we built is not recorded, a week later I do not remember it and the agent remembers even less. If a session closes with a retro, there is a breakdown: what we did, what we keep, where it goes. If it does not, there was work and there is no trace of it.

Yesterday I worked on making those sessions catch themselves up.

The logic came out like this:

1. A session that was never closed with a retro and is more than 5 days old gets picked up.
2. Older than 30 days, leave it alone. Too late, the context has gone stale.
3. Priority goes to the ones where something was built or code was written.
4. The retro is lightweight: not a full breakdown, a short squeeze. What was done, what of it is alive, what to forget.

And the thing I did not get to straight away: **you catch a session up somewhere other than the machine it ran on.**

## Why the obvious placement is the wrong one

My first instinct was to put the routine on every computer. Each machine has its own sessions, so let each one sort itself out. Obvious, symmetric, wrong.

Employee laptops sleep at night. A routine that only runs while a human is awake is not a routine, it is a reminder.

That is not a small distinction. A reminder needs a person to act on it, so it inherits that person's schedule, their holidays, their forgotten chargers, and their closed lid. Everything you built to run unattended now runs attended. The failure is silent: nobody gets an error, the job simply does not fire, and you find out weeks later when the thing it was supposed to produce is missing.

So the design flipped. Session transcripts already sit in shared storage. One always-on machine picks them up and does the work there. An employee's laptop can sleep as long as it likes; their work still gets processed.

**The rule generalises past retros: if background work depends on whether somebody's laptop is switched on, it will break. Move it to where nothing gets switched off.**

## The two thresholds, and why both are needed

The 5-day floor and the 30-day ceiling are doing different jobs, and dropping either one breaks the pipeline in a different way.

**The floor exists so the routine does not fight live work.** A session from this morning may still be open, may still get a proper retro from the human who ran it. Grabbing it early produces a duplicate summary and, worse, teaches you to ignore the summaries because half of them are premature.

**The ceiling exists because context rots.** A 40-day-old session can be reconstructed from its transcript, but nobody will act on the result. The files it touched have moved, the decision it made has been superseded, and the summary lands as archaeology rather than as work. Processing it costs the same tokens as a fresh one and returns nothing. That is the honest reason for the cutoff, and it is worth saying out loud: **we are not skipping old sessions because it is hard, we are skipping them because the output has no consumer.**

Priority on build-and-code sessions follows the same reasoning. A conversation that produced no artifact rarely needs a retro. A session that wrote a script, changed a config, or shipped a change has downstream consequences that outlive the session, and those are exactly the ones that hurt when they go unrecorded.

## Lightweight is a design decision, not a shortcut

A full retro asks what we learned, where each durable rule should live, what got promoted, what got dropped. It is expensive and it earns that cost when the human who did the work is still in the room.

For a five-day-old session reconstructed from a transcript, that ceremony is theatre. Nobody is going to re-litigate a decision they no longer remember making. So the catch-up retro answers three questions and stops: what was done, what of it is still alive, what to forget.

The value of the short version is that it actually gets read. A queue of forty exhaustive retros is a queue nobody opens.

## What this is really about

Two rules came out of this, and neither is specific to retros:

**Move unattended work to unattended hardware.** Anything that must happen whether or not a person is present belongs on a machine nobody closes.

**Give every automated output an expiry.** Both thresholds are versions of the same question: is there still someone who will act on this? If not, do not generate it.

So: what do you do with sessions you abandoned halfway? Throw them out, or come back to them?

---

WhatsApp +1 341 222 9178

Dev-log with the mechanics: https://github.com/tonydzi/clawrush/blob/main/devlog/lost-sessions-get-a-lightweight-retro.md
