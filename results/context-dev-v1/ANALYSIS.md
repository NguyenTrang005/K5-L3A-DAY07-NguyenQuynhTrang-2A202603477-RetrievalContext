# Phân tích E2 — Context lân cận

Đã ghi giả thuyết/chính sách trước khi chạy tại benchmark/EXPERIMENTS.md.
Chạy paired offline trên cùng 17 query dev và cùng dense top-3 đã truy xuất thật.
Corpus local có hash trùng corpus database ở lần retrieval v1. Không chạy test.

## Kết quả

| Cấu hình | Evidence coverage offline | Ký tự TB | Chunk TB |
|---|---:|---:|---:|
| Dense top-3 | 9/15 (60%) | 2551.1 | 3.00 |
| Dense top-3 + hàng xóm | 10/15 (66.7%) | 5272.4 | 6.12 |

Cùng budget 6000 ký tự Unicode, gồm header citation và phân cách; lượng dùng
thực tế khác nhau. Không cắt nội dung chunk, không nối trang khác, không dùng
gold chọn hàng xóm. Hai câu thiếu bằng chứng không tính vào mẫu số coverage.
Không có lỗi nguồn retrieval. Hit@1 vẫn 2/15, Hit@3 vẫn 9/15: ranking không đổi.

## Câu cải thiện và giới hạn

- `d7_dev_14` hỏi cả proactive và retroactive interference. Chunk dense trang
  280 chứa một phần evidence; chunk ngay trước bổ sung phần còn lại. Context
  mới đủ evidence đã ghi, không có câu nào mất coverage so với baseline.
- `d7_dev_01` vẫn trượt. Chunk seed trang 194 không chứa đủ định nghĩa; evidence
  chuẩn nằm ở hai chunk trước đó. Mở rộng chỉ một lớp chưa lấy được cả hai;
  hơn nữa hàng xóm của seed trang 194 xếp sau hàng xóm seed hạng cao hơn và
  bị bỏ vì budget. Không được dùng gold để đặc cách lấy các chunk này.
- Context mới dài khoảng 2.07 lần. Có thể tăng token/chi phí hoặc nhiễu khi nối
  model; chưa có số token hay chi phí model thực tế để kết luận đánh đổi tốt.
- Đây là khớp evidence chuẩn tự động. Nguồn tương đương có thể cần đọc đối chiếu.

## Kết luận cho bước tiếp

Giữ cấu hình này làm ứng viên để đánh giá với agent trên dev; chưa chốt pipeline
cuối. Context đã chuẩn bị nhưng chưa gửi model, nên không gọi số này là chất
lượng câu trả lời hoặc Context Evidence Rate của agent end-to-end.
Model có thể trả lời sai dù context đủ; cần đo answer, citation và abstention.

## Tái chạy

Từ root Day 7, dùng output mới để không ghi đè:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_context --day6-root '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion' --output results/context-dev-v2
```

Không cần database đang chạy hoặc tải model cho thí nghiệm replay này. Cần các
file chunk A của Day 6 và trace dense thật v1. pack_ms chỉ đo tạo context;
saved_retrieval_ms là thời gian từ lần truy xuất cũ, không phải phép đo mới.
