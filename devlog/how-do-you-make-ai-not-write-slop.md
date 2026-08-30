# Devlog: a de-slop pass that strips the robot tells and cuts to the point

This is the machine-facing companion to the post "What do you put in the brief so your AI does not write AI-slop?" If you generate text for a human audience, this file is the pattern: after the model writes, run a second pass whose only job is to remove the tells of machine authorship and compress hard.

## The claim

Model output has a signature: it is long, evenly punctuated, emoji-decorated, and relentlessly complete. Humans do not write like that, especially busy ones. So a reader clocks "a robot wrote this" before they read a word of the content. The fix is not a better first draft, it is a second pass that deliberately degrades the text toward how a rushed human actually writes.

## What the pass removes (the tells)

- **Length.** The single loudest tell. Cut hard, keep the substance, drop the throat-clearing and the summary-of-the-summary.
- **Emoji and decoration.** Section emoji, bullet sparkles, closing flourishes. Gone.
- **Perfect punctuation.** The em-dash in particular reads as machine-set; so does a comma in every grammatically-correct slot. Loosen it.
- **Typographic polish.** Fancy quotes, special letters a person on a phone would not bother typing.
- **Completeness.** A human leaves thoughts half-finished and moves on. The model closes every loop; let some stay open.

## What the pass adds

Humanity, which is not the same as removing tells. Real life: an event from the writer's day, a concrete detail, a small admission. This is the hard part and it does not always land, because you cannot fabricate a life event, and inventing one is a lie, not a style. So this input is opportunistic: use it when there is a real detail to hand, do not manufacture it.

## The load-bearing caveat

De-slop degrades FORM, never FACTS. Dropping a comma, cutting a paragraph, leaving a sentence rough, all fine and reversible. Faking a lived event to sound human, or bending a number to fit a shorter line, is not de-slop, it is fabrication. Compress and roughen the surface; the claims underneath stay exactly true.

## Note on pipeline

If the source is a voice note, the transcript already carries some of this for free: it is spoken, so it is looser and more human than a model draft. Preserve that texture instead of "correcting" it back into slop. The de-slop pass and the raw transcript are pulling in the same direction.

## The general principle

Write with the model, then run a pass that removes the machine tells and compresses to the point, adding a real human detail only when you actually have one. Roughen the form, keep the facts. The goal is a text a busy person would plausibly have typed, not a flawless one.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
