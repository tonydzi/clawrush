# Prompt Cache Lifetime in Coding Agents (Codex, Claude Code, Gemini) — Deep Research Report

**Research questions:** Official vs observed TTLs, non-time invalidators, continue-or-restart heuristics, comparable public measurements, subscription vs API accounting, and failure modes of cold resumes vs summarize-and-restart.  
**Scope / Date:** November 2026; prioritizes 2025–2026 sources.  
**Overall confidence:** Medium-High on official docs and Claude Code/Codex observations; Medium on Gemini CLI/Antigravity and subscription accounting (partial reverse-engineering).

## A. Executive Summary

- Claude Code (subscription, within plan) uses a documented 1-hour ephemeral cache for the main conversation that refreshes on hit; observed human-driven sessions show a sharp cold cliff at ~60 minutes, matching the TTL. Idle compaction (default on for 200k+ sessions at ~54 min) is the vendor’s built-in mitigation.<grok:render card_id="88e43b" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">117</argument></grok:render><grok:render card_id="6f51b7" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">55</argument></grok:render>
- OpenAI Responses API (GPT-5.6+) offers minimum 30-minute (default, 1.25× write) or 12-hour (2.5× write) TTLs with no hard deletion guarantee; earlier models use in-memory (typically 5–10 min inactivity, max 1 h) or extended (typically ~30 min, max 24 h). Codex CLI logged-in sessions were claimed “indefinite” by staff in October 2026, but fleet measurements show gradual decay from ~1 h to near-zero by 24 h, consistent with eviction under load and routing rather than a hard wall.<grok:render card_id="4f3c69" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">115</argument></grok:render><grok:render card_id="1ea32e" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">133</argument></grok:render>
- Gemini implicit caching is best-effort with no fixed TTL or hit guarantee (most entries <<24 h max); explicit caches have user-set TTLs (default ~1 h on older models). Gemini CLI/Antigravity rely on implicit + automatic compaction; one reverse-engineered measurement places an effective ~5-minute cliff.<grok:render card_id="95a4d1" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">151</argument></grok:render><grok:render card_id="59d428" card_type="citation_card" type="render_inline_citation"><argument name="citation_id">81</argument></grok:render>
- Non-time invalidators are extensive and documented: model switch, effort/thinking change, tool/MCP list change, system prompt or CLAUDE.md/AGENTS.md edit, compaction, certain image/tool-result changes, and client upgrades. Most are confirmed by vendor docs or reproducible tests.
- Public measurements (Wokey weekly aggregates, TraceLab arXiv traces, AGNT Cache Wars controlled pauses) show high in-session hit rates (94–98 %) but sharp or gradual drops after idle gaps matching vendor TTLs. No large published fleet log matching the exact idle-bucket curves here; closest are session-level and weekly aggregates.
- Subscription limits count cache reads (heavily discounted) and writes; Claude Code subscription 1 h writes are sometimes weighted closer to 5-minute API rates. Cold large resumes are expensive in both money and quota.
- Decision practice clusters around: compact or handoff before the known TTL on large contexts; keep-alive pings for short gaps; restart when context rot risk or idle exceeds TTL. Quality arguments for restart (context rot, lost-in-the-middle) are independent of cost.

**Confidence tags used below:** [established] widely corroborated · [emerging] early but credible · [speculative] plausible, thin evidence · [fringe] outside consensus.

## B. Per-Vendor Table

