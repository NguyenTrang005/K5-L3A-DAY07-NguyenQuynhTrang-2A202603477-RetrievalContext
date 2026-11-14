# E1 — Kết quả weighted RRF

Giả thuyết/cấu hình ghi trước trong benchmark/EXPERIMENTS.md.
Đã chạy trên 17 câu dev, không lỗi; mẫu số hit là 15 câu có đáp án.
Hash corpus bằng lần chạy v1; benchmark, query, filter, k và candidate giữ nguyên.

| Cấu hình | Hit@1 | Evidence Hit@3 |
|---|---:|---:|
| Dense (chạy lại) | 2/15 | 9/15 |
| RRF ngang trọng số (v1) | 3/15 | 8/15 |
| Weighted RRF dense 0.8 / lexical 0.2 | 2/15 | 9/15 |

Weighted khôi phục d7_dev_02, không làm mất câu Hit@3 nào so với hybrid v1.
Chunk ec76de95… có dense rank 3, TF-IDF rank 7. Chunk 6464d422… có dense
rank 4, TF-IDF rank 5. RRF ngang trọng số ưu tiên chunk thứ hai; weighted
0.8/0.2 đảo lại thứ tự, đưa evidence đủ UCS/UCR về top-3 trang 196.

Hit@3 tăng 1/15 so với hybrid ban đầu, nhưng Hit@1 giảm 1/15 và không vượt
dense. Chưa có bằng chứng nên chọn weighted thay dense. Chênh lệch thời gian
nhỏ của một lần chạy không đủ kết luận weighted nhanh hơn dense; hybrid vẫn
phải chạy thêm lexical. Chi phí API bằng 0, chưa tính điện/phần cứng.

Đã kiểm tra các chunk của d7_dev_02: hai chunk đầu mô tả Pavlov và phản ứng
chung; chunk ec76de95… mới nêu rõ meat powder=UCS, salivation=UCR. Chunk
trang 201 trong hybrid cũ nói spontaneous recovery nên không đủ trả lời.

Lệnh tái chạy từ root Day 7 (dùng thư mục output mới):

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -X utf8 -m src.benchmark_retrieval --cache-folder '..\..\Lab_6\K5-L3A-DAY06-NguyenQuynhTrang-2A202603477-DataIngestion\starter\.model_cache' --dense-weight 0.8 --lexical-weight 0.2 --output results/retrieval-dev-weighted-v2
```

Chưa chạy test, chưa đánh giá agent hay context. Bước tiếp theo dự kiến thử
context có chunk lân cận để xử lý evidence bị chia cắt, với budget công bố rõ.
