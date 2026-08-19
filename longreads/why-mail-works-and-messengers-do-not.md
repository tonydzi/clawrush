# Why the Mail Routine Works and the Messenger One Does Not

*The interaction shape in the working example is the transferable part. The ban question has an honest answer and it is not "use a better library".*

Back to the task — building routines for incoming messages. I need routines for incoming in WhatsApp, Telegram and mail.

Mail, by the way, is where I have it set up best: in the morning the robot writes to me about where and to whom I need to reply and offers reply options — I pick one or write my own. In some cases it just informs me. Everything that needs it goes into calendars and so on.

Right now all routines for all incoming should be configured, and they should probably all run on the hub.

As for WhatsApp, I need to think about how it does not get banned.

## The working example already contains the rule

The mail routine works, and it is worth naming exactly why — because the reason is not "mail is simpler".

**The robot does the reading and the drafting. The human does one click.** That is the whole design. The expensive, slow, high-volume part — going through everything, deciding what needs an answer at all, preparing a draft — happens without a person. What is left for the human is the smallest possible act: choose, or overwrite.

That is the same rule we run in a different wording: **a human belongs at the ends of the pipe, not in the middle.** The mail routine puts them at the end. A messenger routine that asks "shall I reply to this one?" thirty times a day puts them back in the middle, and it will be muted within a week.

Two details in that example that are easy to miss and carry most of the value:

**"Somewhere it just informs me."** Not everything needs a decision. A routine that turns every item into a question is a worse version of the inbox it replaced. Ours filters on exactly that predicate: does this require a human decision? About **658 messages a day** reduce to roughly **24 lines** on that test alone.

**"Puts what is needed into calendars."** The routine does not stop at telling — it changes state somewhere. That is the difference between a digest nobody reads and a thing that removes work.

## Why messengers are harder, and it is not about libraries

Mail has a real API, stable authentication and no opinion about automation. Messengers have the opposite of all three: access is through an account that belongs to a person, and platforms actively look for accounts that behave like programs.

So the honest framing of "how do I keep WhatsApp from getting banned" is: **you cannot make it safe, you can only reduce the surface.** What that means in practice, from what we actually run:

**One machine, one address, always the same.** Ban-sensitive platforms are worked from a single always-on node with a stable IP. An account that appears in three countries in one day is the classic signature. This is also why we do not do that work from laptops, however convenient.

**Rate limits below what a human would hit.** Our own comment rail runs at no more than forty actions a day with at least five minutes between them, and it counts them itself. The cap exists so the account looks like a person having a busy day, not like a script.

**No bulk anything, especially first contact.** Mass first messages are the fastest route to a ban and, separately, they do not work: we measured a batch of catch-up messages converting **zero** while one specific message to one person converted.

**A human presses send on the sensitive surfaces.** Ours do: the machine prepares the text, the person sends it. That is not timidity — it is the only version where a mistake costs one message rather than an account with a year of history in it.

And the boundary worth stating plainly: reading what your own account can already see is one thing; automating outreach at volume is another. We keep the second one human-driven, and we do not pretend the grey zone is white.

## One correction to "everything on the hub"

Running the routines on one always-on machine is right, and we run it that way for the same reason: laptops sleep, and a routine that works only while someone's lid is open is not a routine.

The cost is that this node becomes a single point of failure for every inbound channel at once. Which is fine, provided one thing: **whatever checks the routines are alive must not live on that node.** A watchdog inside the thing it watches dies with it, silently, and the symptom is an inbox that looks quiet.

We paid for that lesson at scale: **552 alerts and approval requests failed to reach a human for 16 days.** Nothing errored. The only symptom was silence.

So: copy the mail routine's shape onto the messengers — read, draft, one click, change some state — keep the sensitive send button under a human, and put the liveness check somewhere other than the hub.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/why-mail-works-and-messengers-do-not.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/why-mail-works-and-messengers-do-not.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