| Vendor / Surface | Official TTL | Observed TTL (coding agents) | Write Surcharge | Read Discount | Key Invalidators | Primary Sources |
|------------------|--------------|------------------------------|-----------------|---------------|------------------|-----------------|
| **OpenAI Responses / Codex** (GPT-5.6+) | Min 30 m (default) or 12 h; may retain longer. Earlier: in-memory ~5–10 min inactivity (max 1 h); extended typically ~30 min (max 24 h). Logged-in Codex claimed “forever” (Oct 2026). | Gradual decay 1–24 h (fleet); sharp mid-loop misses from prefix mutation. | 1.25× (30 m), 2.5× (12 h); none on older models. | 0.1× most; 0.05× some GPT-6.x. | Model, reasoning effort, tools, verbosity/format, compaction, session/routing (prompt_cache_key + machine), top-level instructions on some models. | https://developers.openai.com/api/docs/guides/prompt-caching (accessed Nov 2026); Tibo @thsottiaux 21 Oct 2026 |
| **Anthropic / Claude Code** | 5 min default (refresh on hit); 1 h optional. Claude Code: 1 h main conversation on subscription within plan; 5 min on API key/credits/everything else. | Sharp ~60 min cliff on human returns (fleet + others); resume can still miss even inside TTL. | 1.25× (5 min), 2× (1 h). | 0.1× most; 0.05× Opus/Sonnet 5.5; 0.025× Fable 5.x. | Model, effort (most models), MCP/tools/plugins, system/CLAUDE.md, compaction, images, fast mode, client upgrade. | https://platform.claude.com/docs/en/build-with-claude/prompt-caching; https://code.claude.com/docs/en/prompt-caching |
| **Google Gemini** (API / CLI / Antigravity) | Implicit: best-effort, no fixed TTL (max 24 h, most earlier); explicit: user TTL (default ~1 h on older). | Implicit best-effort; one Antigravity measurement ~5 min cliff. | Explicit write fee; implicit none extra. | ~90 % discount on hits (newer); 75 % older. | Any prefix change; routing/load; multi-turn rules on Gemini 4 (needs ≥~2050 new tokens for full prior). | https://ai.google.dev/gemini-api/docs/caching; Google Cloud context-cache overview |

## C. Key Findings per Question

### Q1. Official vs Observed TTL [established for Anthropic/OpenAI docs; emerging for observed decay]

**OpenAI.** Official docs (developers.openai.com/api/docs/guides/prompt-caching, Nov 2026):  
> “In-memory prompt cache retention… cached prefixes generally remain active for 5 to 10 minutes of inactivity, up to a maximum of one hour.”  
> Extended: “keeps cached prefixes active for longer, up to a maximum of 24 hours… typically around 30 minutes.”  
For GPT-5.6+: `prompt_cache_options.ttl` “30m” (default, 1.25× write) or “12h” (2.5× write); “minimum lifetime… OpenAI may keep entries longer.” Pricing same for reads. Caches not shared across orgs/regions; routing depends on load and `prompt_cache_key`.  

Observed: Fleet Codex data show cold-call share rising 10 % (30–60 min) → 17 % (1–2 h) → 46 % (2–6 h) → 74 % (6–12 h) → 98 % (12–24 h) → 100 % (>24 h). Consistent with documented “typically shorter than max” + eviction under load + per-machine routing, not a hard 24 h wall. Tibo (@thsottiaux, 21 Oct 2026): “for logged in users across Codex & Work we keep cache forever and you don’t have any penalty for coming back to an old conversation… guaranteed to hit the cache.” [single-source staff claim; not in public API docs; contradicted by gradual fleet decay].

**Anthropic.** Official (platform.claude.com/docs/en/build-with-claude/prompt-caching):  
> “By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used.”  
> 1-hour via `"ttl": "1h"`. Lifetime measured from start of the request.  

Claude Code docs (code.claude.com/docs/en/prompt-caching): main conversation gets 1-hour TTL only on subscription within plan usage; 5-minute on API key, credits, or everything else. idleCompaction (documented ~Oct 2026, v2.1.299+): 200k+ sessions idle ~54 min are compacted before the 1-hour expiry.  

Observed: Fleet Claude Code (71k calls) shows almost every human return >1 h cold; sharp cliff at 60th minute. Matches official 1 h. Resume/fork can still miss even inside TTL (GitHub issues).

**Google.** Implicit caching on by default for Gemini 2.5+ (ai.google.dev/gemini-api/docs/caching): best-effort, “no cost saving guarantee,” min prefix 2048–4096 tokens, “send requests with similar prefix in a short amount of time.” Cloud docs: expires no later than 24 h, most earlier. Explicit: user TTL (default ~1 h on older models), guaranteed discount while live. Gemini 4 / Interactions API: implicit only.  

Observed: Sparse for CLI/Antigravity. One reverse-engineered Antigravity measurement places effective expiry ~4 min 45 s–5 min [low-authority / single-source].

### Q2. What Resets the Cache Besides Time [established]

Documented and/or reproducible:

