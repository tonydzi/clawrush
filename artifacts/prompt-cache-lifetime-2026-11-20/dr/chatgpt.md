# DR26-11-20-MACSTUDIOM4-01-0251 — Prompt Cache Lifetime in Codex, Claude Code, Gemini and Other Coding Agents

## A. Executive Summary

The most important correction to the conventional “cache TTL” mental model is that **a vendor-advertised retention period is not necessarily the expected lifetime of a cache hit**. OpenAI now makes this distinction unusually explicit. For pre-GPT-5.6 models, `prompt_cache_retention="24h"` means entries are *eligible* for extended retention, but the documentation says they are “typically around 30 minutes” and may survive “up to 24 hours”; the shorter `in_memory` mode is typically 5–10 minutes of inactivity and at most about an hour. For GPT-5.6+ the API changed again: `prompt_cache_options.ttl` offers a **minimum** 30-minute lifetime by default or a **minimum** 12-hour lifetime in the Responses API, with cache-write charges of 1.25× and 2.5× uncached input respectively. OpenAI explicitly says machine placement, load balancing, routing, and prefix identity still matter. [established] Source: https://developers.openai.com/api/docs/guides/prompt-caching (live documentation, accessed 2026-11-20). citeturn266405view0

That distinction makes your **gradually decaying Codex hit probability from roughly one hour through 24 hours entirely compatible with OpenAI's documented pre-GPT-5.6 architecture**. A hard “24-hour TTL” was never a promise that a particular prefix would remain resident and hit for 24 hours. OpenAI says cache entries are local to serving machines; pre-GPT-5.6 `prompt_cache_key` merely influences routing and “does not pin requests to a machine or guarantee a cache hit.” The documented combination of finite retention, load-driven machine routing, and “typically around 30 minutes, up to 24 hours” predicts a survival curve rather than a cliff. [established] Source: https://developers.openai.com/api/docs/guides/prompt-caching (accessed 2026-11-20). citeturn266405view0

For **current GPT-5.6/GPT-6.x API use**, however, the article should not repeat the older claim “24-hour extended caching with no write surcharge.” That is now stale. GPT-5.6+ uses the new 30-minute/12-hour cache controls and charges writes at 1.25×/2.5×; GPT-6.2 Astra/Sol and GPT-6.1 Sol/Terra cached reads are 0.05× uncached input, while the generic GPT-5.6+ read rate is 0.1×. [established] Source: https://developers.openai.com/api/docs/guides/prompt-caching (accessed 2026-11-20). citeturn266405view0

There is one complication for **ChatGPT-authenticated Codex**. In October 2026 OpenAI publicly announced that logged-in Codex and Work users would retain cached context across old conversations without the API-style resume penalty. Yet two detailed Codex issue reports from October–November 2026 show apparent zero-cache resumes hours later and occasional misses even after short gaps. One report logged a ~164K-token conversation returning after 11 h 44 min with zero cached tokens; another analyzed 26,912 requests across 351 persisted threads and found materially more misses after 15–30+ minute boundaries than inside active turns. These are user reports rather than a formal service guarantee, and it remains possible that the client-visible `cached_input_tokens` metric does not exactly equal internal subscription-plan accounting. [emerging] [low-authority] Sources: https://community.openai.com/t/28-days-of-shipping-at-openai/1403897 (2026-10); https://github.com/openai/codex/issues/56050 (2026-10-22); https://github.com/openai/codex/issues/61757 (2026-11-16). citeturn963314view3turn963314view4turn963314view5

Anthropic is much cleaner. The API supports **5-minute ephemeral caching by default and 1-hour ephemeral caching optionally**, with hits refreshing the lifetime. Claude Code's current environment-variable documentation states explicitly that subscription users get the one-hour TTL automatically, whereas API-key, Bedrock, Vertex, Foundry and Claude Platform-on-AWS users request the one-hour form with `ENABLE_PROMPT_CACHING_1H=1`; otherwise the relevant default is five minutes. [established] Sources: https://platform.claude.com/docs/en/build-with-claude/prompt-caching (accessed 2026-11-20); https://code.claude.com/docs/ko/env-vars (accessed 2026-11-20). citeturn963314view6turn589981search0

Claude Code v2.1.299 then made the one-hour limit operationally visible: for conversations above 200K tokens, idle compaction fires at about **54 minutes**, intentionally just before the one-hour cache expires. The release note says this is done so the next message does not have to reprocess the entire conversation. That is exceptionally strong independent confirmation of your observed 60-minute Claude cliff: Anthropic's own client is engineered around the same boundary. [established] Source: https://github.com/anthropics/claude-code/blob/main/feed.xml, release v2.1.299 dated 2026-10-14. citeturn589981search1

Google's present architecture resembles the OpenAI extended model more than Anthropic's cliff. Current Gemini Enterprise Agent Platform documentation says implicit caching has **in-memory plus durable tiers**, that entries expire no later than 24 hours but “most entries are evicted earlier,” and that implicit hits receive a 90% discount. Explicit caches default to 60 minutes, can have their expiration extended, and have no documented maximum explicit duration. This is one of the clearest official acknowledgments that an advertised maximum lifetime should be modeled probabilistically. [established] Source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview, last updated 2026-11-20. citeturn638687view2

For Gemini CLI, auth path matters. Its own token-caching documentation says automatic cached-content optimization is supported with a Gemini API key or Vertex AI but is not available through the Google Personal/Enterprise OAuth route because that Code Assist API path does not expose cached-content creation. This statement concerns explicit cached-content support and should **not** be stretched into “OAuth gets no backend prefix caching at all”; Google may still use internal/implicit optimization. [established] Source: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md (current documentation, accessed 2026-11-20). citeturn963314view12

The strongest public datasets found show that your work is no longer unique, but it is still unusual in one important dimension: **idle-gap curves from human-driven agent sessions are scarce**. The 2026 GitHub Copilot production paper analyzed 13 million sessions, 3.2 million users and 761 million LLM calls and reported an extremely sharp cache deterioration with idle time: median cache hit rates were ≥95% below two minutes, around 70% in the 2–10-minute bucket, and near zero for 10 minutes–1 hour and >1 hour under its serving setup. TraceLab released ~4,300 real Claude Code/Codex sessions from 43 developers, ~350K LLM steps and ~430K tool calls, and explicitly identifies human-paced gaps as a KV-cache-management problem. A Harvard systems trace spanning 12K sessions and 209B input tokens reports average cache-hit fractions around 0.84 across user-idle transitions. These datasets establish that idle gaps and prefix mutation are major sources of cold prefill, although their serving policies are not directly interchangeable with Claude Code or ChatGPT-authenticated Codex. [established] Sources: https://borowiecki.dev/pdf/2608.00101 (2026-07-30); https://arxiv.org/abs/2606.30560 (2026-06-29); https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/ (2026). citeturn981465view12turn461974view0turn638687view0turn981465view7

The operational conclusion is therefore **not** “always kill a cold session.” Cost and quality point in different directions. A cold 400–700K conversation can be expensive to re-prefill, but it may contain substantially richer state than any summary. Anthropic explicitly warns that aggressive compaction can lose subtle information, while its own long-running-agent research found that structured context resets improved coherence when conversations became too large. Amp provides an unusually useful natural experiment in organizational opinion: in October 2025 it removed compaction because summaries were too lossy and pushed handoffs into fresh threads; by 2026 it reversed course and introduced automatic compaction near 90% context because newer frontier models had become better at it. [established] Sources: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents (2025); https://www.anthropic.com/research/harness-design-long-running-apps (2026); https://ampcode.com/news/handoff (2025-10-23); https://ampcode.com/news/neo (2026). citeturn981465view15turn981465view14turn981465view5turn981465view6

The largest remaining blind spot is **subscription accounting**. Anthropic confirms that caching makes reused content count less against paid-plan limits, and OpenAI exposes cached/uncached token categories in some Codex analytics, but neither vendor publishes a formula saying, for example, “one cached input token consumes exactly 0.05× of a Pro/Max/Plus/Pro quota.” Consequently, converting subscription usage into API-list-price equivalents is useful as a normalized engineering metric but **cannot be presented as a validated measure of subscription quota consumption or vendor marginal cost**. [established] Sources: https://support.claude.com/en/articles/9797557-usage-limit-best-practices (updated 2026-09-22); https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop (accessed 2026-11-20); https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan (accessed 2026-11-20). citeturn638687view1turn981465view17turn266405view3

## B. Per-vendor table: official TTL, observed lifetime, pricing and invalidators

