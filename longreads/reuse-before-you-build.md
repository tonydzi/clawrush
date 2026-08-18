# Reuse Before You Build

*The rule is right. It fails for a reason nobody expects, and we tripped over it this week.*

A rule to add: always reuse the product we have already built. So we do not only build by the AK-47 principle — every time we take on a new task, we think about how to reuse the old.

For example, we have a CRM. We need to process incoming messages from leads. There are two options.

**Option 1.** The session connects Telegram MCP or Telethon and WhatsApp to itself, reads the messages from leads itself, and writes everything itself. That is silly.

**Option 2.** The CRM already monitors Telegram and WhatsApp passively, non-stop. It downloads everything from Telegram into our database; the LLM session reads the fresh messages from our own database and answers them; the CRM sends the replies as soon as the LLM has written them. The CRM is an intermediate layer between Telegram and the LLM, between WhatsApp and the LLM.

We need to think about how to keep a proper registry of everything we have. Before building something new, look at whether something old can be reused. And if something can be done without tokens, let us do it without tokens.

There are things we can build between the "brains" and external systems, so that engineering brains are not troubled with fetch-and-carry — the work of a janitor or a courier. Use the scientist to think. The courier should carry the boxes. Use the surgeon for operations, not for peeling potatoes. Because it is expensive. Because spending tokens is expensive.

## Why reuse rules fail, and it is not because people like building

They fail because **nobody can find the part.** The component exists, it works, and the person solving today's task has no way to know it is there. So "reuse before you build" is not a discipline instruction, it is a **registry** requirement — and the registry needs three fields per part, not one: what it does, **who calls it**, and which paid rail it burns.

The "who calls it" field is the one everyone skips and the one that carries the weight. We measured our own version: **95 gates capable of going red that nothing invokes**, and **19 of 25 recent rules with no caller at all.** All built correctly, all maintained, all unreachable by the next person who needed them.

## We tripped over exactly this, this week

We have a duplicate-check for posts. It compares by link and by text. It was built in advance, tested, and documented.

And a second case for the same post got created anyway — the same post, two folders, two sets of work. Why: **the duplicate-check had to be invoked as a separate command by hand**, and the "create a new case" command never called it. The door existed. It had no caller.

Hours of writing went into a duplicate before anybody noticed. The fix took ten minutes: the create command now runs the check itself and refuses on a match. Which is the general shape — **a reusable part with no caller is not reusable, it is inventory.**

## Doing it without tokens: the ladder we actually run

The instinct is right and it has a concrete form. Ours, cheapest first:

1. **SQL or a plain file read** — zero tokens. Counting, filtering, joining, deduplicating, validating, parsing. All of it is code, none of it is judgement.
2. **grep or a script** — zero tokens.
3. **Retrieval over a curated store** — a few tokens, returns the relevant slice.
4. **Model on that slice** — where judgement genuinely starts.
5. **Model on everything** — last resort, and it needs a stated reason.

A live example of the difference: our inbox takes about **658 messages a day**. A deterministic filter — does this need a human decision, is it addressed to us — leaves about **24 lines**, at zero token cost. Handing 658 messages to a model to summarise what matters would cost real money and return something worse, because the model would rank by interestingness rather than by whether a decision is required.

And the measurement that makes the whole point non-theoretical: over one week on one machine, **82% of output went to mechanical work** — running shell commands, editing code, reading files back. That is the surgeon peeling potatoes, quantified.

## The middleware idea is right, with one cost worth naming

Putting the CRM between the messenger and the model buys three things beyond tokens: credentials never enter the session, retries and duplicate deliveries are handled in one place rather than in every agent, and the message history survives the session that read it.

The cost: **a middle layer can stop silently.** If the collector dies, the model sees an empty table and reports a quiet day — indistinguishable from a genuinely quiet day. So the layer needs a freshness check on its output at the consumer's end, not a check that its process is running. We pay this bill on every collector we own; it is worth it, but it is not free.

Before building something new: does a part for this already exist, and does it have a caller? What is in your registry — and does it list who invokes each thing?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
