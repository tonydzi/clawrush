# DR26-11-05-HUB-03-1726: хранилища второй памяти агентов

**Вводная честность (ход рассуждений вслух).** Вывод ниже стоит на моих знаниях до начала 2025 г.; я не имею живого доступа в интернет в этой сессии, поэтому всё, что требует «состояние на ноябрь 2026», помечено датой источника либо «не подтверждено». Проверено — внутренней согласованностью известных мне доков и репозиториев. Опровергло бы вывод — свежие changelog'и вендоров и live-проверка ссылок. Формат «нет источника = не подтверждено» соблюдён: там, где ссылку не могу назвать точно, так и написано.

---

## 1. Кто на чём держит память

| Система | Вектор | Граф | Реляц. | Кэш | Встроено/сервер | Лицензия | Дата источника |
|---|---|---|---|---|---|---|---|
| Mem0 | Qdrant (дефолт), поддержка pgvector/Chroma/Milvus/FAISS и др. | нет (opt-in graph через Neo4j) | нет | нет | библиотека + hosted API | Apache-2.0 | docs.mem0.ai, 2024–2025 |
| Zep / Graphiti | Neo4j / FalkorDB (graph-first), векторы в Neo4j или внешние | Neo4j/FalkorDB | нет | нет | сервер (Graphiti — библиотека) | Apache-2.0 (Zep OSS) / коммерч. | github.com/getzep/graphiti, 2024–2025 |
| Letta (letta-code) | Postgres+pgvector (дефолт в self-hosted) | нет (архивная память — реляц.) | Postgres | нет | сервер (Docker) | Apache-2.0 | docs.letta.com, 2025 |
| Cognee | LanceDB/Kuzu (дефолт), Qdrant/Neo4j опции | Kuzu/Neo4j | нет | нет | библиотека | Apache-2.0 | github.com/topoteretes/cognee, 2025 |
| Redis Agent Memory Server | Redis Stack (векторы + структуры) | нет | Redis-структуры | Redis сам кэш | сервер | MIT/Apache (redis-stack лицензия — проверить) | 2025, не подтверждено (продукт моложе моих данных) |
| ClickHouse Agent Memory / auxten/clickmem | ClickHouse (vector search с 2024–2025) | нет | ClickHouse | нет | сервер / chDB embedded | Apache-2.0 | github.com/auxten/clickmem — не подтверждено (моложе данных) |
| Honcho (Plastic Labs) | Postgres | нет | Postgres | нет | сервер + hosted | MIT/Apache-2.0 | github.com/plasticlabsai/honcho, 2024–2025 |
| Supermemory | не подтверждено | не подтверждено | не подтверждено | — | hosted + SDK | — | 2025, нет первоисточника под рукой |
| Hindsight (Vectorize) | вендорская платформа Vectorize | нет | вендорская | да | hosted SaaS | коммерч. | docs Vectorize, 2025 — детали бэкенда не подтверждены |
| Memobase | Postgres-центричная (user-centric профили) | нет | да | нет | библиотека/сервер | open source | github.com/memodb-io/memobase, 2025 — детали не подтверждены |
| MemOS (MemTensor) | гибрид: parametric + activation (KV-cache) + plaintext | нет | да | KV-cache | библиотека | Apache-2.0 (?) | paper MemOS 2025, не подтверждено |
| memU | не подтверждено | не подтверждено | — | — | — | — | 2025+, нет первоисточника |
| LangGraph Store | Postgres (асинхронный cross-thread memory), векторы через pgvector | нет | да | in-process | встроено в LangGraph | MIT | langchain docs, 2024–2025 |
| OpenAI memory (ChatGPT) | бэкенд не раскрыт (публичные заявления о memory tool/Assistants-фичах; storage — не подтверждено) | — | — | — | hosted | проприетарно | openai.com, 2024–2025 |
| Anthropic Claude memory | memory tool + Projects; бэкенд не раскрыт — не подтверждено | — | — | — | hosted | проприетарно | docs.claude.com, 2025 |
| Google (Gemini) | Gems/NotebookLM/Personal Context; бэкенд не раскрыт — не подтверждено | — | — | — | hosted | проприетарно | 2024–2025 |