| Vendor / path | Official cache lifetime | What public observations show | Write / read economics | Confirmed or strongly supported invalidators | Assessment |
|---|---|---|---|---|---|
| **OpenAI GPT-5.6+ / GPT-6.x Responses API** | `prompt_cache_options.ttl="30m"` default or `"12h"` in Responses API. These are **minimum lifetimes**, not statements that every request will necessarily reuse the same physical KV entry forever. | Public production observations are still sparse because this regime is recent. OpenAI says routing is automatic on GPT-5.6+, while its new diagnostics expose cache-break causes. | Write: 1.25× at 30m; 2.5× at 12h. Read: generally 0.1×; 0.05× for GPT-6.2 Astra/Sol and GPT-6.1 Sol/Terra. | Prefix rewrite; model change; tools/MCP schema/order change; images changed; compaction/truncation; dynamic data/timestamps inserted before breakpoint; top-level reasoning-effort changes can rewrite hidden instructions; organization/region isolation. | [established] https://developers.openai.com/api/docs/guides/prompt-caching, accessed 2026-11-20. citeturn266405view0 |
| **OpenAI GPT-5.5 / older GPT-5.x / GPT-5.1 Codex / GPT-4.1 API** | `24h` extended mode: “typically around 30 minutes, up to 24 hours.” Earlier `in_memory`: typically 5–10 minutes inactive, up to ~1h. | Gradual survival decay rather than a hard 24h cliff is exactly what this language plus machine-local routing predicts. | No additional cache-write charge in the older retention regime; cached-input price model-specific. | Exact-prefix changes; model/tools/images; compaction; load/routing to a machine without the entry; different organization/region. | [established] https://developers.openai.com/api/docs/guides/prompt-caching. citeturn266405view0 |
| **Codex CLI with API key** | Uses the Responses API endpoint; therefore cache semantics follow the selected model/API retention mode. | OpenAI's own Codex architecture post documents tool/model/configuration causes of cache misses and automatic compaction. | API pricing. | Model; tool definitions; MCP tool-list changes/order; sandbox/approval/cwd if they mutate early prompt structure; model-specific instruction bundle; AGENTS/project instructions when they change the reusable prefix; compaction. | [established] https://openai.com/index/unrolling-the-codex-agent-loop/ (2026). citeturn305116view0turn305116view3 |
| **Codex CLI with ChatGPT login** | Different endpoint: `https://chatgpt.com/backend-api/codex/responses`. An October 2026 OpenAI community announcement said logged-in Codex/Work conversations keep cached context across long resumptions. | Issue #56050 reports an 11h44m resume with zero cached tokens before cache immediately warmed again. Issue #61757 measured 26,912 requests and found more turn-boundary misses at 15m+. Thus the “indefinite/guaranteed” wording is not cleanly reproduced by client telemetry. | Counts against ChatGPT plan usage/credits; exact cached-token weighting is unpublished. | Same prompt mutations as Codex; apparent backend misses also occur without obvious user-visible mutations. | [emerging]; announcement vs telemetry unresolved. https://community.openai.com/t/28-days-of-shipping-at-openai/1403897; https://github.com/openai/codex/issues/56050; https://github.com/openai/codex/issues/61757. citeturn963314view3turn963314view4turn963314view5 |
| **Anthropic API, default ephemeral** | 5 minutes; lifetime refreshes when cache is used. | The behavior is well established and forms the basis of keep-alive tools such as Aider's cache pings. | 5m write 1.25×. Current cache-read multipliers depend on model: e.g. 0.05× for Opus/Sonnet 5.5 and 0.025× for Fable/Mythos 5.x in current pricing. | Prefix mutation before cache breakpoint; model switch; changed system/tools/cache-controlled blocks; cache expiry. | [established] https://platform.claude.com/docs/en/build-with-claude/prompt-caching; https://platform.claude.com/docs/en/about-claude/pricing. citeturn963314view6turn963314view7 |
| **Anthropic API 1h ephemeral** | 1 hour; supported on platforms that implement Anthropic caching. | Claude Code itself schedules 54-minute pre-expiry compaction around this TTL. | 1h write 2×; same model-specific read price. | Same prefix rules; model switch; compaction and cache-controlled structural changes. | [established] same Anthropic docs plus v2.1.299 release. citeturn963314view6turn963314view7turn589981search1 |
| **Claude Code Pro/Max subscription login** | Claude Code docs now say subscription users automatically receive the 1h TTL. | 200K+ conversations are idle-compacted at ~54m specifically “before its one-hour prompt cache expires.” Field reports show the timer can occasionally fail or behave differently by entrypoint/version. | Subscription quota accounting, not API billing. Anthropic says cached reused content “counts less,” but gives no public token multiplier for plan limits. | Model switch definitely cold; compaction deliberately replaces context; client/version/config changes can indirectly alter prompt; other mutations depend on where Claude Code places them. | [established] TTL; [emerging] implementation edge cases. https://code.claude.com/docs/ko/env-vars; https://github.com/anthropics/claude-code/blob/main/feed.xml; https://support.claude.com/en/articles/9797557-usage-limit-best-practices. citeturn589981search0turn589981search1turn638687view1 |
| **Claude Code API key / Bedrock / Vertex / Foundry** | Docs say 5m by default on these paths; `ENABLE_PROMPT_CACHING_1H=1` requests the 1h TTL. | A gateway A/B report found that server-side rewriting a 5m request to 1h did not arm Claude Code's idle-compaction timer; explicitly requesting 1h did. [low-authority] | Provider-specific billing; Anthropic multipliers apply to first-party Anthropic API, cloud provider pricing may differ. | Same logical prefix mutations plus provider/cache namespace. | [established] official env-var rule; [emerging] gateway timer behavior. https://code.claude.com/docs/ko/env-vars; https://github.com/anthropics/claude-code/issues/107073. citeturn589981search0turn589981search2 |
| **Gemini implicit caching, current Cloud Agent Platform** | In-memory + durable tiers; no implicit entry survives >24h, and Google explicitly says **most are evicted earlier**. | User reports and Antigravity issues include intermittent misses within seconds/minutes, consistent either with routing/eviction or hidden prefix mutations, but request serialization is not proven. | Current Cloud docs: cached implicit tokens 90% cheaper; normal input cost on cache creation; no implicit storage fee. | Prefix divergence; project boundary; eviction/capacity; cached backing object modified; model/path differences. | Official behavior [established]; Antigravity attribution [speculative]. https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview; https://github.com/google-antigravity/antigravity-cli/issues/1533. citeturn638687view2turn963314view14 |
| **Gemini explicit context cache** | Default 60m; TTL can be extended; current Enterprise Agent Platform docs state no maximum explicit duration. | Deterministic resource existence makes this far more predictable than implicit cache, subject to model/API support. | 90% cached-token discount for Gemini 2.5+ in the cited platform; storage charges apply. | Explicit expiry/deletion; model/resource incompatibility; changing cached Cloud Storage objects can make cache unusable; project isolation. | [established] https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview; https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-create. citeturn638687view2turn575345search5 |
| **Gemini CLI** | Depends on auth/API path rather than a single CLI-wide TTL. | CLI docs say cached-content optimization is available for Gemini API-key/Vertex routes but not OAuth Code Assist cached-content creation. | Depends on API/plan. | Same prefix/model/tool changes; changing auth path can change the backend/caching facility. | [established] https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md. citeturn963314view12 |
| **Antigravity** | No Antigravity-specific cache-lifetime contract located. Underlying Gemini cache rules are the closest documented model. | Issue #1533 shows warm→zero→warm sequences with 24–55 second gaps; SDK issue #229 reports volatile cache reuse on 30–80K static prefixes. Both are user reports without byte-level request capture. | No Antigravity-specific public cache-accounting formula found. | Unknown hidden harness mutation versus backend routing/eviction remains unresolved. | [speculative] [low-authority]. https://github.com/google-antigravity/antigravity-cli/issues/1533; https://github.com/google-antigravity/antigravity-sdk-python/issues/229. citeturn963314view14turn963314view15 |

## C. Key Findings per question Q1–Q6

### Q1 — Official versus observed TTL

**OpenAI: “up to 24 hours” was never equivalent to “a 24-hour lease.”** [established] The current documentation gives unusually precise language. For older `in_memory` caching it says entries typically remain useful for about 5–10 minutes of inactivity and may persist up to an hour. For the older extended-retention mode it says entries are typically retained around 30 minutes and may survive up to 24 hours. On pre-5.6 models, `prompt_cache_key` improves the probability of colocating related requests but does not pin a conversation to a machine or guarantee a hit. Source: https://developers.openai.com/api/docs/guides/prompt-caching (accessed 2026-11-20). citeturn266405view0

This means your Codex curve—low misses inside an hour, increasing misses over 2–12 hours, and almost no survival by 12–24 hours—is **qualitatively what one would predict from the documented system**. It should not be described as evidence that OpenAI “violates a 24-hour TTL.” A safer statement is that the fleet data measures the *effective cache-survival distribution* seen by Codex sessions, whereas OpenAI's 24-hour value was a maximum retention envelope. [established]

GPT-5.6+ changes the interpretation. The API now advertises minimum retention windows of 30 minutes or 12 hours rather than the old 24-hour maximum-style retention. The write economics also changed. Therefore a November 2026 article must version-stamp any OpenAI observations: **old GPT-5.x/5.1 Codex behavior and GPT-5.6+/GPT-6 behavior are not one cache regime**. [established] Source: https://developers.openai.com/api/docs/guides/prompt-caching. citeturn266405view0

There is also a distinct **Codex subscription path**. OpenAI's own architecture article confirms that ChatGPT-login Codex does not use the ordinary `api.openai.com` endpoint; it sends Responses-style traffic to `chatgpt.com/backend-api/codex/responses`, while API-key authentication uses `api.openai.com/v1/responses`. This makes it unsafe to infer subscription behavior solely from the public API contract. [established] Source: https://openai.com/index/unrolling-the-codex-agent-loop/ (2026). citeturn305116view3

The October 2026 announcement that logged-in Codex sessions have effectively persistent caching therefore deserves its own paragraph rather than being merged with API TTL documentation. The best interpretation today is: **OpenAI intends logged-in Codex resume to avoid API-style cache expiry penalties, but client-visible telemetry has not yet demonstrated a perfect guarantee.** [emerging] The strongest counterexamples are #56050 and #61757. The second is particularly useful because it is not a single anecdote: 351 persisted root threads, 26,912 requests, with intra-turn misses of only ~0.16% but elevated first-call misses after longer turn boundaries. [low-authority] Sources: https://github.com/openai/codex/issues/56050 (2026-10-22); https://github.com/openai/codex/issues/61757 (2026-11-16). citeturn963314view4turn963314view5

