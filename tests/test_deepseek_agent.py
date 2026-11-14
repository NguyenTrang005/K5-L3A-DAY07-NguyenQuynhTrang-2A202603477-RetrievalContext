import json
import unittest

from src.context import ContextBuilder
from src.deepseek_agent import run_agent


CID = "a" * 64
CHUNK = {"id": CID, "source_id": "book", "source": "book.pdf", "page": 1,
         "text": "Evidence text", "score": 1, "metadata": {"char_start": 0, "char_end": 13}}


class Client:
    model = "mock-not-benchmark"

    def __init__(self, final):
        self.final = final
        self.n = 0

    def complete(self, messages, tools, tool_choice):
        name, arguments = ("search_documents", {"query": "search query"}) if self.n == 0 else ("finish_answer", self.final)
        self.n += 1
        return {"choices": [{"message": {"role": "assistant", "content": None,
            "tool_calls": [{"id": str(self.n), "type": "function", "function": {
                "name": name, "arguments": json.dumps(arguments)}}]}, "finish_reason": "tool_calls"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}


class Retriever:
    def search(self, query, *, filters, top_k):
        return [CHUNK]


class DeepSeekAgentTests(unittest.TestCase):
    def run_case(self, final, retriever=None):
        return run_agent("question", Client(final), retriever or Retriever(), ContextBuilder([CHUNK]))

    def test_native_tools_grounded_answer_and_usage(self):
        run = self.run_case({"status": "answered", "answer": f"Answer [{CID}]", "citations": [CID]})
        self.assertEqual(run["status"], "answered")
        self.assertEqual(run["search_count"], 1)
        self.assertEqual(run["usage"]["total_tokens"], 30)
        self.assertEqual(run["events"][0]["query"], "search query")

    def test_abstention_is_supported_without_fake_citations(self):
        run = self.run_case({"status": "abstain", "answer": "Không đủ bằng chứng.", "citations": []})
        self.assertEqual(run["status"], "abstain")

    def test_invalid_citation_and_retrieval_failure_are_errors(self):
        run = self.run_case({"status": "answered", "answer": "Answer", "citations": ["missing"]})
        self.assertEqual(run["status"], "error")
        class Broken:
            def search(self, *args, **kwargs):
                raise RuntimeError("secret-database-value")
        run = self.run_case({}, Broken())
        self.assertEqual(run["status"], "error")
        self.assertNotIn("secret-database-value", json.dumps(run))
