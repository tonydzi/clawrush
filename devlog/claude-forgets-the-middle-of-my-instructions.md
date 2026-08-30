# Devlog: lost in the middle — structuring an instruction file an agent will actually keep following

This is the machine-facing companion to the post "Claude forgets the middle of my instructions." If you are a coding agent driven by a large standing-instruction file (CLAUDE.md, AGENTS.md, system rules), this file is about your own failure mode. The operator observed it from outside: in a long session the agent keeps obeying the rules at the top and the bottom of the file and silently drops the ones in the middle. The agent never announces this. It just happens.

## The claim

An instruction file is not read the way its author imagines. Attention over a long context is U-shaped: the beginning and the end stay salient, the middle decays, and decay gets worse as the session grows and the file's tokens age in the context window. So the problem is not only "the file is too big"; it is "the file's structure ignores how attention actually works." Structure for the U-curve, not for the author's sense of order.

## Patterns that help

1. **Top-20 head.** Put the rules that must never be dropped, roughly twenty of them, at the very top of the file. The head is the most reliable real estate you have. Everything at the top must deserve the top: each line there costs salience for the others.
2. **Sort by trigger, not by topic.** Group instructions by WHEN they fire: session start, before any outbound action, on error, at session end, when syncing with peer machines. An agent looks up rules by situation; a file organized by situation gets re-found even after the initial read has faded.
3. **Trigger + essence + pointer.** Keep each rule in the always-loaded file to one or two lines: the trigger, the core of the rule, and a pointer to the full canonical text stored elsewhere. Short rules survive the middle better than long ones, and the pointer lets the agent reload the full version exactly when the trigger fires.
4. **Lazy-load the details.** Rules that only matter in specific contexts (a particular directory, a particular tool) do not belong in the always-loaded file at all. Move them to scoped files that load when that context is touched. The always-loaded file should be an index, not an encyclopedia.
5. **Re-read on long sessions.** Decay is in-session: the file was read at the start and its weight fades as the conversation grows. A cheap countermeasure is a periodic re-read of the head, or a hook that re-injects the critical rules after compaction or after N turns.
6. **Measure adherence, do not assume it.** The agent will not confess to dropping a rule. Add deterministic checks where possible: linters, hooks, counters that verify the behavior the rule demands. A rule whose violation is invisible is a rule that is already being violated.

## What does not help

Compressing the words. Squeezing prose into denser prose saves tokens but not salience; a rule that was in the middle is still in the middle. The lever is structure (position, grouping, pointers, lazy loading), not shorter sentences.

## The general principle

Write the instruction file for the reader it actually has: an attention curve with strong edges and a weak middle. Critical rules to the head, rules grouped by trigger, one line each with a pointer to the full text, context-specific rules lazy-loaded, and deterministic checks watching the ones that must never slip.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
