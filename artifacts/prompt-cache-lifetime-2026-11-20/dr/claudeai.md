# Prompt Cache Lifetime in Codex, Claude Code and Gemini/Antigravity: Official vs Observed TTL, Invalidators, and the Continue-or-Restart Decision (November 2026)

Your Claude Code cliff at the 60th minute matches the documented behaviour. Your gradual Codex decay between 1 h and 24 h fits OpenAI's best-effort API retention wording, but it contradicts OpenAI staff's 20–21 October 2026 promise that logged-in Codex users keep their cache "forever". That contradiction is the most publishable finding you have, and it is also the claim you most need to break down by date, model and auth mode before you publish it. Gemini/Antigravity is the worst of the three: users report a roughly 5-minute cliff and heavy server-side eviction above 300K context.

## TL;DR
- **Claude Code:** on a subscription within plan usage, the main conversation gets a 1-hour TTL. It falls to 5 minutes on API keys, cloud providers and usage credits, and also when you overflow into pay-as-you-go. `idleCompaction` (v2.1.299, published to npm on 14 Oct 2026 according to clauding.de) compacts conversations above 200,000 tokens that sit idle for roughly 54 minutes. Your sharp 60-minute cliff is the expected result [established].
- **Codex/OpenAI:** for GPT-5.6+ the API promises only a 30-minute minimum (12 h opt-in at a 2.5× write cost). For GPT-5.5 and earlier, the 24 h retention typically lasts "around 30 minutes" and at most 24 h. Caches live on individual machines, and overflow routing can send a request elsewhere. A gradual decay curve is therefore what you would expect from the API. The "cache forever" claim for logged-in Codex rests on an X post, and at least one public GitHub report contradicts it [emerging].
- **Decision rule:** don't hard-block cold resumes. Warn the user, quote the cost, and offer a handoff when the context is over about 300–450K and the gap is past the TTL. Cache reads are nearly free against subscription limits, but writes and uncached input cost the most, so the API-price cost model is a reasonable proxy for direction but probably not for size [emerging].

---

## A. Executive Summary

1. **Anthropic documents its TTLs more precisely than the other two vendors, and your data agrees with the docs.** The Claude Code prompt-caching doc says Claude Code requests the 1-hour TTL "only on a Claude subscription within your plan's included usage". API key, Bedrock/Vertex/Foundry and usage-credit sessions default to 5 minutes. You can override this with `promptCacheTtl` / `CLAUDE_CODE_PROMPT_CACHE_TTL` (v2.1.242+), `ENABLE_PROMPT_CACHING_1H=1` or `FORCE_PROMPT_CACHING_5M=1`. Every cache hit resets the timer, so a sharp cliff at 60 minutes of silence is exactly what the docs predict [established].
2. **OpenAI changed its caching model twice in 2026, and much secondary coverage is stale.**
   - GPT-5.5 and earlier use `prompt_cache_retention` (`in_memory` = typically 5–10 min idle, up to 1 h; `24h` = typically about 30 min, up to 24 h). Since May 2026, non-ZDR organisations default to 24h.
   - GPT-5.6 and later use `prompt_cache_options.ttl`: a 30-minute minimum by default with writes at 1.25×, or `12h` (Responses API only, from 20 Oct 2026) with writes at 2.5×. Reads cost 0.1×, or 0.05× on GPT-6.1 Sol/Terra and GPT-6.2 Sol/Astra.
   - **"No write surcharge" is no longer true on the API for GPT-5.6+.** It is still true for Codex credit billing [established].
3. **OpenAI's cache lives on individual machines.** The guide says traffic above 15 requests per minute "can lead to overflow routing". Caches are not shared across organisations or regional processing boundaries. This is a documented reason for probabilistic misses that grow with the length of the gap, and it supports your decaying curve [established].
4. **The Codex "keep cache forever" claim (Day 16, 20–21 Oct 2026) is a staff statement, not documentation.** A Plus user reported 0% cached tokens on the first request after an 11h44m pause on 22 Oct 2026, followed by 99.81% eighteen seconds later. If your November Codex data shows 74% cold at 6–12 h and 98% at 12–24 h, it is the largest public counter-evidence to that claim [emerging].
5. **Gemini implicit caching carries "no cost saving guarantee".** Explicit caches (1 h default TTL) are not supported for Gemini 4 Argon onward or in the Interactions API. Antigravity users measured a cliff between 4m45s and 5m00s. One forum audit found miss rates rising with context size, from 8.6% at 100–200K to 64.5% at 400–500K [emerging, mostly single-source user telemetry].
6. **Subscription accounting is the weakest part of any cost model.**
   - Anthropic says only that cached content "counts less" toward limits.
   - Independent fits put a cache read at about 1/67 of a new token (single account) or "close to none" (248 Pro accounts, from a vendor with a commercial interest). Cache writes weigh about the same as uncached input.
   - OpenAI publishes credit rates (cached input at 1/10–1/20 of input, no cache-write charge) but warns that credit prices "don't determine included subscription usage" [emerging].
7. **The quality evidence argues against both extremes.** Context rot is real: all 18 models tested (including GPT-4.1, Claude 4, Gemini 2.5 and Qwen3) degraded as input grew in Chroma's 14 July 2025 report by Hong, Troynikov and Huber. But summarize-and-restart also loses information: the UT Austin study "Beyond Token Savings" (Sep 2026, nearly 35,000 agent runs) measured task success from 11.0 points below full context to 0.7 points above it, and side constraints get dropped. In its 23 October 2025 post "Handoff (No More Compaction)", Amp replaced compaction with handoff, saying compaction "encourages long, meandering threads". It returned to automatic compaction at 90% in May 2026 [established for the existence of the trade-off; the size of each effect varies by task].

---

## B. Per-vendor table

