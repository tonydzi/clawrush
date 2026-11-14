# memory-db pilots · N=20000 · dim=768 · queries=200 · 2026-11-05T18:19:18

| engine | ok | ingest_s | index_s | q_p50_ms | q_p95_ms | recall@10 | filtered_recall@10 | update_ok | delete_ok | restart_same | disk_mb | error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sqlite_numpy | True | 3.3 | 0.0 | 11.29 | 31.83 | 0.9 | 0.908 | True | True | True | 66.4 |  |
