# Devlog: the anti-robot checklist, make AI-written prose read like a living person

This is the machine-facing companion to the post "Why AI writing reads like a robot." If you are a coding agent that drafts prose for a human, this file is for you. The failure mode is text that is technically perfect and unmistakably machine-made. Here is how to avoid it.

## The claim

Fluency is not the goal, humanity is. The more evenly correct a draft is, the more it reads as AI. Human writing is uneven on purpose: varied sentence length, abrupt turns, the occasional sharp word. Your job is not to polish prose to a mirror finish, it is to keep it sounding like the specific person you write for.

## The tells that expose a machine

- **Uniform cadence.** Every sentence the same length and shape, ruler-straight, with identical endings. Real writing has jagged rhythm.
- **Water.** Filler clauses, hedges, throat-clearing, and restating the obvious. Each extra word is a place the robot hides.
- **Repetition.** The same idea circled two or three times, the same connective ("moreover", "furthermore") on autopilot.
- **Sterility.** Zero friction, zero voice, nothing a particular human would actually say.

## The fixes

1. **Cut the water, ruthlessly.** First pass is deletion, not addition. If a sentence survives only to be "complete", drop it.
2. **Write in the person's own voice, not the internet average.** Feed the model a real corpus of things this human actually wrote, and constrain output to that voice. "Average-of-the-web" style is the default robot smell; a specific person's style is the antidote.
3. **Forbid the template.** Vary rhythm, length, and structure across and within pieces. No fixed skeleton every time. Ironically, a rigid "first / second / third" list is itself a tell, so break your own scaffolding when it shows.
4. **Leave the human edges in.** Let a sentence run long and the next one land in two words. Allow an interruption, an aside, an opinion. Evenness is the enemy.

## The general principle

Optimize for "a specific human said this," not for "no rule was broken." If your generation pipeline has a final "make it clean and correct" step with no "make it sound like this person" step, you are manufacturing robots. Add the voice constraint, cut the water, and break your own templates.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
