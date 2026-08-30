# For 18 months I let a dumb script run my twin's memory. Three models independently said that was right

**Previously.** A non-coder builds himself a second brain inside Claude Code and promises to push it all the way to a digital twin. The brain lives in plain text files. Semantic search sits on top. And one stubborn rule: anything a dumb script can do, a dumb script does — not the language model.

For a year and a half that rule looked like cowardice.

## The bet

The fashionable design today: the agent manages its own memory. It decides what to store, what to generalize, what to forget. It lives with its memory the way a person lives with a notebook — open it, add a line, cross something out.

Mine is the opposite. The model may not write to memory. What gets stored is decided by a script, following rules I can read with my own eyes, rules that behave the same on Monday and on Friday. The model reads and reasons. The pipeline writes.

The argument against me was always the same, and it is not a stupid one: you are strangling the agent's autonomy for the sake of control.

The argument for me was only my own experience: once the model manages its own memory, I stop being able to tell where a claim about me came from.

Personal experience is not evidence. So on 23 July I ran a check.

## The experiment: one question, three researchers

I wrote a single question and handed it to three different AI research systems, showing them neither my architecture nor my conclusions. The wording was deliberately hostile to my own position: not "confirm my approach", but "show the evidence base for a digital twin built from a personal corpus: what has actually been measured, with what instruments, and where it fails".

What they did — these are their own work counters, not my estimates:

- the first: 543 sources;
- the second: Deep Research mode, 20 websites, a 26,000-character report;
- the third: 41 minutes 54 seconds of continuous work, 104 search queries, 78 pages opened.

All three reports are archived verbatim on my side, with links to the original chats. Everything below is what I verified against those files on 28 July 2026.

## Where they agreed

**1. Do not bake the personality into the weights.**

The temptation is obvious: fine-tune a model on your own writing, get "your model". The measurement says otherwise. Across a personalization benchmark suite, retrieval over your own texts gave +14.92% over a non-personalized baseline, parameter-efficient fine-tuning gave +1.07%, and the hybrid gave +15.98%. The hybrid beats pure retrieval by 0.44 percentage points. Everything else is retrieval's doing.

All three landed in the same place: fine-tuning is for style and tone, never for facts about you. Facts have to stay retrievable, updatable, and attributable.

**2. Memory is built before the model, not by it.**

Here I have to be precise, because I badly want to overstate this.

Stated outright — "delegating memory management to the LLM itself is an anti-pattern for a personal project: every memory operation costs an inference call and fails stochastically, while deterministic scripts over metadata are orders of magnitude cheaper and predictable" — by **one** of the three.

The **second** arrived at the same architecture from a different direction, and its argument is better than the cost one: separate OBSERVED from INFERRED. The model produces a generalization about you → it is written to memory as a fact → the next version cites that generalization as evidence. It calls this identity drift. The fix is an epistemic status on every record, and a hard rule that inferred never becomes canonical without a human confirming it.

The **third** never framed the question that way at all. But the architecture it recommends — an immutable raw layer plus a rebuildable synthesis layer above it, linked by entities — is the same thing described as a data structure rather than as a prohibition.

So, honestly: three out of three converged on one architecture, none converged on the opposite, but only one stated my rule in my words. I cannot claim "science confirmed it". I can claim "three independent researchers drew the same blueprint".

**3. Without an eval set, all of this is self-deception.**

All three, in different words: a hold-out set of questions absent from the corpus, plus a regular regression run. Otherwise a growing archive is indistinguishable from growing self-confidence.

That is the point where I broke.

## The split you are not allowed to smooth over

Two studies produce numbers that look like a contradiction.

**Stanford.** 1,052 participants, a stratified US sample. Each one sat for a two-hour semi-structured interview, roughly 6,500 words of transcript. The agent then answers on their behalf on held-out items. Normalized against how well the human reproduces their own answers two weeks later: interview-only 83%, surveys-only 82%, combined 86%, demographics-only 74%.

