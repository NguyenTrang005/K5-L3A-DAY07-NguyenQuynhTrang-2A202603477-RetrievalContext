# Kế hoạch thí nghiệm dev sau baseline retrieval

## E1 — Weighted RRF

Ghi trước lần chạy: dùng dense 0.8, TF-IDF 0.2, giữ RRF k=60 và 20
candidate/retriever. Giữ nguyên corpus A, query gốc, filter từ cases và cutoff 3.
Không thay benchmark hoặc truy cập test. Không quét nhiều trọng số ở bước này.

Giả thuyết: giảm ảnh hưởng lexical yếu có thể giữ evidence dense trong top-3.
Đánh giá trước/sau bằng Hit@1, Evidence Hit@3, thời gian và lỗi. Ưu tiên
Evidence Hit@3, sau đó Hit@1; thời gian là đánh đổi, chưa chọn agent cuối cùng.
Giữ và báo kết quả kể cả không tăng. File output: results/retrieval-dev-weighted-v1.

Hai lỗi dev làm cơ sở:

- d7_dev_02: dense top-3 có chunk ec76de95… ở trang 196, giải thích đủ
  meat powder=UCS và salivation=UCR. Hybrid thay nó bằng chunk 6464d422… ở
  trang 201 nói về spontaneous recovery; đoạn này không trả lời đủ câu hỏi.
  Hai đoạn đầu nói chung về Pavlov, không đủ hai vai trò cần nêu.
- d7_dev_01: evidence định nghĩa học tập trải qua ranh giới hai chunk A.
  Tìm đúng trang không đồng nghĩa context có đủ câu định nghĩa. Đây là cơ sở
  cho thí nghiệm context lân cận tiếp theo, chưa triển khai ở E1.

Gold chỉ được dùng để chấm/phân tích lỗi dev, không dùng để tính fusion hay chọn
chunk khi chạy. Weighted RRF là giả thuyết chưa bảo đảm khôi phục d7_dev_02:
RRF còn ưu tiên chunk xuất hiện ở cả hai danh sách candidate.

## E2 — Context có chunk lân cận

Ghi trước lần chạy: replay top-3 dense thật từ retrieval-dev-v1, không chạy
lại ranking. Baseline chỉ top-3; cải thiện ưu tiên giữ top-3 rồi bổ sung chunk
ngay trước/sau theo thứ hạng seed. Hàng xóm phải tiếp giáp char offset, cùng
nguồn, cùng trang; loại trùng. Không chọn theo gold và không vượt filter.

Cả hai dùng budget **6000 ký tự Unicode**, tính cả ID, nguồn, trang và dấu
phân cách; giữ nguyên chunk, bỏ chunk không vừa, không cắt text âm thầm.
Mở rộng tối đa 2 hàng xóm mỗi seed, chỉ một lớp, tối đa 9 candidate duy nhất.
Chấm context thực tế được pack bằng evidence_groups sau khi đã chọn xong.

Giả thuyết: hàng xóm bổ sung phần evidence cắt ranh giới. Ưu tiên Context
Evidence Rate, sau đó số ký tự/thời gian; không đổi Hit@1/Hit@3. Báo cả câu
cải thiện, suy giảm, không đổi và context chưa đủ. Chưa chọn agent cuối.

Corpus local Day 6 phải có hash bằng corpus lần retrieval thật. Dùng lại trace
để tách riêng tác động context, không gọi model, không có API/token bill thực tế.
Thời gian pack đo mới; thời gian retrieval lấy từ trace cũ và ghi riêng.
Context này được chuẩn bị cho model, **chưa gửi model**, nên kết quả là đánh
giá context offline, không phải chất lượng câu trả lời hay CER end-to-end agent.
Output: results/context-dev-v1. Không mở cases/gold test.