**Anthropic: the one-hour cliff is contractual enough to engineer against.** [established] Anthropic's API defines 5-minute and 1-hour ephemeral caches, and Claude Code's own v2.1.299 release makes the operational consequence explicit: once a conversation is above 200K tokens and has been idle for approximately 54 minutes, the client can compact it before the one-hour cache expires. Source: https://github.com/anthropics/claude-code/blob/main/feed.xml, v2.1.299, 2026-10-14. citeturn589981search1

That release note is stronger evidence than a generic caching doc because it connects **Claude Code's actual orchestration policy** to the one-hour TTL. Your observed sharp 60th-minute cliff is therefore not just plausible; it is aligned with the threshold Anthropic itself uses to trigger a preventative action. A public article can safely call 60 minutes the dominant subscription-session cache boundary, while noting that actual idle-compaction execution has had version/entrypoint bugs. [established] / [emerging for edge cases] Sources: https://github.com/anthropics/claude-code/issues/103931; https://github.com/agentclientprotocol/claude-agent-acp/issues/1518. citeturn589981search6turn589981search3

For API/cloud authentication, current Claude Code documentation is unusually useful: subscription users receive the one-hour TTL automatically; API-key/Bedrock/Vertex/Foundry users use five minutes unless 1h is explicitly enabled. [established] Source: https://code.claude.com/docs/ko/env-vars (current documentation, accessed 2026-11-20). citeturn589981search0

**Google: implicit TTL is explicitly probabilistic.** [established] Google says implicit caches have in-memory and durable tiers, that in-memory entries may be evicted as capacity is reclaimed, and that all implicit entries expire by 24 hours while most disappear sooner. The official advice to send similar prefixes “in a short amount of time” is therefore not merely an optimization tip; it reflects the absence of a durability guarantee. Source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview, updated 2026-11-20. citeturn638687view2

This also resolves an apparent conflict with Google's 2025 Gemini 2.5 launch wording. That article said a common prefix was **eligible** for an implicit hit and recommended explicit caching when one needed guaranteed cost savings. It never promised a fixed implicit TTL. [established] Source: https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/, 2025-05-08. citeturn638687view3

Antigravity's very short observed misses are therefore not impossible under the Google contract, but attributing them specifically to eviction would overreach. They could also arise from hidden harness changes, routing, model variation, or request serialization. [speculative] [low-authority] Sources: https://github.com/google-antigravity/antigravity-cli/issues/1533; https://github.com/google-antigravity/antigravity-sdk-python/issues/229. citeturn963314view14turn963314view15

### Q2 — What resets the cache besides time?

The key invariant across all three vendors is **prefix identity**, not “session identity.” A session can have the same visible thread ID and still lose its useful cache if the serialized prefix changes before the relevant cache boundary. Conversely, a new logical request can reuse substantial prefix work if it has an identical reusable prefix and lands in the right cache namespace. [established] Sources: OpenAI https://developers.openai.com/api/docs/guides/prompt-caching; Google https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/; Anthropic https://platform.claude.com/docs/en/build-with-claude/prompt-caching. citeturn266405view0turn638687view3turn963314view6

| Candidate invalidator | OpenAI / Codex | Anthropic / Claude Code | Google / Gemini |
|---|---|---|---|
| **Model switch** | **Confirmed.** Codex explicitly lists changing model as a miss cause. | **Confirmed.** Claude Code settings say every model has its own prompt cache; first request after switching rereads the conversation uncached. | Explicit cached resources are model-bound in practical API use; no separate Antigravity rule found. |
| **Reasoning effort / thinking budget** | **Confirmed risk on GPT-6.** OpenAI says changing top-level `reasoning.effort` can rewrite hidden system instructions; use an appended `configuration_update` to preserve the prefix. | Effort affects usage limits, but I found no current Anthropic statement that an effort toggle by itself necessarily invalidates the cache. **[no source found]** | No agent-specific guarantee found. **[no source found]** |
| **Tool list / MCP server change** | **Confirmed.** Tool changes, inconsistent tool ordering and MCP `tools/list_changed` are all named miss causes. | Tools are part of cacheable prompt structure; exact consequences depend on cache breakpoint placement. No Claude-Code-specific blanket statement found equating every MCP update to total-cache loss. | Common-prefix rule implies an early serialized tool mutation can destroy reuse; exact Gemini CLI serialization behavior was not documented in the sources opened. |
| **System prompt / AGENTS.md / CLAUDE.md edit** | Codex initial input contains model instructions, AGENTS files and environment context. Editing a portion that is reconstructed before the cached boundary can break reuse. **Confirmed mechanism; exact mid-session behavior is implementation-dependent.** | A model/system-prompt change can break prefix identity. A 30-session forensics report observed no CLAUDE.md/memory edit cache breaks in its sample, so “every CLAUDE.md edit flushes Claude” would be unsupported. [low-authority] | Same common-prefix principle; no Antigravity-specific test found. |
| **Injected timestamp / volatile system reminder** | OpenAI explicitly says to move timestamps/dynamic content after the cached breakpoint rather than place it in reusable instructions. | Mechanistically dangerous when injected before cached content; no current vendor list of Claude Code's every reminder field found. | Same prefix principle; Google advises putting common content first and variable material later. |
| **Images** | **Confirmed.** Images in cached prefix must be identical. | Images can be part of cacheable content; exact Claude Code mutation behavior not separately documented in opened sources. | Multimodal context can be cached explicitly/implicitly; mutation changes prefix/content. |
| **Compaction / summarization** | **Confirmed.** OpenAI says summarization, compaction or truncation can reset cache reuse; Codex replaces old `input` with a smaller structure. | **Confirmed operationally.** Claude Code idle compaction intentionally changes the following request to a summary. | Compaction is harness-dependent; if serialized prefix changes, prior implicit prefix reuse is lost. |
| **Resume same session** | **Not inherently an invalidator.** Cache survives if prefix + backend placement survive. Observed resume misses exist. | **Not inherently**, but one-hour expiry dominates subscription resumes. | **Not inherently**, but implicit caching is best-effort. |
| **Fork session** | Shared unchanged prefix is potentially reusable; OpenAI's GPT-6 cache-breakpoint work explicitly targets conversation forks. | No blanket fork rule located. | No blanket fork rule located. |
| **Client version upgrade** | Version can change bundled model instructions/tool schemas and therefore indirectly invalidate reuse; version number itself is not a documented cache key. **[no source found for direct invalidation]** | Same: changed prompt/tool serialization can matter, but “upgrade flushes cache” is not a vendor rule. | Same. |
| **Account / organization change** | Caches are not shared across organizations and regional boundaries. **Confirmed.** | Workspaces/cache isolation prevent assuming cross-account reuse. | Cached data is isolated by project number. **Confirmed.** |
| **Subscription → PAYG credits** | Auth path can change endpoint/accounting namespace; no source says the billing event itself flushes a cache. **[no source found]** | Switching from Claude subscription auth to API-key auth changes metering and normally the requested TTL path; no source says “credit fallback” itself is an invalidator. | Provider/API path can differ; no billing-event invalidation rule found. |
| **Crossing 200K / 272K / 1M context** | **No evidence that crossing the pricing/context tier itself invalidates KV cache.** 272K can affect pricing/model behavior but is not documented as a cache flush. | 200K is an **idle-compaction trigger threshold**, not a cache TTL invalidator. | Context size affects eligibility/limits but no generic “1M boundary flush” found. |
| **Rate-limit rerouting / load balancing** | **Confirmed as a hit-probability factor.** Pre-5.6 cache keys influence rather than pin routing; load can spill traffic. | No comparable public Claude Code routing contract found. | In-memory capacity eviction is explicitly load/capacity-dependent. |
| **Regional failover** | Cache isolation across regions means moving execution can lose reuse. | Cloud-platform behavior can vary; no universal Claude Code failover rule found. | Project/region/platform scope matters; cache data is not globally interchangeable by assumption. |

OpenAI's Codex article is exceptionally explicit on the highest-value cases: “Changing the `tools`,” changing the model, sandbox configuration, approval mode or working directory can cause misses; an early MCP implementation even had nondeterministic tool ordering that broke caching. Codex now tries to append changed sandbox/cwd state instead of rewriting older messages precisely to preserve prefix reuse. [established] Source: https://openai.com/index/unrolling-the-codex-agent-loop/ (2026). citeturn305116view0turn305116view1

This creates an important nuance for your article: **configuration change ≠ necessarily total cache loss**. The location of the mutation matters. If a client appends a changed developer message after the existing cached history, the old prefix can remain reusable. If it rebuilds the early system/tool prefix, nearly the whole prompt can become cold. OpenAI's new GPT-6 API effectively formalizes this idea through explicit cache breakpoints and append-only `configuration_update` messages. [established] Source: https://developers.openai.com/api/docs/guides/prompt-caching. citeturn266405view0

A useful new technical detail for GPT-6.2 Responses API: top-level `instructions` are appended after `input` and billed at the uncached rate even on a cache hit. OpenAI therefore tells developers to put reusable instructions into the first `developer` message rather than the top-level field. This can create apparent “partial misses” in telemetry that are not eviction. [established] Source: same OpenAI guide. citeturn266405view0

