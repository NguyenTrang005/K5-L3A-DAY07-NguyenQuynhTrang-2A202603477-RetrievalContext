# Nhận xét dev lần đầu

Đã chạy 3 phương pháp × 17 câu = 51 truy vấn; không lỗi. Mỗi phương pháp
được chấm hit trên 15 câu có đáp án. Hai câu thiếu bằng chứng chỉ lưu retrieval,
không chấm abstention khi chưa có agent.

## Lỗi và giả thuyết để thử tiếp

1. TF-IDF không trả kết quả cho 9 câu dev có đáp án: 01, 03, 04, 07, 08,
   11, 13, 14, 15. Token query không trùng vocabulary corpus theo tokenizer hiện
   tại. Query tiếng Việt, tài liệu tiếng Anh; đây là giới hạn lớn của lexical
   không dịch. Giả thuyết: viết lại/dịch query sang tiếng Anh bằng model có thể
   cải thiện lexical. Nếu thử phải giữ kết quả query gốc này và báo pipeline
   biến đổi query riêng; không dịch dựa trên đáp án hoặc gold.
2. Hybrid làm mất hit top-3 của `d7_dev_02` so với dense, không thêm câu hit mới.
   Fusion hiện tăng Hit@1 từ 2 lên 3 nhưng giảm Hit@3 từ 9 xuống 8. Giả thuyết:
   trọng số lexical ngang dense chưa phù hợp khi lexical yếu; có thể thử weighted
   RRF trên dev, công bố trọng số và kết quả kể cả khi không tăng.
3. Dense còn thiếu evidence đầy đủ ở dev 01, 03, 05, 06, 08, 14. Các câu 01,
   05, 06, 14 có evidence qua ranh giới chunk. Có thể thử chọn chunk lân cận cho
   context, nhưng cần phân biệt cải thiện context với ranking top-3 và đo budget.

Các giả thuyết trên chưa được thử ở lần chạy này. Đây là đánh giá retrieval
tự động, không chứng minh chất lượng câu trả lời. Chưa chọn cấu hình cuối,
chưa chạy test và chưa gọi model sinh câu trả lời.
