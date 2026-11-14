"""Paired dev-only context experiment on saved real dense retrieval."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import time

from .benchmark_retrieval import evidence_hit
from .context import ContextBuilder
from .day6_retriever import ROOT


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6-root", type=Path, required=True)
    parser.add_argument("--retrieval-run", type=Path, default=ROOT / "results/retrieval-dev-v1")
    parser.add_argument("--output", type=Path, default=ROOT / "results/context-dev-v1")
    parser.add_argument("--budget", type=int, default=6000)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a new output directory to preserve prior experiments")
    manifest = read(ROOT / "benchmark/manifest.json")
    for name in ("dev_cases.json", "dev_gold.json"):
        if hashlib.sha256((ROOT / "benchmark" / name).read_bytes()).hexdigest() != manifest["files_sha256"][name]:
            raise ValueError("Dev benchmark checksum mismatch")
    cases = read(ROOT / "benchmark/dev_cases.json")
    gold = {g["id"]: g for g in read(ROOT / "benchmark/dev_gold.json")}
    raw = [json.loads(s) for s in (args.day6_root / "data/processed/chunks_A.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    chunks = [{"id": c["chunk_id"], "text": c["text"], "source_id": c["document_id"],
               "source": c["source"], "page": c["page"], "metadata": c["metadata"]} for c in raw]
    chunks.sort(key=lambda c: c["id"])
    corpus_hash = hashlib.sha256(json.dumps(chunks, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    source_summary = read(args.retrieval_run / "summary.json")
    if corpus_hash != source_summary["corpus_sha256"]:
        raise ValueError("Local corpus differs from real dense retrieval corpus")
    source_traces = read(args.retrieval_run / "traces.json")
    dense = {t["query_id"]: t for t in source_traces if t["method"] == "dense"}
    if set(dense) != {c["id"] for c in cases}:
        raise ValueError("Dense dev cases do not match current benchmark")
    by_id = {c["id"]: c for c in chunks}
    builder = ContextBuilder(chunks)
    traces, summaries = [], []
    for method, neighbors in (("dense_top3", False), ("dense_top3_neighbors", True)):
        runs = []
        for case in cases:
            source = dense[case["id"]]
            if source["query"] != case["question"] or source["filter"] != case.get("filter"):
                raise ValueError("Saved query/filter mismatch")
            for c in source["results"]:
                if any(c[k] != by_id[c["id"]][k] for k in by_id[c["id"]]):
                    raise ValueError("Saved retrieved chunk differs from corpus")
            started = time.perf_counter()
            packed = builder.build(source["results"], budget=args.budget, neighbors=neighbors, filters=case.get("filter"))
            pack_ms = (time.perf_counter() - started) * 1000
            trace = {"query_id": case["id"], "split": "dev", "method": method,
                     "query": case["question"], "filter": case.get("filter"),
                     "status": source["status"], "ranking_ids": [r["id"] for r in source["results"]],
                     "budget_chars": args.budget, "pack_ms": pack_ms,
                     "saved_retrieval_ms": source["elapsed_ms"], "sent_to_model": False,
                     **packed, "answerable": gold[case["id"]]["answerable"]}
            if trace["answerable"]:
                groups = gold[case["id"]]["evidence_groups"]
                trace.update(hit1=evidence_hit(source["results"][:1], groups),
                             hit3=evidence_hit(source["results"], groups),
                             context_evidence_hit=evidence_hit(packed["selected_chunks"], groups))
            runs.append(trace)
        traces.extend(runs)
        scored = [r for r in runs if r["answerable"]]
        n = sum(r["context_evidence_hit"] for r in scored)
        summaries.append({"method": method, "queries": len(runs), "errors": sum(r["status"] != "ok" for r in runs),
                          "context_evidence_rate_offline": {"n": n, "N": len(scored), "rate": n/len(scored)},
                          "hit1": sum(r["hit1"] for r in scored), "hit3": sum(r["hit3"] for r in scored),
                          "mean_context_chars": statistics.mean(r["context_chars"] for r in runs),
                          "mean_candidate_count": statistics.mean(r["candidate_count"] for r in runs),
                          "mean_selected_count": statistics.mean(len(r["context_ids"]) for r in runs),
                          "median_pack_ms": statistics.median(r["pack_ms"] for r in runs)})
    base = {r["query_id"]: r for r in traces if r["method"] == "dense_top3" and r["answerable"]}
    expanded = {r["query_id"]: r for r in traces if r["method"] == "dense_top3_neighbors" and r["answerable"]}
    changed = {"gained": [k for k in base if not base[k]["context_evidence_hit"] and expanded[k]["context_evidence_hit"]],
               "lost": [k for k in base if base[k]["context_evidence_hit"] and not expanded[k]["context_evidence_hit"]]}
    report = {"run_at_utc": datetime.now(timezone.utc).isoformat(), "split": "dev", "budget_chars": args.budget,
              "corpus_sha256": corpus_hash, "benchmark_version": manifest["version"],
              "source_trace_sha256": hashlib.sha256((args.retrieval_run / "traces.json").read_bytes()).hexdigest(),
              "source_retrieval_run": str(args.retrieval_run), "query_count": len(cases), "summaries": summaries,
              "changes": changed, "service_cost_usd": 0,
              "limitations": "Offline context coverage using saved real retrieval, not context sent to a model. No LLM token usage/billing, answer quality or abstention evaluation. Character budget includes citation headers and separators. Mean sizes over all 17 cases. Hit and context denominators use 15 answerable cases. Exact normalized evidence matching; equivalent evidence may need review. Pack timing excludes retrieval, model load and corpus setup."}
    args.output.mkdir(parents=True)
    for name, value in (("traces.json", traces), ("summary.json", report)):
        (args.output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# E2 — Context lân cận trên dev", "", f"Cùng budget {args.budget} ký tự; replay dense top-3 thật, không thay ranking. Context chưa gửi model.", "", "| Context | Evidence coverage offline | Mean chars | Mean chunks | Median pack ms |", "|---|---:|---:|---:|---:|"]
    for s in summaries:
        m = s["context_evidence_rate_offline"]
        lines.append(f"| {s['method']} | {m['n']}/{m['N']} ({m['rate']:.1%}) | {s['mean_context_chars']:.1f} | {s['mean_selected_count']:.2f} | {s['median_pack_ms']:.3f} |")
    lines += ["", "Gained: " + str(changed["gained"]), "Lost: " + str(changed["lost"]), "", report["limitations"]]
    (args.output / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
