import unittest

from src.retrieval import LexicalRetriever, fuse_rrf
from src.benchmark_retrieval import evidence_hit


def chunk(cid, text, start=0, page=1, chapter=6):
    return {"id": cid, "text": text, "source_id": "book", "source": "book.pdf", "page": page,
            "metadata": {"char_start": start, "char_end": start + len(text), "chapter": chapter}, "score": 1.0}


class RetrievalTests(unittest.TestCase):
    def test_evidence_requires_contiguous_same_page_and_all_conditions(self):
        a, b = chunk("a", "hello "), chunk("b", "world", 6)
        groups = [[{"source_id": "book", "page": 1, "evidence": "hello world"}]]
        self.assertTrue(evidence_hit([b, a], groups))
        self.assertFalse(evidence_hit([a, chunk("b", "world", 7)], groups))
        self.assertFalse(evidence_hit([a, chunk("b", "world", 6, page=2)], groups))
        self.assertFalse(evidence_hit([a], groups))
        groups[0].append({"source_id": "book", "page": 1, "evidence": "missing"})
        self.assertFalse(evidence_hit([a, b], groups))

    def test_rrf_uses_ranks_not_incompatible_scores(self):
        a, b, c = chunk("a", "alpha"), chunk("b", "beta"), chunk("c", "gamma")
        a["score"] = 100000
        result = fuse_rrf({"dense": [a, b], "tfidf": [b, c]})
        self.assertEqual(result[0]["id"], "b")
        self.assertEqual(result[0]["component_ranks"], {"dense": 2, "tfidf": 1})

    def test_lexical_filters_before_cutoff_and_returns_no_zero_match(self):
        index = LexicalRetriever([chunk("a", "memory", chapter=6), chunk("b", "memory recall", chapter=8)])
        self.assertEqual(index.search("memory", filters={"chapter": 8}, top_k=1)[0]["id"], "b")
        self.assertEqual(index.search("unfindabletoken"), [])

    def test_weighted_rrf_can_prioritize_dense_and_rejects_invalid_weights(self):
        a, b = chunk("a", "alpha"), chunk("b", "beta")
        rankings = {"dense": [a, b], "tfidf": [b, a]}
        result = fuse_rrf(rankings, weights={"dense": 0.8, "tfidf": 0.2})
        self.assertEqual(result[0]["id"], "a")
        self.assertAlmostEqual(result[0]["score"], 0.8/61 + 0.2/62)
        for weights in ({"dense": -1, "tfidf": 1}, {"dense": 0, "tfidf": 0},
                        {"dense": float('nan'), "tfidf": 1}, {"dense": 1}):
            with self.assertRaises(ValueError):
                fuse_rrf(rankings, weights=weights)
