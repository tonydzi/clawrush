# Synthesis: DR26-11-20-MACSTUDIOM4-01-0251, prompt cache lifetime in coding agents

Ordered by Tony Dzi (Anton Dziatkovskii) and Mycroft, Palo Alto AI Research Lab, 2026-11-20. Written by Mycroft (AI) from the vendor reports in this folder.

Reports collected: ChatGPT Deep research, Claude Research, Grok Expert with the deep-research skill, Mistral deep-research, GLM-5.3-Flash. Each passed our length and source-count gate. The comparison below was built from the first three; Mistral and GLM were collected later and only gate-checked. A Gemini report is included only if `gemini.md` is present in this folder.

The reports gave leads. The facts below were reopened at the primary pages on 2026-11-20 (HTTP 200, quote taken from the page).

## What holds

1. **Claude Code.** The main conversation gets a one-hour cache only on a subscription within included usage; five minutes on usage credits, an API key or a cloud provider. Source: https://code.claude.com/docs/en/prompt-caching
2. **OpenAI.** For GPT-5.6 and later the cache lifetime is a minimum: 30 minutes by default (write rate 1.25x), 12 hours on request (2.5x); cache reads cost 0.1x, and 0.05x on GPT-6.1 and 6.2 models. Older models: in-memory 5 to 10 minutes up to one hour, or extended up to 24 hours. Source: https://developers.openai.com/api/docs/guides/prompt-caching
3. **Signed-in Codex.** Credit billing has "no separate cache-write charge". Source: https://learn.chatgpt.com/docs/pricing
4. **The "forever" statement.** Tibo (OpenAI), 2026-10-21: "for logged in users across Codex & Work we keep cache forever". Source: https://x.com/thsottiaux/status/2112712984644784534 . Our logs after that date and openai/codex#61757 do not show it.
5. **Gemini.** Implicit caching has "no cost saving guarantee"; explicit cache TTL defaults to one hour; a cached prefix on Google Cloud "expires no later than 24 hours after it's created, and most entries are evicted earlier". Gemini CLI on OAuth does not support cached content creation.
6. **Prior measurements.** TraceLab (arXiv 2606.30560): "after 1 hour, almost all steps miss the cache". Copilot traces (arXiv 2608.00101): 90% within a turn, 55% across turn boundaries. Wokey: 98.0% and 95.0% median hit rate on continuation within five minutes. We found no published idle-gap bucket table for Codex out to 24 hours.
7. **Plan accounting.** No vendor publishes how cache reads and writes count against subscription limits. Anthropic support says only that cached portions "count less".

## What the reports got wrong

- Grok: "editing CLAUDE.md invalidates the cache, confirmed in the docs". The docs say the cached prefix stays intact.
- Grok and Claude: "no prior art for idle-gap curves". TraceLab and the Copilot paper exist.
- ChatGPT: effort change, MCP changes and client upgrade are "not documented" Claude Code invalidators. They are documented.
- Claude: presented a table in anthropics/claude-code#66115 as the closest independent analogue of our 60-minute cliff. That comment is our own, from 2026-10-19.
- Grok: OpenAI sentences in quotation marks were paraphrases; "0.025x on Fable 5.x" holds for Fable and Mythos 5.1 and 5.2 only.
- All three explained the gradual Codex decay, each by a different retention mode, and none noticed that gpt-6.1-sol has no 24-hour mode. Three reports agreeing here is not confirmation.

## Not verified by us

Subscription meter weights from reverse engineering; the five-minute cliff reported for Antigravity (one blog); Harvard FreeInference numbers; the contents of the Mistral and GLM reports beyond the gate.

## Decision

Publish the measurement with its limits and with the control run after 2026-10-21. The 300K threshold for Claude Code and the six-hour pause for Codex stay as they are: nothing in the research contradicts them. Splitting cold calls by cause (expiry, compaction, model switch, long-turn miss) is the next measurement worth doing.
