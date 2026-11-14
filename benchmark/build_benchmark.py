"""Build Day 7 benchmark from local Day 6 artifacts; no retrieval/model calls.

Requires pypdf. Run with Day 6's Python or install pypdf in Day 7.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day6-root", required=True, type=Path)
    args = parser.parse_args()
    root = args.day6_root.resolve()
    output = Path(__file__).resolve().parent
    old = [json.loads(s) for s in (root / "benchmark/questions.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    pages = {p["page"]: p for p in map(json.loads, (root / "data/processed/pages.jsonl").read_text(encoding="utf-8").splitlines())}
    chunks = list(map(json.loads, (root / "data/processed/chunks_A.jsonl").read_text(encoding="utf-8").splitlines()))
    pdf_path = root / "data/raw/Psychology2e_WEB.pdf"
    pdf = PdfReader(pdf_path)
    # Local Day 6 PDF may be a selected-page excerpt rather than the full book.
    if len(pdf.pages) == 52:
        pdf_mapping = {original: index for index, original in enumerate(sorted(pages))}
        pdf_layout = "52-page excerpt; local positions 1-26 map to original PDF 193-218; 27-52 map to 259-284"
    elif len(pdf.pages) >= max(pages):
        pdf_mapping = {original: original - 1 for original in pages}
        pdf_layout = "Full book; original PDF page equals physical page"
    else:
        raise ValueError("PDF page count does not match full book or expected excerpt")
    cases, labels = [], []

    def add(qid, split, question, answer=None, evidence=None, filters=None, origin="new_day7", absence=None):
        case = {"id": qid, "split": split, "question": question}
        if filters:
            case["filter"] = filters
        cases.append(case)
        label = {"id": qid, "split": split, "answerable": answer is not None, "origin": origin}
        if answer is not None:
            label.update(expected_answer=answer, evidence_groups=[[
                {"source_id": "openstax_psychology2e", "page": page, "evidence": quote}
                for page, quote in evidence
            ]])
        else:
            label.update(expected_behavior="search_and_abstain", **absence)
        labels.append(label)

    for q in old:
        if q["split"] == "dev":
            add("d7_" + q["id"], "dev", q["question"], q["expected_answer"],
                [(q["gold_page"], q["evidence_quote"])], q.get("filter"), "day6_dev:" + q["id"])

    add("d7_test_01", "test", "Trong shaping, người huấn luyện củng cố điều gì trước khi đạt hành vi mục tiêu?",
        "Củng cố những hành vi xấp xỉ liên tiếp, ngày càng gần hành vi mục tiêu.",
        [(207, "Instead of rewarding\nonly the target behavior, in shaping, we reward successive approximations of a target behavior.")])
    add("d7_test_02", "test", "Điểm khác nhau về nguồn gốc giá trị củng cố giữa primary reinforcer và secondary reinforcer là gì?",
        "Primary reinforcer có tính củng cố bẩm sinh, không cần học; secondary reinforcer không có giá trị vốn có và có tính củng cố khi liên kết với primary reinforcer.",
        [(208, "Primary reinforcers are reinforcers that have innate reinforcing\nqualities. These kinds of reinforcers are not learned."),
         (208, "A secondary reinforcer has no inherent value and only has reinforcing qualities when linked with a primary\nreinforcer.")])
    add("d7_test_03", "test", "Một người đã học được điều gì đó nhưng chỉ thể hiện ra hành vi khi có lý do cần dùng kiến thức ấy. Sách gọi dạng học này là gì?",
        "Latent learning (học tiềm ẩn): học xảy ra nhưng chưa quan sát được trong hành vi cho đến khi có lý do để thể hiện.",
        [(213, "This is known as latent\nlearning: learning that occurs but is not observable in behavior until there is a reason to demonstrate it.")])
    add("d7_test_04", "test", "Recall và recognition khác nhau như thế nào về việc sử dụng gợi ý hoặc gặp lại thông tin?",
        "Recall là truy cập thông tin mà không có gợi ý; recognition là nhận ra thông tin đã học khi gặp lại thông tin đó.",
        [(267, "Recall is what we most often think about when we talk about memory retrieval: it\nmeans you can access information without cues."),
         (267, "Recognition happens when you identify information that you have previously learned after encountering it\nagain.")])
    add("d7_test_05", "test", "Flashbulb memories về sự kiện quan trọng có luôn giữ nguyên độ chính xác theo thời gian không?",
        "Không. Ngay cả flashbulb memories về sự kiện quan trọng cũng có thể giảm độ chính xác theo thời gian.",
        [(270, "Even flashbulb memories for important events can have decreased accuracy with the passage of time.")])

    negatives = [
        ("dev", "16", "Theo phần tài liệu đã index, học giãn cách làm tăng chính xác bao nhiêu phần trăm điểm thi so với học dồn?",
         "Có khuyến nghị học giãn cách nhưng không có mức phần trăm tăng điểm thi so với học dồn.", [283], ["distributed", "cram", "percent", "percentage", "%", "exam"]),
        ("dev", "17", "Mê cung trong thí nghiệm học tiềm ẩn của Tolman được mô tả trong tài liệu có tổng chiều dài chính xác bao nhiêu mét?",
         "Có mô tả thí nghiệm và 10 phiên không củng cố nhưng không có tổng chiều dài mê cung tính bằng mét.", [213, 214], ["Tolman", "maze", "meter", "metre", "length"]),
        ("test", "06", "Trong nghiên cứu Yogo và Fujihara (2008) được tài liệu nhắc đến, dung lượng trí nhớ ngắn hạn tăng chính xác bao nhiêu phần trăm sau năm tuần?",
         "Có thời lượng viết và thời gian năm tuần, cùng nhóm có cải thiện, nhưng không có phần trăm tăng dung lượng trí nhớ.", [282, 283], ["Yogo", "Fujihara", "five weeks", "percent", "percentage", "%"]),
        ("test", "07", "Theo mô tả thí nghiệm búp bê Bobo trong tài liệu, mỗi trẻ cần chính xác bao nhiêu lần quan sát người lớn trước khi bắt chước hành vi gây hấn?",
         "Có mô tả quan sát và bắt chước hành vi gây hấn nhưng không quy định số lần quan sát chính xác cần thiết cho từng trẻ.", [216, 217, 218], ["Bobo", "Bandura", "observ", "trial", "times"]),
    ]
    absence_audit = []
    for split, number, question, reason, related, terms in negatives:
        matches = {term: [n for n, p in sorted(pages.items()) if term.casefold() in p["text"].casefold()] for term in terms}
        absence = {"absence_reason": reason, "related_pages": related,
                   "verification_method": "Search terms across all 52 indexed page texts, inspect related source passages and corresponding PDF pages; top-k absence is not evidence of absence.",
                   "search_terms": terms, "review_status": "AI-assisted draft; student confirmation against source PDF pending"}
        add(f"d7_{split}_{number}", split, question, absence=absence)
        absence_audit.append({"id": f"d7_{split}_{number}", "keyword_page_matches": matches,
                              "related_passages": [{"page": n, "text": pages[n]["text"]} for n in related]})

    checks = []
    for label in labels:
        for group in label.get("evidence_groups", []):
            for e in group:
                n, quote = e["page"], norm(e["evidence"])
                if quote not in norm(pages[n]["text"]):
                    raise ValueError(f"Evidence absent from extracted page: {label['id']}")
                if quote not in norm(pdf.pages[pdf_mapping[n]].extract_text()):
                    raise ValueError(f"Evidence absent from original PDF text: {label['id']}")
                candidates = sorted([c for c in chunks if c["page"] == n and c["document_id"] == e["source_id"]], key=lambda c: c["metadata"]["char_start"])
                joined = "".join(c["text"] for c in candidates)
                if quote not in norm(joined):
                    raise ValueError(f"Evidence missing from strategy A: {label['id']}")
                # Raw page offsets handle evidence crossing chunk boundaries.
                page_text = pages[n]["text"]
                match = re.search(r"\s+".join(re.escape(s) for s in e["evidence"].split()), page_text)
                if match is None:
                    raise ValueError("Unable to locate evidence offsets")
                required = [c["chunk_id"] for c in candidates if c["metadata"]["char_start"] < match.end() and c["metadata"]["char_end"] > match.start()]
                checks.append({"id": label["id"], "page": n, "pdf_text_match": True,
                               "local_pdf_page": pdf_mapping[n] + 1,
                               "page_text_match": True, "strategy_A_coverage": True,
                               "evidence": e["evidence"], "reference_chunk_ids": required,
                               "crosses_chunk_boundary": len(required) > 1})

    def write(name, data):
        (output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for split in ("dev", "test"):
        write(f"{split}_cases.json", [q for q in cases if q["split"] == split])
        write(f"{split}_gold.json", [q for q in labels if q["split"] == split])
    write("evidence_checks.json", checks)
    write("absence_checks.json", absence_audit)
    hashes = {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in
              ("dev_cases.json", "dev_gold.json", "test_cases.json", "test_gold.json")}
    write("manifest.json", {"version": "day7-v1", "status": "Prepared before Day 7 retrieval comparisons; student source review pending",
          "counts": {s: {"answerable": sum(q["split"] == s and q["answerable"] for q in labels),
                         "unanswerable": sum(q["split"] == s and not q["answerable"] for q in labels)} for s in ("dev", "test")},
          "corpus": "OpenStax Psychology 2e; PDF pages 193-218 and 259-284; 52 pages; strategy A, 228 chunks",
          "source_repo": "https://github.com/NguyenTrang005/K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion",
          "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
          "local_pdf_layout": pdf_layout,
          "day6_questions_sha256": hashlib.sha256((root / "benchmark/questions.jsonl").read_bytes()).hexdigest(),
          "files_sha256": hashes, "provenance": "15 Day 6 dev questions reused; 5 new answerable test and 4 new unanswerable questions authored with AI assistance. Day 6 test excluded.",
          "limitations": "Shared corpus/topics across splits; not document-disjoint. PDF text matches do not replace student visual/source review. No Day 7 retrieval metrics measured by this script."})
    print(f"Created {len(cases)} cases; checked {len(checks)} evidence passages against PDF and strategy A.")
    print("Cross-boundary:", sorted({c["id"] for c in checks if c["crosses_chunk_boundary"]}))


if __name__ == "__main__":
    main()