For Anthropic, **model switching is unequivocal**. Claude Code's settings documentation says each model owns a separate prompt cache and that the first request after a switch rereads the whole conversation uncached. [established] Source: https://code.claude.com/docs/en/settings (accessed 2026-11-20). citeturn589981search8

The most interesting Claude-specific “invalidator” is actually deliberate: **idle compaction is a cache-preservation maneuver that intentionally sacrifices the old prefix before the cache would expire anyway**. It performs the expensive summary while the large prefix is still warm, then uses the smaller summary when the user returns. That is economically rational but creates a quality tradeoff because full transcript detail is discarded from the active model context. [established] Source: v2.1.299 release, https://github.com/anthropics/claude-code/blob/main/feed.xml, 2026-10-14. citeturn589981search1

A caution on implementation: public issues document cases where idle compaction did not fire, including an ACP entrypoint and a terminal build, and a gateway experiment where merely rewriting the API TTL to 1h downstream did not arm the local timer. These are useful engineering edge cases but should be tagged [low-authority], not described as Anthropic guarantees. Sources: https://github.com/agentclientprotocol/claude-agent-acp/issues/1518; https://github.com/anthropics/claude-code/issues/103931; https://github.com/anthropics/claude-code/issues/107073. citeturn589981search3turn589981search6turn589981search2

For Google, current official documentation gives two concrete non-time invalidators beyond prefix mismatch: **capacity eviction** from the implicit in-memory tier, and mutation of a Cloud Storage object backing an explicit cache, which can render that cache unusable. Caches are also isolated by Google Cloud project number. [established] Source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview, updated 2026-11-20. citeturn638687view2

### Q3 — How other teams decide “continue or restart”

There is no industry-standard idle-time threshold. The published policies cluster into two separate dimensions: **time/cache economics** and **context quality/context-window pressure**. Most coding-agent products expose policies for the second but not the first.

**Anthropic / Claude Code.** Current official guidance says `/clear` is the right choice when changing tasks, while `/compact` is appropriate when continuing the same long task. Claude Code also auto-compacts near its context limit. This is a task-boundary heuristic rather than an idle-time heuristic. [established] Source: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code (updated 2026). citeturn575345search4

Claude Code's 54-minute idle compaction adds the first major **time-aware** policy found in a mainstream agent: if context ≥200K and the session is on the one-hour cache, compact before expiry. [established] This is effectively Anthropic answering “continue or restart?” with a third option: *keep the logical session, but replace most model-visible history with a warm-cache-generated summary*. Source: https://github.com/anthropics/claude-code/blob/main/feed.xml. citeturn589981search1

**OpenAI / Codex.** Codex automatically compacts when its `auto_compact_limit` is exceeded, using the Responses API compaction endpoint and an opaque compaction item designed to preserve latent state while shrinking context. [established] Source: https://openai.com/index/unrolling-the-codex-agent-loop/ (2026). citeturn305116view2 OpenAI's plan documentation also recommends starting a new Codex chat with a short summary when a conversation gets stuck in repeated auto-compaction; importantly, starting a new chat does not reset plan limits. [established] Source: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan (accessed 2026-11-20). citeturn981465view16

**Zed.** Zed gives one of the clearest numeric context policies: automatic compaction is enabled by default at **90% of the selected model's context window**, configurable as a percentage, absolute token count or remaining-token threshold. If a model's context window is under 80K, Zed instead offers “Start New Thread” / “New From Summary.” [established] Source: https://zed.dev/docs/ai/agent-settings and https://zed.dev/docs/ai/agent-panel (current docs, accessed 2026-11-20). citeturn692134search1turn692134search0

**Amp / Sourcegraph lineage.** Amp is particularly valuable because its policy changed. In October 2025 Amp removed automatic compaction and promoted Handoff into a fresh thread because it considered compaction too lossy. By 2026 its newer architecture automatically compacted near 90% full and removed Handoff, arguing that newer frontier models had become much better at producing useful compactions. [established] Sources: https://ampcode.com/news/handoff, 2025-10-23; https://ampcode.com/news/neo, 2026. citeturn981465view5turn981465view6 This is evidence against presenting either “summary restart is always better” or “never restart” as a stable truth.

**Cline.** Cline's Auto Compact produces a structured summary near context exhaustion and continues from that summary; it also permits rollback. Cline's public documentation emphasizes continuity but does not publish an idle-time cache threshold. [established] Source: https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx (current docs, accessed 2026-11-20). citeturn981465view1

**Aider.** Aider is notable because it explicitly attacks TTL rather than context quality. Its Anthropic caching support has keep-alive pings at approximately five-minute intervals to keep short-lived cache state warm for a configurable period. This is prior art for cache keep-alive economics independent of the Claude-Code hooks you already catalogued. [established] Source: https://aider.chat/docs/usage/caching.html (current docs, accessed 2026-11-20). citeturn981465view2

**Cursor.** Cursor published an engineering report on reorganizing its agent prompt to put stable material before the cache boundary; it reported roughly a 20% reduction in cold-cache misses from one change and a further ~1.6% reduction in cache-read token volume from line-number optimization without measured quality loss. This is primarily prompt-layout engineering, not a resume threshold. [single-source] Source: https://prod.cursor.com/blog/improved-token-efficiency (2026). citeturn981465view0

**Factory.** Factory's context-compression article argues for retaining identifiers and pointers that let the agent re-fetch dropped information rather than trying to serialize every detail into a summary. Separately, Factory's workflow guidance says that when a run has gone materially off-track, launching a fresh session with better instructions can be cheaper than repairing accumulated wrong state. No public numeric idle-TTL restart threshold was found. [emerging] Sources: https://factory.ai/news/compressing-context, 2025-07-21; https://factory.ai/news/build-with-agents, 2025-07-01. citeturn692134search12turn692134search18

**Manus.** Its context-engineering article recommends keeping prompts cache-friendly, maintaining stable prefixes, and—in self-hosted distributed serving—routing the same session consistently to improve prefix reuse. For long contexts it advocates dropping recoverable observations while preserving references such as paths or URLs. It does not publish a simple idle-time restart cutoff. [single-source] Source: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (2025). citeturn692134search14

**Devin/Cognition.** I did not locate a Cognition publication recommending an idle-time or context-fill cutoff. Current Devin CLI continuity features instead include `/pickup` and `/handoff`, where a new local session receives a summary of a cloud session, plus `/context` for inspecting prompt sections. The result surfaced through a release-note aggregator rather than Cognition's own site, so this finding is [single-source] [low-authority] and should not be used as a major article claim. Source: https://devincentral.com/continuity/cli/2026-w43, 2026-10-22. citeturn893033search0

A **cross-vendor “cold-resume probability × context size × quality-risk” controller** was not found. I searched OpenAI/Codex, Anthropic/Claude Code, Gemini/Gemini CLI/Antigravity, Cursor, Amp/Sourcegraph, Cline, Aider, Zed, Factory, Devin/Cognition, Manus, GitHub, arXiv and practitioner blogs. Existing tools either keep a cache warm, warn about expiry, compact near context limits, or create a handoff. **Prior art not found** for a controller that learns an empirical idle-gap survival curve and automatically chooses full resume versus compact/handoff based on expected marginal cost.

### Q4 — Public measurements similar to your fleet data

The answer is now **yes**, although genuinely comparable real-session datasets remain few.

The strongest comparator is the **GitHub Copilot production trace paper**, “Characterizing Developer–AI Interaction at Scale” / associated 2026 production study. It covers approximately **13 million sessions, 3.2 million users, 761 million LLM calls, 95 trillion tokens and 775 million tool invocations**. [established] Source: https://borowiecki.dev/pdf/2608.00101, arXiv-era paper dated 2026-07-30. citeturn981465view12turn461974view0

Its idle-gap curve is unusually relevant. Within its serving configuration, calls after gaps below two minutes had median hit fractions around or above 95%; the 2–10-minute range dropped toward roughly 70%; 10 minutes–1 hour and >1-hour buckets had medians near zero. [established] This is not evidence that Claude, OpenAI or Gemini universally expire there—it describes Copilot's provider/runtime mix—but it establishes at enormous scale that human waiting time is a first-order cache predictor. Source: same paper. citeturn981465view12turn461974view0

The same study has perhaps the best public numbers on **compaction as a cache invalidator**. Compaction occurred in about 7.8% of sessions but touched 44.2% of tokens; median prompt size fell 72.8%, while median cache-hit rate fell 66.1%. About 34.3% of compactions erased ≥90% of the prior hit rate and 21% erased ≥99%. [established] This directly supports separating “compaction reduces future context” from “compaction preserves the old KV cache”—it usually does not. Source: https://borowiecki.dev/pdf/2608.00101, 2026-07-30. citeturn981465view12turn461974view0

The **TraceLab** dataset is the closest open trace to your exact population: roughly **4,300 real Claude Code and Codex sessions**, ~350,000 LLM steps and ~430,000 tool calls from 43 developers across approximately eight months and more than 20 model versions. The authors explicitly describe it as, to their knowledge, the first large-scale cross-provider trace of day-to-day coding-agent use. [established] Source: https://arxiv.org/abs/2606.30560, 2026-06-29. citeturn638687view0

TraceLab finds long growing contexts, high-but-imperfect prefix reuse and human-paced gaps important enough that the authors call for better KV-cache management around those gaps. Its importance for your article is methodological: it independently validates **local agent traces as a legitimate way of studying serving behavior**, while your fleet adds much denser analysis specifically around idle-time cold resumes. [established] Source: same paper. citeturn638687view0