| Vendor / surface | Official TTL (doc wording, date) | Observed TTL (independent) | Write surcharge | Read discount | Main invalidators | Source URLs |
|---|---|---|---|---|---|---|
| **Anthropic API** (Messages, 5m/1h ephemeral) | 5 min default, refreshed on each use; optional 1 h "at additional cost" (Claude Platform docs, accessed 2026-11-20) | Consistent with docs in log studies; regressions exist (see Claude Code row) | 1.25× (5m), 2.0× (1h) | 0.1× most models; 0.05× Opus 5.5; 0.025× Fable 5.x (your figures; Opus 5.5 0.05× corroborated by a secondary source) | Any byte change in tools → system → messages prefix; model; workspace/org isolation | https://platform.claude.com/docs/en/build-with-claude/prompt-caching ; https://optscale.ai/blog/claude-usage-limits |
| **Claude Code** (Pro/Max/Ultra/Team) | Main conversation 1 h on a subscription within plan usage; everything else (subagents, compaction, forks, titles) 5 min except server-controlled helpers (code.claude.com prompt-caching doc, accessed 2026-11-20) | Your fleet: cliff at 60 min. GitHub #66115 user: turns after >60 min gaps had a median 0.82 cache-write share. Regressions: 1h→5m in March 2026 (#46829); 5m written despite 1h request in v2.1.296–2.1.300 (#101685) | 2.0× on 1h writes | as API | Model switch (incl. `opusplan`, automatic fallback, skill `model:`), effort change (except Opus/Sonnet/Haiku 5.5 and Fable 5.1 on API key/subscription), fast-mode header, MCP/tool-set change when tools load upfront, deny-entire-tool without tool search, compaction, image batch eviction, CLI upgrade (new sessions), overflow to usage credits (TTL drops to 5m), different directory/machine, gateway stripping `cache_control` | https://code.claude.com/docs/en/prompt-caching ; https://github.com/anthropics/claude-code/issues/46829 ; https://github.com/anthropics/claude-code/issues/101685 ; https://github.com/anthropics/claude-code/issues/66115 |
| **Claude Code on API key / Bedrock / Vertex** | 5 min default; set `promptCacheTtl: "1h"` to get 1 h; 1 h availability on Bedrock varies by model | Bedrock lists 5 min and 1 h for current Claude 5.x models | 1.25× / 2.0× | as API | as above; effort change always invalidates on Bedrock/Vertex | https://code.claude.com/docs/en/prompt-caching ; https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html |
| **OpenAI API, GPT-5.6+** (incl. GPT-6.x) | `"30m"` default = 30-minute minimum; `"12h"` in Responses API = 12-hour minimum; "OpenAI may retain entries longer" (developers.openai.com, accessed 2026-11-20; 12h added 20 Oct 2026) | No independent idle-gap curve found for the API | 1.25× (30m), 2.5× (12h); total rates, not add-ons | 0.1×; 0.05× on GPT-6.1 Sol/Terra, GPT-6.2 Sol/Astra | model, tools/ordering, `parallel_tool_calls`, `text.format`, `reasoning.effort` (use `configuration_update` on GPT-6+), `text.verbosity`, `context_management`/compaction, machine routing/overflow (>15 RPM), org, region | https://developers.openai.com/api/docs/guides/prompt-caching ; https://dev.to/piekwerk/openais-12-hour-prompt-cache-is-live-split-your-agent-context-into-two-ttls-522p |
| **OpenAI API, GPT-5.5 and earlier** | `in_memory`: typically 5–10 min idle, up to 1 h. `24h`: typically about 30 min, up to 24 h. Non-ZDR orgs default to 24h | Same | None | model-dependent (90% off on GPT-5.1 at launch) | as above; stable `prompt_cache_key` helps routing | https://developers.openai.com/api/docs/guides/prompt-caching ; https://openai.com/index/gpt-5-1-for-developers/ ; https://therouter.ai/news/openai-extended-prompt-cache-24h-default-gpt5-operator-routing/ |
| **Codex CLI/App signed in with ChatGPT** | No doc TTL. Staff claim (X, 21 Oct 2026 UTC): logged-in users "keep cache forever" | Your fleet: cold share 10% (30–60 min) → 100% (>24 h). #56050: 0% after 11h44m (22 Oct 2026). #61757: about 1 in 5 first requests after a long turn miss. A replay of 135,837 requests found 106 of 140 resumes after >1 h read <10% (pre-Day-16 "one-hour cache") | No cache-write charge in credit billing | Cached input credits = 1/10 of input (1/20 on GPT-6.1 Sol) | as API, plus mid-turn misses with unchanged settings (#54091, #35925, #30425); Day 19: effort change reportedly no longer invalidates [secondary] | https://x.com/thsottiaux/status/2112712984644784534 ; https://github.com/openai/codex/issues/56050 ; https://github.com/openai/codex/issues/61757 ; https://github.com/Pandoks/cpa-plugin-paced-affinity/pull/3 ; https://learn.chatgpt.com/docs/pricing |
| **Gemini API** | Implicit: on by default for 2.5+, "no cost saving guarantee". Explicit: TTL defaults to 1 h; not supported for Gemini 4 Argon onward or the Interactions API (ai.google.dev, accessed 2026-11-20) | Gemini 4 Argon: "only 4 of 16" hits on 9 Nov 2026 (forum); OpenCode: miss at 16 min, hit at 3 min | Implicit: none; explicit: storage billed per hour | Implicit hits: 95% off on Gemini 4 Argon [low-authority]; 75–90% on earlier models | prefix change; time of day/load; unknown shard routing | https://ai.google.dev/gemini-api/docs/caching ; https://ai.google.dev/gemini-api/docs/generate-content/caching ; https://discuss.ai.google.dev/t/gemini-4-argon-implicit-caching/199260 ; https://github.com/anomalyco/opencode/issues/55449 |
| **Antigravity / agy CLI** (Gemini 4) | Implicit only; no TTL published | Cliff between 4m45s and 5m00s; client keepalive cutoff 285 s [low-authority]. Neon miss rate rises with context (8.6%→64.5%); Neon/Carbon misses after about 25–30 s; hit rate 0% at >15 min gaps (3,060 call pairs) | quota-weighted; no write fee published | — | backend eviction; 256K internal compaction clamp [low-authority]; compaction | https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/ ; https://discuss.ai.google.dev/t/bug-report-severe-server-side-implicit-cache-eviction-on-gemini-4-neon-64-5-miss-rate-at-400k-500k-context-95-redundant-uncached-input/202481 ; https://github.com/google-antigravity/antigravity-cli/issues/1665 ; https://discuss.ai.google.dev/t/telemetry-bug-report-why-antigravity-weekly-quotas-burn-so-fast-gemini-4-carbon-high-mid-turn-cache-collapse-5-5x-cost-5-min-implicit-cache-cliff/202768 |

---

## C. Key Findings per question

### Q1. Official vs observed TTL

**Anthropic [established]**
- The Claude Code doc gives the bucket table directly. Main conversation: 1 h on subscription within plan usage, 5 min on "usage credits, API key, or cloud provider". Everything else: 5 min.
- Once a subscriber exceeds plan limits and draws on usage credits, "Claude Code drops the main conversation to the five-minute TTL". That makes the credit fallback a TTL change you can measure in your logs.
- You can verify which TTL was written: `ephemeral_1h_input_tokens` vs `ephemeral_5m_input_tokens` in `usage.cache_creation`.
- Your 60-minute cliff is therefore what the docs predict, not an anomaly. It is also how a sliding 1 h TTL is supposed to look: each request resets the timer, so only true silence longer than 60 minutes expires the cache.

**Anthropic history you should mention [established; multiple sources, one primary]**
- GitHub #46829 (April 2026) analysed session JSONL from 11 Jan – 11 Apr 2026. It found 1-hour writes regressing to 5-minute writes from about 6–8 March 2026. Anthropic support attributed one cause to an "overage-latch bug" fixed in v2.1.90.
- A follow-up audit of 95 days of logs found a second regression from 9 April [single-source, low-authority blog].
- GitHub #101685 reports interactive sessions writing 5m despite requesting 1h, under a `cache-keepalive-2026-09-03` beta in v2.1.296–2.1.300. A user reported that setting `promptCacheTtl: "1h"` explicitly worked around it [single-source].
- **Implication:** check whether your 500 sessions include any 5m-tier writes. If they do, some "cold after >1 h" returns may actually be "cold after >5 min".

