# To Make the Rule True, Take the Tool Away

*"I need to check whether this logic already works" is the honest line in the post. Here is how you check it, and the check pays for itself.*

Extremely important to understand: possibly right now, in MVP mode, my Claude Code sessions could work with Telegram themselves and write something to leads. But since we have the CRM, we will use exactly that.

The CRM can autonomously, without tokens, read and download to our server all the dialogues from Telegram — groups, direct messages and so on — and put them in a database. Then the Claude Code sessions, the AI sessions, work with those messages: they write messages to send and send them through the CRM. So the CRM is a layer between the LLM and Telegram.

The sessions themselves do not download from or work with Telegram directly. **I need to check whether this logic already works.**

Why is this needed? You can of course ask a Claude Code session to download messages and so on. But that is silly, it is a waste of tokens.

## The check has a precise form, and it is not reading the code

"Does the session go to Telegram directly?" cannot be answered by looking at instructions, because instructions describe intent. It is answered by one question: **can it?**

If the connector is loaded in the session, the session can — and eventually will, on some busy day, when the direct route is two steps shorter. A rule that depends on an agent choosing the longer path holds until the first time the shorter one is convenient.

So the check is: **list the tools actually available in the session.** If Telegram is among them, the logic is not in force, whatever the documentation says. And the fix is not a stricter instruction — it is removing the capability.

We have paid for the difference between those two twice this week. A duplicate-check for posts existed, was tested and documented — and a second folder for the same post got created anyway, because the create command never called the check. A rule with no enforcement is a preference. Nineteen of our last twenty-five adopted rules had no caller at all.

## Removing the connector pays twice, and the second payment is the bigger one

The post says the direct route is "a waste of tokens", and that is true in the obvious way: pulling message history through a model costs money for work a plain script does for free. Counting, filtering, deduplicating and downloading are code, not judgement.

But the larger cost is the one that does not appear on any invoice for a specific task: **every connector loaded into a session is charged on every session, forever, whether used or not.** Tool definitions are part of the standing context.

Ours, measured: **a session starts at a median 103,574 tokens** across 180 sessions, before any work happens — and that number has grown from 104k to 147k on the worst day. Heavy connectors sit inside that figure. Removing one you do not use is not a small saving; it is a saving repeated on every session for as long as the system exists.

And if a model reasons best while only part of its context is occupied, the connector is also taking up room in the part where it thinks well. Paid twice: in tokens and in headroom.

## An unplanned experiment we ran today

Our Telegram connector dropped out of the session twice today — the server disconnected on its own.

**The work continued without interruption.** Nothing in the actual task needed it, because the messages come from the database anyway. That is precisely the evidence the post is asking for: not a document saying the session should not go to Telegram, but a period during which it could not, and nothing was missed.

Which suggests the cheapest possible verification, and it costs one session: **turn the connector off and do a normal day's work.** If nothing breaks, the layer is real and the connector was rent. If something breaks, you have found the exact place where the design is not implemented yet — which is a better result than an opinion.

## One caveat on the middleware

A layer between the model and the messenger is right, and it introduces one failure the direct route does not have: **the layer can stop silently.** If the collector dies, the model reads an empty table and reports a quiet day — indistinguishable from a genuinely quiet day.

So the layer needs a freshness check on its output *at the consumer* — is the newest message in the database younger than N minutes — rather than a check that its process is running. We pay that bill on every collector we own. It is worth it, but it is not free, and it is the part people discover after the first silent morning.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/take-the-tool-away.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/take-the-tool-away.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