A separate Harvard Systems Group / FreeInference production analysis reports **12K sessions and 209B input tokens across 13 harnesses**. It reports average cache-hit fractions of roughly 0.97 across tool transitions, 0.92 around ask-user transitions, ~0.84 across user-idle transitions and ~0.91 around subagent transitions; the median observed user idle was around 96.5 seconds. [emerging] Source: https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/ (2026) and companion material https://opendata.agentic-system.org/pdf/paper/from-requests-to-sessions (2026). citeturn981465view7turn981465view8

That study also provides an important counterpoint to pure TTL analysis: prompt **mutation** is relatively infrequent as a transition but disproportionately expensive when it happens. Its reported analysis attributes a large fraction of fresh prefill to system-prompt and tool-definition mutations rather than to pure timeout. [emerging] Source: same Harvard analysis. citeturn981465view7

A small but unusually relevant Claude Code forensics report analyzed **30 sessions / 3,203 calls** and attributed a large fraction of cache-write volume to only a few dozen events, including TTL expiry, micro-compaction, resume and model-switch events. Its average context was about 320K tokens, median ~239K and p90 ~707K—close enough to your context regime to be worth mentioning. However, it is one GitHub investigator's reverse engineering rather than a peer-reviewed dataset. [emerging] [low-authority] Source: https://github.com/anthropics/claude-code/issues/94177 (2026). citeturn981465view10

Another practitioner repository, **agent-cost**, reports 88 real Claude Code sessions and 12,937 turns from one developer, totaling roughly 3.94B prompt tokens with an aggregate ~98.9% cache-read fraction. The value here is not its mean—it mixes many short warm turns—but its demonstration that cached history dominates token volume in real coding-agent workloads. [low-authority] [single-source] Source: https://github.com/yingxiangge/agent-cost, report dated 2026-09-10. citeturn981465view11

AGNT's “Cache Wars” is **not** directly comparable because it is a controlled harness experiment rather than observational production logs. It is still useful as a mechanistic test because it holds a workload stable, inserts a 390-second pause and compares harnesses. It should be listed as near-prior-art, not as an external replication of your fleet result. [low-authority] Source: https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses (2026). citeturn981465view9

**Positioning against your data:** your Claude sample is much smaller than Copilot but substantially more detailed for one harness and one exact boundary; your Codex sample is smaller than TraceLab in sessions but is specifically bucketed by human idle gap. I did **not** find another publication reporting a Codex/ChatGPT-authenticated survival curve with buckets as long as 30–60m, 1–2h, 2–6h, 6–12h, 12–24h and >24h. [emerging] That appears to be a genuine contribution.

**Search trail.** I ran more than 30 distinct web searches spanning official developer/help documentation, product release feeds, GitHub issues/repos, arXiv/system papers, engineering blogs and vendor forums. Search families included `prompt_cache_retention`, `prompt_cache_options.ttl`, `prompt_cache_key`, Codex cached-input misses/resume, Claude 5m/1h cache, Claude Code idle compaction, Gemini implicit/explicit caching, Gemini CLI cached-content auth paths, Antigravity cache misses, production coding-agent traces, idle-gap cache-hit data, compaction cache-hit data, and continue/handoff policies for Cursor, Amp/Sourcegraph, Cline, Aider, Zed, Factory, Devin/Cognition and Manus. No second large real-world Codex-specific idle-gap dataset matching your exact methodology was found.

### Q5 — Subscription versus API accounting

This is the largest caveat in your cost analysis.

Anthropic explicitly confirms that **caching reduces consumption of subscription usage limits**. Its September 2026 usage-limit guidance says cached project content “counts less against your limits” when reused, and that after a long-enough inactivity gap the first message can count that content in full again. [established] Source: https://support.claude.com/en/articles/9797557-usage-limit-best-practices, updated 2026-09-22. citeturn638687view1

Anthropic also says paid-plan consumption depends on conversation length, tool use, model choice, effort level and other workload factors, and that Pro/Max/Team-style usage is measured through five-hour and weekly limits shared across Claude surfaces. [established] Source: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work and https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan. citeturn575345search2turn981465view13

What Anthropic **does not publish** is a direct mapping such as:

`Pro/Max quota units = uncached_input + 2.0 × 1h_cache_write + 0.05 × cache_read`

I found no official formula equating subscription utilization with API dollar-equivalent token multipliers. [established absence after search; no source found for a formula] Thus your API-price-normalized metric should be called **API-list-price-equivalent input cost**, not “Claude Max usage” or “the actual cost to Anthropic.”

OpenAI is similarly incomplete. Codex usage under a ChatGPT plan counts against applicable plan usage/credits, and OpenAI says consumption depends on model, context, reasoning, task complexity and tools. [established] Source: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan. citeturn266405view3

OpenAI's Personal Analytics surface for supported plans can separately expose **uncached input, cached input and output tokens**, which proves the distinction survives into at least some subscription/credit telemetry. But that still does not reveal the conversion formula from those categories into Plus/Pro allowance. [established] Source: https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop (accessed 2026-11-20). citeturn981465view17

OpenAI's flexible-credit documentation confirms that eligible Plus/Pro users can continue Codex usage through purchased credits after included allowance is exhausted, but I found no official statement that subscription quota weights cached tokens by the public API's 0.05×/0.1× cached-input rate. [established absence after search] Source: https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans (accessed 2026-11-20). citeturn981465view18

Therefore the article should state explicitly:

> **API list-price weights measure the economic magnitude of cache churn under public API pricing; they do not establish how Claude Pro/Max or ChatGPT Plus/Pro quota meters cache reads and writes internally.**

That claim is [established], and it turns what could otherwise look like a flaw into a clearly bounded normalization method.

### Q6 — Failure modes and the strongest case against blocking cold resumes

The strongest argument **against a hard resume blocker** is information fidelity. A cold full-context resume may cost far more inference, but it retains every constraint, failed hypothesis, user correction, tool result and subtle decision still present in the transcript. A summarize-and-restart operation introduces an information bottleneck whose failures can be silent. Anthropic's context-engineering guidance explicitly warns that aggressive compaction can lose subtle but important information. [established] Source: https://www.anthropic.com/research/effective-context-engineering-for-ai-agents (2025; older than the preferred 12–18-month window, but still current conceptual guidance). citeturn981465view15

The second argument is **amortization**. If a user returns to a cold 500K-token session, pays one cold re-prefill and then works actively for another 50 calls, the expensive resume can be amortized over a long warm continuation. Killing that session preemptively may instead require reading repository state again, reconstructing goals, rediscovering edge cases and paying for a handoff summary. No public benchmark I found establishes a universal break-even point. [speculative]

The third argument is **summary quality is model- and task-dependent**. Amp's historical reversal is the strongest public evidence. In 2025 it considered compaction sufficiently lossy to replace it with explicit fresh-thread handoffs; in 2026 it reversed course and adopted automatic compaction as frontier models improved. [established] Sources: https://ampcode.com/news/handoff, 2025-10-23; https://ampcode.com/news/neo, 2026. citeturn981465view5turn981465view6

The strongest argument **for** reset/handoff is context rot. Anthropic's long-running-agent experiments report that agents became less coherent as context accumulated and that context resets plus structured handoffs were an important part of making long-horizon work reliable; in earlier Sonnet 4.5 testing, compaction alone was insufficient. [emerging] Source: https://www.anthropic.com/research/harness-design-long-running-apps (2026). citeturn981465view14

Claude Code's own support documentation now says quality declines as the context window fills and recommends `/clear` when switching tasks and `/compact` when continuing the same task. [established] Source: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code. citeturn575345search4

Factory and Manus converge on a more sophisticated pattern: **externalize durable state rather than demanding that a summary preserve everything**. Keep repository paths, identifiers, URLs, ADRs, plans and machine-readable task state outside the conversational transcript so a fresh agent can retrieve the original artifact rather than depending on lossy prose memory. [emerging] Sources: https://factory.ai/news/compressing-context, 2025-07-21; https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus, 2025. citeturn692134search12turn692134search14

I found **no randomized or controlled benchmark directly comparing “resume the same large cold coding-agent transcript” versus “summarize it and start a clean session” on identical real software tasks using current November-2026 Claude/Codex/Gemini models**. [no source found] The GitHub Copilot data measure cache consequences of compaction, and Anthropic/Amp provide quality observations, but none isolate that exact decision. A decisive experiment would randomize matched long-running tasks at a cold-return boundary into full-resume and structured-handoff arms, then score task success, regression rate, user corrections, latency, uncached/cached input, and time-to-completion.

## D. Contradictions and Debates

The first major contradiction is **OpenAI's logged-in Codex promise versus observed telemetry**. The strongest pro-OpenAI interpretation is that logged-in Codex has a separate backend retention/accounting system and that `cached_input_tokens` need not be a perfect proxy for whether the user actually pays or consumes quota as if the request were cold. This is plausible because ChatGPT-authenticated Codex uses a different endpoint from API-key Codex and because OpenAI does not publish the subscription metering formula. [emerging] Sources: https://openai.com/index/unrolling-the-codex-agent-loop/; https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan. citeturn305116view3turn266405view3

