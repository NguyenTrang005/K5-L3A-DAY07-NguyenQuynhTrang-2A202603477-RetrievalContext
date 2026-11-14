# Báo cáo Day 7

**Họ tên:** Nguyễn Quỳnh Trang · **MSSV:** 2A202603477 · **Lớp:** K5-L3A

## Dữ liệu và benchmark

- Nguồn, quyền sử dụng, số trang và số chunk:
  - Dùng lại corpus Day 6: OpenStax, Rice University, *Psychology 2e*, chương 6 — Learning và chương 8 — Memory. [Nguồn sách](https://openstax.org/details/books/psychology-2e), [repo Day 6](https://github.com/NguyenTrang005/K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion).
  - Quyền sử dụng theo manifest Day 6: CC BY-NC-SA 4.0; attribution: “OpenStax, Rice University. Access for free at openstax.org.” Không dùng tài liệu mật.
  - Corpus gồm **52 trang**, trang PDF gốc **193–218 và 259–284**, strategy A gồm **228 chunk**. Chunk cố định tối đa 800 ký tự, không overlap; có ID, source, page, chapter và vị trí ký tự.
  - File PDF local hiện là bản trích 52 trang, khác thông tin 755 trang trong manifest Day 6 cũ. Trang local 1–26 tương ứng trang gốc 193–218, local 27–52 tương ứng 259–284. `page` trong benchmark/database là trang PDF gốc; số trang in trong sách nằm ở `printed_page`. Hash PDF thực tế được lưu tại [manifest](../../benchmark/manifest.json).
- Vector store, embedding model, phiên bản và số chiều:
  - PostgreSQL 16.16 + pgvector 0.8.7; database `day6_lab`, bảng `lab_chunks`, khóa `(strategy, chunk_id)`. Kết nối qua `DATABASE_URL` local; không công bố mật khẩu trong báo cáo. Tìm exact cosine bằng `<=>`, score = 1 − cosine distance; không dùng HNSW/IVFFlat.
  - Model local CPU: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, revision `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, **384 chiều**. Query/document dùng cùng encode, normalize, không prefix, `max_seq_length=512` giống Day 6.
  - Python 3.12.10 trên Windows; dependencies: [requirements.txt](../../requirements.txt), phiên bản thực tế: [environment.json](../../results/environment.json). Hash corpus dùng đối chiếu trước các lượt chạy: `922be37c16b06a407c507b15d8aed972298e18deb48b72ffff98822618f1d41e`.
- Agent model, cách chạy và phân chia dev/test:
  - DeepSeek API `deepseek-flash`, `https://api.deepseek.com`, native tool calling; thinking disabled, temperature 0, max output 1200 token/lượt. Tên model trả về trong trace là `deepseek-flash`; không tự khẳng định một revision trọng số backend nếu API không cung cấp.
  - **Dev 17 câu:** 15 có đáp án + 2 thiếu evidence. **Test mới 7 câu:** 5 có đáp án + 2 thiếu evidence. Tái sử dụng 15 câu dev Day 6; không dùng 5 câu test Day 6 đã xem kết quả làm holdout mới.
  - Query/đáp án tiếng Việt, evidence tiếng Anh. Test mới hỏi shaping, primary/secondary reinforcers, latent learning, recall/recognition, flashbulb memory; hai câu thiếu evidence hỏi phần trăm cải thiện trí nhớ và số lần quan sát búp bê Bobo.
  - [Cases và gold](../../benchmark/README.md) tách file. Agent chỉ đọc cases, không nhận gold, đáp án, `answerable` hay `absence_reason`. Chọn cấu hình trên dev, khóa lúc **2026-11-14 09:38:35 UTC**; retrieval test bắt đầu 09:40 UTC và agent test 09:41 UTC. [Selection lock](../../benchmark/selection_lock.json) lưu model/prompt/corpus và hash file; test không dùng để chọn lại.
  - Cách chạy đầy đủ: [RUNNING.md](../../RUNNING.md). Điểm vào agent: `python -m src.run_deepseek`; retrieval: `python -m src.benchmark_retrieval`.
- Cách xác định câu có/thiếu evidence và tiêu chí chấm:
  - Câu có đáp án: ghi expected answer và `evidence_groups`; tất cả đoạn trong một nhóm là bắt buộc, các nhóm là phương án thay thế. Đã kiểm tra **22 đoạn evidence** khớp text PDF và được corpus A bao phủ; học viên review nội dung/nguồn với AI hỗ trợ chuẩn bị.
  - Câu thiếu evidence được xét trong **52 trang đã index**, không phải toàn bộ sách; tìm từ khóa toàn corpus và đọc trang liên quan, ghi [absence checks](../../benchmark/absence_checks.json). Không suy ra thiếu thông tin chỉ từ top-k không tìm thấy.
  - Hit@1/Hit@3 chấm có đủ một nhóm evidence trong top-1/hợp top-3 trên cùng nguồn, trang; chỉ nối chunk liên tục theo char offset. Evidence có thể cắt ranh giới. Đây là mở rộng được công bố trước tại [quy tắc benchmark](../../benchmark/README.md), khác cách một-chunk của starter/Day 6.
  - Mẫu số retrieval/context là 15 câu dev hoặc 5 câu test có đáp án. Context 0/1/2 = không evidence / thiếu điều kiện hoặc nguồn / đủ evidence và nguồn. Grounded answer 0/1/2 = sai hoặc không evidence / đúng một phần / đúng và đủ; từ chối câu có đáp án nhận 0. Citation phải có trong context và hỗ trợ khẳng định. Abstention đúng khi không đủ evidence và không thêm khẳng định thiếu căn cứ.
  - Nhãn semantic do học viên xác nhận trong hội thoại: dev xác nhận toàn bộ, giữ các điểm cá biệt đã chốt; test xác nhận riêng 01–04, 05, 06–07. Không coi đây là đánh giá mù hay chấm độc lập bởi hai người. Lưu [nhãn dev](../../results/agent-dev-review-v1/) và [nhãn test](../../results/agent-test-review-v1/).

## Retrieval và thử nghiệm

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| Baseline | Dense exact cosine; top-3; filter chapter từ cases; không rerank | Query gốc, dùng lại index A Day 6 | dev | 2/15 (13,3%) | 9/15 (60%) | Chưa gửi model ở lượt retrieval; agent xem bảng dưới | Retrieval median 32,50 ms/query; API retrieval 0 USD |
| Phương pháp 2 | TF-IDF cosine; Unicode word tokens; top-3; cùng filter; không dịch query | Đánh giá lexical khi query Việt, corpus Anh | dev | 2/15 (13,3%) | 2/15 (13,3%) | Không đo agent TF-IDF | Median 0,19 ms/query; API 0 USD |
| Phương pháp 3 | Hybrid RRF: 20 candidate mỗi retriever, k=60, trọng số 1:1; xuất top-3 | Kết hợp thứ hạng, không cộng score khác thang | dev | 3/15 (20%) | 8/15 (53,3%) | Không đo agent hybrid | Median 34,00 ms/query; API 0 USD |
| Cải thiện 1 | Weighted RRF dense 0,8 / lexical 0,2; còn lại giữ nguyên | Giảm ảnh hưởng lexical yếu | dev | 2/15 (13,3%) | 9/15 (60%) | Không đo agent weighted | Median 31,56 ms/query; API 0 USD |
| Cải thiện 2 | Dense top-3 + tối đa 1 chunk trước/sau mỗi seed, cùng trang/nguồn; dedup; budget 6000 ký tự | Khôi phục evidence cắt ranh giới | dev | 2/15 (13,3%), giữ ranking | 9/15 (60%), giữ ranking | **Replay offline:** 9/15 → 10/15 (60% → 66,7%); **agent thật:** 15/15 theo review, 11/15 khớp text | Pack median 0,012 → 0,026 ms; agent neighbors 68.759 token, khoảng 0,010607 USD |
| Cấu hình đã chọn | Agent dense, top-3 mỗi search; tối đa 2 search; không hàng xóm; cumulative context ≤6000 ký tự | Chọn bằng dev, không đổi sau test | test | **Query gốc:** 1/5 (20%) | **Query gốc:** 3/5 (60%) | **Agent thật:** 5/5 (100%) theo review; 4/5 (80%) khớp text | Retrieval median 49,09 ms; agent median 4,760 s/câu; 28.529 token, khoảng 0,004949 USD |
| Baseline | Trùng chính xác cấu hình được chọn | Một lượt agent test dùng cho cả hai vai trò, không nhân đôi số mẫu | test | 1/5 (20%) | 3/5 (60%) | Cùng kết quả hàng trên | Cùng lượt chạy, không cộng lại chi phí |
| TF-IDF bổ sung | Cấu hình lexical đã cố định ở dev | Báo thêm, không chọn lại bằng test | test | 1/5 (20%) | 4/5 (80%) | Không đo agent | Median 0,24 ms/query; API 0 USD |
| Hybrid bổ sung | RRF 1:1, 20 candidate/retriever, k=60 | Báo thêm, không chọn lại bằng test | test | 1/5 (20%) | 3/5 (60%) | Không đo agent | Median 33,29 ms/query; API 0 USD |

Một cấu hình có thể đồng thời là phương pháp mới và cải thiện; trong bài này tách rõ 3 phương pháp và 2 thử nghiệm E1/E2. [Kế hoạch thí nghiệm](../../benchmark/EXPERIMENTS.md) ghi giả thuyết trước mỗi lần chạy. Mọi phương pháp dùng cùng 228 chunk A, cases và filter chapter người dùng đã nêu; lexical lọc trước cutoff. Không rerank và không dùng gold suy ra filter.

**Phân biệt phép đo:** bảng Hit@1/Hit@3 dùng query gốc; agent có thể viết lại query tiếng Anh và tìm nhiều lượt, lưu từng query trong trace. CER agent vì vậy không nhất thiết bằng Hit@3 query gốc. Replay context E2 dùng lại dense trace cố định để cô lập ảnh hưởng context, chưa gửi model. Không trộn replay, query gốc và agent thành một phép so sánh.

**Hai lỗi dev, giả thuyết và kết quả trước/sau:**

1. `d7_dev_02`: dense rank 3 chứa meat powder=UCS, salivation=UCR nhưng TF-IDF xếp rank 7. RRF 1:1 đẩy chunk về spontaneous recovery lên top-3, mất evidence. E1 dùng 0,8/0,2 đưa evidence trở lại; Hit@3 tăng 8/15 → 9/15, Hit@1 giảm 3/15 → 2/15. Không vượt dense, nên không chọn weighted chỉ vì hơn hybrid cũ. [Phân tích E1](../../results/retrieval-dev-weighted-v1/ANALYSIS.md).
2. `d7_dev_01` và `d7_dev_14`: evidence trải qua chunk boundary. E2 giữ seed trước, thêm hàng xóm một lớp, budget cả hai 6000 ký tự. Replay tăng coverage 9/15 → 10/15 nhờ `d7_dev_14`; ký tự trung bình tăng 2551 → 5272, khoảng 2,07 lần. `d7_dev_01` chưa được khắc phục ở replay vì cần mở rộng xa hơn và có candidate bị bỏ do budget. [Phân tích E2](../../results/context-dev-v1/ANALYSIS.md).

**Lý do chọn:** agent baseline dev đạt 30/30 điểm answer, không từ chối nhầm, dùng 54.626 token. Agent hàng xóm đạt 28/30, từ chối nhầm `d7_dev_13`, dùng 68.759 token. Do đó chọn baseline không hàng xóm; giữ toàn bộ kết quả không cải thiện. TF-IDF test đạt Hit@3 cao hơn dense nhưng không dùng để chọn lại. Mỗi tập chỉ 15/5 câu có đáp án nên không suy rộng chất lượng tổng quát.

## Agent và đánh giá

- Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:
  - `search_documents(query)`: model tự tạo query, chương trình embed và truy vấn pgvector thật. `finish_answer(status, answer, citations)` kết thúc với answered/abstain. Đây là native tool calling, không dùng mock để báo chất lượng.
  - Buộc retrieval trước trả lời; tối đa 2 search và 3 model call/câu. Top-k=3 mỗi search; tích lũy seed duy nhất theo thứ tự retrieval, chọn nguyên chunk dưới 6000 ký tự Unicode gồm ID/source/page và phân cách. Hàng xóm chỉ bật ở cấu hình E2; không có trong pipeline chọn.
  - Chỉ context tích lũy mới nhất còn hoạt động trong tool history, context cũ được thay bằng thông báo superseded. Không coi đây là giới hạn tổng input token vì prompt, câu hỏi và tool arguments vẫn chiếm token.
  - Citation answered kiểm tra ID thuộc context và có trong answer. Hỗ trợ ngữ nghĩa do học viên review. Với abstain, model đôi khi chèn citation inline dù danh sách `citations` rỗng; evaluator lấy hợp hai nguồn để không bỏ sót. Không sửa prompt/pipeline sau khi đã xem test.
  - Lỗi API/retriever/schema được ghi `status=error`, không thay bằng kết quả giả; test vẫn chạy các câu còn lại. Có một lần smoke lỗi kết nối, lưu riêng; các lượt benchmark dev/test chính không lỗi. Dừng khi finish hoặc hết giới hạn; lỗi giới hạn không giả thành abstention đúng.

| Cấu hình / split | Tool use | Số lượt gọi | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| Baseline / dev | 17/17 (100%) | 21 search, 38 model; 13 câu 1 search, 4 câu 2 search | 0:0, 1:0, 2:15; TB **2,00/2**, 30/30 (100%) | 34/34 (100%) | Answered: 15/15; mọi output: 17/17 | 2/2 (100%) | 0/15 (0%) |
| Có hàng xóm / dev | 17/17 (100%) | 20 search, 37 model; 14 câu 1 search, 3 câu 2 search | 0:1, 1:0, 2:14; TB **1,87/2**, 28/30 (93,3%) | 38/38 (100%) | Answered: 14/14; mọi output: 15/17 | 2/2 (100%) | 1/15 (6,7%) |
| Baseline = selected / test | 7/7 (100%) | 11 search, 18 model; 3 câu 1 search, 4 câu 2 search | 0:1, 1:0, 2:4; TB **1,60/2**, 8/10 (80%) | 14/14 (100%) | Answered: 4/4; mọi output: 7/7 | 2/2 (100%) | 1/5 (20%) |

Citation tính trên các ID khác nhau dùng trong mỗi output, không nhân theo số lần lặp cùng ID; tính cả inline references trong lời từ chối. Mẫu số grounded answer chỉ gồm câu có đáp án. Các mức điểm và citation support là nhãn học viên đã xác nhận, không phải tỷ lệ do model judge tự suy ra.

**Context 0/1/2:** baseline dev và hàng xóm dev đều 0:0, 1:0, 2:15; test 0:0, 1:0, 2:5 theo review học viên. Khớp nguyên văn tự động lần lượt 11/15, 11/15, 4/5. Test 05 giữ context=2 theo review, answer=0 vì từ chối nhầm; không sửa số khớp text thành 5/5. Sự khác biệt cần được hiểu là hai cách chấm và là giới hạn của việc xác nhận evidence tương đương.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| d7_dev_02, E1 | Có đáp án | Dense có evidence UCS/UCR ở rank 3; weighted khôi phục chunk này | Agent baseline trả đúng vai trò bột thịt và tiết nước bọt; citation trang 196 | Context=2, answer=2 theo review; minh họa câu có nguồn |
| d7_dev_13, neighbors | Có đáp án | 2 search; học viên chấm context đủ | Agent vẫn từ chối nêu tên khác/phân loại explicit memory | Context=2, answer=0; ví dụ lỗi sử dụng evidence |
| d7_test_01 | Có đáp án — shaping | 1 search; nguồn trang 207 | Successive approximations; citation `88340d9155ee…`, `681c63ff5c60…` | Context=2, answer=2; 2/2 citation đúng theo review |
| d7_test_02 | Có đáp án — reinforcers | 2 search; nguồn trang 208 | Sơ cấp bẩm sinh, thứ cấp có giá trị nhờ liên kết; 2 citation | Context=2, answer=2; 2/2 citation đúng |
| d7_test_03 | Có đáp án — latent learning | 2 search; nguồn trang 213–214 | Học tiềm ẩn; 2 citation về Tolman và ví dụ | Context=2, answer=2; 2/2 citation đúng |
| d7_test_04 | Có đáp án — recall/recognition | 1 search; nguồn trang 267 | Recall không gợi ý, recognition nhận ra khi gặp lại; 2 citation | Context=2, answer=2; 2/2 citation đúng |
| d7_test_05 | Có đáp án — flashbulb memory | 2 search; context chủ yếu định nghĩa/ví dụ | Từ chối trả lời về độ chính xác theo thời gian; 2 citation inline | Context=2 theo học viên; answer=0 do từ chối nhầm; 2/2 citation đúng theo review, không đồng nghĩa trả lời đủ |
| d7_test_06 | Thiếu bằng chứng — % cải thiện sau 5 tuần | 2 search; mô tả Yogo/Fujihara, không có % được hỏi | Không bịa phần trăm; 2 citation inline | Abstention đúng; 2/2 citation đúng theo review |
| d7_test_07 | Thiếu bằng chứng — số lần quan sát Bobo | 1 search; mô tả thí nghiệm, thiếu số lần chính xác | Từ chối cung cấp số lần; 2 citation inline | Abstention đúng; 2/2 citation đúng theo review |

- Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:
  - Retrieval query gốc: [dev](../../results/retrieval-dev-v1/), [weighted dev](../../results/retrieval-dev-weighted-v1/), [test](../../results/retrieval-test-v1/). Mỗi thư mục có `traces.json`, `summary.json`, README.
  - Replay context: [context-dev-v1](../../results/context-dev-v1/). Agent thật: [baseline dev](../../results/agent-dev-baseline-v1/), [neighbors dev](../../results/agent-dev-neighbors-v1/), [baseline/selected test](../../results/agent-test-baseline-v1/); mỗi thư mục có config và traces chứa tool args/results/context/answer/citation/usage/time.
  - Nhãn từng câu và từng citation: [review baseline dev](../../results/agent-dev-review-v1/agent-dev-baseline-v1/reviews.json), [review neighbors dev](../../results/agent-dev-review-v1/agent-dev-neighbors-v1/reviews.json), [review test](../../results/agent-test-review-v1/agent-test-baseline-v1/reviews.json). Các file Markdown cùng thư mục đặt câu hỏi, gold và context cạnh nhau cho người chấm. ID citation đầy đủ nằm trong trace/nhãn; bảng trên viết ngắn để đọc.
  - Lệnh và cách tái lập: [RUNNING.md](../../RUNNING.md), [test protocol](../../benchmark/TEST_RUN.md). Chạy kiểm tra code: `.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v` — **28 test đạt**. Mock chỉ xác minh logic code, không thay thế benchmark thật.
  - Agent median/câu: baseline dev **3,677 s**, neighbors dev **4,408 s**, test **4,760 s**. Mean context lần lượt **3089**, **5367**, **3800** ký tự. Thời gian retrieval/pack và model load được báo riêng trong summary, không coi là cùng một phép đo. Một lượt chạy mỗi cấu hình nên timing chịu ảnh hưởng cold/warm cache, mạng/API.
  - Token baseline dev **54.626**, neighbors dev **68.759**, test **28.529**; tổng ba lượt chính **151.914 token**. Chi phí ước tính tương ứng **0,009647 / 0,010607 / 0,004949 USD**, tổng **0,025204 USD**. Kể cả smoke thành công: khoảng **0,026701 USD** theo usage quan sát.
  - Ước tính hậu kiểm từ [bảng giá DeepSeek](https://api-docs.deepseek.com/quick_start/pricing/) kiểm tra 14/11/2026: off-peak USD/triệu token là cache-hit input **0,003**, cache-miss input **0,15**, output **0,6**. Các timestamp chạy là thứ Bảy UTC nên áp dụng mức cuối tuần. Công thức `(hit×0.003 + miss×0.15 + output×0.6)/1e6`; chi tiết tại [cost_estimate.json](../../results/cost_estimate.json), tái tính bằng `python -m src.estimate_costs`.
  - Đây là **ước tính, không phải hóa đơn**, chưa tính thuế/credit, biến động giá, request bị tính tiền nhưng không có response usage, điện và phần cứng. Không sửa `cost_usd=null` trong trace cũ; lưu ước tính riêng. Retrieval/embedding local không dùng API trả phí. Không gọi dịch vụ web search/OCR DeepSeek; `search_documents` chạy local.
- Kết quả trước/sau, ví dụ lỗi, đánh đổi và giới hạn:
  - Baseline được chọn vì tốt hơn neighbors trên dev về answer và token; E1/E2 không được trình bày như luôn cải thiện. Test độc lập có 4/5 câu có đáp án được trả lời đúng, 1/5 từ chối nhầm và 2/2 câu thiếu evidence được từ chối đúng theo review. Không diễn giải 8/10 điểm answer thành điểm rubric bài lab hoặc ngưỡng bonus.
  - Agent có thể tự chuyển query sang tiếng Anh và tìm nhiều lượt; trace giữ cả query gốc và từng query model tạo. Điều này giải thích khác biệt giữa retrieval query gốc và context agent, không chứng minh riêng tác động của dịch vì chưa có ablation dịch query.
  - Cùng corpus/chủ đề ở dev/test, bộ test nhỏ, nhãn do học viên xác nhận với AI hỗ trợ, không đánh giá mù. Không suy rộng tính đúng tuyệt đối hay tính an toàn của hệ thống.
  - Citation inline và danh sách citations không luôn đồng nhất, đặc biệt ở abstain. Loader review đã chuẩn hóa để đếm đủ; pipeline gốc vẫn giữ nguyên. Citation hỗ trợ thông tin đi kèm không bảo đảm agent đã trả lời đúng yêu cầu, như test 05.
  - Nội dung tài liệu được coi là dữ liệu trong prompt; chưa có benchmark adversarial prompt injection, không tuyên bố đã chứng minh khả năng chống tấn công. Không đưa đáp án chuẩn vào retrieval/model, không đánh giá bằng vector ngẫu nhiên.

## Thử thách nâng cao (nếu thực hiện)

- Tài liệu, nguồn, quyền sử dụng, số trang và phiên bản:
- Cách xử lý text, bảng, ảnh, biểu đồ; phạm vi index và phần chưa xử lý:
- Cách chia benchmark, schema evidence, model và cấu hình đã chốt trên dev:

| Nhóm test | Đạt / tổng | Tỷ lệ | Lỗi / nhận xét |
|---|---|---|---|
| Bảng | | | |
| Ảnh, sơ đồ | | | |
| Biểu đồ | | | |
| Multi-hop | | | |
| Text | | | |
| Thiếu bằng chứng | | | |
| **Toàn bộ** | | | |

- Trace, nhãn và evidence từng câu; thời gian, chi phí, lỗi hệ thống:
- Giới hạn, cách tái lập và đường dẫn benchmark: