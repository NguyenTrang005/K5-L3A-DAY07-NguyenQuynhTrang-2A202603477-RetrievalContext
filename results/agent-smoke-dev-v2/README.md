# DeepSeek agent — smoke test thật trên dev

Hai câu dev, không đọc gold trong chương trình chạy, không chạy test.
Traces lưu native tool calls, query do model tạo, context, câu trả lời và usage.

| Câu | Trạng thái model | Lượt search | Lượt model | Total tokens |
|---|---|---:|---:|---:|
| d7_dev_02 | answered | 1 | 2 | 3531 |
| d7_dev_16 | abstain | 2 | 3 | 5850 |
| Tổng | | 3 | 5 | 9381 |

Cấu hình: dense, hàng xóm bật, budget 6000 ký tự, tối đa 2 search; thinking
disabled, temperature 0, max_tokens 1200. Xem config.json và response model
thực tế trong traces.json. Chi phí USD chưa tính, không đồng nghĩa API miễn phí.

## Đọc kết quả ban đầu (AI hỗ trợ, chưa phải nhãn chấm của học viên)

- d7_dev_02 trả đúng bột thịt=UCS, tiết nước bọt=UCR. Citation ec76de95… chứa
  hai định nghĩa; citation 9371a991… chứa thông tin tiết nước bọt khi có thức ăn
  là phản xạ không cần học. Các ID đều có trong context thực tế đã gửi model.
- d7_dev_16 từ chối cung cấp phần trăm tăng điểm thi không có evidence.
  Tuy nhiên model thêm giải thích thực tế trong lời từ chối nhưng không dẫn
  citation, dù prompt yêu cầu abstention chỉ nêu thiếu bằng chứng. Học viên cần
  kiểm tra phần thêm này với context trước khi chấm abstention_correct; không
  chỉ dựa vào status=abstain để kết luận câu đạt.

Đây chỉ là kiểm tra kết nối và hành vi hai câu, không phải benchmark toàn dev,
không đủ để chọn cấu hình hoặc báo tỷ lệ thành công tổng quát.
Thư mục agent-smoke-dev-v1 lưu lần kết nối lỗi trong môi trường hạn chế mạng,
không dùng lần đó làm kết quả chất lượng hoặc thay bằng kết quả giả.

Tái chạy: xem src/README.md, dùng output mới. Bước tiếp theo là chạy baseline
và context lân cận trên cùng dev, chấm context/answer/citation/abstention riêng.