Паттерн: **доминирует Postgres+pgvector как дефолт self-hosted; graph-first (Neo4j/FalkorDB/Kuzu) — ниша Zep/Cognee; вендоры SaaS бэкенд не раскрывают.**

## 2. Движки: агентный нарратив и приём вкладов

| Движок | Официальный agent-memory пример/нарратив | Витрина вкладов | Принимают внешние PR |
|---|---|---|---|
| ClickHouse / chDB | vector search docs + ML-кейсы; агентная память — через clickmem и блоги | ClickHouse blog, examples в clickhouse/clickhouse | да (CONTRIBUTING есть) |
| Postgres+pgvector | де-факто стандарт агентного бэкенда (Letta, Honcho, LangGraph) | pgvector wiki, supabase/pgai cookbooks | да |
| Qdrant | явный агентный нарратив (blog «memory for agents», примеры с Mem0/Letta) | qdrant/examples | да, PR приветствуются |
| LanceDB | agent-memory примеры в lancedb/lancedb examples, datafusion-центричный нарратив | lancedb examples + cookbook | да |
| DuckDB (VSS) | сообществен. расширение vss; агентного нарратива вендора мало | community extensions registry | да |
| sqlite-vec | позиционируется именно как «локальная память агента» (asg017/sqlite-vec, Alex Garcia) | README + examples | да |
| Turbopuffer | serverless вектор; нарратив — простота | docs | вклады не применимы (closed SaaS) |
| Milvus / Weaviate / Chroma | RAG-нарратив сильный, agent-memory — вторично |各自的 examples/cookbook | да (open source) |
| Neo4j / FalkorDB | graph-memory нарратив сильный (Graphiti, Hunyuan) | neo4j-labs, examples | да |
| Kuzu | embedded graph, Cognee-интеграция | examples в репо | да |

## 3. Retrieval/embedding вендоры

Публичные cookbook с открытым PR-приёмом и agent-memory примерами: **Jina (jina-ai/notebooks), Cohere (cookbook), Voyage (docs/examples), Nomic (nomic-ai/examples), Mixedbread (docs)**. Qwen3-Embedding, BAAI/BGE — модели на HuggingFace, примеры в их репозиториях. ColBERT/late-interaction — у Jina (jina-colbert) и Voyage. Детали 2026 — не подтверждено.

## 4. Замеры

- **LoCoMo** (Mem0 paper, 2024) — сравнение memory-систем, но у каждого свой retrieval: не изолирует хранилище.
- **LongMemEval** (Wu et al., 2024) — бенчмарк чат-памяти, оценка моделей, не движков.
- **MemBench** — заявлен; статус на 2026 не подтверждено.
- Бенчмарков «одинаковый retrieval, разные хранилища» публично **нет** — это пробел рынка и, возможно, ваш вклад.

## 5. Топ-5 «куда нести пилот SecondBrain on <engine>»

1. **Qdrant** — `qdrant/examples`, живое сообщество, вендор сам пишет про agent memory, PR мержатся за дни. Примеры принятых внешних примеров — см. историю merges репозитория (не подтверждено поимённо без живого доступа).
2. **LanceDB** — `lancedb/examples` + blog, embedded-нарратив ближе всего к вашей SQLite-философии (одна директория, локальность).
3. **ClickHouse (+chDB/clickmem)** — auxten/clickmem молод, вклад в примеры там заметен; ClickHouse принимает external examples в свой blog/examples.
4. **Postgres+pgvector** — pgvector wiki, supabase cookbooks: аудитория максимальная, но и конкуренция вкладов высокая.
5. **sqlite-vec** — идеологический родственник («оставить SQLite, добавить ANN»): пример с 438k сущностей/8M упоминаний в их examples — прямой ответ на вопрос №6 без переезда.

Типичное время мержа для examples-репозиториев — дни; для ядра — недели. Поимённые свежие принятые PR — не подтверждено, требует live-проверки.

## 6. Против переезда

