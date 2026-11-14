# Kết quả agent test sau review

Student explicitly confirmed test 01-04: context=2, answer=2, citations correct; test 05: context=2, answer=0, citations correct; test 06-07: correct abstention and citations. No automatic content grades substituted.

| Cấu hình | Grounded answer | Context đủ (review) | Citation hợp lệ | Từ chối đúng | Từ chối nhầm | Total tokens |
|---|---:|---:|---:|---:|---:|---:|
| agent-test-baseline-v1 | 8/10 | 5/5 | 14/14 | 2/2 | 1/5 | 28529 |

Human-reviewed sufficient evidence and automatic exact quote coverage differ; human labels allow equivalent evidence. Citation count includes inline references omitted from model citation lists. USD cost unknown; tokens are not dollar costs. Single model run per configuration.

## Diễn giải

Baseline và selected là cùng cấu hình đã khóa trước test; một lượt kết quả đại diện cả hai vai trò, không phải hai lần chạy độc lập.

Bốn câu có đáp án đạt 2, một câu bị từ chối nhầm đạt 0: tổng 8/10, trung bình 1.6/2. Hai câu thiếu bằng chứng được từ chối đúng theo review học viên.

Context review đủ 5/5; khớp nguyên văn evidence tự động 4/5. Test 05 giữ cả hai thông tin này: học viên xác nhận context đủ, agent vẫn từ chối; không sửa số tự động hoặc chỉnh pipeline theo test.

Citation hợp lệ tính cả ID inline có trong câu trả lời dù model bỏ khỏi danh sách citations. Nhãn hỗ trợ nguồn do học viên xác nhận. Chi phí USD chưa tính; không ghi 0 cho API.
