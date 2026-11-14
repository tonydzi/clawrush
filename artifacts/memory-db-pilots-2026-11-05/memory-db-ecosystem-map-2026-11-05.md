---
title: "Вторая память агентов: карта движков, экосистемных дверей и позиционирование (05.11.2026)"
type: research
status: proposed
date: 2026-11-05
dr: DR26-11-05-HUB-03-1726 (ведёт голова 2016522); расширение DR26-11-05-HUB-05-1743 (parked, дубль)
corr: voice-task
related: [zep-graphiti-study-2026-11-05.md, temporal-facts-architecture.md, _scratch/memory-db-pilots/bench.py, public-repos/vault-recall/vault_recall_backends.py, 03-Insights/memory-comparison-canary-2026-11-03, 03-Insights/recall-2026-11-03-second-brain-market-and-zep]
---
Machine: hub · Agent: Claude · Operator: Anton · 2026-11-05

# Вторая память агентов: на чём держат другие, куда нести наши интеграции

Простыми словами: наша память сейчас лежит в SQLite и в numpy-файле на одной машине. Другие команды держат то же самое в Postgres (чаще всего), в Qdrant, в LanceDB, реже в ClickHouse и графовых базах. Мы делаем так, чтобы тот же мозг умел жить внутри каждого из этих движков, и приходим в их сообщества с готовым примером «вторая память для агентов на вашей базе».

