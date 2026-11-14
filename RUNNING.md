# Chạy bài Day 7 — Nguyễn Quỳnh Trang, 2A202603477

Kết quả đã chạy và báo cáo: [báo cáo cá nhân](report/individual/2A202603477_NguyenQuynhTrang.md).
Chạy lệnh từ root Day 7 trừ khi ghi rõ. Môi trường đã kiểm tra: Windows,
Python 3.12.10, Docker Desktop. Khuyến nghị Python 3.12 để dùng dependencies
đã thử. Không cần API embedding trả phí; DeepSeek chỉ dùng khi chạy agent.

## 1. Đọc kết quả mà không chạy lại API

- [Benchmark và quy tắc chấm](benchmark/README.md): dev 17, test 7.
- [Retrieval dev](results/retrieval-dev-v1/README.md), [weighted](results/retrieval-dev-weighted-v1/ANALYSIS.md), [context E2](results/context-dev-v1/ANALYSIS.md).
- [Agent dev sau review](results/agent-dev-review-v1/COMPARISON.md).
- [Retrieval test](results/retrieval-test-v1/README.md), [agent test sau review](results/agent-test-review-v1/COMPARISON.md).
- [Cấu hình khóa trước test](benchmark/selection_lock.json), [chi phí ước tính](results/cost_estimate.json).

Các thư mục agent có `config.json` và `traces.json`; thư mục review có nhãn từng
câu/citation và Markdown đối chiếu nguồn. Nhãn do học viên xác nhận, không phải
nhãn tự sinh từ model. Đã có kết quả thật nên không cần gọi API để xem/chấm bài.

## 2. Tạo môi trường Day 7

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Nếu đã có `.env`, giữ file đó, không copy đè. Điền `DATABASE_URL` giống Day 6,
`DAY6_STRATEGY=A`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL=https://api.deepseek.com`,
`DEEPSEEK_MODEL=deepseek-flash`. Không commit `.env`; không đưa key vào chat/log.
Các mật khẩu Docker mặc định của Day 6 chỉ dành cho môi trường lab local.

## 3. Kết nối hoặc tái tạo Day 6

Nếu database cũ còn, tại `Day6/starter` chạy:

```powershell
docker compose -p day6_student_starter up -d --wait
.\.venv\Scripts\python.exe scripts/check_setup.py
docker compose -p day6_student_starter exec -T postgres psql -U day6 -d day6_lab -c "SELECT strategy, count(*) FROM lab_chunks GROUP BY strategy ORDER BY strategy;"
```

Kỳ vọng A=228, B=C=242. Chỉ dùng A cho các so sánh Day 7.

Nếu máy mới, có thể đặt repo Day 6 ở `.local/day6` (đã gitignore) để tái tạo:

```powershell
git clone https://github.com/NguyenTrang005/K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion.git .local/day6
git -C .local/day6 checkout 0045b151db04c4a55b4c9039c903acb1725ab05a
Set-Location .local/day6/starter
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-embedding.txt
Copy-Item .env.example .env
```

Điền `DATABASE_URL` theo cấu hình local của Day 6, đọc README Day 6 trước khi
khởi động. Nếu đã có container/volume cũ dùng cùng cổng/project, dùng lại nó;
không tạo thêm database chiếm cổng và không xóa volume chứa dữ liệu.

```powershell
docker compose -p day6_student_starter up -d --wait
.\.venv\Scripts\python.exe -m src.ingest_vectors
Set-Location ../../..
```

Ingestion dùng chunk JSONL đã commit, đúng embedding revision, nạp A/B/C vào
pgvector; không cần trích xuất lại PDF. Đây là thao tác ghi database, chỉ chạy
khi cần tái tạo, không cần chạy lại nếu dữ liệu đã đủ. Model tải từ Hugging Face
lần đầu, cache ở `Day6/starter/.model_cache`. Nguồn sách và attribution xem
[data/README.md](data/README.md). Các file corpus công khai trong repo Day 6;
không phụ thuộc tài khoản database của tác giả trên dịch vụ ngoài.

