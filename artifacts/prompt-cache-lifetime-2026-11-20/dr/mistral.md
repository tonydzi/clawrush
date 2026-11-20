Used 2 tools

I'll now run the research, starting with vendor-official documentation on prompt caching (OpenAI, Anthropic, Google).

Ran a web search

Initial map obtained. Now I'll open the key official docs to capture exact wording (OpenAI caching guide, GPT-6 caching post, Anthropic prompt caching docs, Gemini caching docs).

Ran a web search

Strong primary sources for OpenAI and Anthropic. Now I'll extract the full OpenAI guide retention/routing wording and the Gemini caching details, plus search Claude Code-specific cache behavior.

Opened page

Key OpenAI retention wording captured. Now let me extract more sections from that guide (cache location, invalidation, usage reporting) plus the Gemini caching full docs.

Ran a web search

Now I'll search for observed/community behavior: Claude Code cache cliffs, Codex CLI cache retention observations, and Gemini CLI/Antigravity specifics.

Ran a web search

Now opening the key Claude Code sources: official caching doc, settings reference, and the TTL regression issue.

Ran a web search

Excellent data. Now the rest of the Claude Code caching doc (cache lifetime tiers) and the settings reference on idleCompaction.

Ran a web search

Now the Codex/OpenAI side: retention discussions, intermittent misses, and the 24h default news.

Ran a web search

Now the Gemini/Antigravity side: official implicitcaching wording and observed behavior.

Ran a web search

Now Q3/Q5: continue-or-restart heuristics, keep-alive economics, and subscription vs API accounting.

Ran a web search

Several key sources surfaced. Opening the most important ones: the "agentic inference field guide" (cites papers), the 120-run continue/compact experiment, Anthropic's context engineering piece, and Manus.

Ran a web search

The field guide maps several public measurements. Extracting its references and finding the underlying papers.

Ran a web search

Opening the three key papers: Copilot traces study, keepalive economics, and the FreeInference characterization.

Ran a web search

Now Q5 (subscription accounting) and Anthropic's official session-value guidance.

Ran a web search

A few more targeted searches: other vendors' session policies, Aider's caching trick, Codex official docs, and the OpenAI forum observation.

Ran a web search

One last fetch for the subscription-rate-card details, then I'll compose the report.

Ran a web search
Prompt cache lifetime in coding agents: official vs observed TTL, invalidators, and the continue-or-restart decision

Research performed 2026-11-20. About 40 web searches and ~30 full document reads. All URLs below were opened and read; claims I could only see in search snippets are marked. Because this is a fast-moving topic, retrieval dates matter and are given throughout.

A. Executive Summary

Ranked takeaways:

OpenAI's "24h" was never a guaranteed 24-hour TTL. The official guide says extended retention "typically keeps entries available for around 30 minutes and can retain them for up to 24 hours," and it explicitly warns that "the minimum lifetime governs eligibility for cache-read pricing. It does not guarantee that every request reuses stored KV tensors." Your observed Codex decay (gradual, not a cliff at 24h) is therefore not an anomaly: it matches documented best-effort behavior, per-machine storage, and load-dependent routing. ( Prompt caching guide, OpenAI, retrieved 2026-11-20)
Claude Code's sharp 60-minute cliff on subscriptions is exactly as documented, with one mechanism nuance: since v2.1.299 (October 14, 2026), long sessions are also compacted at about minute 54 of idle, so by the time you cross the TTL the history may already have been replaced by a summary. Your ">1h = cold" measurement is safe. ( Claude Code prompt caching docs, retrieved 2026-11-20;  Claude Camp)
Google publishes no TTL for implicit caching at all, and practitioners measure a ~5-minute cliff on Gemini 4 / Antigravity, plus mid-turn replica stickiness failures. One careful binary-analysis blog pinned the boundary between 4 min 45 s and 5 min 00 s and found a dormant, flag-gated keep-alive engine hardcoded in Antigravity. Google's only official horizon is a durable tier on Agent Platform that expires "no later than 24 hours" with "most entries evicted earlier." ( Gemini caching docs;  Vertex context caching overview;  Ashish Subedi, 2026-11-19)
You are not first, but you are close to the frontier. Two published production datasets resemble parts of yours: the Harvard FreeInference trace (12,002 human-driven sessions; hit ratio ~58% at 15–30 min gaps, ~18% beyond an hour) and Microsoft's Copilot trace study (13M sessions; 90% hit rate within a turn, 55% across turn boundaries, drastically invalidated by model switches and compaction). No published study reports idle-gap-vs-cold-rate curves for Claude Code and Codex CLI together from fleet-wide local session logs, so your paired two-vendor fleet measurement is a real contribution. ( Khare field guide, 2026-10-18;  FreeInference trace repo;  arXiv:2608.00101)
The economics of your cost model are directionally right but have two caveats: the 0.05x cached-input weight is only correct on the newest models (most GPT-5.6+ reads are 0.1x), and subscription metering is not API metering: Anthropic's API rate limits exclude cache reads from ITPM, measured Pro plans count almost nothing for cache reads, and OpenAI's credit rate card bills cached input at a discounted but positive rate. ( OpenAI prompt caching guide;  Anthropic rate limits;  Wokey measured limits;  OpenAI Help rate card)
Quality evidence argues against blindly blocking large cold resumes: an OpenAI internal report found repeated Codex compactions gradually degrade accuracy, and Amp replaced compaction with handoff for this reason; but a 120-run experiment found no universal winner, and full-history Continue cost 6.5x an entire Fresh run on one model while being faster on another. Cost alone never decides this well. ( Tessl on Amp handoff, 2025-11-14;  120-run experiment)
B. Per-vendor table
	
OpenAI (Responses / Codex CLI, GPT-5.x / GPT-6.x)
	
Anthropic (Claude Code)
	
Google (Gemini CLI / Antigravity)

Official TTL	GPT-5.6+: prompt_cache_options.ttl "30m" default, "12h" optional. Earlier models: in_memory = "typically... 5 to 10 minutes of inactivity, up to one hour"; 24h = "typically... around 30 minutes and can retain them for up to 24 hours." Non-ZDR orgs default to 24h; ZDR orgs to in_memory. 24h is a maximum, not a guarantee.	API: 5-minute TTL default, "refreshed... at no additional cost each time the cached content is used"; optional 1-hour TTL. Lifetime "measured from the start of the request... Time spent generating a response counts against the lifetime." Claude Code subscription: main conversation 1h, everything else (subagents, compaction) 5m; drops to 5m once you are on usage credits.	Implicit caching enabled by default, no published TTL ("send requests with similar prefix in a short amount of time"). Agent Platform (Vertex): two tiers, in-memory + durable; durable prefixes "expire no later than 24 hours after they're created, and most entries are evicted earlier." Explicit caches (Gemini 3 / 2.5): user-set TTL, default 60 min.
Observed TTL	Best-effort streaks: intermittent zero-hit runs even with stable prompt_cache_key and seconds-scale gaps; Azure long sessions "thrash the in-memory prompt cache" past ~150K tokens. Your 1–24h gradual decay fits the docs.	Sharp ~60-min cliff on subscription main thread (your data, confirmed by community phase analysis); documented regression from 1h to 5m writes around March 2026 in a 119,866-call JSONL analysis; sub-minute full misses mid tool-loop also reported.	Antigravity CLI: 98.1% hit at 0–1 min, 82.7% at 1–3 min, 73.6% at 3–5 min, 39.1% at 5–8 min, 30.0% at 8–12 min (3,060 call pairs); binary-analysis blog pinned the cliff between 4m45s and 5m00s; issue reports of cache = 0 after 25–30s gaps on Gemini 4 Neon/Carbon.
Write surcharge	GPT-5.6+: 1.25x input at 30m, 2.5x at 12h, total rates. Earlier models: no cache-write surcharge advertised ("has no additional fees").	1.25x base at 5m; 2.0x base at 1h.	Implicit: none. Explicit: input + hourly storage cost; from 2027-01-12, Gemini 4 Hydrogen+ writes bill at 1.25x with TTL control.
Read discount	Up to 10x off (0.1x); 0.05x on GPT-6.1/6.2 Sol/Astra/Terra ("up to 95%"). Credit rate card: GPT-6.2 Astra 200 credits input / 10 cached.	0.1x standard; 0.05x Opus 5.5 / Sonnet 5.5; 0.025x Fable 5.x / Mythos 5.x.	~90% off cached tokens (0.1x) on implicit hits.
Key invalidators (documented or reproducible)	Any prefix change (tools list/schema/order, structured-output schema, early timestamps, reasoning-effort change on pre-GPT-6 models); machine load ("traffic above 15 requests per minute can lead to overflow routing"); org switch, regional boundary; wrong/absent session-id on the Codex backend (ChatGPT derives cache affinity from it).	Model switch, effort change, fast mode, MCP server change, plugin toggle, denying a whole tool, compaction, image-batch removal, Claude Code upgrade, gateway stripping cache_control, plan-limit fallback (speed and TTL changes).	Any system-prompt/prefix change (0% hit reported on unchanged prompts in streaks); replica stickiness failures mid-turn (6–15s gaps, 0% reads); model switch, compaction (per Copilot study for the class of workload); explicit-cache TTL expiry; storage-object mutation for blob-based explicit caches.
Source anchors	Guide, cookbook, Codex GitHub issues, community threads (sources, section H)	Claude Code docs, platform docs, GitHub issues 46829 / 99096 / 63930 / 2603	Gemini API docs, Vertex overview, Google AI forum, Antigravity GitHub, practitioner measurements
C. Key findings per question
Q1. Official vs observed TTL