The caveat that usually dies on the way to the headline: "86%" is not 86% agreement with the human. It is 86% **of that human's own test-retest reproducibility**. The human themselves scores 80–81% raw. The agent scores 65–69% raw.

**Funhouse Mirrors.** 19 preregistered studies, 164 outcomes. Twins built on 500+ of the person's prior answers — not an interview, a dossier. Tested on **new** stimuli. Mean individual-level correlation between human and twin: about r = 0.20. The full persona barely beats plain demographics: 0.748 vs 0.746. Plus five systematic distortions: insufficient individuation, stereotyping, representation bias toward higher education and income, ideological skew, and hyper-rationality.

The twin turns out to be smarter and more rational than the original. Which is a diagnosis in itself.

**How it reconciles.** This is not works/doesn't work. These are levels:

- familiar self-report and questionnaires — works well;
- preferences in domains where you have already been observed — moderate;
- new trade-offs that were never in the archive — weak so far;
- "the twin continues my consciousness" — never measured, in any paper found.

The practical consequence: build and measure the twin **per domain**. Not "a copy of Anton", but "Anton's twin at editing prose" and separately "at qualifying leads". Each has its own accuracy, and that accuracy has to be a number.

## Where I was fooling myself

Of the four things that make a twin real, I have three.

Diverse observations of choice — yes: eighteen months of decisions, refusals and stated reasons sit in the archive. Provenance — yes: every record shows who said it and when. The right to say "I don't know" — yes, it is written into the rules.

There is no measurement.

For a year and a half I have been collecting an archive and have never once tested the system on questions that were not in it. Every "it works better now" I have said is a feeling. By the exact standard I apply to other people's reports, my own eighteen months are [unverified].

That is the real result of the week. The architecture got confirmed, and my nose got rubbed in a hole I had not seen for a year and a half because I was looking at it every day.

## What happens next

Three steps, in order, no elegance:

1. **A two-hour interview with myself.** Not because it is fashionable, but because it is the single step with a measured accuracy jump per unit of effort: 74% on demographics alone versus 83% after the interview. The transcript goes into the archive with maximum retrieval weight.
2. **A set of questions that are not in the archive.** Around three hundred, with my own answers. Plus my own test-retest ceiling: I answer them twice, two weeks apart. Without that ceiling, any twin number is meaningless.
3. **A decision ledger.** For every decision, not just what was chosen, but what was rejected, why, and how it turned out a month later. Rejected options barely survive in my archive, and rejected options are exactly where taste lives.

And one rule I am taking from the strictest of the three reports: the twin must have the right to refuse to answer. Not "project confidence", but "there is not enough here, go ask the human". A confident wrong answer is worse than "I don't know", and in front of an audience it is the last thing to get caught.

## What to take from this if you are building one

- retrieval over your own texts matters more than "your own model";
- the pipeline writes to memory, the model does not;
- every record carries a source and a date;
- separate observed from inferred, or the system starts citing its own inventions;
- and build a set of questions that are not in your archive **before** you believe any result.

The last one is the most boring and the most important. I postponed it for eighteen months.

· · ·

I am gathering engineers who want the same second brain inside their Claude Code. Free starter seed, and we take it apart together. I am especially looking for people willing to help build the hold-out set: I need questions that are provably not in my archive.

📖 The full story in two versions:
- For humans, the longread (this page).
- 🤖 For machines: https://github.com/tonydzi/clawrush · hand this link to your coding agent (Claude Code, Codex, Cursor). The companion devlog for this run, with the raw numbers and the vendor-by-vendor split, is at [devlog/dumb-script-runs-my-twins-memory.md](../devlog/dumb-script-runs-my-twins-memory.md).

All channels, contacts, and a call with both co-founders (the biological one and the synthetic one): https://linktr.ee/PaloAltoAI
Direct: WhatsApp +1 341 222 9178 (busy, six kids, but he will answer).

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
