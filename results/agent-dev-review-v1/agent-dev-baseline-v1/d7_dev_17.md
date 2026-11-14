# d7_dev_17 — agent-dev-baseline-v1

## Câu hỏi

Mê cung trong thí nghiệm học tiềm ẩn của Tolman được mô tả trong tài liệu có tổng chiều dài chính xác bao nhiêu mét?

## Nhãn benchmark

Có đáp án: False

Có mô tả thí nghiệm và 10 phiên không củng cố nhưng không có tổng chiều dài mê cung tính bằng mét.

## Kết quả agent

Status: abstain

Chưa đủ bằng chứng: các đoạn tài liệu hiện có chỉ mô tả thí nghiệm học tiềm ẩn của Tolman với chuột chạy trong mê cung và hình thành "cognitive map", sau 10 buổi không được củng cố thì đặt thức ăn ở goal box [338e794338d19ec4b1f7d7a5c09c243031fe19c7a27d3720b1b2c191567765e7], nhưng không nêu tổng chiều dài chính xác (mét) của mê cung. Vì vậy không thể xác định con số được hỏi.

Lượt search: 1; token: 2545; context: 2644 ký tự.

## Kiểm tra tự động (không thay chấm nội dung)

{
  "exact_context_evidence_hit": null,
  "citation_list_matches_answer": false,
  "note": "Automatic checks are not human content grades. All embedded citations count, including those omitted from the model citation list."
}

## Citation cần đối chiếu

### 338e794338d19ec4b1f7d7a5c09c243031fe19c7a27d3720b1b2c191567765e7

Trong context: True; trong danh sách citations: False; trong answer: True.

Nguồn: https://openstax.org/details/books/psychology-2e; trang PDF gốc 213

 group that was rewarded with food at the end of the maze. As the unreinforced rats
explored the maze, they developed a cognitive map: a mental picture of the layout of the maze (Figure 6.15).
After 10 sessions in the maze without reinforcement, food was placed in a goal box at the end of the maze. As
soon as the rats became aware of the food, they were able to find their way through the maze quickly, just as
quickly as the comparison group, which had been rewarded with food all along. This is known as latent
learning: learning that occurs but is not observable in behavior until there is a reason to demonstrate it.
6.3 • Operant Conditioning 201

## Toàn bộ context thực tế gửi model trước câu trả lời

[338e794338d19ec4b1f7d7a5c09c243031fe19c7a27d3720b1b2c191567765e7 | https://openstax.org/details/books/psychology-2e | page 213]
 group that was rewarded with food at the end of the maze. As the unreinforced rats
explored the maze, they developed a cognitive map: a mental picture of the layout of the maze (Figure 6.15).
After 10 sessions in the maze without reinforcement, food was placed in a goal box at the end of the maze. As
soon as the rats became aware of the food, they were able to find their way through the maze quickly, just as
quickly as the comparison group, which had been rewarded with food all along. This is known as latent
learning: learning that occurs but is not observable in behavior until there is a reason to demonstrate it.
6.3 • Operant Conditioning 201

[fb399a8fbb345cf3582b60bcedd3707a670dd35a01ba7571c5f7c45c26866e98 | https://openstax.org/details/books/psychology-2e | page 214]
FIGURE 6.15 Psychologist Edward Tolman found that rats use cognitive maps to navigate through a maze. Have you
ever worked your way through various levels on a video game? You learned when to turn left or right, move up or
down. In that case you were relying on a cognitive map, just like the rats in a maze. (credit: modification of work by
"FutUndBeidl"/Flickr)
Latent learning also occurs in humans. Children may learn by watching the actions of their parents but only
demonstrate it at a later date, when the learned material is needed. For example, suppose that Ravi’s dad
drives him to school every day. In this way, Ravi learns the route from his house to his school, but he’s never
driven there himself, so he has not had a chance to demonstrate that he’s learned the way. One morning Ravi’s


[f03f568015873bc0784cc91d90ba19dccff84db7d0d10422aef5b5520d8ff75e | https://openstax.org/details/books/psychology-2e | page 215]
fountain, a statue, or an escalator, adds information to our cognitive map that can be used later to help find our
way out of the building.
LINK T O LEARNING
Watch this video about Carlson's studies on cognitive maps and navigation in buildings (https://openstax.org/l/
carlsonmaps) to learn more.
6.4 Observational Learning (Modeling)
LEARNING OBJECTIVES
By the end of this section, you will be able to:
• Define observational learning
• Discuss the steps in the modeling process
• Explain the prosocial and antisocial effects of observational learning
Previous sections of this chapter focused on classical and operant conditioning, which are forms of associative
learning. In observational learning, we learn by watching others and then imitating, or modeling, what they
do or say. For instance, h

## Chấm vào reviews.json

Đọc nguồn, điền nhãn và lý do; null là chưa chấm, không phải 0.
Câu có đáp án: context_grade và answer_grade 0/1/2. Từ chối nhầm: answer_grade=0.
Câu thiếu evidence: abstention_correct true/false; context_grade/answer_grade giữ null.
Mỗi citation: supports_answer true/false và lý do; citation ngoài context không hợp lệ.
Sau khi đọc: reviewed_by tên người review, review_status=reviewed.
