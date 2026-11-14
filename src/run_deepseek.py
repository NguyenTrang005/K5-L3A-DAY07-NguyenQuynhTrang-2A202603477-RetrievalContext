"""Run native DeepSeek agent; held-out test requires the pre-test selection lock."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from .context import ContextBuilder
from .day6_retriever import Day6Retriever, ROOT
from .deepseek_agent import DeepSeekClient, run_agent
from .selection import load_selection, file_hash


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--dev-ids", nargs="+")
    parser.add_argument("--check-only", action="store_true", help="Check files, configuration and DB without loading model or calling API")
    parser.add_argument("--cache-folder")
    parser.add_argument("--neighbors", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or ROOT / ("results/agent-test-baseline-v1" if args.split == "test" else "results/agent-smoke-dev-v1")
    lock = load_selection() if args.split == "test" else None
    if lock and (args.dev_ids is not None or args.neighbors != lock["agent"]["neighbors"]):
        parser.error("Test must run all cases using locked context policy; no dev-ids override")
    if args.output.exists() and not args.check_only:
        parser.error("Choose a new output directory to preserve prior runs")
    case_path = ROOT / "benchmark" / f"{args.split}_cases.json"
    manifest = json.loads((ROOT / "benchmark/manifest.json").read_text(encoding="utf-8"))
    if file_hash(case_path) != manifest["files_sha256"][case_path.name]:
        raise ValueError("Cases checksum mismatch")
    cases = {c["id"]: c for c in json.loads(case_path.read_text(encoding="utf-8"))}
    args.dev_ids = list(cases) if args.split == "test" else (args.dev_ids or ["d7_dev_02", "d7_dev_16"])
    if len(set(args.dev_ids)) != len(args.dev_ids) or not set(args.dev_ids) <= set(cases):
        parser.error("Only existing dev IDs are allowed")
    load_dotenv(ROOT / ".env")
    for key in ("DEEPSEEK_API_KEY", "DATABASE_URL"):
        if not os.getenv(key):
            parser.error(f"Missing {key} in .env")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    if base_url.rstrip("/") not in ("https://api.deepseek.com", "https://api.deepseek.com/v1"):
        parser.error("Use official DeepSeek API base URL")
    strategy = os.getenv("DAY6_STRATEGY", "A")
    if lock and (model != lock["agent"]["model"] or base_url.rstrip("/") != lock["agent"]["base_url"].rstrip("/")):
        parser.error("DeepSeek model/base URL differs from selection lock")
    if strategy != "A":
        parser.error("Use frozen strategy A")
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=5) as conn:
        conn.read_only = True
        rows = conn.execute("SELECT chunk_id,text,document_id,source,page,metadata FROM lab_chunks WHERE strategy=%s ORDER BY chunk_id", (strategy,)).fetchall()
    chunks = [dict(zip(("id", "text", "source_id", "source", "page", "metadata"), r)) for r in rows]
    corpus_hash = hashlib.sha256(json.dumps(chunks, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    reference = json.loads((ROOT / "results/retrieval-dev-v1/summary.json").read_text(encoding="utf-8"))
    if corpus_hash != reference["corpus_sha256"]:
        raise ValueError("Database corpus differs from frozen retrieval corpus")
    if lock and corpus_hash != lock["corpus_sha256"]:
        raise ValueError("Corpus differs from selection lock")
    if args.check_only:
        print(f"Checks OK | split={args.split} | cases={len(args.dev_ids)} | chunks={len(chunks)} | model={model} | neighbors={args.neighbors} | API calls=0")
        return
    retriever = Day6Retriever(os.environ["DATABASE_URL"], strategy, args.cache_folder)
    builder = ContextBuilder(chunks)
    client = DeepSeekClient(os.environ["DEEPSEEK_API_KEY"], model, base_url)
    args.output.mkdir(parents=True)
    runs = []
    for qid in args.dev_ids:
        case = cases[qid]
        trace = run_agent(case["question"], client, retriever, builder, filters=case.get("filter"), neighbors=args.neighbors)
        trace.update(query_id=qid, split=args.split)
        runs.append(trace)
        (args.output / "traces.json").write_text(json.dumps(runs, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(json.dumps({k: trace[k] for k in ("query_id", "status", "answer", "citations", "search_count", "model_call_count", "usage")}, ensure_ascii=False), flush=True)
        if trace["status"] == "error":
            print("Agent error:", trace.get("error", trace["error_type"]), flush=True)
            if args.split == "dev":
                break
    config = {"run_at_utc": datetime.now(timezone.utc).isoformat(), "model": model,
              "base_url": base_url, "neighbors": args.neighbors, "budget_chars": 6000,
              "max_searches": 2, "top_k": 3, "retriever": "dense", "strategy": strategy,
              "corpus_sha256": corpus_hash, "cases_sha256": hashlib.sha256(case_path.read_bytes()).hexdigest(),
              "thinking": "disabled", "temperature": 0, "max_tokens": 1200,
              "split": args.split,
              "selection_lock_sha256": file_hash(ROOT / "benchmark/selection_lock.json") if lock else None,
              "roles": ["baseline", "selected"] if lock else ["dev_experiment"],
              "note": "No gold supplied to agent; semantic grading done separately. Selected configuration equals baseline, so one test run represents both roles. Rewritten queries logged separately from original-query retrieval benchmark."}
    (args.output / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
