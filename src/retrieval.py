"""Lexical and reciprocal-rank fusion retrievers; no benchmark labels accepted."""
import math
from starter.baseline import TfidfIndex


class LexicalRetriever:
    def __init__(self, chunks):
        self.index = TfidfIndex(chunks)

    def search(self, query, *, filters=None, top_k=3):
        if not query.strip() or type(top_k) is not int or top_k < 1:
            raise ValueError("Require nonempty query and positive integer top_k")
        if filters and (set(filters) != {"chapter"} or type(filters["chapter"]) is not int):
            raise ValueError("Only integer chapter filters supported")
        # Rank all lexical matches, then filter BEFORE selecting the final top-k.
        rows = self.index.search(query, top_k=len(self.index.chunks))
        return [r for r in rows if all(r["metadata"].get(k) == v for k, v in (filters or {}).items())][:top_k]


def fuse_rrf(rankings, k=60, weights=None):
    if k <= 0:
        raise ValueError("RRF k must be positive")
    weights = dict.fromkeys(rankings, 1.0) if weights is None else weights
    if (set(weights) != set(rankings) or
            any(not math.isfinite(w) or w < 0 for w in weights.values()) or
            not any(weights.values())):
        raise ValueError("Require finite nonnegative weights for every retriever, with positive total")
    merged = {}
    for method, results in rankings.items():
        seen = set()
        for rank, chunk in enumerate(results, 1):
            if chunk["id"] in seen:
                raise ValueError("Duplicate ID in ranking")
            seen.add(chunk["id"])
            row = merged.setdefault(chunk["id"], {**chunk, "score": 0.0, "component_ranks": {}, "component_scores": {}})
            row["score"] += weights[method] / (k + rank)
            row["component_ranks"][method] = rank
            row["component_scores"][method] = chunk["score"]
    return sorted(merged.values(), key=lambda c: (-c["score"], c["id"]))


class HybridRetriever:
    def __init__(self, dense, lexical, candidates=20, rrf_k=60, weights=None):
        if candidates < 1:
            raise ValueError("Require positive candidate count")
        self.dense, self.lexical = dense, lexical
        self.candidates, self.rrf_k = candidates, rrf_k
        self.weights = weights

    def search(self, query, *, filters=None, top_k=3):
        if type(top_k) is not int or top_k < 1:
            raise ValueError("Require positive integer top_k")
        n = max(self.candidates, top_k)
        rankings = {"dense": self.dense.search(query, filters=filters, top_k=n),
                    "tfidf": self.lexical.search(query, filters=filters, top_k=n)}
        return fuse_rrf(rankings, self.rrf_k, self.weights)[:top_k]