OpenAI. Exact working from the current guide: in_memory entries "typically remain active for around 5 to 10 minutes of inactivity, up to one hour," and 24h entries "typically keep entries available for around 30 minutes and can retain them for up to 24 hours." Caches "live on individual machines, where traffic above 15 requests per minute can lead to overflow routing," and reuse "requires the entire rendered prefix to match." The guide also states plainly that a specified lifetime "does not guarantee that every request reuses stored KV tensors." Your 30–60 min bucket at 10% cold and the monotonic decay to 100% cold at 24h+ is fully consistent with "typically around 30 minutes" availability plus load-dependent eviction. ( Prompt caching guide) The cookbook adds: "Caching only works if two requests share the same prefix and land on the same machine," with prompt_cache_key improving routing on models before GPT-5.6. ( Prompt Caching 201)

Two routing facts matter for interpreting your Codex data. First, the CLI's cache affinity is thread-based: codex-rs sets session-id (equal to prompt_cache_key), thread-id and x-codex-turn-state; a community proxy that did not forward the header got 2–6% cached production traffic versus ~75% for the identical pipeline, and 0/0/0 versus 99% cached in a controlled 19K-token triple-replay on gpt-6.1-sol after the fix. ( openai-oauth issue #46, 2026-10-18) Second, intermittent zero hits occur even with a stable key on real Codex traffic, which maintainers treat as expected best-effort behavior. ( codex #30425, 2026-06-28) Users have asked for a way to force 24h retention in Codex since the parameter existed; the request remains closed as not planned. ( codex #6698, 2025-11-15;  codex discussion #18782, 2026-04-21) One gateway-operator newsletter dates the "24h default for non-ZDR orgs" change to May 29, 2026 and says GPT-5.5+ supports only 24h; this matches the official default description but the date itself is single-source. ( TheRouter, 2026-06-04) [single-source] Confidence: [established]

Anthropic. Platform docs (retrieved 2026-11-20) promise a 5-minute default TTL refreshed on use, plus a paid 1-hour option, with a subtlety your log analysis may have absorbed: "the lifetime is measured from the start of the request that writes or reads the cache entry... if a response takes 4 minutes to stream, a follow-up request... must start within about 1 minute." ( Prompt caching docs) Claude Code's own doc states the split plainly: on a subscription the "Main conversation: One hour; Everything else: Five minutes, except the server-controlled helper requests," and when you exceed plan limits and draw on usage credits, "Claude Code drops the main conversation to the five-minute TTL." Per-bucket overrides exist (promptCacheTtl, CLAUDE_CODE_PROMPT_CACHE_TTL, subagentPromptCacheTtl, ENABLE_PROMPT_CACHING_1H=1, FORCE_PROMPT_CACHING_5M=1). ( Claude Code docs) The community-observed wrinkle: a two-machine, 119,866-call JSONL analysis documents that main-thread cache writes were 1h-only from February 1 to March 5, 2026, then silently regressed to mostly-5m from March 6–8, costing an estimated 17.1% overpayment at list prices. Anthropic closed the issue as "not planned." ( claude-code #46829, 2026-04-12) A separate medium post claims to have analyzed 34,439 of the author's own responses and dates a similar regression to October 12; I could not open it, so I treat the March regression as the corroborated event. [single-source for the October claim] ( Medium post, unopened) Confidence: [established]

Google. The Gemini API docs describe implicit caching as on-by-default with automatic savings and give no TTL, only advice to "send requests with similar prefix in a short amount of time"; Gemini 4 multi-turn caching only caches the full previous request when the new request adds at least 2,050 tokens, otherwise the last 2,050 tokens are re-processed at the standard rate. ( Gemini caching docs, retrieved 2026-11-20) The Agent Platform overview is the only official horizon statement: prefixes live in an in-memory tier evicted "as capacity is reclaimed" and a durable tier where "a cached prefix expires no later than 24 hours after it's created, and most entries are evicted earlier." ( Vertex context caching overview) Observed: an Antigravity telemetry thread (3,060 consecutive call pairs, Nov 17–19, 2026) measured 98.1% / 82.7% / 73.6% / 39.1% / 30.0% hit rates at 0–1 / 1–3 / 3–5 / 5–8 / 8–12 minute pauses, plus a mid-turn collapse where 9 consecutive 436–501K-token calls got 0% cache after 6–15 s gaps. ( Google AI forum, 2026-11-19) A Gemini 4 Argon thread measured hit streaks (83% chance of hit after a hit, 34% after a miss) and a drop from 93% hit rate before October 30 to 63% in early November, consistent with us-else-stated "15 to 20 minute" expectations per that poster's reading of a Cloud guide. ( Argon forum thread, opened 2026-11-17) Confidence: official = [established]; observed ~5-minute cliff on Antigravity = [emerging] (two independent measurements + issue reports, no vendor confirmation).

Q2. What resets the cache besides time

Claude Code (official list): switching models (including opusplan plan-mode toggles, safety-classifier fallbacks, skill/command frontmatter models), changing effort level, turning on fast mode (including the automatic fallback to standard speed after a rate limit), connecting or removing an MCP server (depending on tool-search deferral), enabling or disabling a plugin, denying an entire tool (scoped rules do not), compacting, accumulating enough images/PDFs to trigger batch removal, and upgrading Claude Code. Gateways that strip cache_control silently uncache the entire history; ones that 400 make Claude Code move the marker forward. ( Claude Code docs) Resuming a session can also rebuild the system-prompt layer once if the prompt changed, and /rewind truncates back to an already-cached prefix, unlike compaction which builds a new one. This list was confirmed as authoritative on 2026-11-20. Confidence: [established]

