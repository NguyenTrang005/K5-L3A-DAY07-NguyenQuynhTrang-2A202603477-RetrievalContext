# Benchmark Day 7 — Learning và Memory

## Phạm vi và trạng thái

Phiên bản `day7-v1`: 24 câu, tạo trước khi so sánh retrieval Day 7.

| Split | Có đáp án | Thiếu bằng chứng | Tổng |
|---|---:|---:|---:|
| Dev | 15 | 2 | 17 |
| Test | 5 | 2 | 7 |

15 câu dev có đáp án tái sử dụng từ Day 6. Năm câu test có đáp án và bốn
câu thiếu bằng chứng do AI hỗ trợ soạn mới. Không dùng lại năm câu test Day 6.
Test mới hỏi các ý trả lời khác với 20 câu cũ; vẫn dùng chung corpus/chủ đề,
không phải đánh giá trên tài liệu độc lập.

Nguồn: OpenStax, Rice University, *Psychology 2e*, chương 6 và 8.
Access for free at https://openstax.org/details/books/psychology-2e.
Theo manifest Day 6: CC BY-NC-SA 4.0. Giữ attribution khi chia sẻ evidence.

Corpus đánh giá: 52 trang gốc 193–218, 259–284; strategy A có 228 chunk.
Chỉ corpus này quyết định có/thiếu bằng chứng, không phải toàn bộ sách hay web.

**Trạng thái:** đã kiểm tra bằng code 22 đoạn evidence với text PDF và chunk A.
Ngày 14/11/2026, học viên xác nhận trong hội thoại đã kiểm tra các file theo yêu
cầu và mọi thứ đã ổn. Chốt phiên bản `day7-v1` trước so sánh retrieval Day 7.
Xác nhận được lưu trong `manifest.json`, thay cho ghi chú pending tại thời điểm
sinh file gold; nội dung câu hỏi/nhãn và hash không thay đổi.
Chưa chạy retrieval trên bộ câu hỏi này; chưa có metrics hoặc nhãn kết quả agent.

## Các file

- `dev_cases.json`, `test_cases.json`: chỉ ID, split, câu hỏi và filter được nêu
  trước trong câu hỏi nếu có. Đây là đầu vào chạy hệ thống.
- `dev_gold.json`, `test_gold.json`: nhãn answerable, đáp án, nhóm evidence,
  hoặc hành vi từ chối và lý do thiếu bằng chứng. Chỉ dùng ở bước chấm.
- `evidence_checks.json`: kiểm tra PDF/text, ID chunk tham chiếu và vị trí trang.
- `absence_checks.json`: kết quả tìm từ khóa trên toàn bộ 52 trang và nguyên văn
  các trang liên quan, giúp học viên kiểm tra bốn câu thiếu bằng chứng.
- `manifest.json`: số lượng, nguồn, giới hạn, SHA-256 của file và PDF.
- `build_benchmark.py`: tái tạo bộ câu hỏi từ project Day 6.

Không truyền file gold, kiểm tra evidence, answerable, reference chunk ID hoặc
absence_reason vào model/retriever. Loader phải chỉ lấy `question` và filter
được phép từ cases; tuyệt đối không suy ra filter từ gold. Mọi phương pháp so
sánh phải dùng cùng corpus A, cases, nhãn, chính sách filter và cutoff.

## Số trang và bản PDF local

PDF ở `Day6/data/raw/Psychology2e_WEB.pdf` trên máy hiện có **52 trang**,
là bản trích, khác mô tả 755 trang trong manifest cũ. Không sửa dữ liệu Day 6.
Các đoạn evidence đã kiểm tra khớp theo ánh xạ:

- Trang local 1–26 tương ứng trang PDF gốc 193–218.
- Trang local 27–52 tương ứng trang PDF gốc 259–284.
- `page` trong gold vẫn là **trang PDF gốc**, khớp database.
- `local_pdf_page` trong `evidence_checks.json` giúp mở đúng trang bản trích.
- Số trang in sách được giữ riêng trong metadata `printed_page` của chunk.

