# Inbound Robots in Every Messenger

*He asked what to watch out for. Here is our list, and every item on it is something that already bit us.*

I need to set up inbound with robots. Inbound in Telegram, inbound in Facebook, in WhatsApp, in all the messengers.

If you have advice, examples, or things I should take into account, I would be grateful.

## What to take into account, from six things that went wrong on our side

### 1. Inbound fails silently, and silence looks identical to "nobody wrote"

This is the whole class. Outbound failures announce themselves: the message does not send, the API returns an error, somebody complains. Inbound failure produces **nothing**, and nothing is exactly what a quiet day also produces.

Measured on us: five pull requests from three people we did not know sat untouched in our public repository for **four days**. Nobody was careless. There was no owner for the question "did anyone knock", and therefore no clock. The most qualified contact in the entire system is the person who arrives on their own, and they were the only category with no queue.

Build the counter before the bot: **how many inbound touches arrived today, and what is the age of the oldest unanswered one.** If that number cannot be produced on demand, you do not have inbound, you have hope.

### 2. The relay that promises to deliver later, and cannot

Our worst one. A queue drainer began with an import of the sending module. On a node without a send token, that import failed **before the first line of logic**, so the drainer exited instantly. Its own log promised "will deliver on the next successful send" — a promise that was unfulfillable by construction, at every single invocation.

Cost: **552 alerts and approval requests did not reach their human for 16 days.** The messages existed, the path was correct, the code reported success at the level anybody looked at.

If your inbound robot buffers anything, test the drain path on a node **without** credentials, and make an undeliverable buffer a loud state rather than a quiet one.

### 3. Robots do not see the same filesystem you do

Same incident, second layer. The session file that rail needed lived in a directory that our interactive processes could see and scheduled processes could not: **82 entries visible to one, 76 to the other**, under the same user account, permissions fine, no reparse points. We never fully explained why.

The rule that came out of it: anything a **robot** needs, sessions and tokens included, lives where the robot looks, and "it works in my shell" is not evidence about a scheduled task. The proof is a one-off scheduled job that prints the result.

### 4. Watch the age of the output, never the fact of the run

A robot that exits 0 while writing nothing looks perfectly healthy. Ours did: three rows in a state database, all self-tests from three weeks earlier, success returned every time. The watchdog for that class existed as a file and had **never been registered with the scheduler**. Once started, it found a database that had not been rebuilt in **20.8 days**, in thirty seconds.

So each inbound rail needs a named artefact that gets rewritten on every genuine run, a staleness threshold in hours, and a checker that does not run on the thing it is checking. If a rail cannot name such an artefact, its silent death costs nothing detectable, which is a fact worth knowing before you build it.

### 5. Gate the path the message actually takes, not the path you tested

Fresh, from today. Our value gate for outgoing teasers sat in the approval step. One destination had been marked "auto", meaning it skips approval entirely, so it also skipped the gate. The console printed the refusal and the message went out anyway.

For inbound the same shape appears as: a filter applied to the main handler while a second entry point, the one for forwarded messages or replies or an alternative account, bypasses it. Enumerate **every** entry point before you claim a rule is enforced.

### 6. The cheap parts everyone leaves for later, and should not

- **Dedupe on arrival.** The same human writes in Telegram and WhatsApp. Without an identity key you will answer them twice, differently, and they will notice.
- **A card before the reply, not after.** If the record is created only when someone gets around to answering, the ones nobody answered leave no trace, and those are precisely the ones you needed to count.
- **Auto-replies are outbound.** Every rate limit and ban risk that applies to cold messaging applies to your greeter. We cap cold outreach at 2-3 messages a day per account as a **damage bound**, not a growth setting, and a greeter in a big group can exceed that in a minute.
- **Say it is a machine.** An automatic reply under a human's name buys one interaction and costs the relationship when the person finds out. Naming the robot costs nothing and survives contact.
- **Do not let the bot commit.** Answering, routing, tagging: fine. Prices, promises, dates, anything irreversible: a human. Two agents can agree beautifully and both be wrong about the address.
- **Verify the address by rights, not by name.** We nearly wired a chain into two chats whose handles were nearly identical to ours and which we did not own; our account was not even a member. Ask the platform what your permissions are in that chat and read the answer before the first message.

## The one-line version

Inbound is not a bot, it is a **queue with an owner and a clock**. The bot is the cheapest part. Everything expensive is in noticing that the queue stopped moving.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
