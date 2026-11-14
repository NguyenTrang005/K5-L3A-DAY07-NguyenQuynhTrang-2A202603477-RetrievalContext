# Đánh giá test sau khi chốt cấu hình

`selection_lock.json` ghi pipeline/model/prompt/corpus, hash benchmark/code,
lý do chọn bằng dev và kế hoạch test. Chọn dense baseline không thêm hàng xóm.
Không sửa pipeline hoặc chọn lại theo kết quả test. Nếu sửa để cải thiện sau khi
xem test, cần test mới và khai báo; không xóa lock hay trace để che thay đổi.

Baseline và cấu hình chọn giống hệt nhau nên dùng **một lượt agent trên 7 câu**
để đại diện cả hai vai trò, ghi rõ trong báo cáo. Bảng retrieval bổ sung chạy
cả dense, TF-IDF, hybrid RRF ngang trọng số đã thử ở dev. Đây không phải vòng
chọn phương pháp mới từ test. Giữ weighted RRF và neighbors trong bảng dev.

Chạy từ root Day 7, Docker/database đang chạy; giữ `.env` giống lúc chạy dev.

## 1. Kiểm tra cấu hình (không gọi API)

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --split test --check-only
```

Kỳ vọng: Checks OK, split=test, cases=7, chunks=228, neighbors=False, API calls=0.
Không cần tải model cho check-only. Chương trình kiểm tra hash của file đóng băng;
nếu có thay đổi, kiểm tra nguyên nhân, không tự sửa hash để bỏ qua khóa.

## 2. So sánh retrieval trên test (không gọi DeepSeek)

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --split test --cache-folder '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.model_cache' --output results/retrieval-test-v1
```

Chạy 3 phương pháp × 7 câu. Hit metrics mẫu số 5 câu có đáp án.
Gold chỉ được dùng chấm sau retrieval; không truyền vào retriever. Không chỉnh
cấu hình theo bảng kết quả này. Traces/summary/README được lưu để báo cáo.

## 3. Chạy agent test (có dùng API token)

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --split test --cache-folder '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.model_cache' --output results/agent-test-baseline-v1
```

Chạy cả 7 câu, không chọn subset và không bật neighbors. Tối đa 21 lượt model.
Chương trình không đọc test_gold. Model có thể viết lại query hoặc tìm hai lượt;
đó là agent pipeline, khác original-query retrieval. Lỗi được giữ trong trace
và chương trình tiếp tục các câu còn lại; không tự rerun để thay lỗi bằng kết quả
tốt. API cost USD chưa tính nếu chưa có bảng giá xác minh, usage token lưu thật.

## 4. Tạo bảng review (không gọi API)

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.prepare_agent_review --split test
```

Chỉ chạy khi đã có đủ 7 trace. Tạo 7 file Markdown và reviews.json tại
`results/agent-test-review-v1/agent-test-baseline-v1/`. Nhãn khởi tạo null.
Xác nhận dev trước đó không tự áp dụng cho test. Review toàn bộ:

- 5 câu có đáp án: context 0/1/2, answer 0/1/2, lý do và từng citation.
- 2 câu thiếu evidence: abstention_correct true/false và lý do.
- Chấp nhận evidence tương đương nếu kiểm chứng nguồn, ghi lại lý do.
- Lỗi model/database: báo riêng, giữ nguyên trace; không chấm giả thành đúng.

Sau khi review mới tổng hợp số liệu cuối và điền báo cáo cá nhân.
Mọi output được giữ nguyên, chương trình từ chối ghi đè thư mục có sẵn.