Sau đó quay root Day 7, chép giá trị DATABASE_URL sang `.env`, kiểm tra:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.day6_retriever --check-only
```

## 4. Chạy kiểm tra code và kiểm tra cấu hình

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --split test --check-only
```

28 unit test đã đạt; các mock chỉ kiểm tra logic, không thay benchmark thật.
Check-only không tải embedding hoặc gọi DeepSeek, nhưng cần database để đối
chiếu hash. Các file khóa phải giữ nguyên; không sửa hash để che thay đổi.

## 5. Tái chạy retrieval trên dev

Ví dụ bên dưới dùng Day 6 ở `.local/day6`. Nếu dùng folder Day 6 có sẵn ngoài
Day 7, thay `--cache-folder` bằng đường dẫn `starter/.model_cache` tương ứng.
Mỗi output phải là thư mục mới, không ghi đè kết quả đã nộp.

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --split dev --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-retrieval-dev
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --split dev --dense-weight 0.8 --lexical-weight 0.2 --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-weighted-dev
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_context --day6-root '.local/day6' --output results/reproduction-context-dev
```

HF_HUB_OFFLINE chỉ dùng khi cache đầy đủ; không chặn DeepSeek API.
Replay E2 cần trace thật `results/retrieval-dev-v1`, không gọi model/database;
corpus local phải có hash trùng corpus đã dùng retrieval.

## 6. Tái chạy agent trên dev — dùng API token thật

```powershell
$devIds = (Get-Content benchmark/dev_cases.json -Raw -Encoding UTF8 | ConvertFrom-Json).id
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --dev-ids $devIds --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-agent-dev-baseline
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --dev-ids $devIds --neighbors --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-agent-dev-neighbors
```

Giữ model/prompt, top-3/search, tối đa 2 search, context budget 6000 ký tự.
Không truyền gold hoặc answerable vào agent. Traces giữ query model viết lại;
không coi chúng là kết quả query gốc của benchmark retrieval.

## 7. Test đã chốt, review và tổng hợp

Test chính đã chạy một lần sau selection lock. Pipeline chọn trùng baseline;
một lượt đại diện hai vai trò. Không tinh chỉnh theo kết quả test rồi báo đó
là đánh giá độc lập. Nếu tái chạy để kiểm tra khả năng tái lập, lưu riêng kết
quả và ghi rõ, không lựa lần chạy tốt hơn để thay số đã báo.

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --split test --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-retrieval-test
.\.venv\Scripts\python.exe -X utf8 -m src.run_deepseek --split test --cache-folder '.local/day6/starter/.model_cache' --output results/reproduction-agent-test
```

Lượt đầu chính thức đã được hướng dẫn trong [TEST_RUN.md](benchmark/TEST_RUN.md).
Tạo review cho một lượt tái chạy riêng nếu cần:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.prepare_agent_review --split test --runs reproduction-agent-test --output results/reproduction-agent-test-review
```

Review gốc đã điền do học viên xác nhận. Không tái sinh đè nhãn. Tổng hợp gốc:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m src.summarize_agent_reviews --split test
.\.venv\Scripts\python.exe -X utf8 -m src.estimate_costs
```

Không chạy lại tổng hợp dev chỉ để cập nhật định dạng: selection lock đã lưu
hash bằng chứng dev dùng lúc chọn. Chi phí hậu kiểm nằm ở file riêng, không
sửa usage hoặc cost null trong trace đã đóng băng. Giá có thể thay đổi; xem
nguồn/ngày/bước tính và giới hạn trong `results/cost_estimate.json`.

## 8. File cần nộp

Nộp repo cá nhân gồm code, tests, requirements, `.env.example`, benchmark,
selection lock, results/traces/reviews và báo cáo đã điền. Người chấm cần quyền
truy cập repo Day 7 và nguồn tái tạo Day 6. Không đưa `.env`, API key, `.venv`,
cache model hoặc nested clone vào commit. Deadline và nơi nộp link theo giảng viên.
