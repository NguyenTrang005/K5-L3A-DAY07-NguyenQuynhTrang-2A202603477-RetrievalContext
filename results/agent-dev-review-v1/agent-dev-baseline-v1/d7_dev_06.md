# d7_dev_06 — agent-dev-baseline-v1

## Câu hỏi

Theo chương 6 — Learning, củng cố âm tính làm tăng hay giảm hành vi và tác động đến kích thích như thế nào?

## Nhãn benchmark

Có đáp án: True

Làm tăng hành vi bằng cách loại bỏ một kích thích khó chịu.

Evidence gốc: openstax_psychology2e, trang PDF gốc 206

In negative reinforcement, an undesirable stimulus is removed to increase a behavior.

## Kết quả agent

Status: answered

Theo chương 6 — Learning, củng cố âm tính (negative reinforcement) **làm tăng** hành vi: "reinforcement, even when it is negative, always increases a behavior" [c684632dce8f8ebc95fad71b9f50267013923da9eab37c397f743d3a01360862]. Cơ chế là một kích thích (thường là kích thích khó chịu) bị **loại bỏ** nhằm tăng hành vi [fb8c44ce1fe9449aa7a68ea4c828984a8c8c8f4b3584b463628b8186a5b37ad0].

Ví dụ trong tài liệu: hệ thống dây an toàn trên ô tô kêu "beep, beep, beep" cho đến khi bạn thắt dây; âm thanh gây khó chịu dừng lại khi bạn thực hiện hành vi mong muốn, làm tăng khả năng bạn thắt dây an toàn trong tương lai [fb8c44ce1fe9449aa7a68ea4c828984a8c8c8f4b3584b463628b8186a5b37ad0]. Tương tự, trong huấn luyện ngựa, người cưỡi tạo áp lực (kéo dây cương hoặc siết chân) rồi gỡ bỏ áp lực khi ngựa thực hiện hành vi mong muốn như rẽ hoặc tăng tốc; áp lực chính là kích thích âm mà ngựa muốn loại bỏ [fb8c44ce1fe9449aa7a68ea4c828984a8c8c8f4b3584b463628b8186a5b37ad0].

Tài liệu cũng lưu ý phân biệt củng cố âm tính với trừng phạt: trừng phạt luôn làm **giảm** hành vi — trừng phạt dương tính là thêm kích thích không mong muốn (ví dụ mắng học sinh để học sinh ngừng nhắn tin trong lớp), còn trừng phạt âm tính là loại bỏ kích thích dễ chịu (ví dụ lấy đi đồ chơi yêu thích khi trẻ cư xử sai) [c684632dce8f8ebc95fad71b9f50267013923da9eab37c397f743d3a01360862].

Lượt search: 1; token: 3031; context: 2658 ký tự.

## Kiểm tra tự động (không thay chấm nội dung)

{
  "exact_context_evidence_hit": false,
  "citation_list_matches_answer": true,
  "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."
}

## Citation cần đối chiếu

### c684632dce8f8ebc95fad71b9f50267013923da9eab37c397f743d3a01360862

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 206

einforcement, even when it is negative, always increases a behavior. In
contrast, punishment always decreases a behavior. In positive punishment, you add an undesirable stimulus
to decrease a behavior. An example of positive punishment is scolding a student to get the student to stop
texting in class. In this case, a stimulus (the reprimand) is added in order to decrease the behavior (texting in
class). In negative punishment, you remove a pleasant stimulus to decrease behavior. For example, when a
child misbehaves, a parent can take away a favorite toy. In this case, a stimulus (the toy) is removed in order to
194 6 • Learning
Access for free at openstax.org

### fb8c44ce1fe9449aa7a68ea4c828984a8c8c8f4b3584b463628b8186a5b37ad0

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 206

stimulus is removed to increase a behavior. For example, car
manufacturers use the principles of negative reinforcement in their seatbelt systems, which go “beep, beep,
beep” until you fasten your seatbelt. The annoying sound stops when you exhibit the desired behavior,
increasing the likelihood that you will buckle up in the future. Negative reinforcement is also used frequently
in horse training. Riders apply pressure—by pulling the reins or squeezing their legs—and then remove the
pressure when the horse performs the desired behavior, such as turning or speeding up. The pressure is the
negative stimulus that the horse wants to remove.
Punishment
Many people confuse negative reinforcement with punishment in operant conditioning, but they are two very
different mechanisms. Remember that r

## Toàn bộ context thực tế gửi model trước câu trả lời

[0a8b347bd7b46f8f27a8c740e4fa398079bb63a277b179f92a5b229267f78f5e | https://openstax.org/details/books/psychology-2e | page 204]
 stimulus (either reinforcement or
punishment) occurs soon after the
response.
TABLE 6.1
Psychologist B. F. Skinner saw that classical conditioning is limited to existing behaviors that are reflexively
elicited, and it doesn’t account for new behaviors such as riding a bike. He proposed a theory about how such
behaviors come about. Skinner believed that behavior is motivated by the consequences we receive for the
behavior: the reinforcements and punishments. His idea that learning is the result of consequences is based
on the law of effect, which was first proposed by psychologist Edward Thorndike. According to the law of
effect, behaviors that are followed by consequences that are satisfying to the organism are more likely to be
repeated, and behaviors that are followed by unpleasant cons

[fb8c44ce1fe9449aa7a68ea4c828984a8c8c8f4b3584b463628b8186a5b37ad0 | https://openstax.org/details/books/psychology-2e | page 206]
stimulus is removed to increase a behavior. For example, car
manufacturers use the principles of negative reinforcement in their seatbelt systems, which go “beep, beep,
beep” until you fasten your seatbelt. The annoying sound stops when you exhibit the desired behavior,
increasing the likelihood that you will buckle up in the future. Negative reinforcement is also used frequently
in horse training. Riders apply pressure—by pulling the reins or squeezing their legs—and then remove the
pressure when the horse performs the desired behavior, such as turning or speeding up. The pressure is the
negative stimulus that the horse wants to remove.
Punishment
Many people confuse negative reinforcement with punishment in operant conditioning, but they are two very
different mechanisms. Remember that r

[c684632dce8f8ebc95fad71b9f50267013923da9eab37c397f743d3a01360862 | https://openstax.org/details/books/psychology-2e | page 206]
einforcement, even when it is negative, always increases a behavior. In
contrast, punishment always decreases a behavior. In positive punishment, you add an undesirable stimulus
to decrease a behavior. An example of positive punishment is scolding a student to get the student to stop
texting in class. In this case, a stimulus (the reprimand) is added in order to decrease the behavior (texting in
class). In negative punishment, you remove a pleasant stimulus to decrease behavior. For example, when a
child misbehaves, a parent can take away a favorite toy. In this case, a stimulus (the toy) is removed in order to
194 6 • Learning
Access for free at openstax.org

## Chấm vào reviews.json

Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.
Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.
Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.
Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.
Sau khi đọc: reviewed_by tên người review, review_status=reviewed.