The strongest opposing interpretation is simpler: at least some logged-in Codex requests really do lose their reusable prefix because of eviction, routing or hidden prompt mutation, so “guaranteed” was an overstatement. The 11h44m zero-cache event in #56050 and the 26,912-request analysis in #61757 support that interpretation, but neither has server-side billing data. [emerging] [low-authority] Sources: https://github.com/openai/codex/issues/56050; https://github.com/openai/codex/issues/61757. citeturn963314view4turn963314view5

The experiment that would settle this is straightforward: capture identical serialized Codex requests and their client-side cached-token fields across long gaps, correlate them with OpenAI's subscription credit/usage ledger, and obtain server diagnostics indicating `hit`, `expired`, `routing_miss`, or `prefix_changed`. Without the billing-side signal, “zero cached tokens” and “user paid a cold-cache penalty” are not strictly equivalent.

The second disagreement is **hard TTL versus probabilistic survival**. Anthropic's one-hour cache behaves close to a classic expiration contract, and Claude Code is designed around it. OpenAI's older extended caching and Google's implicit caching explicitly allow earlier eviction. Therefore a single “cache TTL” column risks comparing unlike quantities. [established] The article should distinguish `minimum guaranteed retention`, `default ephemeral TTL`, `maximum possible lifetime`, and `empirical hit half-life/survival`.

The third debate is **compaction versus handoff versus full transcript**. Amp's 2025 and 2026 policies directly conflict; both positions are defensible because the underlying models changed. Anthropic simultaneously warns about compaction loss and publishes evidence that resetting context can improve long-horizon coherence. [established] Sources: https://ampcode.com/news/handoff; https://ampcode.com/news/neo; https://www.anthropic.com/research/effective-context-engineering-for-ai-agents; https://www.anthropic.com/research/harness-design-long-running-apps. citeturn981465view5turn981465view6turn981465view15turn981465view14

The right synthesis is not a bland compromise. **Full history maximizes information retention; fresh context maximizes signal-to-noise; compaction is a lossy transform between them.** Which wins depends on whether the task's critical state is recoverable from external artifacts. If the essential state lives in code, tests, a task plan and ADRs, restarting is comparatively safe. If it lives in dozens of conversational corrections and uncommitted reasoning constraints, blocking the resume can be actively harmful. [emerging]

The fourth debate is whether **keep-alive pings are economically rational**. Under a five-minute Anthropic API cache, Aider and several Claude-specific tools keep a large prefix warm by paying tiny periodic cache-read calls rather than a later cache rewrite. This can be rational when probability of near-term return × avoided write cost exceeds ping cost. [established mechanism] Source: https://aider.chat/docs/usage/caching.html. citeturn981465view2 With Claude Code subscription's automatic one-hour TTL and 54-minute idle compaction, however, naive keep-alive pings can interfere with the very idle timer intended to solve the problem. This interaction needs client-specific testing before recommending pingers to subscription users. [emerging]

The fifth debate is whether **context-size thresholds such as 200K or 272K should be treated as cache thresholds**. They should not. Anthropic's 200K figure is an idle-compaction policy threshold. OpenAI's 272K threshold is a pricing/context regime boundary in relevant models, not a documented KV-cache invalidator. No evidence found says crossing either value itself flushes a prefix. [established for the distinction; no source found for any contrary flush rule]

## E. Public measurements comparable to yours

| Dataset | Real production/human sessions? | Size | Cache-related result | Comparison with your fleet |
|---|---:|---:|---|---|
| **GitHub Copilot production paper, 2026** | Yes | ~13M sessions; 3.2M users; 761M LLM calls | Idle gap strongly predicts hit-rate collapse; compaction causes large cache-hit drops; model switches are especially destructive. | Much larger population; different serving TTL. Strongest external proof that idle-gap curves matter. https://borowiecki.dev/pdf/2608.00101, 2026-07-30. citeturn981465view12turn461974view0 |
| **TraceLab, UW, 2026** | Yes | ~4,300 Claude Code/Codex sessions, 43 devs, ~350K LLM steps, ~430K tool calls | High but imperfect prefix reuse; growing long contexts; human-paced gaps create KV-cache opportunities/problems. | Closest open cross-provider dataset. Does not expose your exact long-gap bucket curve. https://arxiv.org/abs/2606.30560, 2026-06-29. citeturn638687view0 |
| **Harvard / FreeInference, 2026** | Yes | ~12K sessions; 209B input tokens; 13 harnesses | User-idle transitions average ~0.84 hit fraction; prompt mutation drives disproportionate fresh prefill. | Supports idle + mutation decomposition; median idle much shorter than your hour-scale analysis. https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/. citeturn981465view7 |
| **Claude Code prompt-cache forensics issue** | Yes, one investigator | 30 sessions; 3,203 calls | TTL expiry, compaction, resumes/model switches concentrated cache writes; median context ~239K, p90 ~707K. | Very similar context sizes; tiny sample. [low-authority] https://github.com/anthropics/claude-code/issues/94177. citeturn981465view10 |
| **agent-cost** | Yes, one developer | 88 sessions; 12,937 turns | ~98.9% aggregate prompt-token cache-read ratio; huge context:output asymmetry. | Useful cost-shape replication, no idle-gap curve. [low-authority] https://github.com/yingxiangge/agent-cost. citeturn981465view11 |
| **Codex issue #61757** | Yes, one deployment | 351 root threads; 26,912 requests | 0.16% intra-turn misses, substantially more first-call misses at longer turn boundaries. | Smallest public dataset that looks directly like your Codex methodology. [low-authority] https://github.com/openai/codex/issues/61757, 2026-11-16. citeturn963314view5 |
| **AGNT Cache Wars** | No; controlled benchmark | 6 harnesses / fixed workload | Cache behavior after deliberately introduced pause. | Mechanistic near-prior-art, not real-session evidence. [low-authority] https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses. citeturn981465view9 |

The strongest novelty claim available to you is therefore narrower than “nobody has measured coding-agent caches.” That would now be wrong. A safer claim is:

> **[emerging] We found prior large-scale measurements of coding-agent prefix-cache hit rates and idle-gap effects, but no published Codex/Claude fleet study with hour-scale human-idle buckets and per-return cold-resume cost attribution matching our methodology.**

That wording survives the 2026 literature found here.

A second defensible contribution is the **economic concentration** result. Public studies establish that cache miss events are sparse but expensive; your Claude analysis goes further by attributing a large fraction of total API-price-equivalent input consumption specifically to humans returning after >1h. The closest public analogue is the Claude cache-forensics issue, but its sample is only 30 sessions. [emerging] citeturn981465view10

## F. Decision rules used in practice, with thresholds

A useful rule should not ask only “is the cache cold?” It needs at least four variables: **effective cache-survival probability, context size, whether the task is still the same task, and how much critical state exists only in conversation history**.

For **Claude Code subscription**, the strongest practical threshold is already supplied by Anthropic: 200K+ context and ~54 minutes idle triggers pre-expiry compaction on current supported clients. [established] Source: v2.1.299 release, https://github.com/anthropics/claude-code/blob/main/feed.xml. citeturn589981search1 Thus a sensible policy is: below 200K, continue unless the task changed; above 200K, treat 45–55 minutes as the handoff decision window. If the conversation contains irreplaceable design/debug state, disable or avoid forced compaction and accept a possible cold resume. If state is reproducible from repo/tests/plan, allow idle compaction or prepare a structured fresh-session handoff. This is [emerging], because the economic half of the rule uses your fleet observations while the 54-minute behavior is official.

For **Claude Code API-key users on the default 5m TTL**, keep-alive strategies can make sense for short interruptions. Aider's five-minute ping mechanism is direct prior art. [established] Source: https://aider.chat/docs/usage/caching.html. citeturn981465view2 For interruptions expected to last tens of minutes, enabling the one-hour cache is operationally cleaner than indefinite pings, subject to its 2× write price and expected reuse. [established mechanism] Source: https://platform.claude.com/docs/en/build-with-claude/prompt-caching and pricing docs. citeturn963314view6turn963314view7

For **pre-GPT-5.6 Codex/API extended caching**, do not use “<24h means warm.” The documented retention distribution makes that rule false. Treat time as a probability input. Your own measured curve is exactly the right primitive: at 1–2h continuation is still often warm; by 6–12h a cold return is the more likely state; by 12–24h it is effectively a cold-start decision in your fleet. OpenAI's docs support the probabilistic framing but not your exact percentages. [established framing] Source: https://developers.openai.com/api/docs/guides/prompt-caching. citeturn266405view0

For **GPT-5.6/GPT-6 API**, use the configured minimum TTL directly: 30m if you choose normal retention; 12h if the economics justify 2.5× cache writes. Maintain an append-only prefix, stable tool definitions and cache breakpoints. For an agent expected to sleep for several hours and resume repeatedly, the 12h option makes the decision more deterministic than the old “up to 24h” scheme. [established] Source: same OpenAI documentation. citeturn266405view0

For **ChatGPT-authenticated Codex**, do not yet implement a hard restart based solely on idle time. OpenAI's stated product direction is persistent resume caching, while public client telemetry is contradictory. Until subscription accounting is clearer, cache-hit telemetry should be treated as an observability signal rather than an authoritative monetary meter. [emerging] Sources: OpenAI announcement plus issues above. citeturn963314view3turn963314view4turn963314view5

For **Gemini implicit caching**, there is no defensible universal idle threshold. Google explicitly says most implicit entries disappear before the 24h maximum. [established] If deterministic economics matter and the API/auth path supports it, use an explicit cache with an explicit TTL; otherwise design for a miss. Source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview. citeturn638687view2

