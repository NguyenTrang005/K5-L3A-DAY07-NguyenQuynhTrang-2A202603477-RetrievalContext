"""Create the pre-test selection record once, using dev evidence only."""
from datetime import datetime, timezone
import hashlib
import json

from .day6_retriever import ROOT, MODEL, REVISION
from .deepseek_agent import SYSTEM
from .selection import file_hash


def main():
    destination = ROOT / "benchmark/selection_lock.json"
    if destination.exists():
        raise ValueError("Selection lock already exists; do not overwrite after seeing test outcomes")
    for folder in ("retrieval-test-v1", "agent-test-baseline-v1"):
        if (ROOT / "results" / folder).exists():
            raise ValueError("Expected no test outputs before initial lock")
    config = json.loads((ROOT / "results/agent-dev-baseline-v1/config.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "benchmark/manifest.json").read_text(encoding="utf-8"))
    if config["neighbors"] or config["retriever"] != "dense":
        raise ValueError("Expected the selected dense baseline")
    files = ["src/deepseek_agent.py", "src/context.py", "src/day6_retriever.py",
             "src/retrieval.py", "src/selection.py", "src/run_deepseek.py",
             "src/benchmark_retrieval.py", "starter/baseline.py", "requirements.txt"]
    frozen = {relative: file_hash(ROOT / relative) for relative in files}
    for name in manifest["files_sha256"]:
        frozen["benchmark/" + name] = manifest["files_sha256"][name]
    lock = {"version": "selection-v1", "locked_at_utc": datetime.now(timezone.utc).isoformat(),
            "test_status_at_lock": "No Day 7 test outcomes run or used for selection; test questions authored and student-reviewed before evaluation.",
            "selected_configuration": "agent-dev-baseline-v1", "baseline_equals_selected": True,
            "selection_criteria": "At selection, prioritize reviewed grounded answer, correct abstention/false abstention, then token/time tradeoff on dev. Never select using test outcomes.",
            "reason": "Reviewed dev baseline answer score 30/30 versus neighbors 28/30; false abstention 0/15 versus 1/15; 54626 versus 68759 total tokens. Weighted RRF did not beat dense original-query Hit@3.",
            "label_provenance": "Student confirmed whole dev review set; individual prior labels preserved. Not independently double-graded.",
            "agent": {k: config[k] for k in ("model", "base_url", "neighbors", "budget_chars", "max_searches", "top_k", "retriever", "strategy", "thinking", "temperature", "max_tokens")},
            "agent_context_policy": "Cumulative unique seeds from at most two model-requested searches, top-3 per search; no neighbor expansion. Pack in retrieval insertion order within 6000 Unicode characters including headers/separators.",
            "system_prompt": SYSTEM, "system_prompt_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest(),
            "embedding": {"model": MODEL, "revision": REVISION, "dimensions": 384, "normalized": True, "max_seq_length": 512},
            "corpus_sha256": config["corpus_sha256"],
            "supplementary_retrieval": {"methods": ["dense", "tfidf", "hybrid"], "hybrid_weights": {"dense": 1.0, "tfidf": 1.0}, "rrf_k": 60, "candidates_per_retriever": 20, "cutoff": 3, "query_policy": "Original question, no translation; identical case-provided filters"},
            "test_plan": {"agent_runs": 1, "roles_for_same_run": ["baseline", "selected"],
                          "reason_for_shared_run": "The selected pipeline is exactly the baseline; shared results avoid implying two independent runs.",
                          "expected_queries": 7, "answerable": 5, "unanswerable": 2,
                          "error_policy": "Keep all test cases including errors; no selecting favorable reruns; document operational retries and preserve previous traces.",
                          "metrics": ["Hit@1", "Evidence Hit@3", "Context Evidence Rate", "context 0/1/2", "grounded answer 0/1/2", "citation validity", "citation coverage", "tool use", "abstention", "false abstention", "time", "tokens/cost"],
                          "review_policy": "Read all five answerable and two unanswerable cases and each citation; no auto-filling grades from dev confirmation."},
            "dev_evidence_sha256": {relative: file_hash(ROOT / relative) for relative in ["results/agent-dev-review-v1/summary.json", "results/agent-dev-review-v1/COMPARISON.md", "results/retrieval-dev-v1/summary.json", "results/retrieval-dev-weighted-v1/summary.json", "results/context-dev-v1/summary.json"]},
            "frozen_files_sha256": frozen}
    destination.write_text(json.dumps(lock, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Created benchmark/selection_lock.json before test evaluation; no API calls.")


if __name__ == "__main__":
    main()