OpenAI (official): any change in the rendered prefix before a breakpoint: tool list/schemas/ordering, structured-output schema (use a format update on GPT-6+), reasoning-effort change (use a configuration_update instead to preserve cache), timestamps placed early in the request (move to metadata), top-level instructions (billed uncached every request). Model changes are implicit through per-model routing; org and region changes are hard boundaries ("Caches are not shared across organizations and cannot be reused across regional processing boundaries"). ( Prompt caching guide;  Cookbook;  GPT-6 caching post) For Codex specifically, a rewritten session-id/thread-id (new thread, some orchestrator reruns) can forfeit affinity even with an identical prefix; a proxy miss took production hit rates from ~75% to 2–6%. ( openai-oauth #46) The Codex engineering team's own practices (stable ordering, append-only runtime config, metadata for debug timestamps) are official confirmation that these invalidators are real. ( Cookbook, Learnings from Codex) Confidence: [established]

Google: no official invalidator list beyond prefix matching; observed invalidators from forum telemetry and issues are system-prompt changes, replica/stickiness resets even within turns, and version/model changes. Explicit caches break when underlying Cloud Storage objects change before expiry. ( Vertex overview;  Argon thread) Coverage of Anthropic "context-tier" pricing is official for the API: on models priced by prompt length, cache reads and writes count toward the request's prompt length, so crossing a long-context threshold changes the effective price of everything. ( Prompt caching docs) Confidence: [established] for prefix matching, [emerging] for Antigravity stickiness.

Exceeding context tiers / account switches: documented for OpenAI (org/region boundaries), Claude Code (per-model caches; usage-credit fallback drops the main thread to 5m TTL), and not publicly documented for Gemini quota-based rerouting. Your hypothesis "account or organization switch resets the cache" is safely claimable for OpenAI; treat as [no source found] for the ChatGPT-consumer Codex lane specifically.

Q3. How other teams decide "continue or start fresh"

Ranked by authority:

Anthropic (official): context rot is real across all models ("as the number of tokens in the context window increases, the model's ability to accurately recall information... decreases"), and the recommended levers are compaction, structured note-taking, and sub-agent architectures; compaction "preserves architectural decisions, unresolved bugs, and implementation details" plus the five most recently accessed files, but "overly aggressive compaction can result in the loss of subtle but critical context." Anthropic's own engineers, per a syndicated write-up, found compaction alone insufficient for multi-hour runs and moved to fresh contexts with structured handoff artifacts. ( Effective context engineering, 2025-09-29;  Effective harnesses for long-running agents;  HarnessRouter) Confidence: [established]
OpenAI/Codex: compaction is first-class for "multi-hour reasoning without hitting context limits," and Codex's source warns that repeated compactions can reduce accuracy and recommends small, targeted new threads. Claude Code's client itself nudges: since v2.1.84 it prompts users returning after more than 75 minutes to consider /clear, and v2.1.92 added a footer estimate of uncached tokens for Pro users; both put official weight behind "don't blindly resume a big cold session." ( Codex prompting guide;  Compaction guide;  FylloCode analysis, 2026-08-25) Confidence: [established]
Amp (Sourcegraph): retired compaction entirely in favor of /handoff, which packages current discussion, files, and artifacts into a new thread with a goal, precisely because in-thread summarization drifted. An internal OpenAI report cited in the same coverage attributed gradual Codex accuracy decline to accumulated compacts. ( Tessl, 2025-11-14) Confidence: [established] for the feature change, [emerging] for the internal report (secondhand).
Keep-alive economics: a dedicated arXiv paper frames the trade precisely: pings "cut the post-pause request cost by up to 12.5x"; the optimal interval is the largest safely below the TTL (~4 minutes at a 5-minute TTL, not the 30-second convention); break-even against letting the cache die is ~46 min idle on Anthropic pricing, ~36 min on OpenAI/DeepSeek. ( arXiv:2607.19214) Aider ships --cache-keepalive-pings N (up to N pings at 5-minute spacing). ( Aider caching docs) Antigravity contains a dormant keep-alive engine (270 s ping interval, 285 s staleness cutoff) gated behind a server-side flag, per binary disassembly. ( Subedi) Practitioners reserve end-of-limit Codex prompts to "wake up" a session every ~50 minutes (community practice, unopened link, [low-authority]). ( r/codex) Confidence: [established] for the paper math, [emerging] for vendor adoption.
Compaction thresholds in other harnesses: Cline auto-compacts around 55–75% of window depending on version, with open issues asking for a configurable effective window because 1M-context models "never compact in practice." ( cline #14979;  cline #14329) Cursor ships /summarize and automatic summarization as the equivalent lever. ( Cursor summarization docs) Claude Code idle-compacts sessions over 200K at ~54 minutes of idle, before the 1-hour cache dies. ( Claude Camp;  Developers Digest) Confidence: [established]
Manus: treats "KV-cache hit rate... as the single most important metric for a production-stage AI agent," and lists timestamps in the system prompt, non-deterministic serialization, and mutating old turns as cache killers. ( Manus blog) Confidence: [established] as a vendor statement.
For Devin/Cognition, Factory, Zed and Google I found no published idle-time threshold policies; [no source found] after searches named in section E's trail.
Q4. Public measurements comparable to ours

Prior art exists, and it is close in spirit but not in coverage:

"From Requests to Sessions" (Harvard MadSys / FreeInference), 16 weeks of trace (2026-05-17 to 2026-09-05), 12,002 human-driven sessions, 267 accounts, 1.19M requests, 209B input tokens, with per-block prefix hashes for KV-reuse replay. As summarized by Siddhant Khare's field guide: mean hit ratio ~97% after tool gaps and ~92% after "Ask User" pauses, falling to ~58% for 15–30-minute gaps and ~18% beyond an hour; replaying under a 15-minute TTL, human sessions prefill 60.9% more tokens than a never-expiring cache, and SWE-bench-style agent-only runs need only ~5 minutes of retention while human sessions need about a day. ( GitHub repo;  trace dataset;  Khare field guide, 2026-10-18) Compared to you: same shape (fast decay once a human pauses), but via a third-party free gateway with mixed open-source harnesses, not per-vendor CLI subscription lanes. [secondhand numbers until you read the paper's own tables; the paper link on the repo was not captured]
"Agentic Coding in the Wild" (GitHub Copilot traces, arXiv:2608.00101): 3.2M users, 13M sessions, 761M calls, 95T tokens sampled from June 2026; KV hit rates 90% within a turn, 55% across turn boundaries, "drastically" invalidated by model switches and compaction; idle-time predictor capturing 86–90% of idle. Per the field guide's reading of its box plots: median hit ~95% under 2 minutes, ~70% at 2–10 minutes, ~0–5% beyond 10 minutes. ( arXiv abstract, retrieved 2026-08-24) Compared to you: much larger n, one vendor's internal infra, idle buckets up to ~10 minutes rather than your 1–24h tail.
GitHub issue #46829 (Claude Code): 119,866 API calls across two machines, Jan–Apr 2026, TTL-tier breakdown per call; documents the Feb 1h rollout and March regression to 5m with 17.1% overpayment. ( #46829) This is the closest published raw-session-log cost analysis for Claude Code; your 596M-of-2,349M cold-resume figure is a new decomposition (idle-return cost share) that it does not compute.
Antigravity telemetry (3,060 call pairs, Nov 17–19, 2026) and Subedi's binary-probed ~5-minute cliff: the only public gap-bucketed hit-rate tables for Gemini 4 through Antigravity. ( Forum thread;  Subedi)
The 120-run experiment (Fresh vs Continue vs Compact vs Fork vs Fresh+summary, gpt-6.1-sol and DeepSeek): Continue cost $2.293 vs Fresh $0.194 per delivery in one group, and Continue's cache-read cost alone ($1.266) was 6.5x the entire Fresh run; on the other model Fresh was slowest. Not a cache study, but the best public quality-and-cost joint data on the continue/fresh decision. ( dev.to)
Adjacent systems work (server-side, not vendor-accounting): vLLM × Mooncake (94%+ reusable prefixes in agentic traces, 3.8x hit-rate with a distributed KV store); TensorRT-LLM tech blog 27 (an "eviction cliff" where coding-trace hit rates fall toward 0.73 as the pool overflows; 480 s default block TTL); AgentPerfBench (final-turn contexts up to ~120K tokens); CacheTTL scheduling (arXiv:2511.02230); the HEAR harness↔engine protocol with "without observed task-quality degradation" gains. ( vLLM blog;  TensorRT-LLM blog 27;  arXiv:2609.34683;  arXiv:2610.06597)

What still appears to be missing (your niche): a fleet-scale, two-vendor, machine-local measurement of cold-resume share versus pause buckets exactly on subscription lanes (Claude Code 1h main + 5m subagent mix, Codex ChatGPT-backend), with API-list-price conversion. The nearest are #46829 (Claude only, cost by TTL tier) and Khare's FreeInference numbers (third-party gateway, character limits per-bucket precision). Claim "no comparable public prior art found for the Codex 1–24h decay curve itself"; your FreeInference-based support for the Anthropic bucket shape is strong. Search trail: arXiv (queries: prompt caching empirical, KV cache hit rate measurement, agentic sessions characterization), GitHub (claude-code and codex issues with "cached_tokens", "minutes", "by pause"), Google AI forum, SemiAnalysis, corporate engineering blogs, Reddit r/ClaudeCode + r/codex snippets, Hugging Face datasets, ~35 search-engine queries total.

Q5. Subscription vs API accounting
Anthropic API: cache reads do not count toward ITPM rate limits; cache creation and post-breakpoint input do ("with a 2,000,000 ITPM limit and an 80 percent cache hit rate, you could effectively process 10,000,000 total input tokens per minute"). ( Rate limits doc) Confidence: [established]
Claude Pro/Max/Ultra subscriptions: no official metering formula is published. Measured third-party panels state "cache reads barely count against a plan" and measure Pro at ~17.2M non-cached tokens/week against 71.8M total (75% cache reads); a related GitHub investigation (#45756) is explicitly trying to reverse-engineer the cache-read coefficient against quota, and #46829 reports cache creation counting at full weight. ( Wokey, data week 2026-11-09 to 11-16;  claude-code #46829) Practically: your 25%-of-input-token-equivalents cold-resume cost is an API-price abstraction; against a Pro/Max weekly window, cold resumes waste far more of the meter than the token math implies only if the meter is quota- not dollar-denominated; the usage-credit lane definitely re-bills you (and simultaneously drops you to 5m TTL). Confidence: [emerging], third-party measured, vendor-silent.
OpenAI / Codex credits: the Business/Enterprise rate card meters cached input explicitly and cheaply (GPT-6.2 Astra: 200 credits/M input, 10 credits/M cached, i.e. 0.05x, 1,000/M output). ( OpenAI Help, "updated 2 hours ago" at retrieval) An independent session-file analysis of the consumer Codex usage bar found it behaves like a dollar meter at API-priced rates, with every plan buying roughly 14x its price per week, on a workload of 96% cached input. ( InventiveHQ, 2026-10-04) [single-source for the 14x figure; method is well documented] OpenAI's own 5-hour/weekly limits for consumer Codex plans are documented separately; their cached-token weighting inside the percentage bar is not officially broken out. [no source found]
Q6. Failure modes and counter-arguments (steelman against your cold-resume warnings)

The strongest case against "block the resume of a large cold session":

Summarize-and-restart has its own measured losses. The 120-run experiment's DeepSeek bugfix round passed functional checks 4/6 with a frozen summary versus 6/6 for Fresh; compaction is a lossy model-written summary, and Codex's source and Anthropic's write-ups both concede accuracy effects; Amp's entire redesign was motivated by compaction drift. Irony worth stating in your article: vendors are themselves moving away from the summarization you'd be pushing users toward. ( 120-run experiment;  HarnessRouter;  Tessl)
A cold resume is a one-time cost; a fresh session is a permanent information loss. On a warm continuation, cached reads are 10–40x cheaper than re-prefill, and the cache rebuild happens once; if the diverted work is relevant, the resumed session may finish cheaper on task level than a fresh session that must re-read everything (the 120-run data shows exactly this on DeepSeek, where Continue beat Fresh on speed at equal delivery count). Counter-steelman: your data shows the cold rewrite can cost 25% of total session input across the fleet, an order-of-magnitude larger than the marginal cost of a fresh ~128K-token start, so the burden of proof rests on the continuation being plausibly worth it.
Failure to warn is the current failure mode, but warning coverage is partial: Claude Code's own hints fire at 75 minutes idle but not at 45 minutes on a 5m-TTL context (issue #51218), so a naive "trust the agent" stance under-warns; equally, a naive gate would block flows whose next call is a trivial tail question. ( FylloCode)
Context rot cuts both ways: continuing a 391K-token median context is itself quality-risky, but compacting it drops evidence like what was read but never edited, which is what a handoff file written from the session (not a summary) is designed to solve. ( Anthropic;  theaicommit, 2026-10-31)

Net: a "hard block" is too blunt; a cost-and-relevance gate with a handoff escape hatch matches both vendor guidance and the measured trade-off data.

D. Contradictions and debates
"24h retention" marketing vs behavior. The docs themselves resolve it with "typically... around 30 minutes and can retain them for up to 24 hours," but community complaints ("previously my work would hit average 95% cache hits... now I'd be lucky if I see a cache hit", backend changes thread, rate-limited at my attempt, so treat as [low-authority, snippet-only]) and intermittent-zero-hit issues describe behavior that严格遵守 best-effort semantics while feeling like a regression to users. ( codex #30425)
Anthropic intended-vs-operational TTL. #46829's day-by-day data says the 1h default was live and stable for 33+ days and then reversed server-side; Anthropic closed it "not planned" without explanation. Steelman for Anthropic: billing correct, tier visible per-call, and there are documented escapes (ENABLE_PROMPT_CACHING_1H=1 and per-bucket settings); the doc today says subscription main = 1h, and your November data supports a clean 60-minute cliff, so the regression appears to have been reverted. Present both, keep the date-stamped caution. ( #46829;  Claude Code docs)
Gemini's "no TTL" vs "up to 24 hours." Both statements are official but describe different tiers (implicit in-memory best-effort vs Agent Platform durable tier). Practitioner measurements on the consumer/Developer API lane (5-minute cliff, 25–30 s zero-drops) look nothing like the 24-hour horizon; there is no official reconciliation, and the forum poster's "15 to 20 minute" expectation conflicts with the measured ~5-minute cliff on Antigravity routes. This is the murkiest vendor story of the three; keep both claims separate and labeled in your article. ( Vertex overview;  Subedi;  Argon thread)
Keep-alives: individually rational, collectively corrosive. The keepalive-economics paper itself warns that because residency is priced per read and not per token-hour, "rational adoption is universal adoption" destroys LRU ranking, which is presumably why Google keeps its own keep-alive engine flag-gated and why vendors price 1h writes at 2x. Your tooling article should acknowledge this externality argument rather than presenting pings as a free lunch. ( arXiv:2607.19214)
E. Where your fleet data sits (positioning)
Your Claude Code 60-minute cliff is corroborated by docs, by #46829, and by idle compaction at ~54 minutes being designed "before the prompt cache expired." Nothing contradicts it. ( #46829;  TurboAI idle-compaction guide)
Your Codex 1–24h decay curve is the most novel number and is consistent with every mechanism OpenAI documents (30-minute typical availability, machine-local storage, load overflow routing, best-effort). No public dataset reports this same curve; the FreeInference study provides the closest analogue (58% at 15–30 min, 18% past an hour) but on different infra. ( FreeInference repo)
Your cold-resume cost share (25% of input-token equivalents) has no direct published competitor; the nearest published decomposition is #46829's 17.1% "overpaid vs 1h" fleet figure, which measures TTL-tier waste, not idle-return waste. Frame yours as the first (to my knowledge, after the trail above) published idle-return cost-share measurement on subscription lanes; say "we found no prior measurement combining cold-resume share with pause buckets across two vendors' CLIs." ( #46829)
F. Decision rules used in practice (with thresholds)
Pause < half the effective TTL: always continue. Claude Code subscription main thread: 1h (subagents 5m, so parallel-tool sessions are cooled by your 1h assumption). Codex: expect useful survival to ~30 minutes typical, decaying to nil at 24h, plus occasional sub-minute full misses even while warm: never rely on the last bucket being free ( docs).
Keep-alive only when cheaper than the re-prefill it prevents. A ~4-minute interval for 5-minute TTLs and ~46 minutes for 1-hour TTLs ($46-minute break-even is arXiv:2607.19214's own number; the field's tools converge on 50-minute pings for 1h TTLs). Practitioners: aider --cache-keepalive-pings, karanb192/cache-tax (user's own catalogue), Subedi's Antigravity unlock. ( arXiv:2607.19214;  Aider)
Right-size the write rather than paying the premium blanket: OpenAI's 12h breakpoint only on all-day stable prefixes (2.5x write recovered after the prefix is fully re-read past 30 minutes once); 30m (1.25x) on session context; Anthropic 1h TTL costs 2x versus 1.25x for 5m, so turn it on exactly when idle gaps of 5–60 minutes are common. ( OpenAI guide;  Anthropic pricing; the Respan and Romain Lespinasse write-ups cover the same math,  Respan)
Crossing the 60-minute idle line on Claude Code: the honest options are (a) resume anyway (one 1h-TTL write at 2x, full history intact), (b) hand off (durable summary file + fresh session: ~128K-token cold start plus summary read), or (c) let idle compaction do (b) for you at hour ~54 but accept that the compactor, not you, chose what survives. Given your data, (b) with a handoff document beats (a) purely on cost only when the next segment is unrelated work; for the same task, (a) usually wins on quality per dollar because the one-time re-prefill is cheaper than re-reading everything the summary dropped. ( Claude Code docs)
Prefer breaks to never hit mid-task threshold triggers: run /compact at natural task boundaries, not when memory pressure forces it (official guidance in both vendor docs); idle compaction is disable-able via idleCompaction: false (v2.1.290+). ( Claude Code docs)
Never do these mid-task: model switch, effort change, MCP/plugin toggle, whole-tool deny, client upgrade (official Claude Code list); timestamp/debug drift into the prompt or shuffled tool order (OpenAI cookbook). ( Claude Code docs;  Cookbook)

Practical heuristic that should be your article's headline rule, combining your two datasets and the vendor costs:

Gap < effective TTL (5m / 1h / minutes-at-best on Codex / ~5m Gemini implicit): continue.
Gap > TTL and next work = same task: continue or ping-warm in advance; a single 2x cache write is cheaper and safer than re-reading the corpus into a new session.
Gap > TTL and next work = new task: hand off (write a working-notes file, not a summary the model sees once), then start fresh. Idle-compacted or cold sessions over ~350–400K peak (your 391K median, with 28% over 500K) are already in context-rot territory, so the quality argument and the cost argument point the same way [speculative on the exact 400K number; no published threshold, but the rot literature and the 55% cross-turn hit rate support it].
Gap > several hours (Codex 2–6h+ per your curve) or on Gemini beyond ~10 minutes: cache is effectively dead on arrival (46%+ cold), don't pay for a warmer; decide purely on quality grounds.
G. Recommendations for your article

Safe to publish (multi-source, vendor-confirmed):

Claude Code on a subscription: 1h main-thread cache on subscription, 5m for subagents, sharp cliff at 60 min idle; supported by docs, #46829, and idle compaction at ~54 min. ( Claude Code docs)
The full Claude Code invalidator list. (same)
OpenAI's prompt_cache_retention semantics: in-memory 5–10 min up to 1h; 24h as best-effort max with ~30-min typical window, non-ZDR default 24h; prompt-cache entries machine-local and load-sensitive. ( OpenAI guide)
Gemini implicit caching: on by default, no guaranteed TTL; the only published horizon is a durable tier expiring "no later than 24 hours" with earlier eviction. ( Vertex docs)
Idle-gap decay curves (Copilot, FreeInference, Antigravity): the pause, not the tool loop, is where all production caching dies. This general mechanism exactly matches what your fleet saw on both vendors. ( arXiv:2608.00101;  FreeInference)
The keep-alive math (4-min/5m TTL, 46-min break-even on 1h TTL) with the free-lunch caveat. ( arXiv:2607.19214)
Cache reads are discounted but not free on any vendor's meter; on subscriptions (Claude, Codex credits) they are metered far below input rates but not necessarily at zero. ( Anthropic rate limits;  OpenAI rate card)

Needs caveats:

"OpenAI cached input 0.05x": correct only on GPT-6.1/6.2 Sol/Astra/Terra-class models; most GPT-5.6+ cached reads price at 0.1x. Verify per-model before publishing your cost weights; the rest of your multipliers (Anthropic 0.05x Opus 5.5 / 0.025x Fable, 2x/1.25x writes) match official docs exactly. ( OpenAI guide;  Anthropic docs)
"OpenAI advertises 24h": quote the "typically around 30 minutes... up to 24 hours" sentence verbatim; your measured shape (10% cold at 30–60 min, 46% at 2–6h) is the direct empirical confirmation of "up to" semantics, which is a stronger story than a contradiction.
"Gemini = 1h keep-alive possibility": there is no requestable 1h implicit TTL; explicit caches (Gemini 3 / 2.5, generateContent API) can set any TTL, but Gemini 4's explicit caching is unsupported, so Antigravity cannot opt into one today; the forum ask for a "guaranteed 1-hour cache TTL" remains an open feature request. ([SDK doc]( https://developers.openai.com/codex/… see rather  Gemini docs;  Antigravity thread)
"Cold = less than half of previous context read from cache": OpenAI's cached_tokens excludes hidden system tokens and rounds down to multiples of 128, and Anthropic's is per-breakpoint; state the definition or your per-bucket boundaries are attackable. ( OpenAI guide)
"One-hour cache on subscription = vendor promise": gated by being under plan limits; over the limit the main thread drops to 5m TTL (documented). ( Claude Code docs)

Likely wrong / re-publish only with corrections:

Any statement that OpenAI's 24h or Google's 24h are guarantees; both are explicitly covenanted as "up to"/"typical." Your data itself proves this and should be framed as confirming, not contradicting, the docs.
Any implication that summarized-then-restart is a strictly better outcome at the resume decision point: vendors have publicly backed away from exactly this mechanism (Amp) and retracted from compaction-from-summary for long sessions in favor of handoff artifacts; your decision rule should recommend a handoff (or a second-subagent send with the same prefix) rather than discarding the session wholesale, or you will be published just behind the vendor consensus. ( Tessl;  Anthropic)
Treating the 596M/2,349M cold-resume share as realized cash: on subscription lanes with cheap cache-read-weight meters, the effective waste share is most likely lower on metered limits (reads barely count) but higher where resumes trigger full-rate cache creation against quota. This is the biggest open gap across all of Q5, and your article should say so explicitly. ( Wokey;  claude-code #46829)
H. Sources

All retrieved 2026-11-20 unless noted. Page dates in parentheses where the page states one.

Official OpenAI

 https://developers.openai.com/api/docs/guides/prompt-caching
 https://developers.openai.com/api/docs/guides/prompt-caching.md (markdown mirror used for verbatim quotes)
 https://openai.com/index/better-prompt-caching-for-gpt-6/ (no page date shown)
 https://developers.openai.com/cookbook/examples/prompt_caching_201
 https://developers.openai.com/api/docs/guides/compaction
 https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
 https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing

Official Anthropic
8.  https://platform.claude.com/docs/en/build-with-claude/prompt-caching
9.  https://code.claude.com/docs/en/prompt-caching
10.  https://code.claude.com/docs/en/settings-reference
11.  https://code.claude.com/docs/en/costs
12.  https://platform.claude.com/docs/en/api/rate-limits
13.  https://www.anthropic.com/research/effective-context-engineering-for-ai-agents (2025-09-29)
14.  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Official Google
15.  https://ai.google.dev/gemini-api/docs/caching
16.  https://ai.google.dev/gemini-api/docs/interactions/caching
17.  https://ai.google.dev/gemini-api/docs/caching.md.txt
18.  https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview

Repository issues, forums, and community (independent measurement)
19.  https://github.com/anthropics/claude-code/issues/46829 (2026-04-12)
20.  https://github.com/anthropics/claude-code/issues/99096
21.  https://github.com/anthropics/claude-code/issues/63930
22.  https://github.com/anthropics/claude-code/issues/2603
23.  https://github.com/anthropics/claude-code/issues/102033
24.  https://github.com/openai/codex/issues/6698 (2025-11-15)
25.  https://github.com/openai/codex/discussions/18782 (2026-04-21)
26.  https://github.com/openai/codex/issues/30425 (2026-06-28)
27.  https://github.com/openai/codex/issues/21796
28.  https://github.com/openai/codex/issues/25604
29.  https://github.com/openai/codex/issues/39392
30.  https://github.com/EvanZhouDev/openai-oauth/issues/46 (2026-10-18)
31.  https://github.com/router-for-me/CLIProxyAPI/issues/5300
32.  https://github.com/code-yeongyu/senpi/issues/3901 (2026-10-21)
33.  https://github.com/google-antigravity/antigravity-cli/issues/1665
34.  https://github.com/google-antigravity/antigravity-cli/issues/1533
35.  https://discuss.ai.google.dev/t/gemini-4-argon-implicit-caching/199260 (opened 2026-11-09, retrieved 2026-11-17)
36.  https://discuss.ai.google.dev/t/telemetry-bug-report-why-antigravity-weekly-quotas-burn-so-fast-gemini-4-carbon-high-mid-turn-cache-collapse-5-5x-cost-5-min-implicit-cache-cliff/202768 (2026-11-19)
37.  https://github.com/github/copilot-cli/issues/5526
38.  https://github.com/googleapis/python-genai/issues/1880

Papers and datasets
39.  https://arxiv.org/abs/2608.00101 (Agentic Coding in the Wild, retrieved 2026-08-24)
40.  https://github.com/HarvardMadSys/freeinference_agentic_trace (and  https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace)
41.  https://arxiv.org/abs/2607.19214 (Keepalive Economics)
42.  https://arxiv.org/abs/2610.06597 (HEAR protocol)
43.  https://arxiv.org/abs/2609.34683 (AgentPerfBench)
44.  https://arxiv.org/html/2511.02230v6 (multi-turn agent scheduling with KV-cache TTL)
45.  https://vllm.ai/blog/2026-05-06-mooncake-store (2026-05-06)
46.  https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog27_Evaluating_Agentic_Serving_with_Trace_Replay_and_Job_Level_Metrics.md (figures quoted secondhand via Khare)
47.  https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat (AgentX)

Blogs and practitioner write-ups (lower authority, used for observed behavior)
48.  https://siddhantkhare.com/writing/agentic-inference-field-guide (2026-10-18)
49.  https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/ (2026-11-19)
50.  https://therouter.ai/news/openai-extended-prompt-cache-24h-default-gpt5-operator-routing/ (2026-06-04) [single-source]
51.  https://fyllocode.cc/en/blog/2026-08-25-prompt-cache-expiry-awareness (2026-08-25)
52.  https://harnessrouter.ai/blog/claude-code-compact-vs-new-session
53.  https://tessl.io/blog/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race (2025-11-14)
54.  https://dev.to/z_jc_37f8254a1cb25bff22ed/continue-compact-fork-or-start-fresh-a-120-run-coding-agent-experiment-5e8
55.  https://wokey.ai/claude-usage-limits (data week 2026-11-09 to 11-16)
56.  https://inventivehq.com/blog/codex-subscription-usage-measured (2026-10-04) [single-source for the 14x figure]
57.  https://aider.chat/docs/usage/caching.html
58.  https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
59.  https://blog.laozhang.ai/en/posts/claude-code-cache-miss-token-costs (2026-05-24)
60.  https://theaicommit.com/2026-10-31-how-to-tell-what-claude-code-and-codex-forget-when-they (2026-10-31)
61.  https://kstark007.github.io/blog/agentic-coding-in-the-wild/ (blog summary of the Copilot paper)
62.  https://tessl-adjacent:  https://www.learncursor.dev/fix/cursor-context-limit-reached and  https://docs.cursor.com/en/agent/chat/summarization (Cursor's summarization policy)
63.  https://github.com/cline/cline/issues/14329 and  https://github.com/cline/cline/issues/14979 (compaction thresholds)
64. Not opened (snippet-only, excluded from evidence except where flagged): the community forum thread on cache-hit regression (community.openai.com/t/recent-changes-destroyed-cache-hits/1405097), Reddit r/codex and r/ClaudeAI threads, the Medium post on the October cache regression.

Single recommendation

Publish the two-vendor fleet measurement as a confirmation study with a handoff-gated decision rule: treat the 60-minute Claude Code cliff and the 1–24h Codex decay as vendor-confirmed best-effort behavior (not vendor-controlled knob behavior), and spend your novelty budget on the one number no one else has published: the fleet-wide cost share of idle returns, shared as shares of input-token equivalents with the explicit caveat that subscription meters differ. Confidence [established] on the underlying mechanism claims, [emerging] on the cross-vendor cost-share number. Main assumption it rests on: that cache-hit-against-pause behavior on your subscription lanes generalizes to other accounts, which your six-machine cross-check partially controls for but cannot fully establish (single-organization routing pool).

Sources
2:57am

## Sources (links in the Mistral answer, 243 URLs)
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/cookbook/examples/prompt_caching_201
- https://openai.com/index/api-prompt-caching/
- https://developers.openai.com/api/docs/guides/prompt-caching.md
- https://openai.com/index/better-prompt-caching-for-gpt-6/
- https://www.prompthub.us/blog/prompt-caching-with-openai-anthropic-and-google-models
- https://dev.to/rikuq/openai-prompt-caching-explained-automatic-free-to-enable-90-off-cached-input-tokens-7bn
- https://octomind.run/blog/prompt-caching-explained
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching
- https://community.openai.com/t/how-is-prompt-cache-key-actually-used-in-api-calls/1357766
- https://therouter.ai/news/openai-extended-prompt-cache-24h-default-gpt5-operator-routing/
- https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/
- https://towardsdatascience.com/prompt-caching-with-openai-api-full-hands-on-python-tutorial/
- https://bytetech247.com/ai-productivity/openai-prompt-cache-24-hour-retention/
- https://www.developersdigest.tech/blog/prompt-caching-across-ai-providers-2026
- https://www.nops.io/blog/prompt-caching/
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://www.respan.ai/articles/claude-prompt-caching
- https://hidekazu-konishi.com/entry/anthropic_claude_api_prompt_caching_and_token_efficiency.html
- https://tensormesh.ai/learn/anthropic-prompt-caching-pricing/
- https://hinterbuild.com/blog/anthropic-prompt-caching-deep-dive
- https://www.romainlespinasse.dev/posts/choosing-prompt-cache-tier/
- https://ssimplifi.com/blog/anthropic-prompt-caching-explained
- https://dev.to/rikuq/anthropic-prompt-caching-explained-cachecontrol-markers-the-two-tier-write-premium-and-when-it-25cp
- https://synrouter.ai/blog/anthropic-cache-ttl-5min-vs-1hr
- https://technspire.com/en/blog/anthropic-prompt-caching-pricing-mechanics
- https://octomind.run/blog/claude-cache-ttl
- https://aipromptshub.co/blog/prompt-caching-anthropic-tutorial
- https://ai.google.dev/gemini-api/docs/generate-content/caching
- https://ai.google.dev/gemini-api/docs/caching
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/context-cache/context-cache-overview
- https://ai.google.dev/gemini-api/docs/caching.md.txt
- https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-context-caching
- https://blog.laozhang.ai/en/posts/gemini-context-caching
- https://ai.google.dev/api/caching
- https://ai.google.dev/gemini-api/docs/interactions/caching
- https://github.com/anthropics/claude-code/issues/46829
- https://www.reddit.com/r/ClaudeAI/comments/1s7mkn3/psa_claude_code_has_two_cache_bugs_that_can/
- https://github.com/anthropics/claude-code/issues/102033
- https://medium.com/@reactbd/claude-codes-cache-reportedly-fell-to-5-minutes-all-5-696-of-my-calls-since-then-got-1-hour-6e98053c7368
- https://github.com/anthropics/claude-code/issues/99096
- https://www.developersdigest.tech/blog/claude-code-idle-compaction-turn-off-cache-cost-2026
- https://github.com/anthropics/claude-code/issues/2603
- https://github.com/anthropics/claude-code/issues/63930
- https://code.claude.com/docs/en/prompt-caching
- https://claudcod.com/blog/claude-code-prompt-caching/
- https://www.reddit.com/r/ClaudeAI/comments/1uih6w7/how_prompt_caching_works_in_claude_code_and_how/
- https://docs.bswen.com/blog/2026-03-26-claude-code-pro-vs-max-cache-ttl/
- https://prosperinai.substack.com/p/claude-code-prompt-caching-explained
- https://if.codes/blog/claude-code-subagent-prompt-cache-ttl
- https://www.reddit.com/r/ClaudeCode/comments/1ui6c82/how_prompt_caching_works_in_claude_code_and_how/
- https://blog.laozhang.ai/en/posts/claude-code-cache-miss-token-costs
- https://verboo.ai/en/blog/claude-code-idle-compaction
- https://www.turboai.dev/blog/claude-code-idle-compaction-guide
- https://www.memorylake.ai/en/blogs/claude-code-idle-compaction
- https://www.reddit.com/r/ClaudeCode/comments/1x5n49q/autocompact_self_triggers_when_idle/
- https://code.claude.com/docs/en/settings-reference
- https://claudecamp.ai/blog/claude-code-idle-compaction
- https://www.dsebastien.net/2026-10-16-claude-code-idle-compaction-cheaper-to-resume-but-from-a-summary/
- https://github.com/openai/codex/issues/35300
- https://github.com/openai/codex/issues/29377
- https://github.com/openai/codex/issues/60379
- https://github.com/router-for-me/CLIProxyAPI/issues/5300
- https://github.com/openai/codex/issues/21796
- https://github.com/openai/codex/issues/30425
- https://github.com/EvanZhouDev/openai-oauth/issues/46
- https://github.com/askalf/dario/pull/1234
- https://www.reddit.com/r/codex/comments/1xb9prz/caching_upgraded_massively/
- https://github.com/openai/codex/discussions/18782
- https://community.openai.com/t/recent-changes-destroyed-cache-hits/1405097
- https://community.openai.com/t/new-24h-prompt-caching-retention-only-certain-models/1366221
- https://github.com/code-yeongyu/senpi/issues/3901
- https://github.com/openai/codex/issues/25604
- https://github.com/openai/codex/issues/39392
- https://github.com/openai/codex/issues/6698
- https://github.com/googleapis/python-genai/issues/1880
- https://discuss.ai.google.dev/t/gemini-4-argon-implicit-caching/199260
- https://discuss.ai.google.dev/t/has-anyone-gotten-implicit-caching-to-work/142699?page=2
- https://discuss.ai.google.dev/t/gemini-4-carbon-implicit-cache-frequent-full-misses-with-byte-identical-prefixes-gaps-5-min/201474
- https://www.datastudios.org/post/gemini-api-implicit-caching-0-cached-tokens-causes-fixes
- https://github.com/github/copilot-cli/issues/5526
- https://discuss.ai.google.dev/t/telemetry-bug-report-why-antigravity-weekly-quotas-burn-so-fast-gemini-4-carbon-high-mid-turn-cache-collapse-5-5x-cost-5-min-implicit-cache-cliff/202768
- https://asubedi.com.np/blog/why-antigravity-eats-weekly-quota-fast/
- https://github.com/n2ns/antigravity-panel
- https://discuss.ai.google.dev/t/bug-report-severe-server-side-implicit-cache-eviction-on-gemini-4-neon-64-5-miss-rate-at-400k-500k-context-95-redundant-uncached-input/202481
- https://github.com/google-antigravity/antigravity-cli/issues/1665
- https://aidevhub.net/blog/google-antigravity-prompt-caching
- https://github.com/google-antigravity/antigravity-cli/issues/1533
- https://github.com/google-antigravity/antigravity-cli/issues/1633
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-create
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-update
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-use
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/vertex-ai-zero-data-retention
- https://firebase.google.com/docs/ai-logic/context-caching
- https://blevinscm.github.io/genai-docs/context-cache/Context-caching-overview/
- https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://agentic-ai.readthedocs.io/en/latest/ContextEngineering/anthropic/
- https://ruchitsuthar.com/pathways/agent-engineering/context-engineering-long-running-agents/
- https://www.developersdigest.tech/blog/context-engineering-for-agents-explained
- https://www.morphllm.com/context-engineering
- https://simonwillison.net/2025/Jun/18/context-rot/
- https://dev.to/priyeshdave6/how-context-window-degradation-breaks-long-running-agents-in-production-and-how-to-engineer-your-4pjb
- https://forum.achivx.com/threads/context-rot-what-it-is-and-how-to-notice-degradation-as-the-context-grow
- https://news.ycombinator.com/item?id=44310054
- https://www.tmls.nyc/research/context-rot-mechanistic
- https://tamaton.com/blog/ai-agents/context-rot-why-long-prompts-quietly-break-agents
- https://www.morphllm.com/context-rot
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- https://ragmehta.substack.com/p/how-manus-engineers-context-for-its
- https://tianpan.co/blog/2026/03/02/context-engineering-lessons-from-manus
- https://medium.com/@peakji/context-engineering-for-ai-agents-lessons-from-building-manus-71883f0a67f2
- https://agentmarketcap.ai/blog/2026/04/08/manus-ai-context-engineering-production-agent-lessons
- https://mnemoverse.com/docs/research/agents/kv-cache-context-engineering
- https://medium.com/@joycebirkins/context-engineering-for-complex-agent-systems-kv-cache-file-management-prefill-prompts-and-rag-c7e0f3ba2cd3
- https://dev.to/r3dtuxedo/compact-clear-or-hand-off-running-long-agent-sessions-without-burning-your-limit-3hfp
- https://fyllocode.cc/en/blog/2026-08-25-prompt-cache-expiry-awareness
- https://siddhantkhare.com/writing/agentic-inference-field-guide
- https://www.reddit.com/r/ClaudeAI/comments/1vndhg6/finally_claude_code_has_autocontinue_when_limits/
- https://www.reddit.com/r/codex/comments/1wzapb1/send_continue_to_a_codex_session_when_the_limit/
- https://www.aidonenow.com/blog/step-away-from-claude-code-session-prompt-cache-expiry-idle-compaction-what-happens
- https://getcodeman.com/docs/keeping-agents-running
- https://wokey.ai/claude-usage-limits
- https://voyager.so/blog/claude-usage-limits
- https://optscale.ai/blog/claude-usage-limits
- https://www.ssdnodes.com/learn/claude-usage-limits-explained
- https://tokenmix.ai/blog/complete-claude-limits-guide-2026-tokens-uploads-5-hour
- https://contextbolt.com/blog/claude-usage-limits/
- https://platform.claude.com/docs/en/api/rate-limits
- https://developers.openai.com/codex/pricing
- https://help.openai.com/en/articles/11481834-chatgpt-rate-card-business-enterpriseedu-credit-based-pricing
- https://help.openai.com/en/articles/20001415-chatgpt-rate-card-enterprise-token-based-pricing
- https://www.reddit.com/r/codex/comments/1xqfioy/has_anyone_measured_actual_token_limits_for_codex/
- https://relux.works/en/blog/codex-goal-token-burn/
- https://www.codex-docs.com/en/docs/pricing
- https://inventivehq.com/blog/codex-subscription-usage-measured
- https://github.com/danyuchn/claude-cache-panel
- https://github.com/demouo/claude-code-cache-keepalive
- https://github.com/yujiachen-y/claude-code-cache-keepalive
- https://github.com/karanb192/cache-tax
- https://www.reddit.com/r/ClaudeAI/comments/1w8p8tn/prompt_cache_ttl_when_does_1_hour_beat_the/
- https://harnessrouter.ai/blog/claude-code-compact-vs-new-session
- https://dev.to/theaicommit/how-to-tell-what-claude-code-and-codex-forget-when-they-compact-a-session-532a
- https://aiengineeringfromscratch.com/interviews/agents/compact-or-hand-off
- https://dev.to/z_jc_37f8254a1cb25bff22ed/continue-compact-fork-or-start-fresh-a-120-run-coding-agent-experiment-5e8
- https://theaicommit.com/2026-10-31-how-to-tell-what-claude-code-and-codex-forget-when-they/
- https://thejuliekaiser.com/claude-code-compact-handoff/
- https://practiceoverflow.substack.com/p/compaction-the-hidden-trick-that
- https://huggingface.co/datasets/harvardMadsys/freeinference_agentic_trace
- https://github.com/HarvardMadSys/freeinference_agentic_trace
- https://github.com/marcft/freeinference-tool-loop-cache
- https://data.agentic-system.org/
- https://github.com/HarvardMadSys/freeinference_agentic_trace_site
- https://arxiv.org/html/2608.00101v1
- https://arxiv.org/pdf/2608.00101
- https://kstark007.github.io/blog/agentic-coding-in-the-wild/
- https://www.microsoft.com/en-us/research/wp-content/uploads/2026/08/ghcp_traces-6.pdf
- https://www.alphaxiv.org/abs/2608.00101
- https://www.microsoft.com/en-us/research/publication/agentic-coding-in-the-wild-characterizing-github-copilot-at-production-scale/
- https://arxiv.org/abs/2610.06597
- https://arxiv.org/html/2610.06597
- https://github.com/AI-Infra-Team/awesome-papers/issues/234
- https://www.alphaxiv.org/abs/2610.06597
- https://arxiv.org/abs/2609.01736
- https://github.com/china-qijizhifeng/agentic-harness-engineering
- https://arxiv.org/html/2607.19214v1
- https://arxiv.org/abs/2607.19214
- https://pith.science/paper/2607.19214
- https://arxiv.org/html/2511.02230v4
- https://arxiv.org/html/2511.02230v6
- https://blog.mempko.com/your-agentic-workflows-cache-keepalive-costs-8x-too-much-v2-the-interval-frontier/
- https://arxiv.org/html/2609.34683v1
- https://arxiv.org/abs/2609.34683
- https://arxiv.org/abs/2609.34683v1
- https://artificialanalysis.ai/articles/aa-agentperf
- https://awesomepapers.io/llm-papers/papers/2609.34683
- https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat
- https://www.forbes.com/sites/janakirammsv/2026/08/24/nvidia-amd-ai-agent-benchmark/
- https://www.forbes.com/sites/janakirammsv/2026/08/24/one-agent-benchmark-puts-nvidia-5x-ahead-of-amd-on-cost/
- https://inferencex.semianalysis.com/blog/agentx-inferencexv3-does-cuda-moat
- https://docs.nvidia.com/aiperf/dev/benchmark-modes/semi-analysis-agent-x-how-the-benchmark-works-faq
- https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog27_Evaluating_Agentic_Serving_with_Trace_Replay_and_Job_Level_Metrics.md
- https://medium.com/@krishnafattepurkar/the-kv-cache-memory-placement-reuse-and-why-a-1-7-hit-rate-costs-you-46-ttft-series-article-3-536d6d52cb9b
- https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog30_KV_Cache_Compression_in_TensorRT-LLM.md
- https://developer.nvidia.com/blog/5x-faster-time-to-first-token-with-nvidia-tensorrt-llm-kv-cache-early-reuse/
- https://github.com/NVIDIA/TensorRT-LLM/pull/21935
- https://vllm.ai/blog/2026-05-06-mooncake-store
- https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-05-06-mooncake-store.md
- https://x.com/vllm_project/status/2052113331927060840?lang=en
- https://dev.to/murali8k/mastering-agentic-kv-caching-how-to-slash-llm-agent-latency-and-costs-ol
- https://arxiv.org/pdf/2407.00079
- https://tokenade.net/en/articles/reduce-aider-token-usage
- https://aider.chat/docs/usage/caching.html
- https://aider.chat/docs/config/options.html
- https://github.com/Aider-AI/aider/issues/2492
- https://fast.io/resources/aider-token-limit/
- https://github.com/Aider-AI/aider/issues/2658
- https://github.com/cline/cline/issues/14329
- https://fast.io/resources/cline-token-limit/
- https://github.com/cline/cline/issues/14979
- https://fast.io/resources/cline-context-window/
- https://github.com/cline/cline/discussions/3248
- https://github.com/cline/cline/issues/9515
- https://tessl.io/blog/amp-retires-compaction-for-a-cleaner-handoff-in-the-coding-agent-context-race
- https://zenn.dev/ken_okabe/articles/2026-09-13-context-handoff-critic-loop?locale=en
- https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f
- https://medium.com/@steph.jarmak/how-i-use-amp-after-4-months-and-6000-threads-b4058204e9de
- https://baeseokjae.github.io/posts/amp-code-review-2026/
- https://locoroo.net/reports/2026-may/sourcegraph
- https://claudegpt.si/news/cursor-how-to-compact-context
- https://docs.cursor.com/en/agent/chat/summarization
- https://vibeanswers.com/cursor/losing-context-in-long-chats/
- https://www.learncursor.dev/fix/cursor-context-limit-reached
- https://forum.cursor.com/t/compact-compress-chat/132097
- https://fast.io/resources/cursor-max-files-in-context/
- https://iceberglakehouse.com/posts/2026-03-context-openai-codex/
- https://developers.openai.com/api/docs/guides/compaction
- https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- https://community.openai.com/t/experimental-context-management-compaction-in-codex/1395578
- https://supercode.sh/en/blog/guides/codex-context-window-and-compaction
- https://developers.openai.com/codex/config-reference
- https://community.openai.com/t/codex-rate-limits-discussion-thread/1378553/396
- https://community.openai.com/t/codex-is-destroying-systems/1405770
- https://community.openai.com/t/codex-usage-meter-decreases-during-active-usage-after-reset-ui-backend-desync/1378679
- https://community.openai.com/t/urgent-codex-ui-bug-astra-6-update-erased-months-of-work-causing-runaway-cached-input-charges-case-15158405/1398314
- https://community.openai.com/t/codex-limits-spark-frustration-among-subscribers/1390408?page=11
- https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
- https://caylent.com/blog/prompt-caching-saving-time-and-money-in-llm-applications
- https://docs.litellm.ai/docs/completion/prompt_caching
- https://github.com/anthropics/claude-code/issues/48082
- https://medium.com/@niklas-palm/prompt-caching-with-bedrock-and-anthropic-models-demystified-72261d269845
- https://code.claude.com/docs/en/costs
- https://codersera.com/blog/anthropic-june-2026-billing-change-claude-code/
- https://platform.claude.com/docs/en/about-claude/pricing
- https://ccassist.dev/claude-code-usage-tracker/
- https://www.reddit.com/r/ClaudeCode/comments/1v9unb6/are_usage_limits_counted_on_cache_read/
- https://atomicagent.io/blog/claude-code-pricing/
- https://arxiv.org/abs/2608.00101
- https://theaicommit.com/2026-10-31-how-to-tell-what-claude-code-and-codex-forget-when-they
- https://developers.openai.com/codex/
- https://tessl-adjacent/
