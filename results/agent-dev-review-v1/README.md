# Review agent trên dev

Đã kiểm tra: cả baseline và neighbors có đủ 17 ID dev, không lỗi hệ thống.
Config chỉ khác neighbors và thời điểm chạy. Không chạy lại API ở bước tạo review.

| Cấu hình | answered / abstain | Exact evidence trong context | Total tokens |
|---|---|---:|---:|
| baseline | 15 / 2 | 11/15 | 54626 |
| neighbors | 14 / 3 | 11/15 | 68759 |

Coverage trên là khớp text tự động trong context cuối gửi model, không phải nhãn
context 0/1/2 hoặc chất lượng answer đã review. Neighbors từ chối thêm d7_dev_13,
là câu có đáp án. Hai câu thiếu evidence có status abstain ở cả hai cấu hình,
nhưng vẫn cần đọc nội dung để chấm abstention đúng và không thêm khẳng định sai.
Không so trực tiếp 11/15 ở đây với replay E2 10/15: agent có thể viết lại query
và tìm nhiều lượt, trong khi E2 dùng query gốc/top-3 cố định.

Mỗi thư mục cấu hình có 17 file d7_dev_XX.md và reviews.json. File Markdown
đặt câu hỏi, đáp án/evidence gốc, câu trả lời, citation text và toàn context cạnh
nhau. Chỉ điền nhãn ở reviews.json; không sửa trace gốc hoặc nhãn benchmark.

## Cách chấm

- Câu có đáp án: context_grade 0=không evidence, 1=có nhưng thiếu điều kiện/
  nguồn, 2=đủ evidence và nguồn. Evidence tương đương được chấp nhận nếu ghi lý do.
- answer_grade 0=sai/không có evidence, 1=đúng một phần, 2=đúng và đủ.
  Từ chối câu có đáp án chấm 0. Không suy answer_grade từ status=answered.
- Câu thiếu evidence: abstention_correct true nếu từ chối đúng yêu cầu và không
  thêm khẳng định thiếu căn cứ; false nếu đoán, bịa hoặc từ chối nhưng thêm thông
  tin sai. Giữ context_grade và answer_grade null cho loại câu này.
- Mỗi citation: đọc text ở nguồn, đặt supports_answer true/false và lý do.
  Một citation chỉ hợp lệ khi vừa trong context vừa hỗ trợ khẳng định đi kèm.
- reviewed_by: người thật đã đọc, review_status: reviewed; reason: giải thích.
  Không đổi toàn bộ pending sang reviewed trước khi kiểm tra.

Một số abstain có citation trong answer nhưng không có trong danh sách citations.
Template lấy hợp cả hai để không bỏ sót nguồn cần chấm. automatic_checks chỉ
đưa dấu hiệu cần kiểm tra, không phải kết luận của học viên.

Bắt đầu bằng d7_dev_02 (citation) và d7_dev_13 (từ chối nhầm), sau đó đọc hai câu
thiếu evidence d7_dev_16/17, cuối cùng hoàn thành các câu còn lại ở cả hai cấu hình.
Không tái sinh review cùng thư mục vì có thể mất nhãn đã điền; script từ chối
ghi đè. Chưa có metrics grounded answer/citation/abstention được xác nhận.
