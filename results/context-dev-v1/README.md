# E2 — Context lân cận trên dev

Cùng budget 6000 ký tự; replay dense top-3 thật, không thay ranking. Context chưa gửi model.

| Context | Evidence coverage offline | Mean chars | Mean chunks | Median pack ms |
|---|---:|---:|---:|---:|
| dense_top3 | 9/15 (60.0%) | 2551.1 | 3.00 | 0.012 |
| dense_top3_neighbors | 10/15 (66.7%) | 5272.4 | 6.12 | 0.026 |

Gained: ['d7_dev_14']
Lost: []

Offline context coverage using saved real retrieval, not context sent to a model. No LLM token usage/billing, answer quality or abstention evaluation. Character budget includes citation headers and separators. Mean sizes over all 17 cases. Hit and context denominators use 15 answerable cases. Exact normalized evidence matching; equivalent evidence may need review. Pack timing excludes retrieval, model load and corpus setup.