**Что уже проверено живьём 05.11** (WebFetch и WebSearch из этой сессии, страницы читал сам; дата у всех фактов = 05.11.2026). **Что не проверено** вынесено в конец. Ноги ДР от внешних LLM в эту заметку не брал: нога `legs$r.md` в пилотах головы 2016522 выдумала номера PR (lancedb#1234, qdrant#4567, ClickHouse#34567) и сама призналась, что интернета у неё нет.

## 0. Наш слой сейчас (инвентарь, замер 05.11 на хабе)

| Деталь | Где | Размер |
|---|---|---|
| Лексика | `<vault-imports>\_brain_lex_e5.db`, SQLite FTS5 unicode61 | 105 374 чанка |
| Плотные векторы | `_brain_e5.npy` + `_brain_e5_meta.pkl` (multilingual-e5-base, 768-d), поиск = numpy brute force | те же чанки |
| Граф сущностей | `_brain_entity.db`: entities 438 398 · mentions 8 048 253 · rel 5 056 935 | SQLite, строится детерминированно из wikilink |
| Реранк | bge-reranker-v2-m3 (кросс-энкодер) | в `brain_ask.py` |
| История фактов | `fact_history` / `object_history` (bitemporal), `docs/temporal-facts-architecture.md` | единицы строк |
| Открытая выжимка | `public-repos/vault-recall` (один файл, HTTP + MCP, read-only) | 0.1.0 → 0.2.0 с бэкендами (эта сессия) |
| Серверных БД | нет: Docker-демон на хабе не поднят, psql и clickhouse в PATH нет | |

Всё однопользовательское и однофайловое, между машинами ездит Syncthing. Это и сила (один файл, бэкап = копия), и потолок (один писатель, полный скан векторов).

## 1. На чём держат память другие (проверено 05.11)

| Проект | Хранилище по умолчанию | Сменные бэкенды | ClickHouse | SQLite локально | Источник |
|---|---|---|---|---|---|
| **Mem0** (68,5k★, Apache-2.0) | Qdrant | 25 провайдеров в `mem0/vector_stores/`: qdrant, chroma, pgvector, milvus, pinecone, redis, valkey, elasticsearch, opensearch, supabase, weaviate, faiss, mongodb, turbopuffer, s3_vectors, neptune_analytics, databricks, oracledb, azure_ai_search, vertex_ai, upstash, cassandra, baidu, azure_mysql, langchain | **нет** | нет провайдера | github.com/mem0ai/mem0/tree/main/mem0/vector_stores |
| **Zep / Graphiti** (32,6k★, Apache-2.0) | Neo4j | FalkorDB (+Lite embedded), Amazon Neptune; Kuzu deprecated | нет | нет | github.com/getzep/graphiti, CONTRIBUTING.md «Adding a graph driver» |
| **Cognee** (33,1k★, Apache-2.0) | LanceDB (вектор) + Kuzu (граф) | community-адаптеры в `topoteretes/cognee-community`: вектор Qdrant/Milvus/Pinecone/Redis/Valkey/Weaviate/OpenSearch/Azure; граф Memgraph/NetworkX/Spanner/TuringDB/TypeDB/pgGraph; гибрид DuckDB/FalkorDB; демо «вся память на Postgres» | нет | нет | github.com/topoteretes/cognee, cognee-community |
| **Letta** | Postgres + pgvector (self-hosted) | | нет | | WebSearch 05.11, docs.letta.com |
| **Redis Agent Memory Server** (325★, Apache-2.0) | Redis (вектор + JSON), working + long-term, фоновая экстракция | | нет | | github.com/redis/agent-memory-server; `V0/` = research artifact, поддерживаемый продукт = Redis Cloud |
| **ClickHouse/clickhouse-agent-memory** (0★, 1 fork) | ClickHouse: HOT (Memory engine) · WARM (MergeTree + HNSW 768-d) · GRAPH (рёбра в MergeTree, JOIN) | FastMCP, 8 инструментов, 17 таблиц; эмбеддинги Gemini/OpenAI/hash-fallback | да | | github.com/ClickHouse/clickhouse-agent-memory; CONTRIBUTING нет, issues нет |
| **auxten/clickmem** (66★, MIT) | chDB embedded, опционально ClickHouse-сервер | MCP + адаптеры Claude Code/Cursor/Codex/Aider | да | | github.com/auxten/clickmem |
| **LanceDB как память** | CrewAI перевёл память на LanceDB; плагин `hermes-agent-memory` (16.06.2026) | | | | lancedb.com/blog (два поста), WebSearch 05.11 |
| **Turbopuffer** (закрытый SaaS) | свой движок на объектном хранилище; клиенты Cursor, Notion, Anthropic (BYOC) | в Mem0 есть провайдер | | | turbopuffer.com/customers/notion, WebSearch 05.11 |
| **sqlite-vec** (8,2k★, MIT/Apache) | SQLite, pre-v1 | vec0: float/int8/binary, metadata-колонки и partition keys; в коде есть IVF и DiskANN | | да, это он | github.com/asg017/sqlite-vec |
| **pgvector 0.8.7** | Postgres | с 0.8.0 `hnsw.iterative_scan` лечит «меньше k при фильтре» | | | github.com/pgvector/pgvector README |

Вывод по таблице: **Postgres+pgvector = дефолт self-hosted (Letta, LangGraph, Honcho, демо Cognee)**; **Qdrant = дефолт Mem0 и самая длинная витрина интеграций**; **LanceDB = дефолт embedded (Cognee, CrewAI)**; **ClickHouse в памяти агентов пока почти пуст** (один вендорский демо-репо без звёзд и один сторонний проект на 66★), то есть дверь открыта; **SQLite остаётся локальным дефолтом** только через sqlite-vec.

## 2. Топ-5, что добавляем во вторую память (мой вердикт, не ДР)

Критерии: (а) у вендора есть агентный нарратив и живая витрина, куда примут пример; (б) движок закрывает конкретную дыру нашего SQLite; (в) можно поднять без сервера на ноутбуке (Syncthing-дружелюбно) и с сервером на хабе; (г) не ломает АК-47.

| # | Движок | Какую дыру закрывает | Как живёт у нас | Главный риск |
|---|---|---|---|---|
| 1 | **Postgres + pgvector** (+pgvectorscale / ParadeDB для BM25) | один писатель и полный скан; хаб как общий сервер флота; история фактов и граф в одной транзакционной базе; iterative_scan решает фильтры | `embedded-postgres` (PyPI, PG 18.6 + pgvector 0.8.6, есть win_amd64) на ноутбуке; сервер на хабе | тяжелее SQLite в обслуживании; Syncthing не синкает кластер |
| 2 | **ClickHouse / chDB** | аналитика по памяти (кто что спрашивал, что устарело), HNSW с 25.8, граф через JOIN за 3-10 мс по их же замеру; chDB = тот же SQL без сервера | chDB embedded в `.vault-recall/`; сервер по желанию | HNSW в chDB пока нет (exact cosineDistance); репо вендора без звёзд и без CONTRIBUTING, дверь не протоптана |
| 3 | **Qdrant** | ANN с фильтрами, бинарная квантизация, local mode без сервера | `qdrant-client` local mode (один каталог) → сервер через `QDRANT_URL` | две копии данных (наш индекс + их каталог) |
| 4 | **LanceDB** | embedded ANN в одном каталоге, версии таблиц, Arrow; ближе всего к нашей «один файл» философии | `lancedb` каталог в `.vault-recall/`, IVF при росте | формат молодой, pre-1.0 поведение |
| 5 | **sqlite-vec** | ANN не выходя из SQLite, metadata-фильтры внутри SQL; минимальный шаг | `vec0` таблица рядом с FTS5 в той же базе | pre-v1, ломающие изменения |

Не в пятёрке, но с дверью: **Graphiti** (вклад = `GraphDriver` + `operations/`, фича только после `rfc-approved`, CLA-бот; решение 26.07 «Neo4j-стек не берём» в силе), **Redis** (горячий слой сессий, но OSS = research artifact), **Turbopuffer** (закрыт, вклад только через Mem0-провайдер и примеры), **Milvus/Weaviate/Chroma** (RAG-витрины, агентной памяти как темы меньше).

Пилот-замер движков при одном и том же retrieval ведёт голова 2016522: `_scratch/memory-db-pilots/bench.py` (sqlite_numpy · sqlite_vec · duckdb · chdb · lancedb · qdrant, embedded, одинаковые 768-d векторы, recall@10 против exact, p50/p95, диск, фильтр, update/delete, restart). Результаты будут там же в `results.md`; в эту заметку цифры не переношу, пока прибор не отработал.

## 3. Публикуемый артефакт этой сессии: `vault-recall --backend`

`public-repos/vault-recall` 0.1.0 → 0.2.0: `vault_recall_backends.py` (numpy · sqlite-vec · lancedb · qdrant · pgvector · chdb) с одним контрактом `replace_all / search / count / close`; `vault_recall.py index --backend X` зеркалит индекс в движок, `ask/serve/mcp --backend X` ищут через него; `test_backends.py` сверяет каждый установленный движок с точным косинусом (top-1 равен, recall@10 ≥ 0.9, scope-фильтр без утечек, перезапуск с диска), `--break` даёт красное. Приёмка и статус прогона: раздел 6.

Почему это и есть «интеграция для их экосистемы»: один и тот же вызов `python vault_recall.py index ~/vault --backend pgvector` = «вторая память для агентов на Postgres», `--backend chdb` = «на ClickHouse», и так далее. Пример для их витрины = README-раздел + 20 строк кода, а не форк их проекта.

## 4. Двери экосистем (куда нести, проверено 05.11)

| Экосистема | Куда | Правила | Что несём |
|---|---|---|---|
| **awesome-ai-memory** (topoteretes) | PR в README: имя, URL, Open Source/Managed, GitHub, категория, storage model (Vector/Graph/Both) | «contributions are appreciated» | строка vault-recall (Memory Tools, Vector, Open Source) |
| **Qdrant** | `qdrant/landing_page` → `qdrant-landing/content/documentation/frameworks/<name>.md` (там уже Mem0, Cognee, Cheshire Cat); примеры в `qdrant/examples` (231★, Apache-2.0, есть «Agentic RAG with CrewAI») | PR или issue с предложением | страница `vault-recall` в frameworks + пример в examples |
| **Cognee** | `topoteretes/cognee-community/packages/vector/<adapter>` с README, examples/, tests/ | структура пакета обязательна, Apache-2.0 | не адаптер (у нас не вектор-БД), а пример «vault-recall как источник памяти для Cognee» в их integration guides (Claude Code/Codex/OpenClaw уже есть) |
| **Graphiti** | `graphiti_core/driver/<backend>_driver.py` + `operations/`, тесты `tests/driver/`; новые фичи только после issue с `rfc-approved` | CLA-бот | не сейчас: драйвер = недели работы, решение 26.07 против Neo4j-стека; дверь = issue-RFC «SQLite/pgvector driver», если решим |
| **Mem0** | `mem0/vector_stores/<name>.py` от `base.py` + docs `components/vectordbs/dbs/`; ClickHouse, LanceDB, SQLite там нет | CONTRIBUTING.md в репо, Apache-2.0 | провайдер **ClickHouse** для Mem0 = самый заметный вклад (68,5k★ репо, пустая клетка); второй кандидат LanceDB |
| **ClickHouse** | три тира интеграций: core (их org), partner (вендор), **community** (поддержка только через GitHub и Slack); страница в `ClickHouse/clickhouse-docs` (Mintlify), CLA-бот; репо `clickhouse-agent-memory` без CONTRIBUTING | CLA | (1) провайдер в Mem0 (п. выше), (2) `vault-recall --backend chdb` как community integration page, (3) issue/PR в `ClickHouse/clickhouse-agent-memory` с hybrid search (у них его нет по README) и с нашим бенчем |
| **pgvector** | README-таблица библиотек по языкам (40+ строк); процесса добавления не описано; iterative_scan документирован | PR в README | строка не наша (мы не библиотека); вместо этого пример «agent memory на pgvector» в экосистемах Supabase/Neon/Tiger Data (их cookbook-репо не проверял, см. раздел 7) |
| **LanceDB** | CONTRIBUTING: тесты обязательны, conventional commits, сперва коммент в issue; отдельный examples-репо не подтверждён | без CLA | пост «vault-recall на LanceDB» в их блог-формате «X rebuilt memory on LanceDB» через DevRel + пример |
| **Redis** | `redis/agent-memory-server` (Apache-2.0); OSS = research artifact | не проверял CONTRIBUTING | низкий приоритет: вендор сам увёл поддержку в облако |
| **auxten/clickmem** | 66★, MIT, адаптеры Claude Code/Cursor/Codex | CONTRIBUTING нет | сосед по нише: issue «общий бенч chDB-памяти» + взаимная ссылка; лучший живой тред домена для `/rep-reply` |

Порядок касаний (один PR в репо, мерж, потом следующие, §4.7): **awesome-ai-memory → Qdrant frameworks page → Mem0 ClickHouse provider → ClickHouse community page → clickmem issue**. Каждое касание через `outbound-gate` + `gh_pr_discipline.py` + подпись `08-Templates/outbound-signature.md` (в репо ≥1000★ только имя).

## 5. Позиционирование (одна фраза на экосистему, без продажи)

- ClickHouse: «Second brain for coding agents on ClickHouse: the same vault, the same MCP tool, your cluster underneath; chDB for the laptop, server for the fleet.»
- Postgres/pgvector: «Agent memory you can `pg_dump`: notes, vectors, bitemporal fact history and the entity graph in one transactional database.»
- Qdrant: «Vault recall backed by Qdrant local mode: one directory on a laptop, one URL change for the server.»
- LanceDB: «Embedded agent memory in one folder: Lance tables next to your markdown, sync it like files.»
- Retrieval/embedding вендоры: «Bring your embedder and reranker; vault-recall turns any folder of notes into a memory backend with your model inside.»

## 6. Приёмка `vault-recall 0.2.0` (заполняется по факту прогона)

- `python test_backends.py` (хаб, 05.11 22:30 UTC, rc=0): numpy PASS · sqlite-vec PASS p95 0.8 ms · lancedb PASS p95 11 ms · qdrant PASS p95 6.1 ms · pgvector PASS p95 1.4 ms (embedded-postgres) · chdb SKIP (колеса под Windows нет, у двойника chDB гонялся в WSL).
- `--break` (18:5x UTC): numpy/sqlite-vec/qdrant FAIL «top1 58 != exact 183», строка «test went RED as it must», rc=0.
- `test_vault_recall.py` после патча: «0 failure(s)», rc=0 (поведение `numpy` не менялось).
- Починка по ходу: `embedded-postgres` в системном Python был установлен наполовину (pip убит лимитом, `postgres.bki` отсутствовал) → `--force-reinstall --no-deps`; API пакета = `get_server(pgdata).get_uri()` / `cleanup()`, класса `EmbeddedPostgres` нет (исправлено и в `vault_recall_backends.py`, и в `bench.py` двойника).
- Пилот на 20k чанков (bench.py, 22:27 UTC): **pgvector p50 1.2 ms, recall@10 0.995, фильтр 0.998, рестарт ✅, диск 342 MB**; Qdrant local p50 84 ms, recall 1.0, диск 165 MB; LanceDB flat 157 ms, recall 1.0. Полная таблица семи движков: `04-Projects/DR/DR26-11-05-HUB-03-1726-synthesis.md` §3.

## 7. Retrieval / embedding вендоры для встречного предложения (список, не касания)

Кому имеет смысл принести «вторая память для агентов с вашим эмбеддером внутри» (vault-recall берёт модель через `VAULT_RECALL_EMBED`, любая sentence-transformers-совместимая; для API-эмбеддеров нужен адаптер, это следующий шаг):

| Вендор | Что у них есть по памяти агентов (проверено?) | Дверь |
|---|---|---|
| Jina AI | embeddings v3/v4, reranker; в нашем бенче 03.11 Anima connectome на Jina дал 23/24 | cookbook-репо не проверял |
| Voyage AI (MongoDB) | voyage-3, rerank-2 | docs/examples, не проверял |
| Cohere | embed v4, rerank 3.5 | cookbook, не проверял |
| Nomic | nomic-embed-text, локально | examples, не проверял |
| BAAI/BGE | bge-m3, bge-reranker-v2-m3 (у нас уже реранкер) | HF, issue в FlagEmbedding |
| Mixedbread | mxbai-embed, rerank | docs, не проверял |
| Qwen3-Embedding / Reranker | в кэше хаба | HF |
| Ollama / LM Studio / llama.cpp | локальный инференс эмбеддеров | integrations-списки, не проверял |
| Vespa, Weaviate, Milvus/Zilliz, Elastic, Typesense, Meilisearch, Chroma, Pinecone, Vectara, Exa | retrieval-инфра, у части (Weaviate, Milvus, Chroma, Pinecone, Elastic, Vectara) есть провайдер в Mem0 | их examples-репо, не проверял |

Это раздел 5 расширенного промпта `docs/dr-prompts/DR26-11-05-HUB-05-1743-memory-db.md`; живую проверку дверей этих вендоров отдал рельсе `llm_ask --class web` 05.11, все четыре ноги (gemini квота, muse/claude/grok таймаут 300 с) упали, повторить на свободной машине.

## 8. Что не проверено и что опровергнет вывод

Не проверено: цифры пилота (bench.py ещё не отработал); страницы CONTRIBUTING у LanceDB-examples, Redis, Supabase/Neon/Tiger cookbook; свежие принятые внешние PR в Qdrant landing_page и Mem0 (поимённо); статус HNSW в chDB 4.x; лицензия `clickhouse-agent-memory`; Mem0 CONTRIBUTING по новым провайдерам (видел только список файлов).

Опровергнет топ-5: если bench.py покажет, что embedded-движки на 100k чанков не быстрее numpy brute force при recall ≥ 0.95 (тогда дыра ANN не дыра, и мотив остаётся только экосистемный); если Mem0 отклонит ClickHouse-провайдер по политике (тогда ClickHouse-дверь = только community page); если Postgres на ноутбуке через embedded-postgres не переживёт Syncthing (тогда pgvector = только хаб).

**Ход рассуждений.** Стоит на: живых страницах репо (список файлов Mem0, CONTRIBUTING Graphiti/LanceDB/ClickHouse, README pgvector/sqlite-vec/cognee-community, Qdrant frameworks page), инвентаре наших баз (sqlite3 count), отчёте Codex 03.11 и разборе Zep 05.11. Проверено: каждый факт раздела 1 и 4 читал в этой сессии, дата 05.11. Опровергло бы: цифры пилота и отказ хотя бы двух дверей из пяти.