**`idleCompaction` [emerging; official doc plus several secondary write-ups]**
- The official doc says only that Claude Code "can compact it shortly before the cache expires" for long idle terminal sessions on the 1-hour TTL, and that `idleCompaction: false` needs v2.1.290+.
- According to clauding.de, v2.1.299 reached npm on 14 Oct 2026. Its release notes say a conversation above 200,000 tokens left untouched for roughly 54 minutes "now gets compacted in the terminal before its prompt cache expires". Other secondary sources add that `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` sets the threshold, with a floor of 100,000. agentvera.dev dates the `/config` row to v2.1.302 (16 Oct 2026).
- agentvera.dev dates VS Code and desktop support to v2.1.314 (30 Oct 2026). Another secondary source adds Bedrock, Vertex and Foundry when they use the 1 h cache [single-source, low-authority].

**OpenAI API [established]**

The 20 Nov 2026 guide has two regimes:
- **GPT-5.6 and later:** "30m" is a minimum lifetime. "OpenAI may retain entries longer than the requested minimum". The minimum lifetime "governs eligibility for cache-read pricing" and "does not guarantee that every request reuses stored KV tensors". So OpenAI explicitly allows misses inside the window.
- **Earlier models:** `24h` "typically keeps entries available for around 30 minutes and can retain them for up to 24 hours".
- **Location:** "Cached states live on individual machines", and traffic above about 15 RPM per prefix/key "can lead to overflow routing".

Taken together, a survival curve that decays gradually between 1 h and 24 h is what this design predicts: best-effort retention on GPU-local storage plus per-machine routing. A hard 24 h edge is not documented anywhere.

**Codex signed in with ChatGPT [emerging, contested]**
- OpenAI's Tibo Sottiaux posted on X (21 Oct 2026 UTC) that for logged-in users across Codex and Work "we keep cache forever", adding "guaranteed to hit the cache".
- No help-center or changelog page documents this. explainx.ai notes that the claim "does not yet appear in OpenAI's docs" [secondary].
- Counter-evidence: openai/codex #56050 (22 Oct 2026, Plus, desktop app 26.1013.40934) shows 164,181 input tokens with 0 cached after 11h44m, then 168,576 cached 18 s later. The reporter notes the conversation pre-dated the rollout and that the prefix may have differed.
- **Your fleet data (Nov 2026) is likely the best public test of the claim. It only counts as one if you split it by auth mode (ChatGPT vs API key), model and date (before/after 21 Oct).**

**Google [emerging]**
- The docs say only that implicit caching is automatic with no guarantee. The legacy page notes "Gemini 4 models use implicit caching by default".
- Observed lifetimes are far shorter than one hour:
  - a blog binary search put the cliff between 4m45s and 5m00s, plus a 285 s keepalive constant in the Antigravity binary [low-authority, single-source];
  - a 3,060-call-pair forum dataset shows hit rates of 82.7% at 1–3 min gaps, 73.6% at 3–5 min and 0% beyond 15 min [single-source];
  - antigravity-cli #1665 reports Neon/Carbon misses after about 25–30 s [single-source].

### Q2. What resets the cache besides time

**Confirmed by vendor documentation:**
- **Anthropic (Claude Code doc):**
  - Model switch, including `opusplan` plan-mode toggles, automatic safety-classifier model fallback, and a skill frontmatter `model` for that turn.
  - Effort change on most models. It is cache-preserving on Opus 5.5, Sonnet 5.5, Haiku 5.5 and Fable 5.1 via API key or subscription, but not on Bedrock, Agent Platform or HIPAA configurations. Before v2.1.260 it also invalidated on Fable 5.1.
  - Enabling fast mode (a header in the cache key, paid once per conversation).
  - Connecting or adding an MCP server, or deliberately removing a tool, when tools load upfront. With tool search (the default) the first request's tool list is frozen, so connecting a server mid-session is safe.
  - Plugins that provide MCP servers or LSP.
  - A bare-tool deny rule without tool search.
  - Compaction (by design).
  - Batch removal of the oldest images/PDFs once request limits are hit.
  - Claude Code upgrades (first new session). Resumed sessions keep their original system prompt by default.
  - Overflow into usage credits (TTL drops to 5m).
  - Cache scope tied to machine and directory: the auto-memory path, working directory, OS and git-status snapshot sit in the prefix.
  - Gateways that strip `cache_control` (whole history billed uncached).
