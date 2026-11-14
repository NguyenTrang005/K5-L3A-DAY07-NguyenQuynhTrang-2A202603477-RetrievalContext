# Retrieval test

Original queries; strategy A; identical provided chapter filters. Automatic evidence labels.

Hybrid RRF weights: dense=1.0, TF-IDF=1.0; k=60; 20 candidates per retriever.

| Method | Hit@1 | Evidence Hit@3 | Median ms | Errors |
|---|---:|---:|---:|---:|
| dense | 1/5 (20.0%) | 3/5 (60.0%) | 49.09 | 0 |
| tfidf | 1/5 (20.0%) | 4/5 (80.0%) | 0.24 | 0 |
| hybrid | 1/5 (20.0%) | 3/5 (60.0%) | 33.29 | 0 |

Automatic exact normalized evidence matching; equivalent evidence needs manual review. Errors count as misses for answerable retrieval. No context/agent/abstention metrics. CPU/electricity excluded from cost. Dense database must remain unchanged throughout run. Timing includes embedding/DB per query and cold/warm effects; hybrid independently reruns both components.

Two unanswerable cases are retrieved but excluded from hit metric denominators; retrieval alone cannot measure abstention.