- **Model switch** — separate caches (OpenAI, Anthropic, Claude Code docs). Confirmed.
- **Reasoning effort / thinking budget / verbosity / text format** — part of cache key or prefix (OpenAI docs; Claude Code docs for effort on most models). Confirmed.
- **Tool list / MCP server / plugin change** — tools sit in system prefix (Anthropic tool-use-with-prompt-caching; Claude Code docs). Confirmed. Advisor tool sometimes exception.
- **System prompt / CLAUDE.md / AGENTS.md edit** — changes prefix. Confirmed in Claude Code docs.
- **Compaction / summary rewrite** — replaces history, breaks prefix match (OpenAI, Claude Code). Confirmed.
- **Images present/absent, certain tool results, fast mode header, client version upgrade** — documented Anthropic/Claude Code.
- **Session resume / fork / HTTP session-id** — Codex issues show session-id can affect reuse independently of `prompt_cache_key`. Emerging.
- **Account / org / regional / rate-limit rerouting** — OpenAI docs (caches not shared; routing by load + key). Confirmed as hit-rate reducer.
- **Subscription → pay-as-you-go credits fallback** — Claude Code drops main conversation to 5-minute TTL. Confirmed in docs.
- **Context tier crossings** (200k/272k/1M) — can change pricing and sometimes routing/behavior; not always pure cache invalidators.
- **Injected timestamps / system reminders** — can break exact prefix if placed early. Observed, not always vendor-listed.

Most confirmed by vendor staff/docs or controlled tests (e.g., Zentrik model/reasoning switch tests on Codex).

### Q3. How Other Teams Decide “Continue or Start Fresh” [emerging]

Common patterns (2025–2026 practitioner + vendor):

- **Context-size thresholds:** 200–400k tokens trigger compact or handoff (multiple Claude Code statusline mods, Dave Remy 300k/400k handoff). Claude Code auto-compact near window; idleCompaction at 200k+.
- **Idle-time rules:** Compact or restart before known TTL (1 h Claude Code subscription; ~5 min API; 30 m–12 h OpenAI). Keep-alive pings (many GitHub mods: CacheWarden, claude-thermos, keepwarm, coffee, cachemax) at 50 min / 4 min intervals.
- **Handoff / summary-then-restart:** Claude Code `/compact` + `/clear`, custom HANDOFF.md, Devin `/handoff`, Beacon session handoff, Cursor dynamic context discovery. Preferred for task switches or overnight.
- **Auto-compaction policies:** Claude Code idleCompaction (~54 min), Gemini CLI `/compress` / auto threshold, Antigravity CHECKPOINT ~125–128k.
- **Economics of pings:** One cold 200–500k write costs 12–80× a warm read (depending on model/TTL); pings pay read rate and reset timer. Break-even usually favors pings for gaps < TTL on large contexts.

**Quality arguments (separate from cost):** Context rot / lost-in-the-middle documented across models (Chroma 18-model study, Boolean quantified coding tasks, Anthropic attention-budget notes). Degradation starts well before hard limits (often 30–60 % fill for complex tasks). Compaction is lossy; directed compact + external notes better than pure resume of rotten context. Fresh session often higher task success on long-horizon work.

### Q4. Public Measurements Similar to Ours [emerging]

- **Wokey.ai** (weekly, Nov 2026): Claude Code median continuation hit rate 98.0 % (437 users); Codex × GPT 95.0 % (74 users). Miss causes: >5 min idle 34 % (Claude), new content 55 % (Codex), new conversation/idle >1 h 16–20 %. https://wokey.ai/cache-hit-rate
- **TraceLab / SyFI** (arXiv 2026, ~4.3k sessions / 350k steps Claude Code + Codex): global prefix hit ~95.7 %; user-initiated steps lower (~83–84 %) than tool-result steps (~97–98 %) because human gaps exceed eviction. https://arxiv.org/html/2606.30560v2
- **AGNT Cache Wars** (whitepapers 2026): controlled 390 s pause tests across harnesses. 1 h markers survive; 5 m expire. Claude Code and Codex high post-pause retention when configured for long TTL.
- **Individual session analyses:** Multiple GitHub issues and blogs with per-session token breakdowns showing cold resumes of 170–250k contexts costing 5–7 % of 5-hour limits or tens of dollars at API rates.
- **No exact match** to the large multi-machine idle-bucket curves (500 Claude sessions / 2.3k Codex sessions). Closest are weekly aggregates and controlled pauses. Searched arXiv, GitHub, practitioner blogs, Wokey, Requesty, TraceLab.

