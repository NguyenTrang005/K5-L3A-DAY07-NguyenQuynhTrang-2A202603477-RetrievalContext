# d7_dev_14 — agent-dev-baseline-v1

## Câu hỏi

Thông tin cũ cản trở việc nhớ thông tin mới thuộc loại nhiễu nào? Chiều ngược lại gọi là gì?

## Nhãn benchmark

Có đáp án: True

Proactive interference: cũ cản trở mới. Retroactive interference: mới cản trở cũ.

Evidence gốc: openstax_psychology2e, trang PDF gốc 280

These are examples of proactive interference: when old information hinders the recall of newly learned
information. Retroactive interference happens when information learned more recently hinders the recall of
older information.

## Kết quả agent

Status: answered

Thông tin cũ cản trở việc học/nhớ thông tin mới là **nhiễu tiến (proactive interference)**: "previously learned information interferes with the ability to learn new information" [9b07854c25ff6753b19a2b6dab6b4f6c70b65e1eee0a44a15f6c6c2e24111e88].

Chiều ngược lại là **nhiễu ngược (retroactive interference)**, xảy ra khi thông tin học gần đây hơn cản trở việc nhớ lại thông tin cũ hơn [2fe09a87164de258f0e1c9957712d50c247d3716cbfef1e66fa1c19222a40051].

Lượt search: 1; token: 2442; context: 1945 ký tự.

## Kiểm tra tự động (không thay chấm nội dung)

{
  "exact_context_evidence_hit": false,
  "citation_list_matches_answer": true,
  "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."
}

## Citation cần đối chiếu

### 9b07854c25ff6753b19a2b6dab6b4f6c70b65e1eee0a44a15f6c6c2e24111e88

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 263

 them to
conclude that short-term memory decayed in 18 seconds. During decay, the memory trace becomes less
activated over time, and the information is forgotten. However, Keppel and Underwood (1962) examined only
the first trials of the trigram task and found that proactive interference also affected short-term memory
retention. During proactive interference, previously learned information interferes with the ability to learn
new information. Both memory trace decay and proactive interference affect short-term memory. Once the
information reaches long-term memory, it has to be consolidated at both the synaptic level, which takes a few
hours, and into the memory system, which can take weeks or longer.
Long-term Memory
Long-term memory (LTM) is the continuous storage of information. Unlike 

### 2fe09a87164de258f0e1c9957712d50c247d3716cbfef1e66fa1c19222a40051

Trong context: True; trong danh sách citations: True; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 280

ctive interference happens when information learned more recently hinders the recall of
older information. For example, this week you are studying about memory and learn about the Ebbinghaus
forgetting curve. Next week you study lifespan development and learn about Erikson's theory of psychosocial
development, but thereafter have trouble remembering Ebbinghaus's work because you can only remember
Erickson's theory.
268 8 • Memory
Access for free at openstax.org

## Toàn bộ context thực tế gửi model trước câu trả lời

[2fe09a87164de258f0e1c9957712d50c247d3716cbfef1e66fa1c19222a40051 | https://openstax.org/details/books/psychology-2e | page 280]
ctive interference happens when information learned more recently hinders the recall of
older information. For example, this week you are studying about memory and learn about the Ebbinghaus
forgetting curve. Next week you study lifespan development and learn about Erikson's theory of psychosocial
development, but thereafter have trouble remembering Ebbinghaus's work because you can only remember
Erickson's theory.
268 8 • Memory
Access for free at openstax.org

[9b07854c25ff6753b19a2b6dab6b4f6c70b65e1eee0a44a15f6c6c2e24111e88 | https://openstax.org/details/books/psychology-2e | page 263]
 them to
conclude that short-term memory decayed in 18 seconds. During decay, the memory trace becomes less
activated over time, and the information is forgotten. However, Keppel and Underwood (1962) examined only
the first trials of the trigram task and found that proactive interference also affected short-term memory
retention. During proactive interference, previously learned information interferes with the ability to learn
new information. Both memory trace decay and proactive interference affect short-term memory. Once the
information reaches long-term memory, it has to be consolidated at both the synaptic level, which takes a few
hours, and into the memory system, which can take weeks or longer.
Long-term Memory
Long-term memory (LTM) is the continuous storage of information. Unlike 

[463301a2b387a49b161264fdd87d315f97f448fec5309ea76692e9be906d7bc9 | https://openstax.org/details/books/psychology-2e | page 268]
m with
other memories. It also plays a part in memory consolidation: the process of transferring new learning into
long-term memory.
Injury to this area leaves us unable to process new declarative memories. One famous patient, known for years
256 8 • Memory
Access for free at openstax.org

## Chấm vào reviews.json

Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.
Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.
Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.
Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.
Sau khi đọc: reviewed_by tên người review, review_status=reviewed.
