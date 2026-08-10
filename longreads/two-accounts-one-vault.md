# Two Accounts, One Vault, and Where the Tokens Actually Went

*The comments said we had a leak. We went and measured it. They were right, and the leak was not where anyone guessed.*

We have had an interesting situation with tokens lately.

I am on the maximum Claude Code subscription, and the tokens ran out over the weekend. By Monday morning 80% of the weekly limit was gone.

So I set up another email and another full account for 200 dollars.

Claude Code does not care at all how many accounts you have. An account is just a door into the library. The set of books, once you are inside, can be the same one.

You log in from the new account, connect the same folder, and you are working with the same repository, the same Obsidian, the same second brain.

There was one problem. On the left there are recent chats, and in the new account they are not visible. I made them visible in both the new one and the old one. It turned out not to be simple: there is a pile of system-level detail there, and I got properly sick of it.

The result: one storage, one Obsidian, all our skills, and you can walk in from several accounts at once.

For now the limits are enough, but for how long.

Do you also run accounts on separate emails?

## The comments said we had a leak. So we measured.

Within a day the post had thirty comments, and the loudest ones all said a version of the same thing: a 200 dollar plan should be plenty, something is wrong with your setup, you are probably scanning your whole database in a dumb loop.

That is a claim about a cause, and a claim about a cause deserves the same evidence as a conclusion. So we ran a real audit over seven days of output on the hub machine. Total output: **36.8 million tokens.** The split:

- **shell commands: 54.4%**
- **writing code: 15.6%**
- **reading files: 12.4%**

That is **82% mechanics**. Not thinking, not judgement, not writing, not conversation. Running commands, editing files, reading things. Meanwhile the paid subscription of another vendor sitting right next to it was **4% consumed**, and two more paid rails had never been measured at all, not once.

So yes, there was a leak, and no, it was not a runaway database scan. The leak is architectural: the most expensive rail we own was doing the cheapest category of work, because it was the rail already in my hand.

**The rule that came out of it:** every new component we build now carries one line in its passport naming *which paid tank it burns*. "Claude, because I am Claude" is a design defect, not an answer. Orchestration, judgement, voice, live conversation stay here. Shell, code, bulk reading, extraction, first drafts, deep research get designed onto somebody else's paid subscription from the start, and the default executor is whichever rail has the most headroom left, not whichever one is habitual.

## The second thing we measured, and it is worse for a Russian-speaking audience

While we were counting, we calibrated the token cost of plain text. Cyrillic comes out at **2.17 characters per token**. Latin script: **2.81**. The same sentence in Russian costs roughly **1.3 times more** than in English.

That is not a rounding error when the thing you are paying for is a system prompt, a rules file and a knowledge base that load on every single session. Our measured session start is a median of **91,549 tokens** on one machine and **102,180** on another, and it grew from 86,748 on 31 July to 106,405 on 6 August. That is rent. You pay it every time you open a session, you agreed to it once when you built something, and it is invisible unless you go and count.

Which is why every improvement we ship now gets priced in tokens per run, per day, per month, and as a share of session start. Cheap does not mean useful; the price answers "can we afford this", never "do we need this". But an improvement whose cost nobody named is not an improvement, it is a subscription somebody signed on your behalf.

## On the multi-account part itself

The mechanic in the post is real and it works: the account is the door, the workspace is the books. What it does not do is fix the underlying arithmetic. A second door into the same library gets you a second allowance, and if 82% of what you spend is mechanics, you have bought yourself the right to keep spending it that way for another week.

Both things are worth doing. Only one of them is a fix.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
