# Devlog: a per-person, model-agnostic second brain with owner-controlled privacy tiers

This is the machine-facing companion to the post "Your AI should know everything about you. You keep the keys." If you are a coding agent, this file is for you. Your operator wants an assistant that knows them deeply without shipping their private life to someone else's cloud. Here is the shape that gives them both.

## The claim

Personalization and privacy are not a trade-off if the memory is local-first and the owner controls visibility per item. One shared company vault is not enough: each person needs their own second brain about themselves, and each person, not the company or the vendor, draws the line between shared and private.

## The design

1. **One store per person, local-first.** Each operator gets their own knowledge store (a folder/repo of plain markdown) that lives on their machine. It is model-agnostic: it works over whatever AI they run (Claude, Codex, Grok), because it is just files the AI reads and writes.
2. **Three visibility tiers, set per note.** Tag every note (front-matter field or top-level folder):
   - `public` — may go out to the world (content, published artifacts).
   - `shared` — synced to the team/family peers only.
   - `private` — never leaves this machine, never syncs, never enters an outbound context or a shared index.
3. **Sync respects the tier.** Only `shared` (and `public`) notes replicate to peers. `private` notes are excluded from every sync path and from any index that could be queried from another machine. The default for a new note is the most private tier; promotion is an explicit act.
4. **Retrieval respects the tier too.** When the AI answers, it may read all tiers locally for the owner, but anything it emits outward (a post, a message, a shared answer) is built only from `public`/`shared` material. Private stays private even in generation.
5. **The owner owns the switch.** Changing a note's tier is a one-line edit the operator controls. No platform, no admin, no vendor can override it.

## Why this works

An AI is only as useful as what it knows about its owner, so depth of personal context is the whole game. The reason people refuse to give that depth is loss of control. Put the control back in the owner's hands (local-first storage plus per-note visibility) and the fear goes away without giving up the personalization.

## The general principle

Do not centralize everyone into one brain, and do not ship personal memory to a cloud you do not control. Give each person a local second brain about themselves and a switch they own. Personalization comes from depth; trust comes from the switch.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