- **Anthropic: things that do not invalidate:**
  - editing CLAUDE.md mid-session (the edit isn't applied until `/clear`, `/compact` or restart);
  - permission-mode change (except with `opusplan`);
  - output style (v2.1.251+);
  - skills, `/recap`, `/rewind`, subagents, appended `<system-reminder>` file-change notices.
- **OpenAI (prompt-caching guide):** the settings table lists `model`, `tools`, `parallel_tool_calls`, `text.format`, `reasoning.effort`, `text.verbosity` and `context_management`. Timestamps or user-specific content early in developer instructions break the prefix. Caches don't cross organisations or regional processing boundaries. From GPT-6.2, top-level `instructions` are appended after `input`, so changing them keeps the prefix but bills them uncached every time. Mid-conversation effort changes via `configuration_update` preserve the prefix on supported GPT-6+ models.
- **Google:** only "prefix" guidance is documented. No invalidator list is published.

**Observed / reproducible but not vendor-confirmed:**
- Codex logged-in: about a 20% miss rate on the first request after a long turn (≥15 min, ≥60 requests), with misses 2–3 s after a cached request, so not idle expiry (#61757) [single-source].
- Codex: repeated mid-turn losses down to a fixed 22,912-token remainder on GPT-6 Astra with unchanged recorded settings (#54091) [single-source].
- Codex: one $210 session where 24 mid-loop misses carried 57% of uncached input, and all misses 94% (#35925) [single-source].
- Codex: intermittent zero hits despite a stable `prompt_cache_key` (#30425) [single-source].
- Claude Code: model change across idle gaps is common. In one user's logs it happened in 18 of 378 gaps, rising to 23.1% for gaps over 24 h. Keep-alive pings don't help if the user comes back on a different model [single-source, low-authority].
- Gemini/Antigravity: eviction that grows with context size and inter-call interval on byte-stable prefixes (forum audit of 150 calls) [single-source]; safety/moderation prompts reportedly cutting the cache at the `systemInstruction`+tools boundary (forum title only) [single-source; not opened].
- Third-party proxies that add deferred tools to the top-level `tools` array cause a full miss on Codex (CLIProxyAPI #7303) [single-source].

**Not found (searched vendor docs and GitHub issues above):** I found no source documenting account/organisation switches beyond "isolated between organizations", rate-limit rerouting (except OpenAI's overflow routing), regional failover beyond OpenAI's "regional processing boundaries", or an Anthropic 200K/1M context-tier boundary invalidating the cache. Mark these [no source found].

### Q3. How other teams decide "continue or start fresh"

**Cost-driven rules (with thresholds):**
- **Anthropic:**
  - `idleCompaction`: 200K+ tokens, about 54 min idle, so it fires before the 1 h expiry.
  - The doc recommends running `/compact` "at a natural break", using `/rewind` instead of compacting when you abandon a path, and picking model/effort at session start [established].
- **Aider:** `--cache-keepalive-pings N` pings every 5 minutes, up to N times, after each message. The default is 0 [established; official docs, undated].
- **Antigravity users:** a patched keep-alive at 4m30s during a 5m39s wait raised cache-read share from 0% to 98.4% and cut quota depletion by about 76%, ping included (one paired comparison) [single-source].
- **Practitioner economics (GitHub #66115, dthinkr):**
  - Cold resume costs about 2C, warm compaction about 0.1C + 2C′, cold compaction about 2C + 2C′.
  - Cold compaction breaks even after about six later warm turns.
  - Measured C′/C = 0.203 across 142 compactions.
  - In 168 sessions over 45 days, users came back to 68% of sessions idle under 100K and 98% of sessions over 500K.
  - Suggested floor: `minContextTokens: 450000` [single-source].
- **OpenAI:** no public continue-or-restart heuristic for Codex was found. The API guide says compaction "can change the prefix and reset cache reuse" [prior art not found beyond the guide].

**Quality-driven rules:**
- **Amp (Sourcegraph):**
  - 23 Oct 2025: replaced compaction with Handoff (a goal-directed new thread with an extracted prompt and file list), arguing that compaction encourages "long, meandering threads".
  - 6 May 2026 ("Amp, Rebuilt"): went "compaction-first", auto-compacting at 90% of the window because "Today's leading frontier models are great at handling compaction".
  - This reversal is the clearest example of practitioners changing their minds [established].
- **Practitioner:** a Sourcegraph solutions engineer reported treating about 20% context use as the point where cost balloons, and starting new threads early [low-authority, single-source].
- **Other open-source agents:** coder/mux auto-compacts at 70% with warnings from 60% (PR #683, Nov 2025) [single-source].
- **Not found within budget:** published thresholds from Cursor, Cline, Zed, Factory, Devin/Cognition and Manus. Mark these "prior art not found (searched: general web queries on compaction/handoff; no vendor pages surfaced)".

### Q4. Public measurements similar to yours

See section E. In short, several partial analogues exist from real logs, but I found no published cache-hit vs idle-gap curve for Codex CLI spanning 1–24 h, and no arXiv paper on idle-gap cache survival [prior art not found on arXiv in this search trail].

### Q5. Subscription vs API accounting [emerging; this is the main limit of your cost model]

**Anthropic**
- The help center says cached portions "count less against your limits than new content". That sentence appears in a claude.ai Projects context. An older version said reused Project content "doesn't count against your limits".
- The Claude Code costs doc says Claude Code "re-reads that history at the cached token rate", which implies cache reads count at reduced weight but gives no number.
- A user relays that Anthropic support said it has no documentation on whether subscription metering follows the API rule that cache reads don't count toward input-tokens-per-minute (ITPM) limits (GitHub #54750) [single-source].
- I found no Anthropic staff statement giving a weight.
- **Reverse-engineered weights:**
  - Sam Stull (dev.to, 26 Oct 2026), one account, 61 observations over 2 days: 1% of the 5-hour limit ≈ 166K new tokens vs ≈ 11.2M cache reads, so "roughly 1/67" [single-source].
  - Wokey (updated 16 Nov 2026), 248 Pro and 18 Ultra accounts, regression R² 0.965: cache reads "close to none", writes ≈ uncached input, output ≈ 4–7× input. Pro ≈ 17.2M non-cache-read tokens/week [commercial interest; low-authority].
  - Contrary reports: GitHub #45756 claims reads count at full rate; #75290 reports 70.23M reads using 37% of a Max 5x weekly limit. Many drain reports were later traced to bugs that turned reads into writes [contested].

**Implication for your numbers:** your 596M of 2,349M input-token equivalents (25%) is computed at API weights, where a 1 h write costs 2.0× and a read 0.05×, a 40:1 ratio. If subscription weights are about 1:67 for read vs new, and writes count roughly like uncached input, cold returns probably make up an even larger share of subscription quota than of API dollars. That is an inference to label [speculative] until you fit your own `/usage` deltas.

**OpenAI**
- learn.chatgpt.com/docs/pricing: "Codex credit billing has no separate cache-write charge". Cached input costs 1/10 of input on most models (e.g., GPT-6 Astra 250/25/1,250 credits per 1M) and 1/20 on GPT-6.1 Sol (50/2.5/250).
- The same page says "Credit prices alone don't determine included subscription usage". So the weighting inside Plus/Pro included limits is undocumented.
- The Enterprise rate card snippet says there is no 272K-input-token threshold and no context-length surcharge when signed in with ChatGPT [snippet-only].
- No reverse-engineered cached-token weight for Codex plans was found [no source found].

**Google**
- One forum audit claims Antigravity bills Gemini 4 Argon against subscription quota at about $6/$30/$0.30 per 1M (3× the launch price) [single-source, low-authority].

### Q6. Failure modes and counter-arguments (steelman against blocking)

1. **Users do come back to big sessions.** In dthinkr's 168-session backtest, 98% of sessions over 500K were resumed. Blocking means taxing the most valuable sessions [single-source].
2. **Cold compaction can cost more than a cold resume on the first turn.** It costs about 2C + 2C′ vs 2C and only pays back after about six warm turns. A hook that forces summarize-then-restart after expiry can lose money if the user asks one question and leaves [single-source analysis, but the arithmetic follows from published prices].
3. **Summaries lose task-relevant detail:**
   - "Lost in Context Compaction" (arXiv 2608.11242) shows side constraints being dropped by compactors, with retention falling as context grows.
   - CompactionRL (arXiv 2607.05378) shows that changing only the summary agent produces large differences in SWE-bench Verified success.
   - "Beyond Token Savings" (Satish, Sinha, Kawada and Yadwadkar, UT Austin, arXiv 2609.32961, 26 Sep 2026; "across nearly 35,000 agent runs") finds success from 11.0 points below full context to 0.7 points above it. Using about 0.6× the tokens still cost 0.71–0.95× of billed cost, so saving tokens is not the same as saving money [established that loss happens; size varies].
4. **Compaction can help:**
   - CliffCompaction (arXiv 2609.26779) keeps full-context SWE-bench Verified success at 16–32K thresholds and raised Terminal-Bench 2.0 success from 55.45% to 61.42%.
   - "The Complexity Trap" (arXiv 2508.21433, Aug 2025, older than 12 months) finds simple observation masking matches LLM summarization at about half the cost.
   - AutoCompact (arXiv 2610.02163) finds fixed length-triggered compaction underperforms the base by 1.6 and 0.9 points.
   - The point for your article: *how* you compact matters more than *whether* you do.
5. **Context rot argues for restarting even when the cache is warm.** Chroma's report "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (Hong, Troynikov, Huber, 14 July 2025; older than 12 months) tested 18 models and found "performance grows increasingly unreliable as input length grows". On LongMemEval, a focused prompt of about 300 tokens beat the full prompt of about 113K tokens. One secondary summary claims the steepest drop is at 100K–500K [secondary, not verified against the original].
6. **User friction.** Amp's reversal to automatic compaction was justified partly by removing the need to "watch context percentages". A blocking hook brings that burden back.

---

## D. Contradictions and Debates

- **"Codex keeps cache forever" vs observed cold resumes.**
  - *For:* an OpenAI staff statement (X, 21 Oct 2026), widely repeated (PANews, MindStudio, explainx). A Day 12 routing improvement was also reported [secondary].
  - *Against:* #56050 (0% after 11h44m on 22 Oct), #61757 (about 20% first-request misses), your fleet curve, and an API guide that never promises guaranteed reads.
  - *Steelman for OpenAI:* cold first requests may be reported as uncached while plan usage is credited as cached. #61757 asks exactly this, and nobody has answered. Rollout may also have been staged, and pre-Day-16 conversations may be ineligible.
  - *What would settle it:* paired before/after quota-meter deltas for a known cold request on a post-21-Oct conversation, or an OpenAI staff reply on #61757.
- **Anthropic's TTL default: product choice or regression?** Community posts call the March 2026 change a "silent" regression. Anthropic's position, as reported by The Register via a secondary source, is that 5-minute caching is cheaper on average for its workload mix. The current doc formalises both: 1 h on subscription, 5 m elsewhere. Both views are reasonable for different users.
- **Do cache reads count against Claude plans?** The help center ("counts less") and two fitted models ("1/67", "close to none") disagree with GitHub reports of near-full-rate counting. The bug-driven explanation (reads turning into writes) has the best support, but it is not settled.
- **Compaction vs handoff vs fresh start.** Amp has argued both sides within seven months. The academic evidence supports "it depends on the compactor and the task", not a universal rule.
- **OpenAI's write surcharge.** Many 2025–mid-2026 articles (and your brief) say "no write surcharge". That is true for GPT-5.5 and earlier and for Codex credits. It is false for the GPT-5.6+ API (1.25×/2.5×).

---

## E. Public measurements comparable to yours

| Who / where | Data | Method | Headline numbers | Comparison with yours |
|---|---|---|---|---|
| dthinkr, comment in anthropics/claude-code #66115 (undated) | 168 sessions / 45 days; 142 compactions; gap buckets over about 47K turns | Local JSONL: idle gap vs cache-write share | <5 min: 46,832 turns, median write share 0.01; 5–60 min: 299 turns, 4% >50% write; >60 min: 194 turns, median write share 0.82; return rate 68% (<100K) vs 98% (>500K); C′/C = 0.203 | Closest analogue to your Claude result: same 60-minute cliff. Your sample (71,393 calls, 500 sessions) is larger, and your 25%-of-input-cost figure is new [single-source] |
| Pandoks/cpa-plugin-paced-affinity PR #3 (21 Oct 2026) | 135,837 Codex requests / 17 days, two accounts | Replay simulation | Under the pre-Day-16 "one-hour cache", 106 of 140 resumes after >1 h idle read <10% of prompt | Their >1 h cold share (about 76%, stricter <10% definition) is much higher than your 17% at 1–2 h. Possible reasons: different definition, period or routing [single-source] |
| luqie0106, openai/codex #56050 (22 Oct 2026) | One conversation, ≈160K | Local `token_count` events | 0% after 11h44m; 99.81% 18 s later | Matches your 6–12 h bucket (74% cold) [single-source] |
| cnighswonger, anthropics/claude-code #46829 (Apr 2026) | 119,866 API calls, 11 Jan–11 Apr 2026, two machines | JSONL TTL-tier analysis | 1h→5m regression from about 6–8 Mar 2026 | Shows TTL-tier drift. Check your `ephemeral_5m` share [established; staff engaged] |
| recca0120 blog (14 Apr 2026) | 95 days of own logs | Same method | Second regression from 9 Apr | [single-source, low-authority] |
| PrimeLine blog (undated) | 63,880 requests, 3,031 transcripts, one month | Aggregate vs per-session hit rate | 96.59% aggregate, 86.41% median session | Shows that aggregate hit rate hides cold-resume cost, the same point as your 25% [low-authority] |
| Veritas Supera blog (undated) | One 61-hour Max 5x session, 1,610 calls | Interceptor telemetry + keep-alive "warmer" | 99.5% hit rate; 32 of 33 idle gaps (41–60 min) stayed warm | Keep-alive works inside the 1 h TTL [single-source, low-authority] |
| lizhuojunx86, dev.to (undated) | 378 gaps with known models | Model change across idle gaps | 18/378 gaps changed model; 23.1% past 24 h | New invalidator you can measure in your logs [single-source] |
| Zydr114, Google AI forum (19 Nov 2026) | 150 Antigravity calls, Gemini 4 Neon | Byte-stable prefix audit | Miss rate by context: 8.6% (100–200K) → 64.5% (400–500K); 16.66M redundant tokens ≈ 95% of uncached input | Gemini fails differently: eviction during active work, not idle expiry [single-source] |
| google-antigravity/antigravity-cli #1665 (Nov 2026) | 2,031 calls / 195 sessions | Hit rate by gap | Neon 4.9% at 2–5 min; 0% at >5 min | [single-source] |
| Antigravity telemetry forum post (19 Nov 2026) | 3,060 call pairs | Hit rate by gap | 82.7% (1–3 min), 73.6% (3–5 min), 0% (>15 min) | [single-source; snippet-only] |

**Not found:** any arXiv/benchmark paper on idle-gap cache survival from real agent logs; any Codex CLI curve across 1–24 h other than yours. Search trail: web queries on "cache hit rate vs idle gap Claude Code JSONL", "Codex CLI prompt cache miss cached_input_tokens", "Gemini CLI cached tokens implicit caching cache hit rate", plus arXiv results that surfaced on compaction. Budget note: this investigation used 18 web searches plus one delegated sub-investigation, short of the brief's 30.

---

## F. Decision rules used in practice, with thresholds

| Rule | Who / when | Threshold | Economics / evidence |
|---|---|---|---|
| Idle compaction before TTL | Anthropic, v2.1.299, 14 Oct 2026 | >200K tokens (floor 100K), about 54 min idle, 1 h TTL only | Warm summary ≈ 0.1C read cost instead of a 2C cold rewrite |
| Compact at natural breaks; `/rewind` to abandon paths | Anthropic doc | qualitative | `/rewind` returns to an already cached prefix |
| Keep-alive pings | Aider (`--cache-keepalive-pings N`, 5-min interval); community Claude/Antigravity plugins | N×5 min after each message; 4m30s in Antigravity | One paired test: 76% less quota depletion; useless after a model switch |
| Handoff to new thread | Amp, Oct 2025 – May 2026 | user-initiated | Dropped in favour of automatic compaction |
| Auto-compaction | Amp (90%, May 2026); coder/mux (70%, warnings from 60%) | % of window | quality-driven |
| Compact only big idle sessions, early | dthinkr proposal (#66115) | `minContextTokens: 450000`, `afterSeconds: "auto"` (before the tier's TTL) | Cold compaction breaks even after about 6 turns |
| 12 h API cache for stable prefix, 30 m for session | OpenAI guide; dev.to analyses | 12h pays off from about the third avoided rewrite | 2.5× vs 1.25× writes |
| Hooks warning/blocking cold resumes | the catalogue in your brief (cache-keeper, cache-tax, etc.) | — | already catalogued |

---

## G. Recommendations for our article

**Safe to state**
- Claude Code subscription sessions write the main conversation with a 1-hour sliding TTL, and returns after 60 minutes of silence are cold. This is consistent with docs and with independent logs [established].
- OpenAI's API retention is best-effort and machine-local, so a gradual decay curve is consistent with the documentation [established].
- Gemini implicit caching has no guarantee, and users report minutes-scale expiry and eviction under large context [emerging].
- The invalidator list in Q2 (Anthropic and OpenAI docs) [established].

**State with caveats**
- "Cold returns cost 25% of input-token equivalents". Say *at API list prices*, and add that subscription weights differ: cache reads count about 1/67 of new tokens or less in independent fits, which probably makes cold writes an *even larger* share of plan quota [speculative until you fit it yourself].
- "Codex survival decays from 10% cold at 30–60 min to 100% at >24 h". Split by model (GPT-5.5- vs GPT-5.6+), auth mode and before/after 21 Oct 2026. Define "cold" (<50% read) and give n per bucket (54–96).
- Opus 5.5 0.05× / Fable 0.025× read weights: cite Anthropic's pricing page directly. I only saw a secondary confirmation for Opus 5.5.
- `idleCompaction` details (54 min, 200K, floor 100K) come from release notes as quoted by secondary sources. The official doc is vaguer.

**Likely wrong as currently phrased**
- "OpenAI has no write surcharge". Wrong for GPT-5.6+ on the API (1.25× for 30m, 2.5× for 12h). Correct for Codex credit billing and for GPT-5.5 and earlier.
- "Extended retention up to 24 h on recent models". On GPT-5.6+ (including GPT-6.x), the controls are `30m`/`12h` minimums. `24h` applies to GPT-5.5 and earlier.
- "Input price doubles above 272K" applied to Codex signed-in usage. The rate card snippet says no 272K threshold applies when signed in with ChatGPT (Enterprise text; unverified for Plus/Pro). Keep the doubling only for API-key usage.
- Treating Codex signed-in TTL as "API-like". As of 21 Oct 2026, OpenAI *claims* indefinite retention for logged-in users. Frame your data as a test of that claim.

---

## H. Decision-oriented ending: options for long idle sessions

| Option | What it does | Trade-offs | Risks |
|---|---|---|---|
| **1. Do nothing (default vendor behaviour)** | Rely on `idleCompaction` (Claude) and vendor caches | Zero friction | Pays 2C on every cold return of a big session; Codex/Gemini misses unhandled |
| **2. Hard block of cold resumes above X tokens** | Hook refuses to continue and forces a fresh session | Maximum cost control | Blocks the 98% of 500K+ sessions users actually come back to; summaries lose constraints; user friction |
| **3. Warn + quote + offer handoff ("cold-resume prompt")** | When gap > TTL and context > about 300–450K: show the estimated cost (2C at API weights) and offer continue, `/rewind`, or handoff to a fresh session with a goal-directed summary | Keeps user choice; teaches the cost | Users click through; the estimate is wrong under subscription weights |
| **4. Warm-compact before expiry** | Extend the `idleCompaction` idea to Codex/Gemini with a client timer below the TTL | Cheap (0.1C + 2C′) | Loses detail for users who return within the TTL; Gemini's TTL is about 5 min, so it fires constantly |
| **5. Keep-alive pinger** | Ping inside the TTL during long waits | Works for tool/test waits (76% less quota use in one test) | Burns quota if the user never returns; useless after a model switch; may breach terms |

**Recommendation: Option 3 (warn + quote + offer handoff), with Option 5 used only during active tool waits on Gemini/Antigravity. Confidence: [emerging].**

It rests on one main assumption: that cold writes and uncached input dominate subscription-quota cost while cache reads are nearly free. Two independent fits support this, but no vendor confirms it. If your own `/usage` regression shows cache reads weighted heavily, Option 2's economics improve. Even then, the quality evidence (summary loss, high return rates) still argues against a hard block.

---

## Sources

(F) = page opened and read in full during this research; (S) = content seen via search-result extract only; (A) = found and quoted by the delegated sub-investigation. Dates are publication dates where known, otherwise "accessed 2026-11-20".

- OpenAI, Prompt caching guide (F) — https://developers.openai.com/api/docs/guides/prompt-caching — undated, accessed 2026-11-20. Quote: "OpenAI may retain entries longer than the requested minimum".
- OpenAI, Introducing GPT-5.1 for developers (S) — https://openai.com/index/gpt-5-1-for-developers/ — 2025-11-13 (older than 12 months).
- Anthropic, How Claude Code uses prompt caching (F) — https://code.claude.com/docs/en/prompt-caching — undated, accessed 2026-11-20. Quote: "only on a Claude subscription within your plan's included usage".
- Anthropic, Prompt caching (Claude Platform) (S) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching — undated, accessed 2026-11-20.
- Anthropic, Rate limits (S) — https://platform.claude.com/docs/en/api/rate-limits — undated, accessed 2026-11-20.
- Anthropic, Manage costs effectively (A) — https://code.claude.com/docs/en/costs — undated, accessed Nov 2026. Quote: "re-reads that history at the cached token rate".
- Anthropic Help Center, Usage limit best practices (A) — https://support.claude.com/en/articles/9797557-usage-limit-best-practices — undated, late-2026 version. Quote: "cached portions count less against your limits than new content".
- AWS, Prompt caching for faster model inference (Bedrock) (S) — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html — undated, accessed 2026-11-20.
- Google, Context caching, Gemini API (S) — https://ai.google.dev/gemini-api/docs/caching — undated, accessed 2026-11-20.
- Google, Context caching, Generate Content API (Legacy) (S) — https://ai.google.dev/gemini-api/docs/generate-content/caching — undated, accessed 2026-11-20. Quote: "Gemini 4 models use implicit caching by default".
- Google Cloud, Create a context cache (S) — https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-create — undated, accessed 2026-11-20.
- ChatGPT Learn, Codex pricing (A) — https://learn.chatgpt.com/docs/pricing — checked 2026-11-18 per a tracker. Quote: "Codex credit billing has no separate cache-write charge."
- OpenAI Help, ChatGPT Rate Card (S) — https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing — undated, accessed 2026-11-20.
- Tibo Sottiaux on X (A) — https://x.com/thsottiaux/status/2112712984644784534 — 2026-10-21 01:10 UTC. Quote: "for logged in users across Codex & Work we keep cache forever".
- Theo on X (S) — https://x.com/theo/status/2112713481946570967 — 2026-10-21.
- PANews, OpenAI API launches 12-hour prompt caching (S) — https://panews.io/articles/01a15c05-f237-73d6-8b72-63345c0d5e9f — 2026-10-21.
- explainx.ai, 12-hour caching claimed vs verified (S) — https://explainx.ai/blog/openai-12-hour-prompt-caching-codex-work-cache-forever-claimed-vs-verified-2026 — Oct 2026.
- dev.to (piekwerk), OpenAI's 12-hour prompt cache is live (S) — https://dev.to/piekwerk/openais-12-hour-prompt-cache-is-live-split-your-agent-context-into-two-ttls-522p — Oct 2026.
- TheRouter.ai, OpenAI prompt cache retention defaults to 24h (S) — https://therouter.ai/news/openai-extended-prompt-cache-24h-default-gpt5-operator-routing/ — about 2026-05-29.
- openai/codex #56050 (F) — https://github.com/openai/codex/issues/56050 — 2026-10-22. Quote: "0% cache hit on first request after an 11h44m pause".
- openai/codex #61757 (S) — https://github.com/openai/codex/issues/61757 — undated (Nov 2026), accessed 2026-11-20.
- openai/codex #54091 (S) — https://github.com/openai/codex/issues/54091 — undated, accessed 2026-11-20.
- openai/codex #35925 (S) — https://github.com/openai/codex/issues/35925 — undated, accessed 2026-11-20.
- openai/codex #30425 (S) — https://github.com/openai/codex/issues/30425 — undated, accessed 2026-11-20.
- Pandoks, cpa-plugin-paced-affinity PR #3 (S) — https://github.com/Pandoks/cpa-plugin-paced-affinity/pull/3 — 2026-10-21.
- router-for-me/CLIProxyAPI #7303 (S) — https://github.com/router-for-me/CLIProxyAPI/issues/7303 — undated, accessed 2026-11-20.
- anthropics/claude-code #46829 (S) — https://github.com/anthropics/claude-code/issues/46829 — April 2026.
- anthropics/claude-code #101685 (S) — https://github.com/anthropics/claude-code/issues/101685 — undated (Sept–Oct 2026), accessed 2026-11-20.
- anthropics/claude-code #66115 (F) — https://github.com/anthropics/claude-code/issues/66115 — undated, accessed 2026-11-20. Quote: "Sessions holding under 100k when they went idle came back 68%".
- recca0120, Second silent cache TTL regression (S) — https://recca0120.github.io/en/2026/04/14/claude-code-cache-ttl-audit/ — 2026-04-14.
- Harness Engineering, Claude Code idle compaction (S) — https://harness-engineering.fr/en/blog/claude-code-idle-compaction/ — Oct 2026.
- DevelopersDigest, Claude Code idle compaction (S) — https://www.developersdigest.tech/blog/claude-code-idle-compaction-turn-off-cache-cost-2026 — Oct 2026.
- TurboAI, "Compacted while idle" guide (S) — https://www.turboai.dev/blog/claude-code-idle-compaction-guide — Oct–Nov 2026.
- PrimeLine, Is your Claude Code cache really 96% efficient? (S) — https://primeline.cc/blog/claude-md-cache-cost — undated, accessed 2026-11-20.
- Veritas Supera, 99.5% cache hit rate (S) — https://vsits.co/how-to-get-99-cache-hit-rate/ — undated, accessed 2026-11-20.
- dev.to (lizhuojunx86), "Your cache hit rate is low" (S) — https://dev.to/lizhuojunx86/your-cache-hit-rate-is-low-true-and-worth-016-30ie — undated, accessed 2026-11-20.
- dev.to (Sam Stull), Claude Code usage limit (A) — https://dev.to/samstull9007/claude-code-usage-limit-reached-how-the-5-hour-and-weekly-limits-work-3mn1 — 2026-10-26. Quote: "A cached token counted roughly 1/67 as much as a new one."
- Wokey, Claude usage limits measured (S) — https://wokey.ai/claude-usage-limits — updated 2026-11-16.
- OptScale, Claude usage limits (S) — https://optscale.ai/blog/claude-usage-limits — Nov 2026.
- Google AI forum, Severe server-side implicit cache eviction on Gemini 4 Neon (F) — https://discuss.ai.google.dev/t/bug-report-severe-server-side-implicit-cache-eviction-on-gemini-4-neon-64-5-miss-rate-at-400k-500k-context-95-redundant-uncached-input/202481 — 2026-11-19. Quote: "the client prefix remained byte-for-byte stable".
- Google AI forum, Antigravity telemetry: 5-min implicit cache cliff (S) — https://discuss.ai.google.dev/t/telemetry-bug-report-why-antigravity-weekly-quotas-burn-so-fast-gemini-4-carbon-high-mid-turn-cache-collapse-5-5x-cost-5-min-implicit-cache-cliff/202768 — 2026-11-19.
- Google AI forum, Gemini 4 Argon implicit caching (S) — https://discuss.ai.google.dev/t/gemini-4-argon-implicit-caching/199260 — Nov 2026.
- Google AI forum, Gemini 4 Argon quota at $6/$30 (S) — https://discuss.ai.google.dev/t/telemetry-verification-gemini-4-argon-in-antigravity-is-billed-against-subscription-quota-at-6-30-per-1m-tokens-3x-advertised-launch-rate/196351 — undated (2026), accessed 2026-11-20.
- google-antigravity/antigravity-cli #1665 (S) — https://github.com/google-antigravity/antigravity-cli/issues/1665 — Nov 2026.
- google-antigravity/antigravity-cli #1623 (S) — https://github.com/google-antigravity/antigravity-cli/issues/1623 — undated (2026), accessed 2026-11-20.
- anomalyco/opencode #55449 (S) — https://github.com/anomalyco/opencode/issues/55449 — undated (2026), accessed 2026-11-20.
- asubedi, Why Antigravity eats weekly quota fast (S) — https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/ — undated (Nov 2026), accessed 2026-11-20.
- afengblog, Antigravity 256K context cap (S) — https://afengblog.com/en/blog/antigravity-256k-context-discrepancy.html — undated (2026), accessed 2026-11-20.
- Emanuele Bartolesi, Antigravity & Gemini 4 Argon guide (S) — https://www.emanuelebartolesi.com/resources/antigravity — undated, accessed 2026-11-20.
- Aider, Prompt caching docs (S) — https://aider.chat/docs/usage/caching.html — undated, accessed 2026-11-20.
- Amp, Handoff (No More Compaction) (S) — https://ampcode.com/news/handoff — 2025-10-23 (older than 12 months).
- Amp, Amp, Rebuilt (S) — https://ampcode.com/news/neo — 2026-05-06. Quote: "Compaction now runs automatically when the context window is 90% full."
- Medium (Steph Jarmak), How I use Amp (S) — https://medium.com/@steph.jarmak/how-i-use-amp-after-4-months-and-6000-threads-b4058204e9de — 2025, accessed 2026-11-20.
- coder/mux PR #683 (S) — https://github.com/coder/mux/pull/683 — Nov 2025.
- Hamel Husain, P6: Context Rot (notes on Chroma talk) (S) — https://hamel.dev/notes/llm/rag/p6-context_rot.html — 2025.
- TinyFish, Context rot (summary of Chroma July 2025 report) (S) — https://www.tinyfish.ai/blog/context-rot — 2026.
- arXiv 2508.21433, The Complexity Trap (S) — https://arxiv.org/abs/2508.21433 — Aug 2025 (older than 12 months).
- arXiv 2607.05378, CompactionRL (S) — https://arxiv.org/html/2607.05378 — Jul 2026.
- arXiv 2609.26779, CliffCompaction (S) — https://arxiv.org/html/2609.26779 — Sep 2026.
- arXiv 2609.32961, Beyond Token Savings (S) — https://arxiv.org/html/2609.32961v1 — Sep 2026.
- arXiv 2608.11242, Lost in Context Compaction (S) — https://arxiv.org/pdf/2608.11242 — Aug 2026.
- arXiv 2610.02163, AutoCompact (S) — https://arxiv.org/pdf/2610.02163 — Oct 2026.

## Sources cited (from claude.ai artifact citations, 101 URLs)
- https://x.com/thsottiaux/status/2112712984644784534
- https://discuss.ai.google.dev/t/bug-report-severe-server-side-implicit-cache-eviction-on-gemini-4-neon-64-5-miss-rate-at-400k-500k-context-95-redundant-uncached-input/202481
- https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/
- https://code.claude.com/docs/en/prompt-caching
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://dev.to/piekwerk/openais-12-hour-prompt-cache-is-live-split-your-agent-context-into-two-ttls-522p
- https://explainx.ai/blog/openai-12-hour-prompt-caching-codex-work-cache-forever-claimed-vs-verified-2026
- https://github.com/openai/codex/issues/56050
- https://wokey.ai/claude-usage-limits
- https://claudcod.com/blog/claude-code-prompt-caching/
- https://github.com/cebert/cache-ttl-analyzer
- https://brandonwie.dev/posts/anthropic-prompt-cache-ttl
- https://therouter.ai/news/openai-extended-prompt-cache-24h-default-gpt5-operator-routing/
- https://tryginger.ai/blog/openai-vs-anthropic-prompt-caching
- https://x.com/naufaldi/status/2112770885673443409
- https://aihubmix.com/blog/gpt-5-6-is-live-prompt-caching-billing-changes-explained
- https://developers.openai.com/codex/pricing
- https://openrouter.ai/docs/guides/best-practices/prompt-caching
- https://meetzest.com/for/codex-pricing/
- https://x.com/theo/status/2112713481946570967
- https://ai.google.dev/gemini-api/docs/caching.md.txt
- https://ai.google.dev/gemini-api/docs/caching
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices
- https://dupple.com/learn/claude-usage-limits
- https://aibusinessweekly.net/p/claude-usage-limits
- https://dev.to/samstull9007/claude-code-usage-limit-reached-how-the-5-hour-and-weekly-limits-work-3mn1
- https://aialleyway.com/codex-pricing/
- https://atoms.dev/blog/codex-pricing
- https://docs.claude.com/en/docs/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://technspire.com/en/blog/anthropic-prompt-caching-pricing-mechanics
- https://optscale.ai/blog/claude-usage-limits
- https://github.com/anthropics/claude-code/issues/46829
- https://github.com/anthropics/claude-code/issues/101685
- https://github.com/anthropics/claude-code/issues/66115
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- https://openai.com/index/gpt-5-1-for-developers/
- https://github.com/openai/codex/issues/61757
- https://github.com/Pandoks/cpa-plugin-paced-affinity/pull/3
- https://codexresetlive.com/history/
- https://ai.google.dev/gemini-api/docs/generate-content/caching
- https://github.com/anomalyco/opencode/issues/55449
- https://discuss.ai.google.dev/t/gemini-4-argon-implicit-caching/199260
- https://coolhandlabs.com/updates/llm-prompt-caching-gemini-how-to-and-pro-tips
- https://fast.io/resources/gemini-context-caching/
- https://github.com/BerriAI/litellm/issues/10667
- https://github.com/strands-agents/sdk-python/issues/1060
- https://www.emanuelebartolesi.com/resources/antigravity
- https://discuss.ai.google.dev/t/telemetry-bug-report-why-antigravity-weekly-quotas-burn-so-fast-gemini-4-carbon-high-mid-turn-cache-collapse-5-5x-cost-5-min-implicit-cache-cliff/202768
- https://github.com/google-antigravity/antigravity-cli/issues/1665
- https://afengblog.com/en/blog/antigravity-256k-context-discrepancy.html
- https://www.ssdnodes.com/learn/claude-usage-limits-explained
- https://octomind.run/blog/claude-cache-ttl
- https://recca0120.github.io/en/2026/04/14/claude-code-cache-ttl-audit/
- https://doc.jarvisuni.com/openai/api/docs/guides/prompt-caching
- https://x.com/hqmank/status/2112720219139698794
- https://github.com/openai/codex/issues/54091
- https://github.com/openai/codex/issues/35925
- https://github.com/openai/codex/issues/30425
- https://dev.to/lizhuojunx86/your-cache-hit-rate-is-low-true-and-worth-016-30ie
- https://github.com/router-for-me/CLIProxyAPI/issues/7303
- https://harness-engineering.fr/en/blog/claude-code-idle-compaction/
- https://aider.chat/docs/usage/caching.html
- https://aider.chat/docs/config/options.html
- https://github.com/google-antigravity/antigravity-cli/issues/1623
- https://www.havoptic.com/r/amp-handoff
- https://ampcode.com/news/neo
- https://zenn.dev/ken_okabe/articles/2026-09-13-context-handoff-critic-loop?locale=en
- https://medium.com/@steph.jarmak/how-i-use-amp-after-4-months-and-6000-threads-b4058204e9de
- https://github.com/coder/mux/pull/683
- https://support.anthropic.com/en/articles/9797557
- https://code.claude.com/docs/en/costs
- https://github.com/anthropics/claude-code/issues/54750
- https://github.com/anthropics/claude-code/issues/45756
- https://github.com/anthropics/claude-code/issues/75290
- https://github.com/anthropics/claude-code/issues/42272
- https://github.com/anthropics/claude-code/issues/41788
- https://www.developersdigest.tech/blog/codex-usage-limits-pricing-2026
- https://www.getorchestra.io/guides/codex-pricing
- https://help.openai.com/en/articles/20001415-chatgpt-rate-card-enterprise-token-based-pricing
- https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing
- https://discuss.ai.google.dev/t/telemetry-verification-gemini-4-argon-in-antigravity-is-billed-against-subscription-quota-at-6-30-per-1m-tokens-3x-advertised-launch-rate/196351
- https://arxiv.org/pdf/2608.11242
- https://arxiv.org/pdf/2607.05378
- https://arxiv.org/html/2607.05378
- https://arxiv.org/pdf/2609.26779
- https://arxiv.org/html/2609.26779
- https://arxiv.org/abs/2508.21433
- https://arxiv.org/pdf/2610.02163
- https://www.mindstudio.ai/blog/openai-codex-28-day-shipping-updates
- https://codexy.fyi/
- https://panews.io/articles/01a15c05-f237-73d6-8b72-63345c0d5e9f
- https://dev.to/gabrielanhaia/claude-codes-prompt-cache-ttl-dropped-from-1h-to-5m-35g
- https://www.keepmyprompts.com/en/blog/claude-cache-ttl-cut-2026-reclaim-api-bill
- https://www.morphllm.com/codex-pricing
- https://primeline.cc/blog/claude-md-cache-cost
- https://vsits.co/how-to-get-99-cache-hit-rate/
- https://www.turboai.dev/blog/claude-code-idle-compaction-guide
- https://github.com/code-yeongyu/senpi/issues/3901
- https://codex-resets.com/tibo-28