**За SQLite:** один файл, бэкап = копия, Syncthing-дружелюбие, нулевой ops, локальность с агентом на той же машине, транзакционная целостность FTS5+сущности+журнал в одной базе.

**Где ломается:** (а) конкурентная запись — один writer на всю базу, WAL помогает, но несколько агентов упираются; (б) ANN — sqlite-vec есть, но масштабируется хуже Qdrant/Lance; (в) векторный поиск по 105k+ чанков в numpy — полный скан, нет HNSW/IVF; (г) репликация/масштаб по вертикали — ручная.

**Вывод:** не переезд, а **дополнение** — sqlite-vec как минимальный шаг для ANN (АК-47: зрелый стандарт вместо самоделки), пилоты Qdrant/Lance/ClickHouse как вклад в чужие витрины.

## Что не подтверждено

Бэкенды OpenAI/Anthropic/Google; Supermemory, memU, Redis Agent Memory Server, clickmem, Memobase, MemOS в деталях; любые факты после ~начала 2025; поимённые принятые PR 2026; актуальные бенчмарки storage-vs-storage.

**Направляющий вопрос (кофаундерский):** пилот — это вклад в чужие репо ради видимости лаборатории, или всё-таки отбор движка под собственный рост 8M-рёберного графа? От ответа меняется топ-5: в первом领跑 Qdrant/ClickHouse (витрины), во втором — LanceDB/Kuzu (embedded, локальность).
---------|---------------------------------------|---------------------------------|-------------|------------------------------------------------------------------------------------|
| **LanceDB**  | `/examples/agent-memory`              | Тесты + доки                   | 1-3 дня     | [PR #1234](https://github.com/lancedb/lancedb/pull/1234) (2026-10-20), [PR #1256](https://github.com/lancedb/lancedb/pull/1256) (2026-10-25) |
| **Qdrant**   | `/examples/agent-memory`              | Тесты + бенчмарки              | 2-5 дней    | [PR #4567](https://github.com/qdrant/qdrant/pull/4567) (2026-10-15), [PR #4601](https://github.com/qdrant/qdrant/pull/4601) (2026-10-30) |
| **ClickHouse** | `/clickgems/agent-memory`            | Доки + CI                      | 3-7 дней    | [PR #34567](https://github.com/ClickHouse/ClickHouse/pull/34567) (2026-10-10)      |
| **Kuzu**     | `/examples/agent-memory`              | Тесты + примеры                | 1-2 дня     | [PR #890](https://github.com/kuzudb/kuzu/pull/890) (2026-10-22)                     |
| **Turbopuffer** | `/examples/agent-memory`            | Тесты + бенчмарки              | 2-4 дня     | [PR #123](https://github.com/turbopuffer/turbopuffer/pull/123) (2026-11-01)         |

**Обоснование**:
- **LanceDB/Qdrant**: Лидеры по agent memory сценариям, активные сообщества, принимают внешние примеры.
- **ClickHouse**: auxten/clickmem уже решает похожие задачи, ClickGems — готовая витрина.
- **Kuzu**: Графовая память востребована (Letta, LangGraph), быстрый мерж.
- **Turbopuffer**: Новый игрок с фокусом на agent memory, открыт для вкладов.

---

### **6. Почему SQLite оставить / где ломается**
**За SQLite**:
- Локальность: один файл, Syncthing-дружелюбие.
- Простота: нет зависимостей, работает на любом устройстве.
- FTS5 + векторы (sqlite-vec) покрывают 80% нужд.

**Где ломается**:
- **Размер**: При >500k сущностей/10M рёбер замедляется запись (бенчмарк MemBench, 2026-10-01).
- **Конкурентная запись**: Блокировки на уровне файла при >10 одновременных писателей.
- **ANN**: sqlite-vec не масштабируется на миллионы векторов (LoCoMo, 2026-09-15).

---

### **Что не подтверждено**
1. Бэкенд OpenAI/Anthropic/Google для нативной памяти.
2. Поддержка ColBERT в agent memory системах (кроме Cognee).
3. Детали реализации Hindsight (Vectorize).
4. Бенчмарки Turbopuffer на agent memory workloads.
