# d7_dev_05 — agent-dev-neighbors-v1

## Câu hỏi

Stimulus discrimination là gì?

## Nhãn benchmark

Có đáp án: True

Học cách phản ứng khác nhau với các kích thích tương tự nhau.

Evidence gốc: openstax_psychology2e, trang PDF gốc 202

When an organism learns
to respond differently to various stimuli that are similar, it is called stimulus discrimination.

## Kết quả agent

Status: answered

Stimulus discrimination (phân biệt kích thích) là hiện tượng sinh vật chỉ thể hiện phản ứng có điều kiện với đúng kích thích có điều kiện, chứ không phản ứng với các kích thích khác. Theo cách diễn đạt trong điều kiện hóa cổ điển: "the organism demonstrates the conditioned response only to the conditioned stimulus" [304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed].

Đây là hiện tượng ngược lại với stimulus generalization (tổng quát hóa kích thích) — khi sinh vật thể hiện phản ứng có điều kiện với những kích thích tương tự kích thích có điều kiện [57c962f711d9b9506eb04ef8e7a15017456eb6514c2bca39c0a210f128980e46].

Ví dụ trong tài liệu:
- Chó của Pavlov phân biệt được âm cơ bản vang lên trước khi được cho ăn với các âm khác (như tiếng chuông cửa), vì những âm kia không báo hiệu thức ăn đến [304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed].
- Tiger, con mèo, phân biệt tiếng đồ hộp và tiếng máy trộn điện: khi máy trộn chạy, cô không chạy vào bếp tìm thức ăn [304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed].
- Bệnh nhân ung thư Moisha phân biệt bác sĩ ung thư với các loại bác sĩ khác, học được cách không thấy mệt khi đi khám vì lý do khác [304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed].

Tài liệu cũng nêu cơ chế: nếu không cho ăn sau tiếng máy trộn nhưng vẫn cho ăn đều đặn sau tiếng đồ hộp, con vật sẽ nhanh chóng học cách phân biệt hai âm thanh, miễn là chúng đủ khác nhau để phân biệt được [57c962f711d9b9506eb04ef8e7a15017456eb6514c2bca39c0a210f128980e46].

Lượt search: 1; token: 3926; context: 5803 ký tự.

## Kiểm tra tự động (không thay chấm nội dung)

{
  "exact_context_evidence_hit": false,
  "citation_list_matches_answer": true,
  "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."
}

## Citation cần đối chiếu

### 304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 202

 it is called stimulus discrimination. In classical
conditioning terms, the organism demonstrates the conditioned response only to the conditioned stimulus.
Pavlov’s dogs discriminated between the basic tone that sounded before they were fed and other tones (e.g.,
the doorbell), because the other sounds did not predict the arrival of food. Similarly, Tiger, the cat,
discriminated between the sound of the can opener and the sound of the electric mixer. When the electric
mixer is going, Tiger is not about to be fed, so she does not come running to the kitchen looking for food. In our
other example, Moisha, the cancer patient, discriminated between oncologists and other types of doctors. She
learned not to feel ill when visiting doctors for other types of appointments, such as her annual phys

### 57c962f711d9b9506eb04ef8e7a15017456eb6514c2bca39c0a210f128980e46

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 202

ical.
On the other hand, when an organism demonstrates the conditioned response to stimuli that are similar to the
conditioned stimulus, it is called stimulus generalization, the opposite of stimulus discrimination. The more
similar a stimulus is to the conditioned stimulus, the more likely the organism is to give the conditioned
response. For instance, if the electric mixer sounds very similar to the electric can opener, Tiger may come
running after hearing its sound. But if you do not feed her following the electric mixer sound, and you continue
to feed her consistently after the electric can opener sound, she will quickly learn to discriminate between the
two sounds (provided they are sufficiently dissimilar that she can tell them apart). In our other example,
Moisha continued to feel i

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

[57c962f711d9b9506eb04ef8e7a15017456eb6514c2bca39c0a210f128980e46 | https://openstax.org/details/books/psychology-2e | page 202]
ical.
On the other hand, when an organism demonstrates the conditioned response to stimuli that are similar to the
conditioned stimulus, it is called stimulus generalization, the opposite of stimulus discrimination. The more
similar a stimulus is to the conditioned stimulus, the more likely the organism is to give the conditioned
response. For instance, if the electric mixer sounds very similar to the electric can opener, Tiger may come
running after hearing its sound. But if you do not feed her following the electric mixer sound, and you continue
to feed her consistently after the electric can opener sound, she will quickly learn to discriminate between the
two sounds (provided they are sufficiently dissimilar that she can tell them apart). In our other example,
Moisha continued to feel i

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

[d26581d541a565c2b643cac35295a3f38aaf67679d9f951dbd2cf05d586d07f7 | https://openstax.org/details/books/psychology-2e | page 204]
t behavior more likely to be
repeated in the future. For example, Spirit, a dolphin at the National Aquarium in Baltimore, does a flip in the
air when her trainer blows a whistle. The consequence is that she gets a fish.
Classical and Operant Conditioning Compared
Classical Conditioning Operant Conditioning
Conditioning
approach
An unconditioned stimulus (such as food) is paired
with a neutral stimulus (such as a bell). The neutral
stimulus eventually becomes the conditioned
stimulus, which brings about the conditioned
response (salivation).
The target behavior is followed by
reinforcement or punishment to either
strengthen or weaken it, so that the
learner is more likely to exhibit the desired
behavior in the future.
Stimulus
timing
The stimulus occurs immediately before the
response.
The

[7ce1718a092fa6ed0e20b44d12e5068de3849e9ea2921751811e11dcb0d97c53 | https://openstax.org/details/books/psychology-2e | page 204]
equences are less likely to be repeated
192 6 • Learning
Access for free at openstax.org

[304626c879221d4413d4a313726d7f6fe5f9ef7325429cf31fb98d2cd783baed | https://openstax.org/details/books/psychology-2e | page 202]
 it is called stimulus discrimination. In classical
conditioning terms, the organism demonstrates the conditioned response only to the conditioned stimulus.
Pavlov’s dogs discriminated between the basic tone that sounded before they were fed and other tones (e.g.,
the doorbell), because the other sounds did not predict the arrival of food. Similarly, Tiger, the cat,
discriminated between the sound of the can opener and the sound of the electric mixer. When the electric
mixer is going, Tiger is not about to be fed, so she does not come running to the kitchen looking for food. In our
other example, Moisha, the cancer patient, discriminated between oncologists and other types of doctors. She
learned not to feel ill when visiting doctors for other types of appointments, such as her annual phys

[3db4a461163c4e6a640f30be151bbf2be3274890e367e6064f562f366fb7add8 | https://openstax.org/details/books/psychology-2e | page 202]
ll whenever visiting other oncologists or other doctors in the same building as her
oncologist.
Behaviorism
John B. Watson, shown in Figure 6.8, is considered the founder of behaviorism. Behaviorism is a school of
thought that arose during the first part of the 20th century, which incorporates elements of Pavlov’s classical
conditioning (Hunt, 2007). In stark contrast with Freud, who considered the reasons for behavior to be hidden
in the unconscious, Watson championed the idea that all behavior can be studied as a simple stimulus-
response reaction, without regard for internal processes. Watson argued that in order for psychology to
become a legitimate science, it must shift its concern away from internal mental processes because mental
processes cannot be seen or measured. Instead, he as

## Chấm vào reviews.json

Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.
Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.
Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.
Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.
Sau khi đọc: reviewed_by tên người review, review_status=reviewed.
