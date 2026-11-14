# d7_test_04 — agent-test-baseline-v1

## Câu hỏi

Recall và recognition khác nhau như thế nào về việc sử dụng gợi ý hoặc gặp lại thông tin?

## Nhãn benchmark

Có đáp án: True

Recall là truy cập thông tin mà không có gợi ý; recognition là nhận ra thông tin đã học khi gặp lại thông tin đó.

Evidence gốc: openstax_psychology2e, trang PDF gốc 267

Recall is what we most often think about when we talk about memory retrieval: it
means you can access information without cues.

Evidence gốc: openstax_psychology2e, trang PDF gốc 267

Recognition happens when you identify information that you have previously learned after encountering it
again.

## Kết quả agent

Status: answered

Theo giáo trình, có ba cách truy xuất thông tin từ bộ nhớ dài hạn: recall (nhớ lại), recognition (nhận ra) và relearning (học lại) [96da03b961decd95a55b48913595e28f4af6bcd660fa4ff459493b6217ae92a2].

- **Recall** là việc truy xuất thông tin **không cần gợi ý (cues)** — ví dụ bạn dùng recall khi làm bài thi tự luận [35e8bab52f2d44d3644cf2360fe2df54652bcc7bb94d1b16bde7d11297c416e1].
- **Recognition** xảy ra khi bạn **nhận diện thông tin đã học trước đó sau khi gặp lại nó**, và nó bao gồm một quá trình so sánh. Ví dụ: làm bài trắc nghiệm là dựa vào recognition để chọn đáp án đúng; hay khi dự họp lớp sau 10 năm, bạn có thể không recall được tất cả bạn học nhưng lại nhận ra nhiều người nhờ ảnh kỷ yếu [35e8bab52f2d44d3644cf2360fe2df54652bcc7bb94d1b16bde7d11297c416e1].

Tóm lại, điểm khác biệt cốt lõi là recall đòi hỏi truy xuất mà không có gợi ý, còn recognition diễn ra khi thông tin được gặp lại và bạn so sánh/nhận diện nó [35e8bab52f2d44d3644cf2360fe2df54652bcc7bb94d1b16bde7d11297c416e1].

Lượt search: 1; token: 2855; context: 2791 ký tự.

## Kiểm tra tự động (không thay chấm nội dung)

{
  "exact_context_evidence_hit": true,
  "citation_list_matches_answer": true,
  "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."
}

## Citation cần đối chiếu

### 96da03b961decd95a55b48913595e28f4af6bcd660fa4ff459493b6217ae92a2

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 267

information out of memory storage and back into conscious awareness is known as retrieval. This would be
similar to finding and opening a paper you had previously saved on your computer’s hard drive. Now it’s back
on your desktop, and you can work with it again. Our ability to retrieve information from long-term memory is
vital to our everyday functioning. You must be able to retrieve information from memory in order to do
everything from knowing how to brush your hair and teeth, to driving to work, to knowing how to perform your
job once you get there.
There are three ways you can retrieve information out of your long-term memory storage system: recall,
recognition, and relearning. Recall is what we most often think about when we talk about memory retrieval: it
means you can access inform

### 35e8bab52f2d44d3644cf2360fe2df54652bcc7bb94d1b16bde7d11297c416e1

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 267

ation without cues. For example, you would use recall for an essay test.
Recognition happens when you identify information that you have previously learned after encountering it
again. It involves a process of comparison. When you take a multiple-choice test, you are relying on
recognition to help you choose the correct answer. Here is another example. Let’s say you graduated from high
school 10 years ago, and you have returned to your hometown for your 10-year reunion. You may not be able to
recall all of your classmates, but you recognize many of them based on their yearbook photos.
The third form of retrieval is relearning, and it’s just what it sounds like. It involves learning information that
you previously learned. Whitney took Spanish in high school, but after high school she did n

## Toàn bộ context thực tế gửi model trước câu trả lời

[96da03b961decd95a55b48913595e28f4af6bcd660fa4ff459493b6217ae92a2 | https://openstax.org/details/books/psychology-2e | page 267]
information out of memory storage and back into conscious awareness is known as retrieval. This would be
similar to finding and opening a paper you had previously saved on your computer’s hard drive. Now it’s back
on your desktop, and you can work with it again. Our ability to retrieve information from long-term memory is
vital to our everyday functioning. You must be able to retrieve information from memory in order to do
everything from knowing how to brush your hair and teeth, to driving to work, to knowing how to perform your
job once you get there.
There are three ways you can retrieve information out of your long-term memory storage system: recall,
recognition, and relearning. Recall is what we most often think about when we talk about memory retrieval: it
means you can access inform

[35e8bab52f2d44d3644cf2360fe2df54652bcc7bb94d1b16bde7d11297c416e1 | https://openstax.org/details/books/psychology-2e | page 267]
ation without cues. For example, you would use recall for an essay test.
Recognition happens when you identify information that you have previously learned after encountering it
again. It involves a process of comparison. When you take a multiple-choice test, you are relying on
recognition to help you choose the correct answer. Here is another example. Let’s say you graduated from high
school 10 years ago, and you have returned to your hometown for your 10-year reunion. You may not be able to
recall all of your classmates, but you recognize many of them based on their yearbook photos.
The third form of retrieval is relearning, and it’s just what it sounds like. It involves learning information that
you previously learned. Whitney took Spanish in high school, but after high school she did n

[cf151fc41cd78266e685c5340060946e3ea6f09b188b4ba2e5ecb94a4a266ebf | https://openstax.org/details/books/psychology-2e | page 263]
e "magic number" 7 plus or minus 2. However, more contemporary research has found
working memory capacity is 4 plus or minus 1 (Cowan, 2010). Generally, recall is somewhat better for random
numbers than for random letters (Jacobs, 1887) and also often slightly better for information we hear (acoustic
encoding) rather than information we see (visual encoding) (Anderson, 1969).
Memory trace decay and interference are two factors that affect short-term memory retention. Peterson and
Peterson (1959) investigated short-term memory using the three letter sequences called trigrams (e.g., CLS)
that had to be recalled after various time intervals between 3 and 18 seconds. Participants remembered about
80% of the trigrams after a 3-second delay, but only 10% after a delay of 18 seconds, which caused

## Chấm vào reviews.json

Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.
Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.
Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.
Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.
Sau khi đọc: reviewed_by tên người review, review_status=reviewed.
