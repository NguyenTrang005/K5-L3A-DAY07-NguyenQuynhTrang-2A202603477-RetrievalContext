import unittest

from src.context import ContextBuilder
from src.benchmark_retrieval import evidence_hit
from test_retrieval import chunk


class ContextTests(unittest.TestCase):
    def test_neighbors_restore_boundary_evidence_without_changing_seeds(self):
        a, b = chunk("a", "hello "), chunk("b", "world", 6)
        builder = ContextBuilder([a, b])
        seeds = [b]
        base = builder.build(seeds)
        expanded = builder.build(seeds, neighbors=True)
        gold = [[{"source_id": "book", "page": 1, "evidence": "hello world"}]]
        self.assertFalse(evidence_hit(base["selected_chunks"], gold))
        self.assertTrue(evidence_hit(expanded["selected_chunks"], gold))
        self.assertEqual(seeds, [b])

    def test_no_cross_page_gap_or_recursive_neighbors_and_no_duplicates(self):
        chunks = [chunk("a", "aa", 0), chunk("b", "bb", 2), chunk("c", "cc", 4),
                  chunk("d", "dd", 6), chunk("e", "ee", 10), chunk("f", "ff", 0, page=2)]
        builder = ContextBuilder(chunks)
        one = builder.build([chunks[1]], neighbors=True)
        self.assertEqual(set(one["context_ids"]), {"a", "b", "c"})
        multi = builder.build(chunks[:3], neighbors=True)
        self.assertEqual(len(multi["context_ids"]), len(set(multi["context_ids"])))
        self.assertNotIn("e", multi["context_ids"])
        self.assertNotIn("f", multi["context_ids"])

    def test_budget_includes_headers_and_preserves_seeds_first(self):
        a, b = chunk("a", "hello "), chunk("b", "world", 6)
        builder = ContextBuilder([a, b])
        seed_only = builder.build([b])
        packed = builder.build([b], neighbors=True, budget=seed_only["context_chars"])
        self.assertEqual(packed["context_ids"], ["b"])
        self.assertLessEqual(packed["context_chars"], seed_only["context_chars"])
        self.assertEqual(packed["decisions"][-1]["skip_reason"], "budget")
        self.assertEqual(builder.build([b], budget=1)["context"], "")

    def test_metadata_filter_applies_to_neighbors(self):
        a, b = chunk("a", "aa", chapter=8), chunk("b", "bb", 2, chapter=6)
        result = ContextBuilder([a, b]).build([b], neighbors=True, filters={"chapter": 6})
        self.assertEqual(result["context_ids"], ["b"])
