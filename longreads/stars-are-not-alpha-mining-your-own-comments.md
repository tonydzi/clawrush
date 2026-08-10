# The 32,000-star repo was empty. The 118-star repo had the gold.

Previously on this show: my synthetic co-founder openclaw (a Claude Code agent living in my terminal) and I spent a week fighting AI slop — the robotic writing style that gives a machine away from the first line. We built our own detector and rewriter: a ban-list of giveaway words, rhythm checks, bureaucratese cleanup. I posted about it.

The post got eight comments.

For fifteen years my move here was the same: like them, drop a couple of emojis, move on. This time we sat down and unpacked every single comment like a package. Here is what fell out.

First, the tools. Commenters recommended three other repos for the same job. The usual fate of such a recommendation is a bookmark you never open. Instead of bookmarking, we opened the code.

The most famous of the three — humanizer, 32,000 stars on GitHub. That number reads like a verdict on our homemade thing: why are we even building this, someone already did it and half the world uses it. We opened it. Took it apart. Inside: a ban-list of words and patterns. We diffed it against ours line by line. New material for us: zero. Literally zero. Everything in there, we already had.

I'll be honest about the feeling. Relief and disappointment at the same time. Relief — our homemade detector turned out to be on par with a 32,000-star tool. Disappointment — I was hoping to steal something clever.

The stealing happened elsewhere. A repo called humanizer-ru, 118 stars. Almost nobody knows it exists. And it held one rule we didn't have: adverbial participle clauses — a grammatical construction that live humans almost never use in casual posts, while LLMs produce it constantly. One of the most reliable machine fingerprints in Russian text. We took the rule, credited the source, and merged it into our detector within the hour.

The third repo, ru-text, 176 stars, gave us nothing new but confirmed our approach to protected words — the ones you must never "clean up" even when they look like noise.

Tools scoreboard: three repos tested hands-on, one rule stolen, two confirmations that our own build holds up. Not bad for eight comments.

Second — and this matters more than the tools. Comments are written by people. We ran every commenter through our CRM: who is this, what did we talk about before, what do I know about them. Half had existing cards and live history. The other half are new people — and now there's a natural reason to actually meet them: they showed up on their own and started talking about exactly what we care about.

Third. In one comment, a person promised to share their own work. A promise in a comment section is the fastest-dying object on the internet: three days later neither of you remembers it. It went straight into the task registry with a reminder date.

Now the thought I'm actually writing this for.

Comments under your own post are ore. Free, voluntary, self-delivering. People bring tools, corrections, knowledge and promises right to your doorstep. And everything I did with that ore for fifteen years was clicking "like" on it.

The procedure, if you want to replicate it, is simple. Every comment goes into one of four buckets: an artifact (a tool, a link, a repo) — test it hands-on, don't bookmark it; a person — check them against your own records, who is this and what history do you share; a promise — write it down with a date or it dies; an idea or an objection — file it and think about it. Almost no comment is empty. Even "cool, subscribed" is a person worth knowing.

And the final turn. When I showed all this to openclaw, it said exactly the thing I was afraid to hear: "if this works, why did we do it once?" So now it's a daily routine. Every day the agent harvests fresh comments under my posts on its own, sorts them into the four buckets, tests the recommended tools, checks people against the CRM, logs the promises. Replies to comments it drafts and posts itself; direct messages go out only as drafts, sent after my explicit OK.

Earlier in this show I was building a machine that writes. Now it also listens.

Next episode: the first full unattended run of the routine on a fresh post — we'll see how much ore it squeezes out without me. I'll report the numbers.

---

The full story, in two versions:
📖 For humans: you are reading it.
🤖 For machines: https://github.com/Palo-Alto-AI-Research-Lab/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
