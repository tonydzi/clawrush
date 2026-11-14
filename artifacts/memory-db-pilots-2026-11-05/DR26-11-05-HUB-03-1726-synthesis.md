---
title: "DR26-11-05-HUB-03-1726: хранилище второй памяти, кто на чём, пилоты движков, куда нести"
dr_id: DR26-11-05-HUB-03-1726
date: 2026-11-05
type: reference
stage: raw
status: synthesized
origin: anton (голосом 05.11.2026, voice-task)
machine: hub
operator: anton
authored_by: claude
reviewed_by: codex (read-only VERIFY 2016472/2016476/2016481/2016486 в комнате <chat-id>)
related: ["[[DR26-11-05-HUB-03-1726-prompt]]", "[[business-plan-2026-10-agent-memory]]", "[[insight-2026-11-03-antra-memory-vs-ours]]", "[[concept-bible-platinum]]"]
tags: [dr, agent-memory, storage, clickhouse, pgvector, qdrant, lancedb, duckdb, sqlite, pilots, oss-contribution]
---
Machine: hub · Agent: Claude · Operator: Anton · 2026-11-05

# Простыми словами

Наша вторая память лежит не «в SQLite», а в трёх слоях: SQLite держит текстовый поиск и граф сущностей, numpy-файлы держат векторы, SQLite же ведёт журналы. Остальной рынок делает то же самое, только дефолт у всех один: Postgres с pgvector для self-host, Qdrant у Mem0, граф у Zep и Cognee. ClickHouse зашёл в тему через облако и через маленький проект clickmem на встроенном ClickHouse (chDB).

Пилоты на нашем живом срезе (20 000 чанков, одни и те же векторы e5 768-d, 200 запросов) показали: на нашем масштабе наш numpy-скан быстрее всех, ClickHouse и DuckDB честно работают и дают фильтры, правки, рестарт. Переезжать не надо. Надо добавлять движки как «витрины» для OSS-вклада и как страховку под рост графа и многопользовательскую запись.

# 1. Что у нас сейчас (замер 05.11.2026, `<vault-imports>`)

| Слой | Движок | Размер |
|---|---|---|
| Текст (BM25) | SQLite FTS5 `_brain_lex_e5.db`, 105 374 чанка | 426 MB |
| Граф сущностей | SQLite `_brain_entity.db`: 438 398 сущностей, 2.1M ключей, 8.0M упоминаний, 5.06M рёбер | 1.4 GB (+6.9 GB `_bt`) |
| Векторы | numpy: OpenAI 105 374×3072 f32 (1.3 GB) и multilingual-e5-base 105 374×768 (324 MB), метаданные в pickle | 1.6 GB |
| Журналы | SQLite `turnstate/turnstate.db`, `_embed_cache.sqlite` | <10 MB |
| CRM и чаты | SQLite `leads.db` 1.9 GB, `dm_messages.db` 697 MB | 2.6 GB |

Вывод: SQL у нас = SQLite в роли «метаданные + FTS + граф + журнал». ANN-индекса нет, векторы ищутся полным скан-умножением в RAM. Это и есть точка сравнения.

# 2. Кто на чём держит память (живые доки, 05.11.2026)

| Система | Вектор | Граф | Реляц./метаданные | Режим | Источник |
|---|---|---|---|---|---|
| Mem0 (68.5k★) | Qdrant по умолчанию; 20+ бэкендов: pgvector, Chroma, Milvus, Redis, Turbopuffer, S3 Vectors, FAISS… | Neo4j опционально | нет | библиотека + SaaS | docs.mem0.ai/components/vectordbs/overview |
| Mem0 cloud | мигрировали сотни миллионов записей с pgvector на Turbopuffer, 3 TB+ эмбеддингов | | | SaaS | turbopuffer.com/customers/mem0 |
| Zep / Graphiti (32.6k★) | внутри графа | Neo4j, FalkorDB, Kuzu (embedded), Amazon Neptune через GraphDriver | нет | библиотека/сервер | github.com/getzep/graphiti |
| Letta (letta-code 3.8k★; V1-сервер retired) | pgvector | нет | Postgres (LETTA_PG_URI) | сервер | docs.letta.com/guides/selfhosting/postgres |
| LangGraph Store | pgvector (HNSW, cosine) через IndexConfig | нет | Postgres (namespaced KV) | библиотека | reference.langchain.com langgraph.store.postgres |
| Cognee (33.1k★) | LanceDB по умолчанию; pgvector, Qdrant, Weaviate, Milvus | NetworkX по умолчанию; Kuzu/Ladybug, Neo4j, FalkorDB | SQLite/Postgres | библиотека | docs.cognee.ai/guides/store-configurations |
| Redis Agent Memory Server (325★) | Redis (RediSearch) | нет | Redis | сервер, REST+MCP; сам называет OSS «research foundation» | redis.github.io/agent-memory-server |
| ClickHouse Cloud Agent Memory | ClickHouse | нет | ClickHouse | облачная фича, per-user store | clickhouse.com/docs/products/cloud/features/ai-ml/agents/memory |
| auxten/clickmem (66★, последний push 18.06.2026) | chDB (embedded ClickHouse) или ClickHouse; эмбеддинги локально | нет | ClickHouse | библиотека, MIT, адаптеры Claude Code/Cursor/Codex/Aider… | github.com/auxten/clickmem |
| Honcho (Plastic Labs) | pgvector | нет | Postgres + Redis кэш | сервер | dev.to обзор 2026, не первоисточник |
| Hindsight (Vectorize) | своя платформа | | | SaaS; **внешние PR не принимают** (CONTRIBUTING:175, нашёл Codex) | github.com/vectorize-io/hindsight |
| Anima Connectome | архив событий + L1/L2/L3 пересказы | нет | SQLite/файлы | библиотека | [[insight-2026-11-03-antra-memory-vs-ours]] |

