"""Prepare ungraded review sheets from real agent results; no API calls."""
import argparse
import json
from pathlib import Path
import re

from .benchmark_retrieval import evidence_hit
from .day6_retriever import ROOT
from .selection import load_selection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("dev", "test"), default="dev")
    parser.add_argument("--runs", nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    args.output = args.output or ROOT / f"results/agent-{args.split}-review-v1"
    if args.split == "test":
        load_selection()
    runs = args.runs or (["agent-test-baseline-v1"] if args.split == "test" else ["agent-dev-baseline-v1", "agent-dev-neighbors-v1"])
    if args.output.exists():
        parser.error("Use a new output directory to preserve review edits")
    gold = {q["id"]: q for q in json.loads((ROOT / "benchmark" / f"{args.split}_gold.json").read_text(encoding="utf-8"))}
    cases = {q["id"]: q for q in json.loads((ROOT / "benchmark" / f"{args.split}_cases.json").read_text(encoding="utf-8"))}
    args.output.mkdir(parents=True)
    for name in runs:
        traces = json.loads((ROOT / "results" / name / "traces.json").read_text(encoding="utf-8"))
        if len(traces) != len(cases) or {t["query_id"] for t in traces} != set(cases):
            raise ValueError("Run must contain every dev ID exactly once")
        folder = args.output / name
        folder.mkdir()
        reviews = []
        for trace in traces:
            qid = trace["query_id"]
            label = gold[qid]
            listed = trace["citations"]
            embedded = re.findall(r"\[([0-9a-f]{64})\]", trace["answer"])
            citations = list(dict.fromkeys(listed + embedded))
            selected = {c["id"]: c for c in trace["selected_chunks"]}
            record = {"query_id": qid, "split": args.split, "answerable": label["answerable"],
                      "status": trace["status"], "reviewed_by": None, "review_status": "pending",
                      "context_grade": None, "answer_grade": None, "abstention_correct": None,
                      "reason": "", "citation_reviews": [
                          {"id": cid, "in_context": cid in selected, "in_citation_list": cid in listed,
                           "in_answer": cid in embedded, "supports_answer": None, "reason": ""} for cid in citations],
                      "automatic_checks": {
                          "exact_context_evidence_hit": evidence_hit(trace["selected_chunks"], label["evidence_groups"]) if label["answerable"] else None,
                          "citation_list_matches_answer": set(listed) == set(embedded),
                          "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."}}
            reviews.append(record)
            lines = [f"# {qid} — {name}", "", "## Câu hỏi", "", cases[qid]["question"],
                     "", "## Nhãn benchmark", "", f"Có đáp án: {label['answerable']}", "",
                     label.get("expected_answer", label.get("absence_reason", ""))]
            for group in label.get("evidence_groups", []):
                for e in group:
                    lines += ["", f"Evidence gốc: {e['source_id']}, trang PDF gốc {e['page']}", "", e["evidence"]]
            lines += ["", "## Kết quả agent", "", f"Status: {trace['status']}", "", trace["answer"],
                      "", f"Lượt search: {trace['search_count']}; token: {trace['usage']['total_tokens']}; context: {trace['context_chars']} ký tự.",
                      "", "## Kiểm tra tự động (không thay chấm nội dung)", "", json.dumps(record["automatic_checks"], ensure_ascii=False, indent=2),
                      "", "## Citation cần đối chiếu"]
            for citation in record["citation_reviews"]:
                c = selected.get(citation["id"])
                lines += ["", f"### {citation['id']}", "", f"Trong context: {citation['in_context']}; trong danh sách citations: {citation['in_citation_list']}; trong answer: {citation['in_answer']}."]
                if c:
                    lines += ["", f"Nguồn: {c['source']}; trang PDF gốc {c['page']}", "", c["text"]]
            lines += ["", "## Toàn bộ context thực tế gửi model trước câu trả lời", "", trace["context"],
                      "", "## Chấm vào reviews.json", "", "Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.",
                      "Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.",
                      "Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.",
                      "Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.",
                      "Sau khi đọc: reviewed_by tên người review, review_status=reviewed."]
            (folder / f"{qid}.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
        (folder / "reviews.json").write_text(json.dumps(reviews, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Prepared {len(cases)*len(runs)} ungraded {args.split} review sheets; no grades auto-filled.")


if __name__ == "__main__":
    main()
