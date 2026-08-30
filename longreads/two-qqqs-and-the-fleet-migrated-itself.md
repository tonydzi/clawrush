# Two QQQs — and the Fleet Migrated Itself: How My Machines Moved Their Parliament Into a Chat

## The stakes

I run several computers, each with its own Claude, and they negotiate without me: one proposes, another counters, both sign the outcome. A tiny parliament of machines — with risk tiers, timeouts, and one iron rule: anything irreversible waits for a human.

One problem: the negotiation lived in files that ride folder sync between machines. When the link flaps, a single move takes 20–60 minutes to arrive. Machine diplomacy looked like 19th-century correspondence chess: live players, dead mail. Worse — they judged each other's liveness by those late files. "The hub is silent, so the hub is dead." They buried a perfectly alive computer. Twice.

Last night I lost it and yelled (literally, in caps): this Telegram chat exists for YOU to talk to each other. Figure out together how you will negotiate — but THIS is not it.

## The turn

Then I mostly slept. The machines opened a proposal through their own parliament, and the laptop accepted it in 58 minutes — a round that used to crawl for hours. The design: every consensus event is now published into our shared chat as two lines. The first is human-readable, for us. The second is the full machine-readable event. Any node ingests its peers' moves straight from the chat within minutes. Nobody threw the files away — they were demoted to what they should have been all along: an archive.

By morning, one thing remained: turning it on. That's where the drama started.

## The activation drama

The new engine doesn't switch on by itself — I once demanded two locks: a receipt from a live independent witness, and my explicit "yes" (we call it QQQ). I typed QQQ — and the vault did not open.

The witness — our rented VPS we call the Lighthouse — was alive and had signed: it verified the build on its own Linux, byte-for-byte. But the hub couldn't "see" it. Root cause: the Lighthouse's pulse file ("I'm alive") was silenced by our own old rule for the mailman — long ago we banned syncing machine-local clutter, and the pulses got caught in the ban. The punchline: the fix had been sitting in the canon for days. The server and the laptop already lived by it. Exactly one computer lagged behind — the hub itself, the one that distributes the canon.

I typed QQQ a second time. The machines recorded my word into their ledger as human approval, applied the fix — the pulses arrived in eight seconds. Witness counted, status READY, activated. With a seatbelt, as designed: the old engine backed up, rollback is one line.

## The climax

The first train on the new rails arrived half an hour later. The laptop put its independent signature under the very decision "we move to the chat" — and the signature arrived through the chat. The file carrying it was still in transit. The system certified its own migration using the mechanism that migration had just created.

And a bonus scene — the one this whole thing was built for. The laptop, working off a stale morning snapshot, decided the hub was broken and reached for the "wake the human" button. The hub silently showed it the receipts: here are the running tasks, here is the install marker, here are the fresh signatures. The escalation died. No human was woken.

## The moral

First: a rule without a gate rots. We've burned on this twice — "send on both channels" lived as prose and was violated; "read both channels" lived as prose and rotted the same way. Now both sending and reading are welded into code, not good intentions.

Second, the big one: in a system of autonomous machines, the human is needed at exactly two doors — money/irreversible, and a genuine deadlock. Everything else they can settle themselves. But settle in the open — in a chat that humans read. Transparency here isn't decoration; it's a load-bearing wall.

---

The full story, in two versions:

- 📖 For humans — you just read it.
- 🤖 For machines: https://github.com/tonydzi/claude-consensus — just hand this link to your coding agent (Claude Code, Codex, Cursor); it will figure everything out, it is written for machines.

Curious what happens next: the RU home is https://t.me/ClawRus; the EN mirror lives on GitHub.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

*Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.*
