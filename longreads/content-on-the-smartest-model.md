# Write Content on the Smartest Model

*The rule is right. It is also unenforceable as written, and we can show exactly why.*

I have a rule: always write content on the smartest model. Content is written on the smartest model.

Right now the smartest model we have is Fable. Or in ChatGPT, the Sol model.

And I give the task not only to employees but to my code as well: that it should always check. If content is being made through a dumb model, then please, artificial director, do not be dense — point out that it is worth switching.

This rule goes into my Bible.

## We run this rule, and enforcement is the hard part

It exists on our side, worded almost identically, and it explicitly assigns the checking to the agent rather than to the person. So this is not commentary from outside — it is a rule we are supposed to enforce, and the honest report is that **enforcing it mechanically is close to impossible after the fact.**

The reason is simple: **a finished text does not carry the name of the model that wrote it.** You can sometimes guess from the flatness of the prose, but a guess is not a check, and a check that runs on taste will be wrong in both directions — flagging good cheap output and missing bad expensive output.

This is the general shape of rules that fail quietly. We measured our own: **19 of the last 25 adopted rules had no caller at all** — nothing invoked them, nothing went red when they were ignored. Correctly written and completely inert. A rule assigned to "the agent should check" without a mechanism is one of those.

## The fix is a stamp, not a detector

The same answer we arrived at from an unrelated failure: **record provenance at the moment of creation.** Engine, model, date, on every produced artifact.

That converts the question from a judgement call into a filter. "Which drafts were written on the weak model" becomes a query rather than an inspection. And the recovery becomes mechanical too: regenerate exactly those, rather than re-reading everything and hoping to notice.

We learned this the expensive way on transcripts: a weaker engine silently replaced words with plausible neighbours, and the errors were only findable because the two engines produced distinguishable output. That accident is not something to rely on. A stamp does not rely on it.

## Where the rule needs a boundary, or it costs you

"Content on the smartest model" is right for the part that is judgement: voice, argument, anything a human will read as coming from a person. It is wasteful for the mechanical half of producing content — classification, extraction, tagging, deduplication, turning a transcript into a structured list. That work is measured by correctness rather than by taste, and a cheaper model does it at a fraction of the cost.

Our split runs on that line: thinking, synthesis and voice go to the best available model; grunt work goes to the cheap one. With one gate that keeps it honest — **if the cheap output falls below the bar, escalate the piece upward rather than shipping it.** Economy that lowers quality is not economy; it is a discount taken out of the reader's experience.

There is a second, less obvious cost to "always the smartest": rate limits. Spending the best model's window on tagging means it is unavailable for the one piece that needed it. We wrote about that separately — the week the best paid model sat 95% unspent while the work ran on a weaker one is the same mistake in the other direction.

## One practical warning about the wording

A rule that names a specific model expires. Names change monthly, and a Bible entry saying "the smartest is X" is wrong within weeks and keeps being followed.

We hit this directly: a model name in our own notes came through two transcriptions in two different forms, and settling which one was real took a live search rather than memory. The rule should say **"the smartest available"**, and the current answer to that should live in one place with a date on it — so that updating the fact does not require editing the rule.

So: keep the rule, add a stamp so it can be checked, draw the line at judgement versus mechanics, and never hard-code the name of a model into a permanent document.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