For **Zed**, the published rule is context-based, not time-based: 90% window utilization triggers compaction by default. [established] Source: https://zed.dev/docs/ai/agent-settings. citeturn692134search1

For **task boundaries**, Anthropic's rule is probably the most generally useful: `/clear` for a different task; `/compact` for continuing the same one. [established] Source: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code. citeturn575345search4 This is qualitatively consistent with Zed, Amp, Cline, Factory and Manus even though their mechanics differ.

A practical cross-vendor policy can therefore be expressed as:

1. **Different task → fresh session.** Preserve durable repo/project instructions, not conversational baggage.
2. **Same task, warm cache, context comfortably below quality threshold → continue.**
3. **Same task, cache likely cold, context small/moderate → continue; the reconstruction cost of restart may exceed the cache saving.**
4. **Same task, cache likely cold, context very large, state mostly reproducible → structured handoff/restart.**
5. **Same task, cache likely cold, context very large, substantial non-recoverable conversational state → permit one full cold resume rather than automatically destroying context.**
6. **Near a known expiry while still warm → create the handoff before expiry**, which is exactly the principle behind Claude Code's 54-minute idle compaction. [established mechanism] citeturn589981search1

For an automated tool, I would score something like `P(cold | idle, vendor, model, auth path) × reusable_prefix_tokens × uncached/cache-read cost ratio`, then combine it with a separate **context-loss risk** score based on task status, uncommitted state, recent corrections, and availability of an external plan. A tool implementing this cross-vendor expected-cost/quality policy was **prior art not found** in the searches above.

## G. Recommendations for your article

**Safe claim — [established]:** “Claude Code subscription sessions are built around a one-hour prompt-cache TTL, and current Claude Code deliberately compacts 200K+ conversations at roughly 54 minutes idle to avoid a cold rewrite.” This is directly supported by Anthropic's environment-variable documentation and v2.1.299 release. Sources: https://code.claude.com/docs/ko/env-vars; https://github.com/anthropics/claude-code/blob/main/feed.xml. citeturn589981search0turn589981search1

**Safe claim — [established]:** “A nominal OpenAI 24-hour extended cache did not mean a 24-hour guaranteed hit.” Current OpenAI docs explicitly describe older extended retention as typically around 30 minutes and up to 24 hours, with routing/cache locality factors. Source: https://developers.openai.com/api/docs/guides/prompt-caching. citeturn266405view0

**Safe claim — [established]:** “Gradual Codex cache survival decay between one and 24 hours is compatible with OpenAI's documented older caching architecture.” This is a synthesis of your observation and OpenAI's retention/routing contract; phrase it as compatibility, not proof of the exact backend mechanism. citeturn266405view0

**Needs correction — [established]:** “Recent OpenAI models support up to 24h extended retention with no write surcharge.” This is no longer generally current. GPT-5.6+ now uses 30m/12h retention and charges 1.25×/2.5× for cache writes. Older GPT-5.x models retain the older semantics. Source: same OpenAI guide. citeturn266405view0

**Safe with caveat — [emerging]:** “Logged-in Codex is intended to retain caches across long idle resumes.” Cite OpenAI's October 2026 product announcement, but immediately note that public client telemetry has recorded apparent misses after hours and even shorter boundaries. Do **not** write “Codex caches are guaranteed forever” without that caveat. Sources: https://community.openai.com/t/28-days-of-shipping-at-openai/1403897; https://github.com/openai/codex/issues/56050; https://github.com/openai/codex/issues/61757. citeturn963314view3turn963314view4turn963314view5

**Safe claim — [established]:** “Cache misses are not only TTL events.” OpenAI confirms model changes, tool changes, MCP ordering/list mutations, prefix rewrites and compaction; Google confirms capacity eviction and project isolation; Anthropic confirms per-model caches. Sources: https://openai.com/index/unrolling-the-codex-agent-loop/; https://developers.openai.com/api/docs/guides/prompt-caching; https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview; https://code.claude.com/docs/en/settings. citeturn305116view0turn266405view0turn638687view2turn589981search8

**Do not claim — [speculative]:** “Crossing 200K/272K/1M flushes the cache.” No such rule was found. Anthropic's 200K is a client idle-compaction trigger. OpenAI's context/pricing boundaries should not be conflated with cache validity. [no source found for a tier-triggered flush]

**Do not claim — [speculative]:** “Updating CLAUDE.md always makes a session cold.” Prefix mutation can do so, but one small Claude forensics dataset found no such breaks from CLAUDE.md/memory edits in its sample. [low-authority] Source: https://github.com/anthropics/claude-code/issues/94177. citeturn981465view10

**Safe claim — [established]:** “Google implicit caching has no fixed hit guarantee; current Cloud docs cap lifetime at 24h while saying most entries are evicted sooner.” Source: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview. citeturn638687view2

**Needs caveat — [speculative]:** “Antigravity's cache randomly expires after tens of seconds.” There are reports showing that symptom, but there is no byte-for-byte request capture demonstrating that the prefix truly stayed identical. Say “Antigravity users have reported intermittent zero-cache calls within seconds/minutes; routing, hidden prompt mutation and backend eviction are not yet distinguished.” [low-authority] Sources: https://github.com/google-antigravity/antigravity-cli/issues/1533; https://github.com/google-antigravity/antigravity-sdk-python/issues/229. citeturn963314view14turn963314view15

**Safe novelty claim — [emerging]:** “Large public coding-agent datasets now measure cache reuse and idle-gap effects, but we found no previous hour-scale Codex/Claude fleet analysis with the same cold-resume cost attribution.” Cite GitHub Copilot, TraceLab and Harvard and describe precisely how your methodology differs. Sources: https://borowiecki.dev/pdf/2608.00101; https://arxiv.org/abs/2606.30560; https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/. citeturn981465view12turn638687view0turn981465view7

**Safe caveat — [established]:** “API-price-equivalent token cost is not the same thing as subscription-plan consumption.” Both Anthropic and OpenAI acknowledge that caching affects usage accounting, but neither publishes a simple Plus/Pro/Max multiplier matching API prices. Sources: https://support.claude.com/en/articles/9797557-usage-limit-best-practices; https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop. citeturn638687view1turn981465view17

**Avoid a hard universal “never resume cold” recommendation.** [emerging] A better article conclusion is conditional because a large cold transcript can still be the highest-fidelity state representation. Anthropic's long-horizon work supports context resets for coherence, but its context-engineering guidance also warns that compaction loses detail; Amp reversed its own policy as model quality changed. citeturn981465view14turn981465view15turn981465view5turn981465view6

The concrete options are therefore:

- **Full resume:** highest state fidelity; potentially worst cold-prefill cost and context-rot risk.
- **Warm-cache handoff before expiry:** usually best economics; risks summary loss; Claude Code's 54-minute compaction is direct prior art.
- **Fresh session with structured external state:** best for task boundaries and heavily polluted contexts; requires good plans/ADRs/test state.
- **Keep-alive:** useful on short TTLs when expected return is near; wastes requests if the user never returns and can interact badly with idle-compaction logic.
- **Explicit/durable cache:** best where the API supports it and predictable retention is more important than write/storage cost.

**Single recommendation — [emerging]: implement “handoff-before-expiry, but never hard-block full resume.”** For Claude subscription sessions, use the 45–55-minute region as the decision window for large contexts; for old OpenAI extended caches use your measured survival curve rather than a nominal 24h TTL; for GPT-5.6+/GPT-6 use the configured 30m/12h contract; for Gemini implicit cache assume misses are possible at any later point unless an explicit cache is being used. The main assumption is that **task state can usually be externalized into code, tests, plans and a structured handoff, but some high-value sessions contain irreducible conversational state**. A soft warning offering `continue full context`, `handoff + restart`, and `cancel` preserves that escape hatch while capturing most of the avoidable cache tax.

## H. Sources

OpenAI, **Prompt caching**, live API documentation, accessed 2026-11-20.  
https://developers.openai.com/api/docs/guides/prompt-caching citeturn266405view0

OpenAI, **Better prompt caching for GPT-6**, 2026-09-22.  
https://openai.com/index/better-prompt-caching-for-gpt-6/ citeturn266405view1

OpenAI / Michael Bolin, **Unrolling the Codex agent loop**, 2026; exact publication date was not displayed in the opened page text.  
https://openai.com/index/unrolling-the-codex-agent-loop/ citeturn266405view2turn305116view0

OpenAI Developer Community, **28 days of shipping at OpenAI**, thread opened 2026-10-06; relevant cache announcement posted during the October 2026 sequence.  
https://community.openai.com/t/28-days-of-shipping-at-openai/1403897 citeturn963314view3

OpenAI Codex GitHub issue #56050, cache miss after long idle resume, 2026-10-22. [low-authority]  
https://github.com/openai/codex/issues/56050 citeturn963314view4

OpenAI Codex GitHub issue #61757, persisted-thread cache-miss analysis, 2026-11-16. [low-authority]  
https://github.com/openai/codex/issues/61757 citeturn963314view5

OpenAI Help Center, **Using Codex with your ChatGPT plan**, live documentation, accessed 2026-11-20.  
https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan citeturn266405view3

OpenAI Help Center, **Reviewing Work and Codex usage and using Personal Analytics in ChatGPT desktop**, live documentation, accessed 2026-11-20.  
https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop citeturn981465view17

OpenAI Help Center, **Using credits for flexible usage in ChatGPT personal plans**, live documentation, accessed 2026-11-20.  
https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans citeturn981465view18

