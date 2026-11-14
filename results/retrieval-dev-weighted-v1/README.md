# Retrieval dev

Original queries; strategy A; identical provided chapter filters. Automatic evidence labels.

Hybrid RRF weights: dense=0.8, TF-IDF=0.2; k=60; 20 candidates per retriever.

| Method | Hit@1 | Evidence Hit@3 | Median ms | Errors |
|---|---:|---:|---:|---:|
| dense | 2/15 (13.3%) | 9/15 (60.0%) | 32.06 | 0 |
| tfidf | 2/15 (13.3%) | 2/15 (13.3%) | 0.15 | 0 |
| hybrid | 2/15 (13.3%) | 9/15 (60.0%) | 31.56 | 0 |

Automatic exact normalized evidence matching; equivalent evidence needs manual review. Errors count as misses for answerable retrieval. No context/agent/abstention metrics. CPU/electricity excluded from cost. Dense database must remain unchanged throughout run. Timing includes embedding/DB per query and cold/warm effects; hybrid independently reruns both components.

Two unanswerable cases are retrieved but excluded from hit metric denominators; retrieval alone cannot measure abstention.