### Q5. Subscription vs API Accounting [emerging]

- **Claude Pro/Max:** Cache reads count against 5-hour and weekly limits but at heavy discount (measured ~0.025× in one reverse-engineering; API is 0.05–0.1×). Cache writes count; subscription 1 h writes sometimes weighted like 5-minute API (1.25×) rather than 2×. Cold large resumes move meters significantly (documented 5–7 % of 5 h for 170–210k Opus). Usage credits fall back to API pricing and 5-minute TTL. https://support.claude.com and reverse-engineered posts (Zenn, L2Cache).
- **ChatGPT Plus/Pro / Codex:** Usage measured in credits or message/token equivalents. Cached input discounted (~0.05–0.1×). Staff claim of “no penalty” on resume for logged-in users (Oct 2026). Exact mapping of cache writes/reads to subscription meters not fully public; dashboard shows cached vs uncached in some views. API list prices used in fleet model overstate subscription cost for cache hits.
- Main limitation of pure API-list cost models: subscription meters apply discounted weights and have hard windows; cache survival directly affects how quickly limits are hit.

### Q6. Failure Modes and Counter-Arguments [emerging]

**Against blocking cold large resumes:**
- Summary quality loss: compaction drops specifics, qualifications, and intermediate reasoning. Multiple practitioner reports of “dumber” post-compact agents.
- Lost context: file contents, prior decisions, tool results not perfectly recovered from summary + re-reads.
- User friction: extra handoff step, restart latency.
- Some tasks benefit from continuous history (debugging state, long refactor).

**Evidence on summarize-and-restart:**
- Context rot studies (Chroma, Boolean terminal-bench style) show measurable accuracy drops with fill even when information is present. Fresh or compacted sessions often recover performance.
- Claude Code team practices and community consensus treat high fill as a quality problem, not only cost. Directed compact + external memory/notes mitigates loss.
- No large controlled A/B on “cold resume of 400k+ vs summary restart” for coding task success. Strongest case for restart is quality at high fill + cost; strongest against is lossy summary on complex stateful tasks.

## D. Contradictions and Debates

- **Codex “forever” vs observed gradual decay.** Staff post (Tibo, 21 Oct 2026) claims indefinite for logged-in Codex/Work with guaranteed hits. Official API docs and fleet measurements show probabilistic, load-dependent retention up to 24 h max with practical shorter lifetimes. Steelman for staff claim: product-side routing or longer retention for ChatGPT-auth sessions not reflected in public API docs. Counter: measurements post-date the claim and still show decay. [emerging conflict]
- **1-hour vs 5-minute economics.** Some analyses (Wokey, practitioner) find blanket 1 h writes net more expensive because most reuse is <<5 min. Claude Code still defaults to 1 h on subscription for main conversation. Trade-off depends on idle distribution.
- **Compaction quality.** Vendor presents idleCompaction as cost-saving; practitioners note detail loss and sometimes prefer manual directed compact or pure restart. Both sides have evidence; outcome is task-dependent.
- **Gemini implicit reliability.** Docs emphasize best-effort and no guarantee; some users report high hits with stable prefixes, others near-zero. Load, routing, and prefix stability dominate.

## E. Public Measurements Comparable to Ours

Prior art exists but is not identical:

- Wokey.ai weekly multi-client aggregates (hit rates + miss causes by idle).
- TraceLab arXiv cross-provider coding-agent traces (hit rate by trigger type, human vs tool gaps).
- AGNT Cache Wars controlled pause studies.
- Numerous single-session or small-N reverse-engineerings of cold-resume cost.

**No prior art found** for multi-machine, multi-thousand-session idle-bucket cold-rate curves of the exact form published here. Searched: arXiv (“prompt cache” agent OR coding), GitHub issues (claude-code, openai/codex), practitioner blogs, Wokey, Requesty, TraceLab, OpenAI/Anthropic forums.

## F. Decision Rules Used in Practice, with Thresholds