Hash PDF thực tế được ghi lại trong manifest Day 7; không dùng hash cũ để khẳng
định file local hiện tại là toàn bộ sách.

## Schema evidence và cách chấm

`evidence_groups` là danh sách các nhóm bằng chứng thay thế. Đủ **một nhóm**
là đạt; **tất cả đoạn trong nhóm đó** đều cần được hỗ trợ. Ở phiên bản này mỗi
câu có một nhóm; các câu so sánh mới có thể cần hai đoạn trong cùng nhóm.

Một đoạn có thể nằm trên nhiều chunk liên tiếp. Khi kiểm tra text tự động,
chỉ nối chunk cùng nguồn/trang, đúng thứ tự `char_start`, có vùng ký tự liên tục;
không nối qua khoảng trống để tạo evidence không thật. Danh sách chunk trong
file kiểm tra là tham chiếu cho người chấm, không phải ID bắt buộc duy nhất.
Chấp nhận evidence tương đương ở vị trí khác nếu đọc nguồn xác nhận và ghi lý do.

- **Hit@1:** top-1 có đủ một nhóm evidence hay không.
- **Evidence Hit@3:** hợp của top-3 có đủ một nhóm evidence hay không.
- **Context Evidence Rate:** context thực tế gửi model có đủ một nhóm hay không.
- Mẫu số ba chỉ số trên chỉ gồm câu có đáp án: 15 dev hoặc 5 test.

Cách chấm hợp của nhiều chunk được công bố trước để xử lý evidence cắt ngang
ranh giới. Nó khác phép chấm một chunk của starter/Day 6; không so trực tiếp
metrics cũ như cùng một định nghĩa và không chạy starter với schema này mà chưa
viết adapter evaluator. Báo cùng định nghĩa cho cả ba phương pháp Day 7.

Context chấm 0/1/2: không có / có nhưng thiếu evidence hoặc nguồn / đủ cả hai.
Câu trả lời có đáp án chấm 0/1/2: sai hoặc không có evidence / đúng một phần /
đúng đầy đủ và có evidence. Từ chối câu có đáp án chấm 0.
Citation phải có trong context và hỗ trợ nội dung; không chỉ kiểm tra ID.
Với câu thiếu bằng chứng, đạt khi nêu rõ không đủ thông tin cho yêu cầu cụ thể,
không bịa con số; có thể nói phần thông tin có nguồn nhưng không thay bằng suy đoán.
Báo abstention đúng, từ chối nhầm, tool use, thời gian, chi phí và lỗi riêng.

## Review và chốt

1. Đọc 15 câu dev và nguồn; xem các câu cắt ranh giới trong evidence_checks.
2. Đọc các trang liên quan và kết quả tìm toàn corpus cho bốn câu thiếu evidence.
   Từ khóa chỉ hỗ trợ kiểm tra, không chứng minh tuyệt đối rằng thông tin vắng mặt.
3. Đọc đáp án và nguồn của test một lần ở giai đoạn soạn nhãn; việc tạo nhãn
   không phải chạy test. Sau khi chốt, không dùng đầu ra test để điều chỉnh.
4. Ghi xác nhận thực tế và phiên bản benchmark trước khi so sánh trên dev.
   Manifest đã ghi nhận xác nhận review của học viên ngày 14/11/2026.
5. Chốt pipeline và tiêu chí chọn trên dev, sau đó chạy baseline/cấu hình chọn
   trên cùng test. Nếu dùng đầu ra test để chỉnh, tạo test mới và ghi lịch sử.

## Tái tạo

Chạy từ root Day 7 bằng Python có `pypdf`, ví dụ môi trường Day 6:

```powershell
& '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.venv\Scripts\python.exe' -X utf8 benchmark/build_benchmark.py --day6-root '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion'
```

Lệnh ghi lại các file benchmark được sinh. Không chạy lại sau khi review/chốt
nếu không chủ động tạo phiên bản mới. Script không truy cập database, không gọi
model và không cần API key; project Day 6 được đọc, không bị sửa.
