# Code

Đặt code của bạn tại đây hoặc mở rộng [starter](../starter/README.md). Khung agent chưa kết nối model và vector store thật.

## Retrieval Day 7

- `day6_retriever.py`: dense cosine search trên pgvector Day 6, đọc dữ liệu.
- `retrieval.py`: TF-IDF dùng lại thuật toán trong starter và hybrid RRF.
- `benchmark_retrieval.py`: chạy riêng dev, kiểm tra hash dev, không đọc test.

Chạy từ root Day 7 sau khi cài `requirements.txt`, cấu hình `.env` và bật database:

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --cache-folder '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.model_cache' --output results/retrieval-dev-v2
```

Offline dùng cache đã có từ Day 6; nếu chưa có cache đầy đủ cần tải đúng revision
trước. Mỗi lần dùng thư mục output mới để giữ kết quả cũ. Có thể chỉ chạy lexical
bằng `--methods tfidf`, không cần tải model nhưng vẫn đọc chunk từ database.

Ba phương pháp dùng cùng 228 chunk A, query gốc tiếng Việt và filter `chapter`
đã được cung cấp trong câu hỏi. TF-IDF không dịch query; corpus là tiếng Anh.
Hybrid dùng RRF `sum(1/(60+rank))` trên tối đa 20 candidate mỗi retriever,
không cộng trực tiếp cosine của dense với TF-IDF. Trace hybrid có rank/score
của từng thành phần cho các chunk cuối. Đây là cấu hình đầu tiên, chưa chọn
pipeline cuối cùng và chưa thực hiện đủ hai thí nghiệm cải thiện agent.

Đọc `results/retrieval-dev-v1/README.md`, `summary.json`, `traces.json` để xem
kết quả thực tế. Nhãn hit tự động theo nhóm evidence; evidence tương đương cần
review nguồn. Chưa có đánh giá context cuối, câu trả lời, citation hay abstention.

## Context lân cận (E2)

`context.py` chọn top-3 trước, thêm hàng xóm liền kề cùng nguồn/trang, dedup và
pack nguyên chunk theo budget 6000 ký tự gồm header. Không nhận nhãn gold.
`benchmark_context.py` so sánh top-3 và top-3 + hàng xóm bằng replay dense trace
thật đã lưu; kiểm tra hash corpus/benchmark và chỉ đọc dev.

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_context --day6-root '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion' --output results/context-dev-v2
```

Kết quả đầu tiên ở `results/context-dev-v1/`: context, ID, quyết định chọn/bỏ,
ranking gốc, độ dài, thời gian pack và evidence coverage offline. Context chưa
gửi model nên chưa thay thế đánh giá context và câu trả lời của agent thật.

## Agent DeepSeek thật

Điền `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL` vào `.env`
theo `.env.example`, giữ cấu hình database. Không đưa key vào code/trace.
`deepseek_agent.py` dùng native function calling: model tự tạo search query,
nhận context rồi gọi finish_answer với answered/abstain, câu trả lời và citation.
`run_deepseek.py` chỉ đọc cases dev, không đọc gold hoặc test. Mỗi câu tối đa
2 lượt search, 3 lượt model, top-k=3, budget context 6000 ký tự. Trước khi chạy
toàn dev cần xem kết quả smoke, vì mỗi lần chạy dùng API token thật.

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --neighbors --cache-folder '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.model_cache' --output results/agent-smoke-dev-v3
```

Mặc định chỉ chạy d7_dev_02 và d7_dev_16. Dùng `--dev-ids d7_dev_01` để chạy
một câu khác; bỏ `--neighbors` để thử baseline top-3. Output phải là thư mục
mới. Cần database chạy và kết nối mạng DeepSeek; HF_HUB_OFFLINE chỉ áp dụng
cho tải embedding, không chặn API DeepSeek.

`config.json` lưu cấu hình; `traces.json` lưu model response, native tool call,
query thực tế (có thể được model viết lại), kết quả retrieval, context, đáp án,
citation, token/cache usage và thời gian. Không coi query viết lại là kết quả
query gốc trong benchmark retrieval trước. USD cost để null nếu chưa có đơn
giá xác minh, không báo 0 cho model API. Không có mock fallback khi lỗi.

Code chỉ kiểm tra citation ID ở context và trong câu trả lời; hỗ trợ ngữ nghĩa,
abstention và độ đúng phải đọc nguồn chấm riêng. Chưa chạy toàn bộ dev/test.
