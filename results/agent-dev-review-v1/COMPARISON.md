# Kết quả agent dev 

| Cấu hình | Grounded answer | Context đủ (review) | Citation hợp lệ | Từ chối đúng | Từ chối nhầm | Total tokens |
|---|---:|---:|---:|---:|---:|---:|
| agent-dev-baseline-v1 | 30/30 | 15/15 | 34/34 | 2/2 | 0/15 | 54626 |
| agent-dev-neighbors-v1 | 28/30 | 15/15 | 38/38 | 2/2 | 1/15 | 68759 |


## Diễn giải

Ưu tiên baseline cho bước chốt pipeline: điểm câu trả lời cao hơn, không từ chối nhầm ở dev và dùng ít token hơn. Cấu hình hàng xóm vẫn là kết quả thí nghiệm cần giữ lại, không xóa vì không tốt hơn.

Context do người dùng xác nhận đủ: 15/15 ở cả hai. Khớp nguyên văn evidence tự động: 11/15 ở cả hai. Không thay số tự động thành số review; đây là hai cách kiểm tra khác nhau.

d7_dev_13 neighbors giữ answer_grade=0 do từ chối câu có đáp án, dù context_grade=2. Các nhãn cũ không bị ghi đè bằng xác nhận chung.
