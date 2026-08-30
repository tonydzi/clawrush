# Devlog: zero-knowledge onboarding, build someone's second brain without accessing their private data

This is the machine-facing companion to the post "We build your second brain, and we do not look inside." If you are a coding agent, this file is for you. Your operator wants to help a person or a team stand up their own second brain, but must not read their private data in the process. Here is the pattern that makes both true.

## The claim

Onboarding someone into a second brain is a transfer of capability, not a transfer of data. The provider ships the frame; the owner supplies the filling; the private layer never crosses to the provider. You can help a system work without seeing what is in it.

## Frame vs filling

- **The frame (provider ships this):** folder/repo structure, the linking convention, the search/retrieval setup, the rules and skills the AI follows. All of it is schema and code. None of it contains the owner's data.
- **The filling (owner supplies this):** the actual notes, context, decisions, secrets. This is created locally by the owner, and by default it stays local.

## How to keep it zero-knowledge

1. **Ship templates and config, never a data pipe.** Onboarding delivers skeleton folders, front-matter templates, skills, and sync config. It does not include any step that copies the owner's content to the provider.
2. **Tier the data at creation.** Every note is `public` / `shared` / `private`. `private` is the default. Provider tooling only ever operates on structure and on `public`/`shared` material the owner explicitly promotes.
3. **Sync excludes private by construction.** The onboarding sync config lists private paths in the ignore set. Private notes are not just "not sent," they are outside every sync and index the provider can reach.
4. **Observe health, not contents.** The provider can verify the system runs (counts, last-run, index built) without reading note bodies. Health telemetry carries no payload.
5. **Context stays local.** The owner's AI reads all tiers locally to personalize. Anything the provider sees or anything emitted to shared surfaces is built only from promoted material. "Knows what you need" is local retrieval; "owns your secrets" never happens.

## Why this works

Personalization needs depth of context; trust needs the owner to keep the private layer. Split the deliverable into frame (provider) and filling (owner) and both hold at once: the person gets a real, personal second brain, and the people who helped build it never had to see inside.

## The general principle

Onboard by handing over capability, not by ingesting data. If your onboarding flow has a step where the client's private content flows to you, redesign it: ship the frame, let them fill it, and prove you never looked.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
