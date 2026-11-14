"""Aggregate completed human labels without calling a model or grading text."""
import argparse
import json
from pathlib import Path
import statistics

from .day6_retriever import ROOT


def ratio(n, total):
    return {"n": n, "N": total, "rate": n / total if total else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    args = parser.parse_args()
    review_root = ROOT / f"results/agent-{args.split}-review-v1"
    runs = ["agent-test-baseline-v1"] if args.split == "test" else ["agent-dev-baseline-v1", "agent-dev-neighbors-v1"]
    reports = []
    for name in runs:
        reviews = json.loads((review_root / name / "reviews.json").read_text(encoding="utf-8"))
        traces = json.loads((ROOT / "results" / name / "traces.json").read_text(encoding="utf-8"))
        by_id = {r["query_id"]: r for r in reviews}
        if len(by_id) != len(traces) or set(by_id) != {t["query_id"] for t in traces}:
            raise ValueError("Review and trace IDs differ")
        for r in reviews:
            if r["review_status"] != "reviewed":
                raise ValueError("Incomplete review: " + r["query_id"])
            if r["answerable"]:
                if r["answer_grade"] not in (0, 1, 2) or r["context_grade"] not in (0, 1, 2):
                    raise ValueError("Missing answer/context grade")
            elif type(r["abstention_correct"]) is not bool:
                raise ValueError("Missing abstention review")
            if any(type(c["supports_answer"]) is not bool for c in r["citation_reviews"]):
                raise ValueError("Missing citation support label")
        answered_cases = [r for r in reviews if r["answerable"]]
        missing_cases = [r for r in reviews if not r["answerable"]]
        citations = [c for r in reviews for c in r["citation_reviews"]]
        successes = [t for t in traces if t["status"] != "error"]
        grade_counts = {str(g): sum(r["answer_grade"] == g for r in answered_cases) for g in (0, 1, 2)}
        context_counts = {str(g): sum(r["context_grade"] == g for r in answered_cases) for g in (0, 1, 2)}
        total_points = sum(r["answer_grade"] for r in answered_cases)
        report = {"configuration": name, "queries": len(traces), "errors": len(traces)-len(successes),
                  "tool_use": ratio(sum(t["search_count"] > 0 for t in successes), len(successes)),
                  "answer_grade_counts": grade_counts, "grounded_answer_score": ratio(total_points, 2*len(answered_cases)),
                  "grounded_answer_mean_out_of_2": total_points/len(answered_cases),
                  "context_grade_counts": context_counts,
                  "reviewed_context_evidence_rate": ratio(context_counts["2"], len(answered_cases)),
                  "automatic_exact_context_evidence_rate": ratio(sum(r["automatic_checks"]["exact_context_evidence_hit"] is True for r in answered_cases), len(answered_cases)),
                  "citation_validity": ratio(sum(c["in_context"] and c["supports_answer"] for c in citations), len(citations)),
                  "outputs_with_citations": ratio(sum(bool(r["citation_reviews"]) for r in reviews),len(reviews)),
                  "answered_outputs_with_citations": ratio(sum(bool(by_id[t['query_id']]["citation_reviews"]) for t in traces if t["status"] == "answered"),sum(t["status"] == "answered" for t in traces)),
                  "citation_list_mismatch_ids": [r["query_id"] for r in reviews if not r["automatic_checks"]["citation_list_matches_answer"]],
                  "abstention_correct": ratio(sum(r["abstention_correct"] for r in missing_cases),len(missing_cases)),
                  "false_abstention": ratio(sum(t["status"] == "abstain" for t in traces if by_id[t["query_id"]]["answerable"]),len(answered_cases)),
                  "search_count_distribution": {str(n): sum(t["search_count"] == n for t in traces) for n in sorted({t["search_count"] for t in traces})},
                  "usage": {k: sum(t["usage"].get(k,0) for t in traces) for k in ("prompt_tokens","completion_tokens","total_tokens","prompt_cache_hit_tokens","prompt_cache_miss_tokens")},
                  "median_elapsed_ms": statistics.median(t["elapsed_ms"] for t in traces),
                  "mean_context_chars": statistics.mean(t["context_chars"] for t in traces), "cost_usd": None}
        reports.append(report)
    provenance = "Student explicitly confirmed test 01-04: context=2, answer=2, citations correct; test 05: context=2, answer=0, citations correct; test 06-07: correct abstention and citations. No automatic content grades substituted." if args.split == "test" else "Student review confirmations in conversation; remaining grades completed following explicit all-cases satisfactory confirmation. Existing individual grades preserved. Not independent AI/human double grading."
    summary = {"split": args.split, "label_source": provenance,
               "limitations": "Human-reviewed sufficient evidence and automatic exact quote coverage differ; human labels allow equivalent evidence. Citation count includes inline references omitted from model citation lists. USD cost unknown; tokens are not dollar costs. Single model run per configuration.", "configurations": reports}
    (review_root / "summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines = [f"# Kết quả agent {args.split} sau review", "", summary["label_source"], "", "| Cấu hình | Grounded answer | Context đủ (review) | Citation hợp lệ | Từ chối đúng | Từ chối nhầm | Total tokens |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in reports:
        def fmt(key):
            m = r[key]
            return f"{m['n']}/{m['N']}"
        lines.append(f"| {r['configuration']} | {fmt('grounded_answer_score')} | {fmt('reviewed_context_evidence_rate')} | {fmt('citation_validity')} | {fmt('abstention_correct')} | {fmt('false_abstention')} | {r['usage']['total_tokens']} |")
    if args.split == "test":
        lines += ["", summary["limitations"], "", "## Diễn giải", "", "Baseline và selected là cùng cấu hình đã khóa trước test; một lượt kết quả đại diện cả hai vai trò, không phải hai lần chạy độc lập.", "", "Bốn câu có đáp án đạt 2, một câu bị từ chối nhầm đạt 0: tổng 8/10, trung bình 1.6/2. Hai câu thiếu bằng chứng được từ chối đúng theo review học viên.", "", "Context review đủ 5/5; khớp nguyên văn evidence tự động 4/5. Test 05 giữ cả hai thông tin này: học viên xác nhận context đủ, agent vẫn từ chối; không sửa số tự động hoặc chỉnh pipeline theo test.", "", "Citation hợp lệ tính cả ID inline có trong câu trả lời dù model bỏ khỏi danh sách citations. Nhãn hỗ trợ nguồn do học viên xác nhận. Chi phí USD chưa tính; không ghi 0 cho API."]
    else:
        lines += ["", summary["limitations"], "", "## Diễn giải", "", "Ưu tiên baseline cho bước chốt pipeline: điểm câu trả lời cao hơn, không từ chối nhầm ở dev và dùng ít token hơn. Cấu hình hàng xóm vẫn là kết quả thí nghiệm cần giữ lại, không xóa vì không tốt hơn.", "", "Context do người dùng xác nhận đủ: 15/15 ở cả hai. Khớp nguyên văn evidence tự động: 11/15 ở cả hai. Không thay số tự động thành số review; đây là hai cách kiểm tra khác nhau.", "", "d7_dev_13 neighbors giữ answer_grade=0 do từ chối câu có đáp án, dù context_grade=2. Các nhãn cũ không bị ghi đè bằng xác nhận chung.", "", "Citation support được ghi theo xác nhận review toàn bộ của học viên; không phải kết quả bộ kiểm tra ID tự động. Các citation inline bị bỏ khỏi danh sách citations vẫn được tính và cần chuẩn hóa loader metrics sau này."]
    (review_root / "COMPARISON.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    for r in reports:
        print(r["configuration"], "answer", r["grounded_answer_score"], "citations", r["citation_validity"], "tokens", r["usage"]["total_tokens"])


if __name__ == "__main__":
    main()
