Thought Process

I'll conduct this deep research investigation systematically. The request is fully specified (format A–H, English, in-chat Markdown), so I'll proceed directly: plan → extensive searches (30+) → open and verify key sources → synthesize the report with confidence tiers and flags.

Plan
0 of 8 complete
Search official docs: Anthropic, OpenAI, Google caching (TTLs, surcharges, discounts)
Search invalidators: tool/MCP changes, model switch, compaction, thinking budget, etc.
Search continue-vs-restart heuristics: Manus, Anthropic blog, Amp, Cursor, Aider, Cognition, Zed, Devin
Search public measurements of cache hit vs idle gap; prior art repos (cache-keeper, cache-tax etc.)
Search subscription vs API accounting (Claude Pro/Max, ChatGPT limits)
Search context rot / summarize-restart degradation evidence
WebFetch key doc pages for exact wording and dates
Write full report (A-H) in chat with citations, tiers, flags
Thought Process

Starting with the official documentation for all three vendors (search batch 1 of ~8):

1 Searches

Excellent first batch — I found a key GitHub issue (claude-code#46829) with 119K API calls of measurement data, plus OpenAI's extended retention docs. Continuing with search batch 2 (Gemini, Codex, subscription specifics):

1 Searches

Strong results — I now have OpenAI's exact retention wording, a major Claude Code TTL-regression issue, and Gemini's new caching rules. Next: search batch 3 on cache invalidators:

1 Searches

Invalidators are mapping out well (thinking-budget changes, MCP changes, reasoning-effort switches — with a notable GPT-6 exception). Search batch 4: continue-vs-restart heuristics from other teams:

1 Searches

Strong prior art found (Manus, Amp handoff, Anthropic cookbook). Search batch 5: public measurements and cache-keeper tools:

1 Searches

Partial results. Continuing with search batch 6 (more measurements, context-rot evidence, Chroma):

1 Searches

Chroma's Context Rot (July 2025) confirmed. Search batch 7: subscription vs API accounting (Q5):

1 Searches

Search batch 8: Gemini CLI / Antigravity, Claude Code's official costs doc, idleCompaction:

1 Searches

Now I have the full landscape. Time to open the critical primary sources for exact wording. Fetch batch 1 (official vendor docs):

Explored 2 files

Two primary sources captured with exact pricing tables (confirming your 0.05x/0.025x/1.25x/2x weights) and a full invalidation taxonomy. The Claude Code TTL table was truncated — fetching the remainder plus OpenAI's guide:

Explored 2 files

The Claude Code page truncates at the same point each time — trying the markdown endpoint for the TTL table, plus OpenAI's retention section:

Explored 2 files

OpenAI's guide gives me the exact retention wording and — critically — a new GPT-5.6+ cache write surcharge (1.25×/2.5×). Still need the Claude Code TTL-allocation table; trying a targeted fetch of the tail of the markdown page:

Ran 1 commands

curl works. Extracting the final sections (cache lifetime table, TTL selection, hit-rate checking):

Ran 1 commands

The TTL table is captured — including the crucial detail that falling back to usage credits silently drops the main conversation to the 5-minute TTL. Now fetching the Anthropic "Prompt caching is everything" blog, OpenAI's diagnostics page, and the big GitHub measurement issue:

Explored 3 files

GitHub issue #46829 fully captured — Anthropic staff confirmed the March 2026 TTL change, and lizthegrey identified the exact bugs. WebFetch budget is capped, so switching to curl for the remaining sources:

Ran 2 commands

The Anthropic "caching is everything" blog (Apr 30, 2026) is captured with strong quotes. Getting the rest of it plus Manus/Amp/Aider:

Ran 1 commands

Now extracting Manus and Aider, and fetching the next source batch (subscription accounting + pricing):

Ran 1 commands

Manus and Aider captured (including Aider's built-in --cache-keepalive-pings). Next batch: subscription accounting, OpenAI pricing table, Gemini explicit caching, and the codex issue via GitHub API:

Ran 2 commands

GitHub API is rate-limited; using WebFetch for the two codex issues and Gemini's explicit-caching section (fresh message, fresh web budget):

Explored 3 files

WebFetch quota is now exhausted session-wide — switching fully to curl for the remaining ~10 sources:

Ran 3 commands

Both codex issues fully extracted with measurement tables. Now extracting the remaining six sources:

Ran 6 commands

The original postmortem is captured verbatim. Testing whether WebSearch still has budget for the last gap areas (Deriv URL, Cursor/Zed, Antigravity, gemini-cli):

1 Searches

Search budget is now exhausted (40 queries run). Extracting the last few local files for tool economics details:

Ran 1 commands

All research is complete — 40 search queries run, 25+ sources opened and verified. Marking todos done and writing the full report:

Thought Process
DR26-11-20-MACSTUDIOM4-01-0251 — Prompt cache lifetime in Codex, Claude Code and Gemini: official vs observed TTL, invalidators, continue-or-restart, public measurements

Research date: 2026-11-20. Method note: 40 web search queries run; every URL listed in Section H was opened and read in full during this session except where explicitly flagged as "search-index capture" or "[no source found — search trail listed]". Nothing below is quoted from memory; all quotes were taken from pages opened today.

A. Executive Summary
There is no single "official TTL" at any vendor in November 2026 — there are TTL buckets, and which bucket a request lands in is a function of billing state, model, client version and request type. For Claude Code, the official docs state verbatim: "Claude Code requests the one-hour TTL only on a Claude subscription within your plan's included usage"; the table gives Main conversation: One hour (subscription) / Five minutes (usage credits, API key, or cloud provider) (code.claude.com/docs/en/prompt-caching, accessed 2026-11-20). Your fleet's "sharp cliff at the 60th minute" is exactly this table.
OpenAI's "up to 24 h" is explicitly not a guarantee in the current docs: "24h: Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours" (developers.openai.com/api/docs/guides/prompt-caching, accessed 2026-11-20). Your observed gradual Codex decay between 1 h and 24 h is more consistent with the documented wording than a hard 24 h would be. Azure's implementation note (KV-tensor offload to GPU-local storage "when memory is full") provides the eviction-under-load mechanism (learn.microsoft.com, 2026-11-06).
Your OpenAI price model needs one correction: cache writes are no longer free on the newest OpenAI models. "For GPT-5.6 and later, cache writes cost 1.25× the standard, uncached input-token rate for the default 30-minute lifetime. In the Responses API, you can choose a 12-hour minimum lifetime at a write rate of 2.5×" (developers.openai.com/api/docs/guides/prompt-caching, accessed 2026-11-20). No surcharge remains only on pre-5.6 models.
Your Anthropic price weights are confirmed by official docs: 1.25× (5-min write) / 2× (1-h write), reads 0.05× on Opus 5.5 and Sonnet 5.5, 0.025× on Fable 5.1/5.2 and Mythos, 0.1× on everything else (platform.claude.com/docs/en/build-with-claude/prompt-caching, accessed 2026-11-20).
The biggest gap in your cost model (Q5) is only partially closeable from public sources. Anthropic officially says cached portions "count less against your limits" (no formula: support.claude.com, updated ~2026-10-30); issue evidence says cache creation tokens count at full rate and reads much cheaper (github.com/anthropics/claude-code#46829, Apr 2026); one plugin author claims subscription quota is "gated by request count, not token cost" (contradicting the above; [single-source, low-authority]). Treat your API-list-price cost model as a defensible upper-bound proxy, not a quota model.
For Q4, no one has published your kind of curve. No public source found that plots cache-hit rate vs idle-gap buckets from real agent session logs at your scale (71K–2.3K sessions). Closest: a 119,866-call JSONL analysis of a TTL regression (#46829) and a 41-day single-session cost breakdown (Reddit r/LLMDevs, ~May 2026). Your fleet measurement is, as of today, the largest public-by-vendor-shape dataset on this question — see Section E for the full trail.
Practitioner practice has converged on three named patterns: keep-alive pings (Aider --cache-keepalive-pings, cache-tax /keepwarm 90m), idle compaction before expiry (Claude Code idleCompaction, built-in), and extract-then-restart ("Handoff", Amp, Oct 2025). Nobody publishes thresholds validated by task-quality data.

Confidence summary: vendor pricing and invalidator claims below are [established] (official docs, multiple corroborations). Vendor quota weighting is [emerging] at best. Your gradual-decay interpretation for Codex is [emerging] and, notably, the docs support it.

B. Per-vendor table (official vs observed, as of 2026-11-20)
	
ANTHROPIC (CLAUDE CODE / MESSAGES API)
	
OPENAI (RESPONSES API / CODEX CLI)
	
GOOGLE (GEMINI API / CLI)

Official TTL	5-min default, "refreshed for no additional cost each time the cached content is used"; 1-h optional ("1-hour cache duration at additional cost"). Claude Code: main conversation 1 h only on subscription within plan usage; everything else (subagents, forks, compaction, titles) 5 min; usage-credits/API-key/cloud = 5 min everywhere unless you set promptCacheTtl: "1h" (code.claude.com, platform.claude.com)	Retention buckets: in_memory = "typically remain active for around 5 to 10 minutes of inactivity, up to one hour"; 24h = "typically keeps entries available for around 30 minutes and can retain them for up to 24 hours". Orgs without ZDR default to 24h; ZDR orgs default to in_memory. GPT-5.6+: default "30m" minimum lifetime or "12h" (developers.openai.com)	Implicit caching: enabled by default on Gemini 2.5+; min prefix 2,048 (2.5 Pro) / 4,096 (3.x, 4.x); no TTL stated in the caching guide; Vertex blog (older): "Implicit caches are cleared in 24 hours or less". Explicit caching: TTL you set, billed hourly per stored MTok; explicit caching not supported on Gemini 4 models or the Interactions API (aistudio.google.com/docs/caching, search-index capture; cloud.google.com Vertex blog, older — 2024/2025)
Observed TTL	Your fleet: cold in almost every case after >1 h idle on subscription; cliff at 60th minute — consistent with the 1-h bucket. Known drift episode: default silently moved 1 h→5 m in early March 2026 for some billing states (staff-confirmed; see Q1)	Your Codex fleet: gradual decay 10% (30–60 m) → 17% (1–2 h) → 46% (2–6 h) → 74% (6–12 h) → 98% (12–24 h) → 100% (>24 h). Consistent with "typically ~30 minutes availability, up to 24 h" + eviction under load; consistent with 24h default bucket for non-ZDR orgs	No public fleet-scale observation found. Google forum reports of implicit-cache misses above the advertised minimum threshold exist (search-index capture, Apr 2026) [single-source each]
Write surcharge	1.25× (5-min), 2× (1-h) — official	No surcharge: pre-GPT-5.6 models. 1.25× (30-min) / 2.5× (12-h) on GPT-5.6+ — official (developers.openai.com)	Implicit: none stated. Explicit: input price to create + hourly storage charge — official
Read discount	0.1× standard; 0.05× Opus 5.5 & Sonnet 5.5; 0.025× Fable 5.1/5.2, Mythos 5.1/5.2 — official pricing table with per-MTok prices (platform.claude.com)	"discounted up to 95%" (i.e. 0.05×) on newest; ~0.1× widely reported on GPT-5.x-generation (HoneyHive, community); per-model table sits on the pricing page (Cloudflare-blocked in this sandbox — see H)	Implicit: "same 75% token discount" as explicit (2025 announcement; Gemini 3/4-era forum posts cite 90–95%) [mixed-vintage sources]
Invalidators (confirmed)	Model switch; effort change (except Fable 5.1+, Opus 5.5, Sonnet 5.5, Haiku 5.5 on API/subscription since v2.1.260); fast-mode toggle; MCP server add/remove (unless tool-search defers); plugin enable/disable (MCP-providing only); deny-rule tool removal (without tool search); compaction; image accumulation (batch removal); client upgrade; falling back from subscription to usage credits (drops TTL 1 h→5 m); gateway stripping cache_control (code.claude.com; platform.claude.com)	Model change; tools change; parallel_tool_calls; text.format (Structured Outputs); reasoning.effort (GPT-5.6-: full/partial miss; GPT-6+: changeable "without breaking cache" per changelog entry — see Q2); text.verbosity; compaction/context management; different prompt_cache_key (routing, pre-5.6) (developers.openai.com guide; openai/codex#35416)	Prefix change (tools/system/messages order like Anthropic); for Gemini 4 agent loops: "caches the full previous request only if the new request adds at least 2,050 tokens"; below that, "re-processes the last 2,050 tokens of the previous request at the standard input rate" (aistudio.google.com/docs/caching, search-index capture)
Key sources	docs (accessed 2026-11-20), API docs, #46829	guide (accessed 2026-11-20), #35416, #29377, Azure	caching docs (search-index capture), Google blog (2025-05-08)
C. Key findings per question
Q1. Official vs observed TTL

Anthropic — official. The API doc is precise and current: "By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used. The lifetime is measured from the start of the request that writes or reads the cache entry… If 5 minutes is too short, you can use a 1-hour cache duration at additional cost" (platform.claude.com/docs/en/build-with-claude/prompt-caching, accessed 2026-11-20) [established]. Claude Code allocates TTLs per request bucket: the one-hour TTL is requested for the main conversation only on a Claude subscription within plan usage; once you cross into usage credits, "Claude Code drops the main conversation to the five-minute TTL, which charges a lower rate for cache writes" (code.claude.com/docs/en/prompt-caching, accessed 2026-11-20) [established]. You can override: promptCacheTtl / CLAUDE_CODE_PROMPT_CACHE_TTL (v2.1.242+), ENABLE_PROMPT_CACHING_1H=1, FORCE_PROMPT_CACHING_5M=1 [established]. Verify per call via usage.cache_creation.ephemeral_1h_input_tokens vs ephemeral_5m_input_tokens (same page).

Anthropic — observed/drift. A JSONL analysis of 119,866 API calls across two machines (2026-01-11→04-11) found the default silently flipped 1 h→5 m around 2026-03-06 for that user's billing state: Feb 1–Mar 5 shows ephemeral_5m = 0 for 33 straight days; Mar 8 onward 5-minute writes outnumber 1-hour 5:1; quantified waste $949 (Sonnet 4.6) + $1,582 (Opus 4.6), 17.1% of cache spend (github.com/anthropics/claude-code/issues/46829, opened 2026-04-12) [emerging→established: Anthropic staff replied]. Staff (Jarred-Sumner, 2026-04-12) confirmed a deliberate March 6 change as part of a "cache optimization", said "the client picks TTL per request based on expected cache-reuse pattern" and that "1h everywhere would increase total cost for their request mix"; lizthegrey (2026-05-08) later identified two client bugs (overage-latch; telemetry-disabled fallback) fixed in v2.1.90 (2026-04-01) and v2.1.106 (2026-04-13) [established]. Implication for your article: the 1-h default on subscription is real but conditional (billing state, org config, client version, bugs); anyone citing a "hard 1-hour Anthropic cache" without the conditions will be wrong for someone.

OpenAI — official. Exact doc wording, accessed 2026-11-20 (developers.openai.com/api/docs/guides/prompt-caching):

"Organizations without Zero Data Retention enabled default to 24h. Organizations with Zero Data Retention enabled default to in_memory."
"in_memory: Entries typically remain active for around 5 to 10 minutes of inactivity, up to one hour."
"24h: Extended retention typically keeps entries available for around 30 minutes and can retain them for up to 24 hours."
Extended retention supported on gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, gpt-5.1-codex-max, gpt-5.1, gpt-5.1-codex, gpt-5.1-codex-mini, gpt-5.1-chat-latest, gpt-5, gpt-5-codex, gpt-4.1.
"For GPT-5.6 and later, cache writes cost 1.25× … default 30-minute lifetime … 12-hour minimum lifetime at a write rate of 2.5×."

That "typically around 30 minutes … up to 24 hours" sentence is the single most important doc line for your Codex section: OpenAI documents a decaying availability distribution, not a hard TTL — your observed 1 h→24 h gradual decay is what the wording predicts. The mechanism is described in Azure's mirror doc: extended retention "works by offloading the key/value tensors to GPU-local storage when memory is full" — i.e., a capacity-managed tier, hence eviction under load (learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching, 2026-11-06) [established]. Azure adds: for gpt-5.4 and older the default is in_memory; "For gpt-5.5, extended retention is enabled by default." Whether the Codex CLI passes prompt_cache_retention explicitly is not documented publicly [no source found — searched OpenAI docs and codex repo; see E]. Codex CLI facts that are established: fresh codex exec sessions use the thread ID as the Responses API prompt_cache_key (openai/codex#29377, 2026-06-22), and on models before GPT-5.6 "Keys influence routing; they do not pin requests to a machine or guarantee a cache hit" (guide, same URL) [established].

Google — official. Implicit caching is on by default for Gemini 2.5+ with per-model minimums (2.5 Flash/Pro 2,048; 3.x and 4.x 4,096); savings are passed through automatically; the Interactions API and Gemini 4 models do not support explicit caches (aistudio.google.com/docs/caching, search-index capture, content verified 2026-11-20) [established]. No TTL is stated for implicit caches in the current guide; the older Vertex AI blog says "Implicit caches are cleared in 24 hours or less" (cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching, undated in capture — pre-2025 source, treat as historical) [emerging for 2026 behavior]. The 2025 announcement promised "the same 75% token discount" as explicit caching (developers.googleblog.com, 2025-05-08) — note this is a 2025 promise for 2.5 models; current 3.x/4.x discount percentages on hits are reported at 90–95% in developer-forum posts [single-source, low-authority each]. Gemini CLI / Antigravity cache behavior: [no source found] — searched Google's docs, the gemini-cli GitHub repo README and Antigravity pages; neither documents cache TTL or hit-rate behavior. This is a genuine hole; for Gemini CLI the only official statement adjacent to caching is the API doc's "send requests with similar prefix in a short amount of time".

Your Codex decay curve vs docs — verdict: consistent. The docs' "typically ~30 min, up to 24 h" plus GPU-local eviction predicts a monotone decaying survival curve with a heavy tail to 24 h, exactly your 46%→74%→98%→100% buckets. What the docs do not explain is your near-flat behavior below ~1 h (10% cold at 30–60 min) unless Codex sessions mostly hit a warm 24h-bucket entry; the likeliest reconciliation is that Codex (non-ZDR org) lands in the 24h bucket by default, where ~30-min typical availability plus LRU pressure under fleet load produces your shape. That reconciliation is ours, not documented — label it [speculative] in the article, and note the test that would settle it: run identical Codex sessions with prompt_cache_retention: "in_memory" vs "24h" vs unset and compare the survival curves (OpenAI guide documents the parameter; Codex CLI exposes prompt_cache_key_override per a contributor comment in #29377, 2026-08-25).

Q2. What resets the cache besides time

All of the following are confirmed by vendor docs opened today unless flagged.

Anthropic (Claude Code + API) — [established] (code.claude.com/docs/en/prompt-caching; platform.claude.com/docs/en/build-with-claude/prompt-caching):

Model switch — "Each model has its own cache. Switching with /model means the next request reads the entire conversation history with no cache hits, even though the content is identical." Includes the opusplan setting (each plan-mode toggle is a switch) and automatic safety-classifier fallback.
Effort change — invalidates on most models; kept on Fable 5.1+, Opus 5.5, Sonnet 5.5, Haiku 5.5 with API key/subscription (v2.1.260+); still invalidates on Bedrock, Google Cloud Agent Platform, apps gateway, or with CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS.
Fast-mode toggle — separate caches per speed; automatic speed fallback after a rate limit also counts.
MCP servers — with tool search (default on supported models), mid-session connect/disconnect does not invalidate; without it, adding definitions or intentionally removing tools invalidates, while a server silently dropping out does not.
Plugins — never invalidated for skills/commands/agents/hooks; invalidated like MCP for MCP-providing plugins; re-enabling a previously disabled plugin can hit the older cache entry if still in TTL.
Deny rules on a whole tool — invalidates when tool search is off (definition removed from request).
Compaction — by design invalidates the conversation layer; the summarization request itself reuses the prefix only when warm (see "cache-safe forking" below).
Image accumulation — when request limits are hit, oldest images are dropped in batches and "the next request reprocesses the conversation from the earliest of those messages onward" (partial invalidation).
Client upgrade — "A new Claude Code version typically updates the system prompt or tool definitions, so the first conversation you start after an upgrade builds its cache from the top."
Billing-state change — crossing from subscription into usage credits silently drops the main-conversation TTL from 1 h to 5 m (docs; bug variants documented in #46829 and related issue #49139 "billing state affecting TTL selection").
Gateway handling — a gateway that strips cache_control while returning success makes "your entire conversation history bill as uncached input on every turn."
API-level table (same sources): tool-definition changes invalidate everything; web-search/citations toggles and speed setting invalidate system+messages; tool_choice and image changes invalidate messages only; thinking parameters (mode or budget_tokens) "always invalidate message blocks" and tool/system too on models that render config ahead of them; dropping unpreserved thinking blocks invalidates from that block onward.
Keeps cache: file edits, mid-session CLAUDE.md edits (loaded at session start), permission-mode changes, output-style changes (delivered as a message), skills/commands, /recap, /rewind (truncates to a cached prefix), spawning subagents, forks.

OpenAI — [established] from the guide (developers.openai.com/api/docs/guides/prompt-caching) unless noted: the main settings that affect the cached prefix are model, tools, parallel_tool_calls, text.format (Structured Outputs; on GPT-6+ a format update can be appended instead), reasoning.effort ("On supported models, use a configuration update to change effort while preserving the earlier prefix"), text.verbosity, and compaction (context_management) which "can prevent reuse from the first changed token onward". For Codex specifically: changing reasoning effort to a new value causes a full-ish cache miss on GPT-5.6-class models; measured table in openai/codex#35416 (2026-07-26): hit rate drops ~93%→~66%, lost 4,096–5,120 tokens, and — notably — "Returning to a previously set reasoning level does not cause a severe cache miss" (effort-keyed cache entries). The legacy cookbook "Prompt Caching 201" listed "Changes to reasoning effort" as a cause, applying "only to models before GPT-5.6" (quoted in #35416; the cookbook itself was Cloudflare-blocked in this sandbox — see H) [emerging]. For GPT-6, a Sep 2026 changelog entry titled "Better prompt caching for GPT-6" states effort can now change "without breaking cache" — URL not resolvable in this sandbox (search-index capture); treat as [emerging]. Account/organization: Anthropic isolates caches between organizations and on some providers between workspaces; Azure does not share caches between subscriptions [established]. Rate-limit rerouting: on Anthropic, automatic model fallback is a model switch, and fast-mode fallback is a toggle [established]; on OpenAI, re-routing manifests as probabilistic misses because keys "influence routing… do not pin requests to a machine" [established].

Injected timestamps / system reminders: Anthropic's own engineering write-up: "We've broken this ordering before… putting an in-depth timestamp in the static system prompt, shuffling tool order definitions non-deterministically, and updating parameters of tools" — their fix is to append changes as <system-reminder> messages "which helps preserve the cache" (claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything, 2026-04-30) [established]. Manus says the same: "A common mistake is including a timestamp—especially one precise to the second—at the beginning of the system prompt" (manus.im blog, 2025-07-18).

Q3. How other teams decide "continue or start fresh"
Anthropic (Claude Code): builds the harness around cache economics — "we run alerts on our prompt cache hit rate and declare SEVs if they're too low"; plan mode exists because swapping tool sets would break cache (EnterPlanMode/ExitPlanMode are tools; instructions appended as messages); tool search defers rather than removes; compaction uses "cache-safe forking" (identical system prompt + tools + prepended parent history, compaction prompt appended, "compaction buffer" reserved) (claude.com blog, 2026-04-30) [established]. Productized idle policy: "If you leave a long conversation idle while it is on the one-hour TTL, Claude Code can compact it. To turn idle compaction off, set idleCompaction to false" (v2.1.290+) (code.claude.com) [established]. Community-observed trigger: it compacts shortly before the 1-hour cache expires, saving the cold rewrite (reddit r/ClaudeAI "Claude Code Compacts Automatically Before Cache", search-index capture) [low-authority].
Manus: "the KV-cache hit rate is the single most important metric for a production-stage AI agent"; input:output ≈ 100:1; keep prefix stable, context append-only, serialization deterministic, mask tools rather than remove (manus.im blog, 2025-07-18) [established].
Amp (Sourcegraph): removed compaction entirely (Oct 2025) in favor of Handoff — "Instead of summarizing a thread, you're extracting from it what matters for your next task", generating a new-thread prompt + file list that the user edits before starting (ampcode.com/news/handoff, 2025-10-23) [established]. Rationale is quality, not cost: compaction is "lossy" and encourages "long, meandering threads… stacking summary on top of summary."
Aider: the oldest keep-alive implementation still documented: "--cache-keepalive-pings N to tell aider to ping every 5 minutes to keep the cache warm… up to N times over a period of N*5 minutes" (aider.chat/docs/usage/caching.html, page content references claude-3-5-sonnet (2024) — stale, flag as historical) [established that the mechanism exists; dated].
Cognition/Devin: no idle/cost thresholds published; their doctrine is full-context sharing and "actions carry implicit decisions" (cognition.com/blog/dont-build-multi-agents, 2025-06, search-index capture) — implicitly anti-restart, pro-single-thread [emerging].
Anthropic research: compaction vs structured note-taking vs sub-agents chosen by task shape; context treated as "a finite resource with diminishing marginal returns" (anthropic.com/research/effective-context-engineering-for-ai-agents, 2025-09-29, search-index capture of full text) [established as guidance, not thresholds].
Practitioner rules with actual numbers (all [single-source] / [low-authority] but reproducible): compact before stepping away, because "A 150K→20K compaction reduces the next cold-start write from ~$0.56 to ~$0.075"; "Compact proactively at ~60% context capacity rather than waiting for auto-compaction" (Reddit r/LLMDevs cost analysis, 41-day Sonnet 4.6 session, ~May 2026, full post captured: cache reads 353.2M tok = $105.96, writes 27.7M tok = $103.88, output only ~7% of spend); cache-tax's guard threshold: ask before a cold send when context ≥ 50,000 tokens and estimated rewrite cost ≥ $5 (/cache-tax guard refuse 5), ping after 50 idle minutes (github.com/karanb192/cache-tax, README accessed 2026-11-20).
Not found: published continue-vs-restart thresholds from Cursor, Zed, Factory, Google/Antigravity, or OpenAI for Codex CLI ([no source found — searched vendor docs and changelogs; see E trail]). Cursor/Zed docs surfaced no threshold pages in the searches run; treat "Cursor compacts at window-full" as folklore until you can cite their docs.
Q4. Public measurements comparable to yours

Closest prior art, ranked by similarity (none publishes an idle-gap curve):

anthropics/claude-code#46829 — 119,866 API calls, 2 machines, JSONL usage.cache_creation.ephemeral_5m_input_tokens/ephemeral_1h_input_tokens per call, 2026-01-11→04-11. Headline: default TTL silently 1 h→5 m around 2026-03-06; 17.1% cache-spend waste ($949 Sonnet + $1,582 Opus); "220M tokens written to 5m tier generated 5.7B cache reads"; subscription users first hit 5-hour quotas in March 2026 (github.com/anthropics/claude-code/issues/46829) [emerging→established, staff-confirmed]. Same method as yours (per-call usage fields from local logs), different question (TTL identification vs idle-gap survival).
Reddit r/LLMDevs cost analysis (~May 2026) — single 41-day Sonnet 4.6 session, full ledger: cache read 353.2M tok ($105.96), cache write 27.7M tok ($103.88), input 19.1K, output 1.1M ($16.50); "Cache operations account for ~93%" of cost; estimated 200–400 cold starts at ~100K context (reddit.com/r/LLMDevs/comments/1ti7xlj, search-index capture of full post) [single-source, low-authority]. Corroborates your "cold resumes dominate spend" framing.
openai/codex#29377 — controlled cache-key experiment on gpt-5.5, 62,639-char static instructions, 18,362 input tokens/run: default thread-key cross-session reuse 13.2–27.2% vs 99.7% with a stable fixed key (once), then inconsistent 13–30% — quantifies the probabilistic routing your fleet sees (github.com/openai/codex/issues/29377, 2026-06-22) [emerging, n=1 config].
openai/codex#35416 — per-call hit-rate tables from ~/.codex/sessions/*.jsonl on gpt-5.6-luna: 92–99% hit when effort unchanged, 65–66% after effort change; deterministic repro script included (github.com/openai/codex/issues/35416, 2026-07-26) [emerging].
cache-tax README — one transcript-verified case: "A two-line recap in a 330k-token session triggered a $6.61 estimate. After resending, the reported cache write was $6.28"; plus a 2026-09-19 keep-warm verification (ping at min 50 read 157k; message at min 62 read 156,886 from cache) (github.com/karanb192/cache-tax) [single-source, but instrumented].
dev.to measurement — Opus 5.5, 200K-token session: warm turn ~$0.04 vs post-idle rewrite ~$1.00 ("Ten minutes at the coffee machine can add $0.96"); notes idle compaction shipped to VS Code/Desktop in Claude Code 2.1.314 (2026-10-30) (dev.to/gabrielanhaia, 2026-11-02, AI-assisted post) [low-authority].
Deriv engineering post — claims production GPT-5 agent hit rate raised to 85.8%, input-token cost −77% ([search-index capture only; URL not resolvable in this sandbox] — [no verified source]; do not cite in your article without opening it).

Idle-gap curves: no prior art found. Where I searched: arXiv (query variants "prompt cache hit rate idle time", "KV cache survival measurement", "LLM cache hit rate production"), GitHub issues in anthropics/claude-code and openai/codex, OpenAI/Anthropic/Google developer forums, r/ClaudeAI, r/LLMDevs, r/codex, HoneyHive/Helicone/Respan/Langfuse engineering blogs, dev.to, Medium. Everything found is either (a) TTL-identification (case 1), (b) cost ledger (cases 2, 5, 6), (c) controlled single-variable tests (cases 3, 4), or (d) synthetic API microbenchmarks your team already excluded. Nobody publishes cache-hit-vs-idle-gap survival curves from real agent logs; nobody publishes your 596M/2,349M cold-resume share-of-spend figure. Your November 2026 fleet data would be the first public artifact of that shape, at ~72x the call volume of the largest existing public dataset (#46829: 120K calls vs your ~71K sessions / 2.3K+ sessions across vendors).

Q5. Subscription vs API accounting

What is established, by vendor:

Anthropic. Official help-center text (the only direct statement): "Our system also includes caching that helps you optimize your limits: Content in projects is cached and counts less against your limits when reused. Claude remembers context from earlier in the conversation… Caches expire after a period of inactivity. If you come back to a project after a long break, your first message counts that content in full again" (support.claude.com/en/articles/9797557-usage-limit-best-practices, updated ~2026-10-30) [established — but no formula]. The Claude Code costs doc says displayed costs are computed at API list price and that Teams/Enterprise draw from a per-seat allowance on rolling 5-hour + weekly windows, with usage credits capped separately (code.claude.com/docs/en/costs, search-index capture of full page) [established]. Reverse-engineered evidence: #46829's author states "Cache creation tokens count toward quota at full rate; cache reads are significantly cheaper," inferring it from subscribers (himself included) first hitting 5-hour quotas right after the 5-min TTL flip, and Anthropic's usage-limit reset on 2026-04-23 (#46829); staff promised follow-up on cache-read quota weighting in related issue #45756 (referenced in #46829) [emerging]. Conflicting claim: the cache-keepalive README asserts "On Pro/Max subscription plans, your quota is gated by request count, not token cost — every keepalive turn eats your 5-hour quota. On subscriptions, this plugin makes things worse" (github.com/yujiachen-y/claude-code-cache-keepalive, accessed 2026-11-20) [single-source, low-authority, and hard to reconcile with the "cached portions count less" official text — keep both, flag the contradiction]. Also relevant: cache reads don't count toward ITPM rate limits on current API models (respan.ai, 2026-05-11, updated 2026-11-20) [single-source vendor-adjacent].

OpenAI. Official: ChatGPT/Codex usage will be "measured in tokens", with Plus/Pro/Business allowance shared across ChatGPT and Codex starting December (help.openai.com/en/articles/20001625, updated ~Nov 2026, search-index capture — page is JS-gated to curl) [established]. For Business/Enterprise credit plans, the Rate Card prices "credits per 1M input tokens, cached input tokens, and output tokens" — i.e., cached input has its own (cheaper) credit rate, so cache reads demonstrably cost less quota in credit-metered contexts (help.openai.com/en/articles/11481834-chatgpt-rate-card, search-index capture) [emerging]. For Plus/Pro subscription quota weighting of cached vs uncached tokens: no vendor statement found [no source found — searched help center and community forum]. Community datapoint (Codex usage discussion): a full session costed at "Input: $2.50 / Output: $10.00 / Cached input: $1.25 (50% discount)" in API-equivalents against a weekly cap (search-index capture, GitHub discussion #2251) [single-source].

Bottom line for your model: API-list-price accounting is the only cross-vendor consistent frame, and all published community measurements use it. Present your 596M/2,349M figure explicitly as "API-equivalent", as cache-tax does ("These are API-equivalent costs, not extra subscription charges"), and state Anthropic's official vagueness ("counts less against your limits") as the reason a true quota model can't be built from public information yet.

Q6. Failure modes and counter-arguments (the case against blocking cold resumes)
Summary loss is real and vendor-acknowledged. Amp removed compaction for exactly this reason: "Every time you compact a thread, what's in the context window gets replaced with a summary. Whether that summary contains exactly what you think it should is up to the agent… compaction, we found, encourages long, meandering threads… stacking summary on top of summary" (ampcode.com/news/handoff, 2025-10-23) [established as an argued position by a credible vendor]. Claude Code mitigates rather than denies: users can steer what the summary keeps (same post).
Aggressive idle-time context clearing demonstrably degraded quality in production. Anthropic's postmortem: "On March 26, we shipped a change to clear Claude's older thinking from sessions that had been idle for over an hour… A bug caused this to keep happening every turn for the rest of the session, which made Claude seem forgetful and repetitive. We fixed it on April 10" (anthropic.com/engineering/april-23-postmortem, 2026-04-23) [established]. Steelman for your opponents: this is direct evidence that "clean up cold context automatically" can backfire; your hook-based blockers are the mirror image of the same risk class (interventions on idle sessions can corrupt the session).
High fill degrades quality (argument for restart). Chroma's Context Rot (18 LLMs incl. GPT-4.1, Claude 4, Gemini 2.5): "model performance grows increasingly unreliable as input length grows… even under these minimal conditions" (trychroma.com/research/context-rot, 2025-07) [established]. Anthropic's own research echoes it ("context rot… an attention budget") (anthropic.com/research/effective-context-engineering-for-ai-agents, 2025-09-29).
The two arguments do not cancel — they operate on different axes: rot says a 500K-token context is a bad context; handoff-loss says a summary is a lossy encoding of it. The honest synthesis (Amp's, Manus's, Anthropic cookbook's): extract-then-restart with user-reviewable extraction beats both "continue cold at 500K" and "auto-summarize". What is missing is any controlled study of summarize-then-restart vs continue on coding-task success: [no source found] — searched arXiv (compaction, context compression, agent memory), Cognition/Devin blog, Manus, Anthropic cookbook; nothing with task-success error bars. The only quantified quality datapoint is the postmortem's "strict response length caps… knocked 3% off benchmark accuracy" (same URL) — different intervention, similar shape.
D. Contradictions and debates (preserved, not averaged)
"OpenAI caches last 24 h" vs "typically ~30 minutes". Marketing-adjacent phrasing (GPT-5.1 announcement, Nov 2025: "Extended prompt caching (up to 24 hours)") vs the guide's hedged wording. Your fleet data is evidence for the hedged reading. Side A (hard TTL) rests on announcement language; Side B (distribution + eviction) rests on current docs + Azure's implementation note + your measurements. Side B is stronger on current evidence; the announcement wording is stale, not wrong.
Was Anthropic's March 2026 TTL change a "nerf"? User framing: "20–32% increase in cache creation costs… quota inflation" (#46829, 2026-04-12). Anthropic's framing: intentional per-request TTL selection because "1h everywhere would increase total cost for their request mix" (staff, same issue), plus two client bugs (lizthegrey, 2026-05-08) that wrongly forced 5-minute TTL for some seats. Both can be true: the policy is defensible, the implementation had bugs, and the communication was silent until caught. Present all three; the "quietly nerfed" blog framing (Apr 20, 2026, search-index capture) adds heat, not data.
Subscription quota weighting. Official "cached portions count less against your limits" (support.claude.com) vs "gated by request count, not token cost" (cache-keepalive README) vs "cache creation counts at full rate; reads significantly cheaper" (#46829 author). Irreconcilable with public sources today; the experiment that would settle it: two identical subscription sessions differing only in keepalive pings, comparing 5-hour-window consumption — nobody has published this.
Effort changes and cache on GPT-5.6 vs GPT-6. #35416 (2026-07-26) shows real misses on gpt-5.6-luna; the Sep 2026 changelog says GPT-6 changed effort doesn't break cache; the guide hedges with "on supported models, use a configuration update". Not a contradiction so much as a version boundary, but the community still reports Codex-client friction ("custom harness getting random prompt_cache_retention errors", Aug 2026, search-index capture).
Compaction: keep it (Anthropic, with cache-safe forking + user steering) vs remove it (Amp). Both are principled; Anthropic optimizes continuity cost, Amp optimizes thread focus. No public benchmark separates them.
Gemini discount percentages. Official 2025: 75% implicit discount; 2026 forum reports: 90–95% on 3.x; Vertex blog: 90% explicit. Vintage differences, but Google does not publish a current per-model discount table for implicit caching — a real documentation gap your article should name.
E. Public measurements comparable to ours — summary verdict and search trail

Verdict: Direct prior art for hit-rate vs idle-gap curves from real agent session logs: no prior art found. Partial prior art exists for method (#46829 — same per-call usage-field parsing), scale context (#46829's 119,866 calls is the largest public dataset; yours is ~10–30x larger in sessions and covers two vendors), and headline economics (r/LLMDevs: 93% of spend on cache ops; cache-tax: $6.28 cold rewrite on a 330K session; dev.to: 25x warm/cold ratio at 200K on Opus 5.5).

Search trail (queries run, 2026-11-20): "prompt cache hit rate idle time measurement blog"; "Claude Code cache tax cold session cost blog"; "Codex CLI cache cold start measurement"; "OpenAI 24 hour prompt cache retention measured"; "Gemini implicit caching hit rate measurement"; "codex prompt cache hit rate idle pause measurement analysis"; arXiv-style queries "compaction quality loss coding agent benchmark study arxiv 2025 2026", "long context degradation coding agent performance study arxiv"; vendor-forum queries on discuss.ai.google.dev and community.openai.com; engineering-blog queries (HoneyHive, Respan, Helicone-adjacent); GitHub issue search in anthropics/claude-code and openai/codex. Additionally: caching-related repos surfaced under the prompt-caching GitHub topic (keepalive plugins, Cachebeat) — none publish datasets, only tools.

Comparable-to-yours claims you can make safely: largest published agent-log cache study by session count; first cross-vendor (Anthropic+OpenAI) survival curve by idle bucket; first cost attribution of cold resumes as a share of total spend (25% at list prices). Attribute method lineage to #46829 (2026-04) publicly — it precedes you and strengthens credibility.

F. Decision rules used in practice, with thresholds
RULE (NAMED)
	
SOURCE & DATE
	
THRESHOLD
	
TRADE-OFF / RISK

Anthropic built-in idle compaction	code.claude.com docs (accessed 2026-11-20); idle compaction shipped broadly in 2.1.314 per dev.to (2026-11-02)	Triggers on long conversation idle on the 1-h TTL, before expiry; off via idleCompaction: false	Saves the cold rewrite; compacts without asking — summary-quality risk; requires 1-h TTL to be in effect (subscription, or promptCacheTtl: "1h")
Compact-before-idle (manual)	r/LLMDevs analysis (~May 2026); official docs tip ("run /compact at a natural break")	Before any break expected >5 m (API/credits) or >1 h (subscription); community heuristic: compact proactively at ~60% of window	150K→20K cuts cold write ~$0.56→~$0.075 (their example); loses detail — the Amp critique
Keep-warm ping (1-h cache)	cache-tax /keepwarm 90m (README, Nov 2026); Aider --cache-keepalive-pings (docs, stale 2024-era)	cache-tax: ping at 50 idle min; stop if reads hit 0 or writes ≥10% of reads; Aider: every 5 min up to N times	Pings are real turns that cost tokens and quota; keepalive README warns it's counterproductive on subscriptions [single-source]; depends on "reads refresh TTL" invariant Anthropic can change
Cold-send guard	cache-tax hook/mod (README, accessed 2026-11-20)	Ask when context ≥50,000 tok AND estimated rewrite ≥$5; refuse-once fallback	Friction on every long cold resume; estimate is model-price-table dependent
Handoff (extract-then-restart)	Amp (2025-10-23); analog: Claude Code /recap keeps cache and appends summary	Amp: user supplies next-task goal; editable generated prompt + file list	Quality-first; does not directly minimize token cost; user review time
Stay-on-TTL hygiene	Manus (2025-07-18); Anthropic blog (2026-04-30); code.claude.com docs	Pick model+effort at session start; never add/remove tools mid-session; append-don't-rewrite; tool search defer; promptCacheTtl: "1h" on API-key billing	Zero-cost rule set; no threshold; doesn't survive genuine long idles
Codex routing hygiene	developers.openai.com guide (accessed 2026-11-20); #29377 (2026-06-22)	Pre-GPT-5.6: stable prompt_cache_key, ~15 req/min per key, partition high-volume keys deterministically	Routing ≠ pinning; cross-session reuse 13–30% even with same prefix absent key control (measured)
Codex retention config	developers.openai.com guide	Non-ZDR orgs already default to 24h; explicitly set prompt_cache_retention: "24h" for ≤gpt-5.5 models on ZDR orgs; GPT-5.6+: "12h" at 2.5× write if prefixes truly stable	2.5× write premium only pays if gaps genuinely land between 30 min and 12 h — your fleet's buckets say a minority of returns do

No vendor publishes a validated "continue vs restart" threshold tied to task-success. Every threshold above is cost-derived. The quality side (context rot) has evidence that large contexts degrade but no threshold tied to a restart decision; the closest you can cite is your own median-peak-391K / 28%-above-500K distribution against Chroma's degradation findings.

G. Recommendations for your article

Safe to state confidently ([established]):

Claude Code requests a 1-h TTL for the main conversation only on subscription-within-plan usage; 5 m everywhere else (subagents, compaction, credits, API keys, cloud providers); overridable via promptCacheTtl / ENABLE_PROMPT_CACHING_1H=1; verifiable per call via ephemeral_1h/5m_input_tokens (code.claude.com/docs/en/prompt-caching).
Anthropic write surcharges (1.25×/2×) and per-model read discounts (0.1×/0.05×/0.025×) exactly as you weighted them (platform.claude.com).
The Anthropic invalidator list (model, effort, fast mode, MCP-without-tool-search, plugins-with-MCP, compaction, image-batch removal, client upgrade, billing-state flip) (code.claude.com).
OpenAI retention tiers with the verbatim "typically… around 30 minutes… up to 24 hours" wording, and the GPT-5.6+ write surcharge (1.25×/2.5×) (developers.openai.com).
That OpenAI "24 h" is a capacity-managed tier with eviction under load (learn.microsoft.com Azure doc).
That your Codex 1 h→24 h gradual decay is consistent with documented behavior — phrase as consistency, not confirmation, since bucket assignment for Codex's own traffic is not documented.

Needs caveats:

"The cliff is sharp at the 60th minute" — true on subscription-within-included-usage. On usage credits, API keys, or Bedrock/Vertex it is a 5-minute cliff. Say "on Claude subscription plans, within included usage" every time.
Your Codex price weight "cached input 0.05×" — established only as "up to 95% discount" on the newest models; the GPT-5.x generation is widely reported at ~0.1× (HoneyHive, updated 2026-11-17). Name the model per weight or give both.
"OpenAI has no write surcharge" — wrong for GPT-5.6+ (1.25×/2.5×). Keep it only as "no surcharge on models through GPT-5.5-era extended retention".
Subscription-quota claims — present as three-way contradiction (Section D.3) with your numbers labeled "API-equivalent", the cache-tax convention.
Idle compaction behavior — official docs confirm existence and the off-switch; the "compacts 200K+ sessions shortly before the hour" specificity is community-observed ([low-authority]).
GPT-6 effort-change-without-cache-break — changelog quote exists but URL not openable from this sandbox; pair it with #35416's counter-evidence for 5.6-class models.

Likely wrong as currently framed:

Any implication that vendor TTLs are hard guarantees. All three vendors use "typically"/"or less" language for the tiers that matter to you (OpenAI guide; Vertex blog for Gemini implicit). Frame your curves as measurements of a distribution the vendors refuse to guarantee.
Any claim that keep-alive pings save money on Claude subscriptions — the strongest available source says the opposite there (pings burn request-gated quota) [single-source]; on API billing they can save money (cache-tax's measured case).
"Gemini implicit caching has no TTL" — docs omit one; the best available statement (cleared in ≤24 h) is a pre-2025 Vertex blog. Mark the whole Gemini section as doc-gap + [emerging].

Also include (strengthens the piece): the March–April 2026 Anthropic TTL episode as the reason fleet-level monitoring matters (staff-confirmed, with the two fixed client bugs), and Anthropic's own practice of treating cache-hit rate as an SLO ("declare SEVs") — it validates your fleet-monitoring methodology from the vendor's side.

H. Sources

Opened and read in full this session (2026-11-20) unless marked otherwise:

https://platform.claude.com/docs/en/build-with-claude/prompt-caching — Anthropic API prompt caching (pricing table, invalidation table, minimums; accessed 2026-11-20)
https://code.claude.com/docs/en/prompt-caching — How Claude Code uses prompt caching (TTL table, idleCompaction, invalidators, env vars; accessed 2026-11-20)
https://developers.openai.com/api/docs/guides/prompt-caching — OpenAI prompt caching guide (retention buckets, write surcharge, cache keys; accessed 2026-11-20)
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching — Azure OpenAI prompt caching (GPU-local offload, model lists, cache_write_tokens; published/updated 2026-11-06)
https://github.com/anthropics/claude-code/issues/46829 — "Cache TTL silently regressed from 1h to 5m" (119,866 calls; staff responses by Jarred-Sumner 2026-04-12 and lizthegrey 2026-05-08; opened 2026-04-12, read 2026-11-20)
https://github.com/openai/codex/issues/35416 — "Changing reasoning level results in cache miss" (2026-07-26, per-call tables)
https://github.com/openai/codex/issues/29377 — "Expose prompt_cache_key for independent codex exec" (2026-06-22, routing experiment)
https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything — Anthropic engineering blog (2026-04-30, Thariq Shihipar)
https://www.anthropic.com/engineering/april-23-postmortem — "An update on recent Claude Code quality reports" (2026-04-23)
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus — Manus (2025-07-18)
https://ampcode.com/news/handoff — Amp "Handoff (No More Compaction)" (2025-10-23)
https://aider.chat/docs/usage/caching.html — Aider prompt caching (--cache-prompts, --cache-keepalive-pings; content references 2024-era models — historical)
https://support.claude.com/en/articles/9797557-usage-limit-best-practices — Claude usage-limit best practices (updated ~2026-10-30)
https://github.com/karanb192/cache-tax — Cache Tax README (accessed 2026-11-20; repo actively updated Nov 2026)
https://github.com/yujiachen-y/claude-code-cache-keepalive — cache-keepalive README (accessed 2026-11-20)
https://www.honeyhive.ai/learn/prompt-caching — HoneyHive cross-vendor comparison (updated 2026-11-17)
https://www.respan.ai/articles/claude-prompt-caching — Respan, Anthropic caching pricing deep-dive (2026-05-11, updated 2026-11-20)
https://tokenade.net/en/articles/claude-code-compact — "Claude Code /compact: What It Costs and What Survives" (2026-10-01, updated 2026-10-07)
https://dev.to/gabrielanhaia/a-200k-token-claude-session-left-idle-re-buys-its-cache-004-becomes-100-3mfp — 200K-token idle re-buy measurement (2026-11-02; AI-assisted post — low-authority)
https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/ — Google implicit caching announcement (2025-05-08)
https://www.trychroma.com/research/context-rot — Chroma "Context Rot" (2025-07; full text captured via search index)
https://www.anthropic.com/research/effective-context-engineering-for-ai-agents — Anthropic research (2025-09-29; large text capture via search index)
https://aistudio.google.com/docs/caching — Gemini context caching docs (implicit section captured verbatim via search index 2026-11-20; explicit-cache subsection not reachable from this sandbox)
https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching — Vertex AI context caching blog (pre-2025, historical; captured via search index)
https://code.claude.com/docs/en/costs — Claude Code "Manage costs effectively" (full capture via search index)
https://www.reddit.com/r/LLMDevs/comments/1ti7xlj/claude_code_cost_analysis_cache_rewarming_write — 41-day session cost ledger (~2026-05; full post captured via search index; low-authority)
https://www.reddit.com/r/ClaudeAI/comments/1sk3m12/followup_anthropic_quietly_switched_the_default — TTL/usage-credits community report (search-index capture; low-authority)
https://www.reddit.com/r/ClaudeAI/comments/1x1a6ym/claude_code_compacts_automatically_before_cache — idle-compaction community report (search-index capture; low-authority)
https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-bedrock-one-hour-duration-prompt-caching — Bedrock 1-h cache option (2026-01; snippet-level capture)
https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits — ChatGPT/Codex token-measured usage (updated ~Nov 2026; search-index capture — JS-gated to direct fetch)
https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing — Rate Card (search-index capture; snippet-level)
https://cognition.com/blog/dont-build-multi-agents — Cognition context principles (2025-06; search-index capture)
https://news.hamidun.com/en/news/13277/anthropic-explains-claude-code-degradation-and-resets-user-r — rehost of source 9 (low-authority; original cited as #9)

Referenced but not openable from this sandbox (verify before citing in your article):

https://developers.openai.com/cookbook/examples/prompt_caching_201 — OpenAI "Prompt Caching 201" (Cloudflare-blocked here; content known via direct quotes in #35416 and search index, Feb 2026)
"Better prompt caching for GPT-6" changelog entry (2026-09-22, developers.openai.com — search-index capture, URL not resolvable)
Deriv engineering post on 85.8% cache hit rate / −77% input cost (search-index capture, URL not resolvable) — [no verified source]
Gemini CLI and Antigravity caching documentation — [no source found]; searched Google docs (ai.google.dev, aistudio.google.com, docs.cloud.google.com), the google-gemini/gemini-cli repository surface, and Antigravity pages; neither names a cache TTL or hit-rate behavior.
OpenAI per-model cached-input price table (https://developers.openai.com/api/docs/pricing — Cloudflare-blocked here; current cached-input discounts known only via guide text "up to 95%" and third-party tables)

Claims left explicitly unverified in the text above: Codex CLI's effective default prompt_cache_retention for consumer orgs ([speculative] — reconciliation offered in Q1); subscription quota weighting formulae (Q5, three-way contradiction); any validated continue-vs-restart quality threshold (none exists publicly).

## Sources (links in the GLM answer, 35 URLs)
- https://code.claude.com/docs/en/prompt-caching
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://support.claude.com/en/articles/9797557-usage-limit-best-practices
- https://github.com/anthropics/claude-code/issues/46829
- https://aistudio.google.com/docs/caching
- https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching
- https://github.com/openai/codex/issues/35416
- https://github.com/openai/codex/issues/29377
- https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/
- https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- https://www.reddit.com/r/ClaudeAI/comments/1x1a6ym/claude_code_compacts_automatically_before_cache
- https://ampcode.com/news/handoff
- https://aider.chat/docs/usage/caching.html
- https://cognition.com/blog/dont-build-multi-agents
- https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- https://github.com/karanb192/cache-tax
- https://www.reddit.com/r/LLMDevs/comments/1ti7xlj/claude_code_cost_analysis_cache_rewarming_write
- https://dev.to/gabrielanhaia/a-200k-token-claude-session-left-idle-re-buys-its-cache-004-becomes-100-3mfp
- https://code.claude.com/docs/en/costs
- https://github.com/yujiachen-y/claude-code-cache-keepalive
- https://www.respan.ai/articles/claude-prompt-caching
- https://help.openai.com/en/articles/20001625-understanding-chatgpt-and-codex-usage-limits
- https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing
- https://www.anthropic.com/engineering/april-23-postmortem
- https://www.trychroma.com/research/context-rot
- https://www.honeyhive.ai/learn/prompt-caching
- https://tokenade.net/en/articles/claude-code-compact
- https://www.reddit.com/r/ClaudeAI/comments/1sk3m12/followup_anthropic_quietly_switched_the_default
- https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-bedrock-one-hour-duration-prompt-caching
- https://news.hamidun.com/en/news/13277/anthropic-explains-claude-code-degradation-and-resets-user-r
- https://developers.openai.com/cookbook/examples/prompt_caching_201
- https://developers.openai.com/api/docs/pricing
