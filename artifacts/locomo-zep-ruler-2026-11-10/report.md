## LoCoMo by Zep's ruler (getzep/zep-papers@4b7f26cc locomo_eval), N = 1540, K = 20

| System | Overall | Single-hop | Multi-hop | Open-domain | Temporal | Runs | Reader / Judge |
|---|---:|---:|---:|---:|---:|---:|---|
| Full context (no memory system) | 86.6 | 94.4 | 90.8 | 68.8 | 67.6 | 1 | gpt-6-sol / grok-4.20-0309-non-reasoning |
| Zep Cloud contexts (published by Zep) | 75.9 ± 0.4 | 80.5 ± 0.3 | 72.9 ± 0.6 | 63.5 ± 1.5 | 70.0 ± 0.3 | 3 | gpt-6-sol / grok-4.20-0309-non-reasoning |
| Mem0 OSS 2.2.1 (fact extraction) | 78.6 ± 0.2 | 83.8 ± 0.3 | 81.2 ± 0.8 | 63.9 ± 1.0 | 67.0 ± 0.4 | 3 | gpt-6-sol / grok-4.20-0309-non-reasoning |
| Our time-stamped turn log (dense E5) | 72.1 ± 0.2 | 84.5 ± 0.3 | 71.0 ± 1.2 | 58.3 ± 0.8 | 44.9 ± 0.7 | 3 | gpt-6-sol / grok-4.20-0309-non-reasoning |
| Graphiti OSS 0.31.2 (Zep's open core, no cross-encoder) | 42.2 ± 0.4 | 45.6 ± 0.6 | 51.1 ± 1.0 | 46.5 ± 1.8 | 24.4 ± 1.6 | 3 | gpt-6-sol / grok-4.20-0309-non-reasoning |
| Zep's published answers, re-judged by our judge | 71.7 | 76.3 | 70.2 | 57.3 | 65.1 | 1 | gpt-4o-mini@zep-published / grok-4.20-0309-non-reasoning |
| Zep's published answers, Zep's own judge | 75.1 | 79.8 | 74.1 | 67.7 | 66.0 | 1 | gpt-4o-mini@zep-published / gpt-4o-mini@zep-published |

Reference numbers from Zep's post (their models gpt-4o-mini / gpt-4o-mini): Zep Cloud 75.14, full context 72.9, Mem0 Graph 68.44 and Mem0 66.88 (the two Mem0 numbers are quoted by Zep from Mem0's paper).

Judge calibration on Zep's 1540 published answers: our judge CORRECT 1104 (71.7%), Zep's judge CORRECT 1157 (75.1%), agreement 1445/1540 = 93.8%, Cohen's kappa 0.84.