Паттерн: **вектор + реляционные метаданные в одном Postgres** = дефолт индустрии; **граф** = Zep/Cognee; **embedded** (LanceDB, Kuzu, chDB, sqlite-vec) = локальные агенты, наш класс. Никто из крупных не держит память в ClickHouse как в основном слое; ClickHouse сам продаёт это как фичу облака и через chDB.

# 3. Пилоты: один корпус, одни векторы, шесть движков

Прибор: `<repo>\_scratch\memory-db-pilots\bench.py` (0 LLM). Срез: 20 000 случайных чанков из `_brain_e5.npy` (seed 7), 768-d, нормированные. Запросы: 200 held-out чанков, gold = точный top-10 по косинусу на numpy. Проверки: ingest, индекс, p50/p95, recall@10, фильтр по `source_type`, update (подмена вектора обязана стать top-1), delete, рестарт (переоткрыть и получить тот же ответ), диск. Хаб в это время был под нагрузкой (другие сессии, WMI-шторм), цифры = порядок величины, не финал. Docker-демон на хабе не поднят, поэтому серверные Postgres/Qdrant-server/Redis не гонялись; ClickHouse гонялся как chDB в WSL (на Windows колеса chDB нет).

| Движок | Где | ingest s | index s | p50 ms | p95 ms | recall@10 | фильтр | update | delete | рестарт | диск MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **SQLite+numpy (наш)** | Win | 3.5 | 0 | **2.0** | **2.4** | 1.000 | 1.000 | ✅ | ✅ | ✅ | 66 |
| sqlite-vec 0.1 (vec0) | Win | 7.2 | 0 | 62 | 300 | 1.000 | 1.000 | ✅ | ✅ | ✅ | 69 |
| DuckDB 2.0 + VSS HNSW | Win | 114 | 4.5 | 5.3 | 7.0 | 0.993 | 0.988 | ✅ | ✅ | ✅ | 189 |
| **ClickHouse 26.9 (chDB 4.4), cosineDistance скан** | WSL | 8.1 | 0 | 30 | 36 | 1.000 | 1.000 | ✅ (ALTER UPDATE) | ✅ | ✅ | 227 |
| LanceDB 0.41, IVF_PQ 64×48 | Win | 125 | 8.8 | 404 | 660 | 0.633 | 0.616 | ✅ | ✅ | ✅ | 66 |
| LanceDB 0.41, flat (без IVF_PQ) | Win | 59.55 | 0.0 | 157.42 | 475.76 | 1.000 | 0.998 | ✅ | ✅ | ✅ | 64 |
| Qdrant local mode (HNSW на диске) | Win | 157.67 | 0.0 | 84.25 | 147.86 | 1.000 | 1.000 | ✅ | ✅ | ✅ | 165 |
| **Postgres 18.6 + pgvector 0.8.6 HNSW** (embedded-postgres, без Docker) | Win | 24.98 | 13.8 | 1.21 | 2.18 | 0.995 | 0.998 | ✅ | ✅ | ✅ | 342 |

Строки LanceDB flat / Qdrant local / pgvector дописаны сессией H62283 (f9a9c736) 05.11 по файлам `results-win-lance-flat-qdrant.json`, `results-win-qdrant.json`, `results-win-pgvector.json`; движок pgvector добавлен в `bench.py` классом `Pgvector` (бэкап `bench.py.bak-pgvector-f9a9c736-20261105`), Postgres поднят через `embedded-postgres` (PyPI), индекс HNSW `vector_cosine_ops`, `hnsw.iterative_scan=relaxed_order`. Machine: hub · Agent: Claude · Operator: Anton · 2026-11-05


Что это значит (честно):
- На 20k×768 наш numpy-скан в RAM быстрее любого движка. На полном корпусе 105k×3072 скан = ~40 мс, тоже не больно. **Скорость не причина переезжать.**
- ClickHouse через chDB: без сервера, SQL, фильтры, мутации, рестарт — всё работает. 30 мс на скан. Это рабочий «SecondBrain on ClickHouse» за один файл адаптера. Векторный индекс `vector_similarity` (USearch HNSW) не включал, это следующий шаг.
- DuckDB VSS даёт HNSW с recall 0.99 и 5 мс, но ingest через executemany медленный (нужен Arrow-батч), и HNSW-persistence у них помечена experimental.
- sqlite-vec: самый родной вариант (та же SQLite), но это тоже скан, 62 мс p50 и 300 мс p95 на 20k. Проект без коммитов с мая 2026 (8.2k★).
- LanceDB с PQ — моя ошибка конфигурации, не приговор движку; честный flat-прогон идёт.

