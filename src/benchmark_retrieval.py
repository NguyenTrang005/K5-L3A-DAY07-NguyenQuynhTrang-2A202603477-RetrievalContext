"""Original-query retrieval comparison; test requires a pre-test selection lock."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import statistics
import time

import psycopg
from dotenv import load_dotenv

from .day6_retriever import Day6Retriever, MODEL, REVISION, ROOT
from .retrieval import LexicalRetriever, HybridRetriever
from .selection import load_selection


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def evidence_hit(results, groups):
    """Join only contiguous/overlapping chunks from the same source and page."""
    pages = defaultdict(list)
    for chunk in results:
        pages[(chunk["source_id"], chunk["page"])].append(chunk)
    blocks = defaultdict(list)
    for key, chunks in pages.items():
        current, end = "", None
        for chunk in sorted(chunks, key=lambda c: (c["metadata"]["char_start"], c["id"])):
            start, stop = chunk["metadata"]["char_start"], chunk["metadata"]["char_end"]
            if end is None or start > end:
                if current:
                    blocks[key].append(normalize(current))
                current, end = chunk["text"], stop
            elif stop > end:
                current += chunk["text"][end - start:]
                end = stop
        if current:
            blocks[key].append(normalize(current))
    return any(all(any(normalize(e["evidence"]) in text for text in blocks[(e["source_id"], e["page"])])
                       for e in group) for group in groups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", nargs="+", choices=("dense", "tfidf", "hybrid"), default=["dense", "tfidf", "hybrid"])
    parser.add_argument("--cache-folder")
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--dense-weight", type=float, default=1.0)
    parser.add_argument("--lexical-weight", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or ROOT / f"results/retrieval-{args.split}-v1"
    lock = load_selection() if args.split == "test" else None
    weights = {"dense": args.dense_weight, "tfidf": args.lexical_weight}
    if any(not math.isfinite(w) or w < 0 for w in weights.values()) or not any(weights.values()):
        parser.error("Weights must be finite, nonnegative, with positive total")
    if lock and (weights != lock["supplementary_retrieval"]["hybrid_weights"] or args.methods != lock["supplementary_retrieval"]["methods"]):
        parser.error("Test retrieval methods and weights must match selection lock")
    if args.output.exists():
        parser.error("Output already exists; choose a new --output to preserve previous runs")
    bench = ROOT / "benchmark"
    manifest = json.loads((bench / "manifest.json").read_text(encoding="utf-8"))
    # Only opens the requested split, after validating lock for test.
    for name in (f"{args.split}_cases.json", f"{args.split}_gold.json"):
        if hashlib.sha256((bench / name).read_bytes()).hexdigest() != manifest["files_sha256"][name]:
            raise ValueError(f"Benchmark checksum changed: {name}")
    cases = json.loads((bench / f"{args.split}_cases.json").read_text(encoding="utf-8"))
    gold = {g["id"]: g for g in json.loads((bench / f"{args.split}_gold.json").read_text(encoding="utf-8"))}
    load_dotenv(ROOT / ".env")
    url = os.environ["DATABASE_URL"]
    strategy = os.getenv("DAY6_STRATEGY", "A")
    if strategy != "A":
        parser.error("This benchmark is frozen on strategy A")
    with psycopg.connect(url, connect_timeout=5) as conn:
        conn.read_only = True
        rows = conn.execute("SELECT chunk_id,text,document_id,source,page,metadata FROM lab_chunks WHERE strategy=%s ORDER BY chunk_id", (strategy,)).fetchall()
    chunks = [dict(zip(("id", "text", "source_id", "source", "page", "metadata"), r)) for r in rows]
    if len(chunks) != 228:
        raise ValueError("Expected 228 strategy A chunks")
    corpus_hash = hashlib.sha256(json.dumps(chunks, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    if lock and corpus_hash != lock["corpus_sha256"]:
        raise ValueError("Corpus differs from pre-test lock")
    index_start = time.perf_counter()
    lexical = LexicalRetriever(chunks)
    lexical_seconds = time.perf_counter() - index_start
    retrievers = {"tfidf": lexical}
    model_seconds = 0
    if set(args.methods) & {"dense", "hybrid"}:
        started = time.perf_counter()
        dense = Day6Retriever(url, strategy, args.cache_folder)
        model_seconds = time.perf_counter() - started
        retrievers.update(dense=dense, hybrid=HybridRetriever(dense, lexical, weights=weights))
    args.output.mkdir(parents=True)
    traces, summaries = [], []
    for method in args.methods:
        runs = []
        for case in cases:
            started = time.perf_counter()
            trace = {"query_id": case["id"], "method": method, "query": case["question"],
                     "filter": case.get("filter"), "split": args.split, "query_transformation": None}
            if method == "hybrid":
                trace["fusion_weights"] = weights
            try:
                results = retrievers[method].search(case["question"], filters=case.get("filter"), top_k=3)
                trace.update(status="ok", results=[{**c, "rank": i} for i, c in enumerate(results, 1)])
            except Exception as error:
                trace.update(status="error", results=[], error_type=type(error).__name__)
            trace["elapsed_ms"] = (time.perf_counter() - started) * 1000
            label = gold[case["id"]]
            trace["answerable"] = label["answerable"]
            if label["answerable"]:
                trace["hit1"] = evidence_hit(trace["results"][:1], label["evidence_groups"])
                trace["hit3"] = evidence_hit(trace["results"], label["evidence_groups"])
            runs.append(trace)
            traces.append(trace)
        answerable = [t for t in runs if t["answerable"]]
        summary = {"method": method, "queries": len(runs), "answerable": len(answerable),
                   "errors": sum(t["status"] == "error" for t in runs),
                   "hit1": {"n": sum(t["hit1"] for t in answerable), "N": len(answerable)},
                   "hit3": {"n": sum(t["hit3"] for t in answerable), "N": len(answerable)},
                   "median_ms": statistics.median(t["elapsed_ms"] for t in runs),
                   "service_cost_usd": 0}
        for metric in ("hit1", "hit3"):
            summary[metric]["rate"] = summary[metric]["n"] / summary[metric]["N"]
        summaries.append(summary)
        print(json.dumps(summary, ensure_ascii=False), flush=True)
        (args.output / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {"run_at_utc": datetime.now(timezone.utc).isoformat(), "split": args.split, "strategy": "A",
              "benchmark_version": manifest["version"], "original_queries": True,
              "filter_policy": "Apply user-provided case filter equally to all methods",
              "corpus_sha256": hashlib.sha256(json.dumps(chunks, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
              "model": MODEL, "revision": REVISION, "dimensions": 384, "normalized": True,
              "max_seq_length": 512, "lexical": "Starter TF-IDF; Unicode word tokens; raw TF; smoothed IDF; cosine; no translation",
              "hybrid": {"fusion": "weighted RRF", "weights": weights, "rrf_k": 60, "candidates_per_retriever": 20},
              "setup_seconds": {"lexical_index": lexical_seconds, "model_load": model_seconds},
              "limitations": "Automatic exact normalized evidence matching; equivalent evidence needs manual review. Errors count as misses for answerable retrieval. No context/agent/abstention metrics. CPU/electricity excluded from cost. Dense database must remain unchanged throughout run. Timing includes embedding/DB per query and cold/warm effects; hybrid independently reruns both components.",
              "summaries": summaries}
    (args.output / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# Retrieval {args.split}", "", "Original queries; strategy A; identical provided chapter filters. Automatic evidence labels.", "", f"Hybrid RRF weights: dense={args.dense_weight}, TF-IDF={args.lexical_weight}; k=60; 20 candidates per retriever.", "", "| Method | Hit@1 | Evidence Hit@3 | Median ms | Errors |", "|---|---:|---:|---:|---:|"]
    for s in summaries:
        lines.append(f"| {s['method']} | {s['hit1']['n']}/{s['hit1']['N']} ({s['hit1']['rate']:.1%}) | {s['hit3']['n']}/{s['hit3']['N']} ({s['hit3']['rate']:.1%}) | {s['median_ms']:.2f} | {s['errors']} |")
    lines += ["", report["limitations"], "", "Two unanswerable cases are retrieved but excluded from hit metric denominators; retrieval alone cannot measure abstention."]
    (args.output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
