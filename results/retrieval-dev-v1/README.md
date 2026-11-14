# Retrieval dev v1

Original queries; strategy A; identical provided chapter filters. Automatic evidence labels.

| Method | Hit@1 | Evidence Hit@3 | Median ms | Errors |
|---|---:|---:|---:|---:|
| dense | 2/15 (13.3%) | 9/15 (60.0%) | 32.50 | 0 |
| tfidf | 2/15 (13.3%) | 2/15 (13.3%) | 0.19 | 0 |
| hybrid | 3/15 (20.0%) | 8/15 (53.3%) | 34.00 | 0 |

Automatic exact normalized evidence matching; equivalent evidence needs manual review. Errors count as misses for answerable retrieval. No context/agent/abstention metrics. CPU/electricity excluded from cost. Dense database must remain unchanged throughout run. Timing includes embedding/DB per query and cold/warm effects; hybrid independently reruns both components.

Two unanswerable cases are retrieved but excluded from hit metric denominators; retrieval alone cannot measure abstention.
