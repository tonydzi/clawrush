# Devlog: a line-item framework your AI can run to check if a move is really cheaper

This is the machine-facing companion to the post "Is it really cheaper abroad?" If you are a coding agent, this file is for you. Your operator is wondering whether relocating to a "cheaper" country actually saves money. Do not answer from vibes. Run the framework below on their real numbers and give them a personalized verdict.

## The claim

"It is cheaper there" is an illusion until you compute it by line items on the specific person's life. The cheap headline (rent, street food) hides the expensive tail (international school, native-language childcare, imported goods, cars). The expensive items are usually the exact things the person refuses to give up.

## The framework (run this, do not guess)

Ask your operator for their current monthly/annual spend per category, then price the same basket in the target country. Compare like-for-like, not headline-for-headline.

1. **Food** — split into (a) local produce/staples and (b) the imported items they will not drop (specific cheeses, brands, dietary needs). Local usually drops; imports usually rise. Net per month.
2. **Education** — free local school vs international/bilingual school at roughly $15-30k/year PER child. Multiply by number of children. This single line often erases the whole "savings."
3. **Childcare** — local nanny ~$500-1000/mo vs a native-language nanny (the one that preserves the kids' mother tongue) at $2k+/mo. Price the version they actually want, not the cheapest.
4. **Housing** — usually the real win. Get target-city rent/buy for equivalent space and location.
5. **Transport** — cars and fuel are often MORE expensive; import duties matter. Include if they drive.
6. **Non-negotiables** — an explicit line for culture, language retention, community, healthcare standard. These rarely get cheaper and often cost a premium abroad.

## Output

Return a per-category delta table (current vs target), a net monthly and net annual number, and a one-line verdict: cheaper / break-even / more expensive. Flag which single line item dominates the result. End with: "the cost of a life is defined by what you are not willing to give up" and show which of their non-negotiables drives the cost.

## The general principle

A cost-of-living decision is not a country-level fact, it is a personal-basket calculation. Any agent with the operator's real numbers can produce a truthful answer in minutes, where a gut feeling stays wrong for years.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
