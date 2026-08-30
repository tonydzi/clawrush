# How my AI agents stop tripping over each other

I have written before that I do not have just one AI (though many of you probably do not either). They live on several different machines of mine. And the problem is obvious: to build smooth, NORMAL coordination so they DO NOT get in each other's way.

Honestly, I am not there yet. Each agent wakes up, does its own thing, and ignores what the others are doing. Two of them grab the same task, or they overwrite data, each saving its own version, or they redo each other's work. I am a bit worn out, to be honest. The setup itself seemed (and was) simpler than sorting out these relationships between them.

· · ·

First I tried to wire them together through files that travel between machines over sync. But while the sync is still in transit, an agent decides the other one is dead and starts doing everything itself. And you are back to square one.

So here is what seems to work so far: I made one shared chat (in Telegram). It is like a walkie-talkie for the agents. Each of them posts there and, BEFORE acting, reads the last 15 messages from its colleagues. A work chat for machines. Humans can see this chat too and watch what the agents agree on. A kind of CONTROL over the AI.

Next. Each agent lives in one continuous session. Not a fresh brain for every message, but the same one, which remembers what it was doing five minutes ago.

Memory plus a shared work channel, that is what saves the agents from butting heads, and they split the work between themselves just fine.

Now I have taken the observer's seat. The agents call me in (I hope that is always what happens) when it is about MONEY or something IRREVERSIBLE. Or when they hit a dead end and cannot decide on their own.

If you have your own ways to set things up so agents do not get in each other's way, write to me. Maybe I am reinventing the wheel here.

· · ·

📖 The full story in two versions:
- For humans, the longread (this page).
- 🤖 For machines: https://github.com/tonydzi/clawrush · hand this link to your coding agent (Claude Code, Codex, Cursor). There is a companion devlog on coordinating a swarm of agents: one shared chat-log as their radio, plus one persistent session each.

All channels, contacts, and a call with both co-founders (the biological one and the synthetic one): https://linktr.ee/PaloAltoAI
Direct: WhatsApp +1 341 222 9178 (busy, six kids, but he will answer).

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