# 4. Топ-5, куда нести пилоты (проверено по GitHub API 05.11.2026)

| # | Движок | Дверь вклада | Правила | Свежие мержи |
|---|---|---|---|---|
| 1 | **ClickHouse** | `ClickHouse/examples` (233★, push 05.11), папка `ai/` (сейчас только `clickhousectl`, `mcp`) | self-contained пример + README, kebab-case, **CLA на первом PR** (подписываю сам, §0 CLA) | #513 pg-analytics lab, #505, #504 (sdairs, сотрудник, 23–30.10) |
| 2 | **Qdrant** | `qdrant/examples` (231★, push 22.10), 46 папок-примеров | PR с ноутбуком/скриптом | #137, #136 Discord RAG (21.10), #134 neural search (18.10), #133 (14.10) |
| 3 | **LanceDB** | `lancedb/vectordb-recipes` (986★, push 04.11) | PR, внешние авторы мержатся | #361 (04.11), #358 Nvidia RAG blueprint, #357 AG2 multi-agent RAG, #356 MiniMax RAG (внешние, апрель) |
| 4 | **Postgres + pgvector** | `pgvector/pgvector-python` (1.5k★, push 05.11) `examples/` | PR; в самом pgvector (23.6k★, ≥1000★ = только имя без ссылок) | не считал; Docker-пилот ещё не сделан |
| 5 | **DuckDB** | `duckdb/community-extensions` (355★, push 05.11): PR с одним `description.yml` в `extensions/<name>/`; расширение должно жить в публичном репо | формальная дверь, самая «инженерная» | регистр живой |

Резерв: `auxten/clickmem` (MIT, но тишина с 18.06.2026, 4 issue), `asg017/sqlite-vec` (тишина с 18.05.2026), `redis/agent-memory-server` (лицензия NOASSERTION, «research foundation»), `kuzudb/kuzu` **archived** 10.10.2025 (Ladybug = преемник, в список не брать по старому имени).

Гейты из ревью Codex (2016486): Hindsight PR не принимает; Letta требует AI_POLICY с человеческой проверкой и фразой подтверждения — за Антона не подписываем, значит PR в Letta только если он сам прочитает и подтвердит; Cognee принимает код/тесты/доки от ветки dev.

# 5. Форма вклада, чтобы это была починка/пример, а не непрошеная фича (§4.7)

В каждую витрину несём **один** пример `second-brain-on-<engine>`: адаптер нашей схемы (chunks + entities + mentions + журнал) под движок, скрипт ingest из numpy/pkl, 3 запроса (вектор, вектор+фильтр, граф-соседи) и честный замер против SQLite из этой заметки. Текст от Майкрофта с раскрытием ИИ, подпись по `08-Templates/outbound-signature.md`, ≥1000★ = только имя. Один PR на репо, следующий после мержа. Исходящее только после `artifact.proposed` → ревью Codex → `outbound-gate`.

# 6. Против переезда (сильнейшие доводы)

За SQLite: один файл, Syncthing-дружелюбие, бэкап = копия, нулевой ops, транзакция FTS+граф+журнал в одной базе, работает на всех 8 узлах флота без демонов. Где ломается: одна пишущая сессия на базу (у нас пишут десятки сессий и рутины), нет ANN (на 3072-d и миллионе чанков скан станет секундами), граф в 5M рёбер в SQLite без графового движка = ручные JOIN-ы. Ответ: не переезд, а второй слой: chDB/DuckDB для аналитики и фильтров, граф при росте в Kuzu/Ladybug или FalkorDB, векторный индекс по факту боли.

# 7. Чего не хватает и что не подтверждено

- Браузерный веер ДР (ChatGPT/Gemini/Claude.ai/Grok/Perplexity, кворум 4/6) **не запущен**: кворум по этому ДР не набран. Внутренние ноги: GLM ответил (320 с, без веба, честно пометил), Mistral ответил (**выдумал номера PR**, таблица PR в его ответе = шум), Gemini 429 (квота до ~10.11), Grok таймаут 600 с, Codex-рельса таймаут пробы версии. Легло: `_scratch\memory-db-pilots\legs\`.
- Серверные Postgres+pgvector, Qdrant server, Redis, Neo4j/FalkorDB не гонялись (docker-демон не поднят). 
- Бэкенды нативной памяти OpenAI/Anthropic/Google не раскрыты.
- Нет публичного бенчмарка «одинаковый retrieval, разные хранилища»; LoCoMo/LongMemEval/BEAM сравнивают системы целиком. Это и есть свободная ниша для нашего вклада.