- **Claude Code subscription, context >200k, idle approaching 50–54 min:** Let idleCompaction run or manually `/compact` before the hour.  
- **Any agent, large context, idle > known TTL:** Prefer summarize + restart or handoff over pure cold resume (cost + quality).  
- **Short idle (<TTL) on large context:** Continue; consider keep-alive ping.  
- **Task switch or overnight:** Handoff note + fresh session.  
- **Context >30–60 % of window on complex work:** Compact or restart for quality (context rot), independent of cache.  
- **Model/tool/MCP change:** Expect full cold; do it at natural break.  
Tools: Claude Code idleCompaction, `/compact`, `/clear`, various keep-warm mods, Devin/Beacon handoff, Cursor dynamic context.

## G. Recommendations for Our Article

**Safe claims:**
- Claude Code subscription main-conversation 1 h TTL with sharp observed cliff at 60 min and idleCompaction at ~54 min for 200k+.
- OpenAI documented in-memory vs extended vs 30 m/12 h minima; no write surcharge on older models; routing and load affect hits.
- Documented invalidators (model, tools/MCP, effort, compaction, system prompt).
- High in-session hit rates in public aggregates; cold resumes dominate cost of long-idle returns.
- Cache reads count (discounted) against subscription limits.

**Need caveats:**
- Codex “indefinite” staff claim vs gradual observed decay — present both; note product vs API distinction and lack of independent confirmation of “forever.”
- Exact subscription weighting of 1 h writes (sometimes closer to 1.25×).
- Gemini CLI/Antigravity effective TTLs (thin public data).

**Likely wrong or overstated if claimed without caveat:**
- Hard 24 h wall for Codex.
- Cache survival guarantees under load or after routing changes.
- That summarize-and-restart always preserves task success (lossy; depends on task and summary quality).

## H. Sources

- https://developers.openai.com/api/docs/guides/prompt-caching (accessed Nov 2026)
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://code.claude.com/docs/en/prompt-caching
- https://ai.google.dev/gemini-api/docs/caching
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview
- Tibo (@thsottiaux) X post 21 Oct 2026 (quoted via multiple secondary; original post)
- https://wokey.ai/cache-hit-rate and https://wokey.ai/claude-code-cache (Nov 2026)
- https://arxiv.org/html/2606.30560v2 (TraceLab, 2026)
- AGNT Cache Wars whitepapers (agnt.gg, 2026)
- Claude Code changelog / settings (v2.1.299+ idleCompaction)
- Multiple GitHub issues: anthropics/claude-code, openai/codex (resume, cache, compaction)
- Practitioner: Zentrik, L2Cache, Respan, Boolean context-rot, Chroma studies
- Keep-warm tools: CacheWarden, claude-thermos, keepwarm, claude-code-coffee, cachemax (GitHub)

**Verification pass:** All URLs above were opened or extracted via tool in this session. Quotes are direct from the pages. Staff X claims are single-source. No fabricated citations. Gaps remain on exact Codex product-side retention mechanics and large-scale Gemini CLI telemetry.

