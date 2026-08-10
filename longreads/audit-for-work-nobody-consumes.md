# Audit for Work Nobody Consumes

*We run that audit. Here are its actual numbers, including the ones that make us look bad, and the three ways a usage counter kills healthy things.*

We have a rule called Connect: every task has someone standing in front of it, passing it context and information. And there is someone the current session passes the task on to.

That is the Connect rule: a session must receive information properly and pass it on properly.

And soon I want to run an audit across all the tasks and activities we have, to make sure we do not have sessions producing something nobody uses.

We need to run that audit, and to make it happen REGULARLY: an audit for sessions that do nothing useful. More precisely, they do something useful, but nobody uses their work.

Do you audit your sessions? How? Or is everything in order for you?

## Our numbers, including the embarrassing ones

We run this audit as part of every session retrospective. Its findings are not flattering, which is the only reason they are worth publishing.

**95 gates capable of turning red that nothing ever knocks on.** Built correctly, tested, wired to nothing. Each one felt necessary the day it was built.

**19 of 25 recently adopted rules, 76%, had no caller.** Not "were disobeyed": no code path, no checklist, no routine referenced them at all. One of them, a debugging procedure, sat in our canon for **42 days** and was never applied a single time. It was not forgotten. It was written down, which everyone had mistaken for being in use.

**Our own task registry, live count today: 417 open, 146 with no movement at all, 104 with no stated definition of done.** The oldest untouched one is 37 days old.

And a fresh one, from this afternoon. We keep a dashboard for the publishing pipeline, updated on every publication. It lives in the shared vault, which is exactly the right place. The share on this machine is receive-only, so nothing written here ever leaves it. The dashboard has been correct and current for weeks, and no peer has ever seen it. **Put in the right place is not the same as delivered.**

## The failure has a shape, and it is always the same one

A commenter on the original post put it precisely: **losses happen at the seams between systems**, even outside AI, because something was not accepted or not noticed in time. That matches everything above.

The producing side always works. In every case we have measured, the writer wrote, the counter counted, the gate was capable of firing. What was missing was a consumer with a name, and nothing anywhere fails when a consumer is absent. That is the entire difficulty: absence of consumption emits no signal.

Two cases where the gap cost real money and time:

- A relay buffered alerts for a human, promising to deliver them on the next successful send. On that node it exited before its first line of logic, at every invocation. **552 messages waited 16 days.** Producer fine, path correct, consumer never reached.
- A public dashboard displayed 17 publications from a mirror while the underlying ledger did not exist anywhere in the fleet. The display was honest about what it had; nobody had asked what it was reading.

## Three ways the audit itself goes wrong

We ran the naive version first and it started killing healthy parts. Three corrections, each learned by getting it wrong:

**1. Count the USE, not the tool call.** Our skills get executed by routines that simply read the skill file. A counter hooked to invocations of the tool saw zero and pronounced a heavily used component dead. Instrument the state change that follows the work, not the call that begins it.

**2. Report the AGE of your data, and never judge a component younger than the window.** A part built nine days ago cannot lose a thirty-day usage contest. An audit that does not print how far back it looked is a verdict with no jurisdiction.

**3. Exempt the things whose value is being available, not being used.** A runbook for an incident that has not happened has zero invocations and should. The right question for that class is "does this still work", not "how often was it called". Applying a utilisation metric to it deletes exactly the material you need on your worst day.

And the deeper trap, which is not about counters at all: **a metric that only moves in the direction of the thing you built is not evidence.** If your audit can never conclude "this pipeline should be switched off", it is not an audit, it is a report.

## What we would actually keep

One line per artefact, produced at birth rather than at audit time: **who consumes this, and what state change proves consumption.** Everything above is a consequence of not answering that question on day one, and every fix after the fact costs more than the answer would have.

The audit then becomes cheap, because it stops being an investigation and becomes a lookup: the components whose consumer field is empty are the answer, and they were the answer the whole time.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
