# DR26-11-05-HUB-05-1743 · Databases and infrastructure for an agent "second brain"

Machine: hub · Agent: Claude · Operator: Anton · 2026-11-05
Кормит решение: выбор движков хранения для пилотов SecondBrain вместо SQLite и список экосистем для outreach (anton 05.11 голосом, voice001 t1793894659).
Реестр: `dr_registry.py` → DR26-11-05-HUB-05-1743. Веер: все браузерные рельсы, максимальное рассуждение, кворум 4/6.

---

## PROMPT (paste verbatim)

You are doing a deep technical research report for an engineering team that runs a "second brain" (long-term memory) for a fleet of LLM coding agents (Claude Code, Codex, Cursor, Gemini) across ~8 machines (Windows, macOS, Linux).

**Our current stack (facts, do not re-research):**
- ~105k text chunks from ~25k markdown notes (Obsidian vault), multilingual (Russian + English).
- Dense retrieval: multilingual-e5-base (768-d) vectors in a numpy file; lexical: SQLite FTS5 (unicode61); fusion by RRF; cross-encoder rerank (bge-reranker-v2-m3). One process, loopback HTTP + MCP server, read-only over the vault.
- Entity graph in SQLite: 438k entities, 8.0M mentions, 5.1M co-occurrence edges (built deterministically from wikilinks, no LLM).
- A small bitemporal fact history (valid_from / valid_to / expired_at) in SQLite, few rows yet.
- Everything is single-node, files synced between machines by Syncthing; no server databases are running today (no Postgres, no ClickHouse, no Docker).
- Open-source extraction: github.com/tonydzi/vault-recall (one-file HTTP+MCP memory backend).

**Questions to answer, with citations (URL + date seen) for every factual claim:**

1. **Landscape (as of November 2026).** Which storage engines do the leading agent-memory projects actually use under the hood, and which backends they officially support? Cover at least: Mem0, Zep/Graphiti, Letta, LangMem/LangGraph Store, Cognee, Supermemory, memU, Redis Agent Memory Server, Hindsight (vectorize), Agent Zero Memory, Memori, ClickHouse/clickhouse-agent-memory, auxten/clickmem, LanceDB (CrewAI, Hermes), Turbopuffer (Cursor, Notion). For each: default store, pluggable backends list, whether SQLite is the local default, and whether ClickHouse / Postgres+pgvector / Qdrant / Redis / graph DB are supported. Give a table.

2. **Engine deep-dives.** For each of these engines evaluate fitness as the storage layer of an agent second brain with ~100k-10M chunks, 768-1024-d vectors, hybrid (BM25 + vector) search, metadata filters (tenant/project/date), bitemporal fact history, and an entity graph with 2-hop queries:
   - Postgres + pgvector (+ pgvectorscale, ParadeDB pg_search, pg_textsearch / Tiger Data). Embedded options for laptops (embedded-postgres / pgserver / pgbox on PyPI).
   - ClickHouse (vector similarity index HNSW via usearch since 25.8; chDB embedded; clickhouse-agent-memory HOT/WARM/GRAPH tiers). Status of the vector index (experimental vs GA), filtered ANN, full-text index status.
   - Qdrant (local in-process mode vs server; hybrid search with sparse vectors; payload filters).
   - LanceDB (embedded, Arrow/Lance format, hybrid search, versioning).
   - Graph: Neo4j / FalkorDB / FalkorDB Lite / Kuzu (deprecated) via Graphiti; is a dedicated graph DB needed for 2-hop over 5M edges or does SQL (Postgres recursive CTE, ClickHouse JOIN) suffice?
   - Redis (RediSearch vector + JSON) as hot/session tier.
   - SQLite extensions: sqlite-vec, sqlite-vss, DuckDB vss. Honest ceiling of staying on SQLite.
   For each: write throughput for incremental re-index, p50/p95 query latency at 100k and 1M chunks (published benchmarks only, with source), RAM footprint, filtered-ANN correctness (does it return fewer than k?), multi-writer story across machines, backup/sync story for a laptop fleet, license.

3. **Top-5 recommendation.** Rank the five most promising engines/infrastructure pieces to add as pluggable backends to our second brain, with a one-paragraph justification each, what we gain over SQLite+numpy, and the single biggest risk. State explicitly which should be the default for (a) single laptop, (b) shared fleet server, (c) 10M+ chunks.

4. **Ecosystem doors for publishing integrations.** For ClickHouse, Postgres/pgvector, Qdrant, LanceDB, Redis, Graphiti, Mem0, Cognee, LangGraph Store: where do community integrations get listed (docs page, integrations repo, awesome list, partner portal, Discord/Slack channel, Show-and-tell discussions), the exact repo/path to PR, the contribution rules (CLA, DCO), and a recent example of an accepted community integration PR with date. Include github.com/topoteretes/awesome-ai-memory and any "awesome-pgvector"/"awesome-clickhouse" lists.

5. **Companies and OSS projects doing retrieval / embeddings / rerankers** that could use a "second brain for agents" layer on top of their tech: embedding providers (Voyage, Jina, Cohere, Nomic, BAAI/BGE, Mixedbread), rerankers, retrieval infra (Vespa, Weaviate, Milvus/Zilliz, Elastic, Typesense, Meilisearch, Turbopuffer, Chroma, Pinecone, Vectara, Exa), and local inference (Ollama, LM Studio, llama.cpp). For each: do they have an "agent memory" story today (link), an integrations/examples repo accepting PRs, and a named DevRel / community contact channel.

6. **Benchmarks.** Which public benchmarks are credible for memory quality (LongMemEval, LoCoMo, ConvoMem, BEAM, DolphinBench, STATE-Bench) and which published numbers are self-reported vs independently reproduced? What minimal protocol would let us compare storage engines fairly when retrieval algorithm and embeddings are held constant (Recall@k, nDCG@k, p95, RAM, ingest time, correction/delete, restart, idempotency, tenant isolation)?

**Output format:** Markdown. Sections 1-6 in order. Every claim with [source](URL) and date. Separate "measured by source" from "vendor claim". End with: (a) a 10-line executive summary in plain language, (b) a list of what you could not verify. Do not pad. Prefer primary sources (repo READMEs, docs, release notes, papers) over blog roundups.
