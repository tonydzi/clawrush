# memory-db pilots · N=20000 · dim=768 · queries=200 · 2026-11-05T22:27:50

| engine | ok | ingest_s | index_s | q_p50_ms | q_p95_ms | recall@10 | filtered_recall@10 | update_ok | delete_ok | restart_same | disk_mb | error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | True | 24.98 | 13.8 | 1.21 | 2.18 | 0.995 | 0.998 | True | True | True | 342.2 |  |