## Web search results (from Grok API, 146 URLs)
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching.md
- https://platform.claude.com/docs/zh-TW/build-with-claude/prompt-caching
- https://docs.claude.com/en/docs/build-with-claude/prompt-caching?s=03
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://ofox.ai/docs/develop/models/claude/caching
- https://www.respan.ai/articles/claude-prompt-caching
- https://tanstack.com/ai/latest/docs/advanced/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching.md
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview
- https://ai.google.dev/gemini-api/docs/caching
- https://ai.google.dev/gemini-api/docs/caching?lang=python
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/prompt-caching
- https://aistudio.google.com/docs/caching
- https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/
- https://blog.laozhang.ai/en/posts/gemini-context-caching
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview?hl=id
- https://www.datastudios.org/post/gemini-api-implicit-caching-0-cached-tokens-causes-fixes
- https://ofox.ai/docs/develop/advanced/gemini-explicit-cache
- https://archive.md/2026.01.25-083223/https://platform.openai.com/docs/guides/prompt-caching
- https://infro.io/blog/openai-12-hour-prompt-cache
- https://platform.openai.com/docs/llms-full.txt
- https://juejin.cn/post/7699305324096815155
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://thegenaimagazine.com/prompt-caching-anthropic-vs-openai-2026
- https://developers.openai.com/api/docs/guides/prompt-caching.md
- https://arte.itlibra.com/en/articles/openai-claude-prompt-caching-comparison
- https://openrouter.ai/docs/features/prompt-caching
- https://www.digitalapplied.com/blog/prompt-caching-changes-openai-anthropic-september-2026
- https://community.openai.com/t/new-24h-prompt-caching-retention-only-certain-models/1366221
- https://www.honeyhive.ai/learn/prompt-caching
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- https://wokey.ai/claude-code-cache
- https://communityone.io/servers/1538242239812341960/pixel/news/claude-code-cold-resume-usage-limit-measured-2026-11-16/
- https://www.swarchitect.net/en/claude-code-idle-compaction-2026-10/
- https://wokey.ai/cache-hit-rate
- https://l2cache.app/en/claude-code-resume-usage-limit
- https://dev.to/theagentloop/your-cache-hit-rate-is-lying-to-you-its-the-caller-mix-ec1
- https://cachewarm.danubelabs.net/
- https://l2cache.app/en/claude-code-cold-session-tax
- https://github.com/anthropics/claude-code/issues/51764
- https://vsits.co/how-to-get-99-cache-hit-rate/
- https://zentrik.ai/blog/cache-is-part-of-the-context
- https://agnt.gg/whitepapers/the-cache-wars-2
- https://medium.com/@lyx_62906/openai-prompt-caching-how-20-suffix-tokens-burned-our-codex-quota-51c0d208c849
- https://github.com/openai/codex/issues/36664
- https://github.com/openai/codex/issues/35925
- https://planyield.dev/changes/2026-10-21-codex-prompt-cache-indefinite/
- https://github.com/openai/codex/issues/41875
- https://github.com/earendil-works/pi/issues/12273
- https://github.com/openai/codex/issues/44716
- https://jdav.is/prompting-mechanics/openai-and-codex/
- https://qcode.cc/en/claude-code-idle-compaction
- https://www.turboai.dev/blog/claude-code-idle-compaction-guide
- https://www.turboai.dev/blog/claude-code-env-vars-v2-1-299
- https://www.turboai.dev/docs/claude-code/env-vars/CLAUDE_CODE_AUTO_COMPACT_WINDOW
- https://membase.com/blog/claude-code-compact
- https://9to5ai.tech/claude-code-compacted-while-idle-prompt-cache
- https://zenn.dev/zozotech/articles/1a26d1775c06f7
- https://www.claude-cn.org/posts/claude-code-idle-compaction
- https://www.its-tahir.com/blog/claude-code-compacted-while-idle
- https://www.matthewswong.com/en/blog/claude-code-prompt-caching-ttl-tuning/
- https://github.com/openai/codex/issues/39397
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching
- https://www.threads.com/@jh__0816_/post/DffriEJCfjZ
- https://news.lavx.hu/article/codex-cli-users-face-steep-cache-write-costs-on-bedrock-s-gpt-5-6-sol-as-prompt-caching-breaks-down
- https://code.claude.com/docs/en/prompt-caching
- https://omniscio.com/guides/claude-code-prompt-cache
- https://knightli.com/en/2026/05/18/claude-code-prompt-cache-token-optimization/
- https://github.com/openai/codex/issues/17814
- https://docs.passion8.cc/en/docs/claude-code/prompt-caching
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices
- https://support.claude.com/en/articles/12429409-extra-usage-for-max-20x-plans
- https://zenn.dev/tksfjt1024/articles/25c0ab111c277c?locale=en
- https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- https://claude-monitor.com/claude-usage-limits
- https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
- https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- https://github.com/anthropics/claude-code/issues/24147
- https://techbytes.app/posts/what-a-week-of-claude-code-holds-the-usage-meter/
- https://reveneau.com/guides/claude-code-usage-limits/usage-credits-after-the-limit
- https://www.wojcieh.net/building-context-guard-google-antigravity-strategic-compaction/
- https://antigravity.google/docs/cli/commands/context/
- https://godofprompt.ai/blog/prompt-cache/
- https://github.com/google-antigravity/antigravity-cli/issues/1072
- https://alteroid.com/antigravity-quota-prompt-cache-keepalive/
- https://antigravitylab.net/en/articles/integrations/antigravity-gemini-api-context-caching-production-guide
- https://discuss.ai.google.dev/t/open-source-native-context-usage-sidecar-panels-for-antigravity-100-local-mit-zero-extra-tokens/202215
- https://iceberglakehouse.com/posts/2026-03-context-gemini-cli/
- https://www.codexusage.dev/
- https://flaviocopes.com/ai-subscription-vs-api-pricing/
- https://news.google.com/rss/articles/CBMibEFVX3lxTE11QXN2Z1RWXzNZZzBvZzVaVDZNcUpnNGdoNXkwMTlCUGR4d01rWHBNdXhrVUxCbTdsZEhUNkRTdm5UV2xhRjVhUjI0ZlRrZEtjUTFPT1dqQm5lVzJ2d0xkN2k1YjZiWE1od2VCdw?oc=5
- https://reasonmachines.com/guides/codex-usage-limit
- https://learn.chatgpt.com/docs/enterprise/usage-insights
- https://www.codexusage.dev/dashboard
- https://developers.openai.com/codex/pricing
- https://inventivehq.com/blog/codex-subscription-usage-measured
- https://caprock.dev/guides/codex-usage-and-cost/
- https://community.openai.com/t/pro-500-weekly-codex-work-allowance-at-100-after-2-5-days-38-9-chats-25-6-unknown-case-19471937/1414581
- https://arxiv.org/html/2606.30560v2
- https://agnt.gg/whitepapers/the-cache-wars-2.pdf
- https://siddhantkhare.com/writing/agentic-inference-field-guide
- https://www.corpusiq.io/docs/hermes/best-practices/prompt-caching
- https://tracelab.cs.washington.edu/exp/prefix_cache/cache_hit_ratio/
- https://galileo.ai/blog/the-2026-caching-playbook-for-agents-bigger-prompts-smaller-bills
- https://www.requesty.ai/data/coding-agent-cache-hit-rate-oct-2026
- https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses
- https://aicostbudget.com/en/blog/agent-prompt-cache-hit-rate-cost
- https://fezu.dev/docs/agents-and-sessions/auto-compact
- https://docs.devin.ai/work-with-devin/devin-handoff
- https://tokenrip.com/blog/claude-code-handoff
- https://docs.beacon.sh/concepts/session-handoff
- https://claudeblattman.com/workflows/session-management/
- https://thejuliekaiser.com/claude-code-compact-handoff/
- https://code.claude.com/docs/en/context-window.md
- https://ai-devkit.com/skills/session-compact/
- https://x.com/daveremy/status/2120555748816306628
- https://x.com/nickwm/status/2099355900343464121
- https://aisubhub.top/en/news/tibo-api-cache-and-codex-work-continuity/
- https://x.com/KolinHuang/status/2112745885415125313
- https://x.com/codex_resets/status/2112713080748884113
- https://x.com/dani_avila7/status/2112751682807558561
- https://x.com/xmglab/status/2112726061658067407
- https://x.com/codex_resets/status/2111244672563826885
- https://x.com/coder_zeff/status/2113212387096690945
- https://x.com/kr0der/status/2112751731373400155
- https://x.com/codex_resets/status/2113770661063569413
- https://claude-codex.fr/en/prompting/context-rot/
- https://morphllm.com/context-rot
- https://www.mintlify.com/library/context-rot
- https://boolean.ai/blog/context-rot-quantified
- https://ai-fundamentals.kwise.app/04-context-rot/article
- https://www.braingrid.ai/blog/context-rot
- https://www.powerduck.com/blog/what-is-context-rot-in-ai-agent-sessions/
- https://juejin.cn/post/7708236158950293519
- https://claudecodeguide.dev/docs/foundations/context-window
- https://www.producttalk.org/context-rot/
- https://github.com/Efs-O/CacheWarden
- https://github.com/izeigerman/claude-thermos
- https://github.com/andreichiritescu/claude-code-cache-keep-warm
- https://github.com/cnighswonger/claude-code-coffee
- https://github.com/the-cybersapien/claude-cache
- https://github.com/declanbx/keepwarm
- https://github.com/Christandoh/context-cache
- https://github.com/paulbkim-dev/claude-code-cache-warmer
- https://github.com/nateherkai/claude-code-mods
- https://github.com/helloimdevman/cachemax
