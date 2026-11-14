# Định dạng dữ liệu

## Corpus thực tế của bài làm

Bài dùng lại `data/processed/chunks_A.jsonl` trong [repo Day 6](https://github.com/NguyenTrang005/K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion), phiên bản tham chiếu `0045b151db04c4a55b4c9039c903acb1725ab05a`.
Corpus OpenStax *Psychology 2e*, chương 6/8, 52 trang, 228 chunk A.
Attribution: OpenStax, Rice University. Access for free at openstax.org.
Quyền sử dụng theo manifest Day 6: CC BY-NC-SA 4.0. Giữ attribution khi chia sẻ.
Không commit lại cache model hoặc database volume. Tái tạo pgvector bằng code
ingestion Day 6 như [RUNNING.md](../RUNNING.md); benchmark Day 7 nằm ở
`benchmark/`, không dùng các example JSON bên dưới để báo kết quả.

PDF local là bản trích 52 trang; benchmark dùng số trang PDF gốc 193–218 và
259–284. Hash thực tế và ánh xạ trang nằm ở `benchmark/manifest.json` và
`benchmark/evidence_checks.json`. Nguồn sách:
https://openstax.org/details/books/psychology-2e.

## Schema starter

Các file `example_*.json` chỉ minh họa định dạng, không đủ để nộp bài. Dữ liệu thật là JSON array UTF-8; nếu dùng định dạng khác, ghi cách chuyển trong README.

- **Chunk:** `id`, `text`, `source_id`, `source`, `page`, `metadata`. ID phải duy nhất; giữ phiên bản hoặc ngày nếu có.
- **Câu có đáp án:** `id`, `split` (`dev` hoặc `test`), `question`, `expected_answer`, `gold`: danh sách `{source_id, page, evidence}`. Với schema mẫu, mỗi evidence phải nằm trọn trong một chunk đúng nguồn và trang; các phần tử `gold` là evidence thay thế. Với câu multi-hop cần nhiều đoạn, bạn có thể mở rộng schema, ghi rõ nhóm evidence bắt buộc và cách chấm. Có thể thêm `filter` do người dùng cung cấp trước.
- **Câu thiếu evidence:** `id`, `split`, `question`, `answerable: false`, `expected_behavior: "search_and_abstain"`, `absence_reason`. Xem `agent_cases_example.json`.

Không đưa `gold` hoặc nhãn đáp án vào model và retrieval tool. Ghi nguồn dữ liệu và quyền sử dụng. Cách chuyển một số định dạng Day 6: [starter/README.md](../starter/README.md).