Anthropic, **Prompt caching**, live Claude API documentation, accessed 2026-11-20.  
https://platform.claude.com/docs/en/build-with-claude/prompt-caching citeturn963314view6

Anthropic, **Pricing**, live Claude API documentation, accessed 2026-11-20.  
https://platform.claude.com/docs/en/about-claude/pricing citeturn963314view7

Anthropic, **Claude Code environment variables**, live docs, accessed 2026-11-20.  
https://code.claude.com/docs/ko/env-vars citeturn589981search0

Anthropic, **Claude Code settings**, live docs, accessed 2026-11-20.  
https://code.claude.com/docs/en/settings citeturn589981search8

Anthropic, **Claude Code v2.1.299 release feed**, release dated 2026-10-14.  
https://github.com/anthropics/claude-code/blob/main/feed.xml citeturn589981search1

Anthropic Claude Code issue #107073, gateway/idle-compaction A/B report, 2026. [low-authority]  
https://github.com/anthropics/claude-code/issues/107073 citeturn589981search2

Anthropic Claude Code issue #103931, idle-compaction failure report, 2026-10. [low-authority]  
https://github.com/anthropics/claude-code/issues/103931 citeturn589981search6

Agent Client Protocol / Claude Agent ACP issue #1518, idle-compaction entrypoint behavior, 2026-11. [low-authority]  
https://github.com/agentclientprotocol/claude-agent-acp/issues/1518 citeturn589981search3

Anthropic Claude Code issue #94177, prompt-cache forensics, 2026. [low-authority]  
https://github.com/anthropics/claude-code/issues/94177 citeturn981465view10

Anthropic Help Center, **Usage limit best practices**, updated 2026-09-22 / current page updated shortly before access.  
https://support.claude.com/en/articles/9797557-usage-limit-best-practices citeturn638687view1

Anthropic Help Center, **How do usage and length limits work?**, current documentation, accessed 2026-11-20.  
https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work citeturn575345search2

Anthropic Help Center, **Use Claude Code with your Pro, Max or Ultra plan**, live documentation, accessed 2026-11-20.  
https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan citeturn981465view13

Anthropic Help Center, **Models, usage, and limits in Claude Code**, current documentation, accessed 2026-11-20.  
https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code citeturn575345search4

Anthropic Research, **Effective context engineering for AI agents**, 2025; older source retained because it remains directly relevant to compaction loss.  
https://www.anthropic.com/research/effective-context-engineering-for-ai-agents citeturn981465view15

Anthropic Research, **Harness design for long-running apps**, 2026.  
https://www.anthropic.com/research/harness-design-long-running-apps citeturn981465view14

Anthropic, **An update on Claude Code quality reports**, 2026.  
https://www.anthropic.com/research/april-23-postmortem citeturn589981search11

Google Cloud, **Context caching overview — Gemini Enterprise Agent Platform**, last updated 2026-11-20 UTC.  
https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview citeturn638687view2

Google Cloud, **Create a context cache**, current documentation, accessed 2026-11-20.  
https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-create citeturn575345search5

Google Developers Blog / Logan Kilpatrick, **Gemini 2.5 Models now support implicit caching**, 2025-05-08.  
https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/ citeturn638687view3

Google Gemini CLI, **Token caching**, current GitHub documentation, accessed 2026-11-20.  
https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md citeturn963314view12

Google AI Developers Forum, **Implicit caching hits are inconsistent**, 2025. [single-source forum evidence]  
https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666 citeturn963314view13

Google Antigravity CLI issue #1533, intermittent cache-hit report, 2026-11. [low-authority]  
https://github.com/google-antigravity/antigravity-cli/issues/1533 citeturn963314view14

Google Antigravity Python SDK issue #229, cache-volatility report, 2026-09-28. [low-authority]  
https://github.com/google-antigravity/antigravity-sdk-python/issues/229 citeturn963314view15

Zhu et al., **TraceLab: Characterizing Coding Agent Workloads for LLM Serving**, arXiv, 2026-06-29.  
https://arxiv.org/abs/2606.30560 citeturn638687view0

GitHub Copilot production-trace paper, 2026-07-30.  
https://borowiecki.dev/pdf/2608.00101 citeturn981465view12turn461974view0

Harvard Systems Group, **Agentic Traces / FreeInference production analysis**, 2026.  
https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/ citeturn981465view7

Companion FreeInference / agentic-systems paper, 2026.  
https://opendata.agentic-system.org/pdf/paper/from-requests-to-sessions citeturn981465view8

yingxiangge, **agent-cost**, real Claude Code session analysis, report dated 2026-09-10. [low-authority]  
https://github.com/yingxiangge/agent-cost citeturn981465view11

AGNT, **The Cache Wars: Prompt Cache Efficiency in LLM Agent Harnesses**, 2026. [low-authority controlled benchmark]  
https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses citeturn981465view9

Cursor, **Improved token efficiency for longer agent runs**, 2026. [single-source vendor engineering report]  
https://prod.cursor.com/blog/improved-token-efficiency citeturn981465view0

Amp, **Handoff**, 2025-10-23.  
https://ampcode.com/news/handoff citeturn981465view5

Amp, **Rebuilt / Neo architecture update**, 2026.  
https://ampcode.com/news/neo citeturn981465view6

Amp, **Threads documentation**, live docs, accessed 2026-11-20.  
https://ampcode.com/docs/threads citeturn981465view4

Amp, **Model selector documentation**, live docs, accessed 2026-11-20.  
https://ampcode.com/docs/model-selector citeturn981465view3

Cline, **Auto Compact**, live documentation, accessed 2026-11-20.  
https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx citeturn981465view1

Aider, **Prompt caching**, live documentation, accessed 2026-11-20.  
https://aider.chat/docs/usage/caching.html citeturn981465view2

Zed, **Agent Settings / Automatic Compaction**, live documentation, accessed 2026-11-20.  
https://zed.dev/docs/ai/agent-settings citeturn692134search1

Zed, **Agent Panel**, live documentation, accessed 2026-11-20.  
https://zed.dev/docs/ai/agent-panel citeturn692134search0

Factory, **Compressing Context**, 2025-07-21.  
https://factory.ai/news/compressing-context citeturn692134search12

Factory, **Agent Native Development / Build with Agents**, 2025-07-01.  
https://factory.ai/news/build-with-agents citeturn692134search18

Manus, **Context Engineering for AI Agents: Lessons from Building Manus**, 2025. [single-source vendor engineering essay]  
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus citeturn692134search14

Devin Central, **Devin CLI adds interruptible steering and session summaries**, 2026-10-22. [low-authority; release-note aggregator rather than Cognition primary source]  
https://devincentral.com/continuity/cli/2026-w43 citeturn893033search0

## Sources (from ChatGPT report metadata, 51 URLs)
- https://agnt.gg/whitepapers/the-cache-wars-prompt-cache-efficiency-llm-agent-harnesses
- https://aider.chat/docs/usage/caching.html
- https://ampcode.com/docs/model-selector
- https://ampcode.com/docs/threads
- https://ampcode.com/news/handoff
- https://ampcode.com/news/neo?from=bd_signal
- https://arxiv.org/abs/2606.30560
- https://borowiecki.dev/pdf/2608.00101
- https://code.claude.com/docs/en/settings?_rsc=vr6dg
- https://code.claude.com/docs/ko/env-vars
- https://community.openai.com/t/28-days-of-shipping-at-openai/1403897
- https://developers.googleblog.com/gemini-2-5-models-now-support-implicit-caching/
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://devincentral.com/continuity/cli/2026-w43
- https://discuss.ai.google.dev/t/have-anyone-checked-out-the-implicit-caching-for-gemini-api-caches-hits-are-inconsistent-for-me/82666
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-create?hl=en
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview
- https://factory.ai/news/build-with-agents
- https://factory.ai/news/compressing-context
- https://github.com/agentclientprotocol/claude-agent-acp/issues/1518
- https://github.com/anthropics/claude-code/blob/main/feed.xml
- https://github.com/anthropics/claude-code/issues/103931
- https://github.com/anthropics/claude-code/issues/107073
- https://github.com/anthropics/claude-code/issues/94177
- https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx
- https://github.com/google-antigravity/antigravity-cli/issues/1533
- https://github.com/google-antigravity/antigravity-sdk-python/issues/229
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md
- https://github.com/openai/codex/issues/56050
- https://github.com/openai/codex/issues/61757
- https://github.com/yingxiangge/agent-cost
- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans
- https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- https://openai.com/index/better-prompt-caching-for-gpt-6/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://opendata.agentic-system.org/pdf/paper/from-requests-to-sessions
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching?_bhlid=44b6a1b689fab6535cd6a5b4832b355c52b84738&fcdaa149_sort_date=desc
- https://prod.cursor.com/blog/improved-token-efficiency
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-max-or-ultra-plan?campaignId=13755893&content=Oct2024AnalysisTool&medium=email&messageTypeId=140367&source=i_email
- https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices?stream=top
- https://systems.seas.harvard.edu/blog/agentic-traces-freeinference/
- https://www.anthropic.com/research/april-23-postmortem
- https://www.anthropic.com/research/effective-context-engineering-for-ai-agents?source=post_page-----f64bd1b56d9f---------------------------------------
- https://www.anthropic.com/research/harness-design-long-running-apps
- https://zed.dev/docs/ai/agent-panel?highlight=profile
- https://zed.dev/docs/ai/agent-settings
