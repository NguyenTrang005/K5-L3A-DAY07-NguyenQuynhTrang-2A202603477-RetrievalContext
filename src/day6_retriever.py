"""Read-only Day 6 adapter. Run from the Day 7 root: python -m src.day6_retriever.

Uses the embedding and SQL search settings from the student's Day 6
starter/src/{embeddings,store}.py. No database writes or re-ingestion.
"""
import argparse
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

ROOT = Path(__file__).resolve().parents[1]
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
REVISION = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"


class Day6Retriever:
    def __init__(self, database_url, strategy="A", cache_folder=None):
        from sentence_transformers import SentenceTransformer

        self.database_url = database_url
        self.strategy = strategy
        self.model = SentenceTransformer(
            MODEL, revision=REVISION, device="cpu", cache_folder=cache_folder
        )
        self.model.max_seq_length = 512
        if self.model.get_sentence_embedding_dimension() != 384:
            raise ValueError("Day 6 requires 384-dimensional embeddings")

    def search(self, query, *, filters=None, top_k=3):
        if not query.strip() or type(top_k) is not int or top_k < 1:
            raise ValueError("Require a nonempty query and positive integer top_k")
        if filters and (set(filters) != {"chapter"} or type(filters["chapter"]) is not int):
            raise ValueError("Only an integer chapter filter is supported")
        vector = self.model.encode(query, normalize_embeddings=True).tolist()
        vector_text = "[" + ",".join(str(float(x)) for x in vector) + "]"
        with psycopg.connect(self.database_url, connect_timeout=5) as conn:
            conn.read_only = True
            rows = conn.execute(
                """SELECT chunk_id,text,document_id,source,page,metadata,
                          1-(embedding <=> %s::vector) AS score
                   FROM lab_chunks
                   WHERE strategy=%s AND metadata @> %s
                   ORDER BY embedding <=> %s::vector,chunk_id LIMIT %s""",
                (vector_text, self.strategy, Jsonb(filters or {}), vector_text, top_k),
            ).fetchall()
        keys = ("id", "text", "source_id", "source", "page", "metadata", "score")
        return [dict(zip(keys, row)) for row in rows]


def main():
    parser = argparse.ArgumentParser(description="Check Day 6 connection and dense retrieval")
    parser.add_argument("--check-only", action="store_true", help="Check DB without loading model")
    parser.add_argument("--query", default="What is the role of experience in learning?")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--cache-folder", help="Optional path to Day 6 starter/.model_cache")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    url = os.getenv("DATABASE_URL")
    if not url:
        parser.error("Set DATABASE_URL in Day 7 .env using your Day 6 configuration")
    strategy = os.getenv("DAY6_STRATEGY", "A")
    with psycopg.connect(url, connect_timeout=5) as conn:
        conn.read_only = True
        count = conn.execute(
            "SELECT count(*) FROM lab_chunks WHERE strategy=%s", (strategy,)
        ).fetchone()[0]
    print(f"Day 6 connection OK | strategy={strategy} | chunks={count}")
    if count == 0:
        raise RuntimeError("No chunks for selected strategy; check the Day 6 database")
    if args.check_only:
        return
    retriever = Day6Retriever(url, strategy, args.cache_folder)
    results = retriever.search(args.query, top_k=args.top_k)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
