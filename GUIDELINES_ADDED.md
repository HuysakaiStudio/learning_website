# Hướng Dẫn và Chú Thích Đã Thêm

## Tổng Quan
Đã thêm các chú thích hướng dẫn chi tiết cho việc tạo bài viết, tạo flashcard và giải thích về hệ thống bảng xếp hạng.

## 1. Tạo Bài Viết ([`templates/kien_thuc/tao_bai_viet.html`](templates/kien_thuc/tao_bai_viet.html))

### Đã thêm:

#### Hướng dẫn cú pháp MathJax & Markdown
- Công thức inline: `$x^2 + y^2 = z^2$`
- Công thức block: `$$\int_a^b f(x)dx$$`
- Định dạng văn bản: in đậm, in nghiêng, tiêu đề
- Phân cách nội dung

#### Nguyên tắc tạo bài viết nghiêm túc
✅ **Nội dung chính xác:** Đảm bảo kiến thức đúng, có nguồn gốc rõ ràng

✅ **Trình bày rõ ràng:** Sử dụng công thức MathJax đúng cú pháp, dễ đọc

✅ **Có ví dụ minh họa:** Giúp người học hiểu sâu hơn

✅ **Ngôn ngữ chuẩn mực:** Tránh viết tắt, lỗi chính tả

❌ **Không spam:** Không đăng nội dung trùng lặp, vô nghĩa

❌ **Không vi phạm:** Không chép nguyên văn từ nguồn khác mà không trích dẫn

💡 **Mẹo:** Bài viết chất lượng cao sẽ được ưu tiên hiển thị và nhận được nhiều lượt xem hơn!

## 2. Tạo Bộ Flashcard ([`templates/kien_thuc/tao_flashcard_set.html`](templates/kien_thuc/tao_flashcard_set.html))

### Đã thêm:

#### Hướng dẫn tạo Flashcard chất lượng

**Sử dụng MathJax cho công thức:**
- Mặt trước: `Tính đạo hàm của $f(x) = x^2$`
- Mặt sau: `$$f'(x) = 2x$$`

**Nguyên tắc tạo flashcard:**

✅ Ngắn gọn, súc tích - mỗi thẻ 1 khái niệm

✅ Câu hỏi rõ ràng, câu trả lời chính xác

✅ Sử dụng công thức MathJax đúng cú pháp: `$inline$` hoặc `$$block$$`

✅ Có ví dụ cụ thể khi cần thiết

❌ Không tạo thẻ quá dài, khó nhớ

❌ Không sao chép nguyên văn từ sách mà không hiểu

## 3. Thêm Flashcard ([`templates/kien_thuc/them_flashcard.html`](templates/kien_thuc/them_flashcard.html))

### Đã thêm:

#### Hướng dẫn sử dụng MathJax chi tiết

**Công thức inline:** `$x^2 + 1$` → hiển thị trong dòng

**Công thức block:** `$$\frac{a}{b}$$` → hiển thị riêng 1 dòng

**Ví dụ:**
- Mặt trước: `Tính $\int x^2 dx$`
- Mặt sau: `$$\int x^2 dx = \frac{x^3}{3} + C$$`

⚠️ **Lưu ý:** Mỗi thẻ nên ngắn gọn (1 khái niệm), dễ nhớ. Tránh tạo thẻ quá dài hoặc phức tạp!

## 4. Bảng Xếp Hạng ([`templates/leaderboard/index.html`](templates/leaderboard/index.html))

### Đã thêm:

#### Thông báo quan trọng về hệ thống xếp hạng

⚠️ **Lưu ý quan trọng:** Chỉ những bài thi ở chế độ **"Thi thật"** mới được tính vào bảng xếp hạng. Các bài luyện tập không ảnh hưởng đến thứ hạng của bạn.

## 5. Chọn Chế Độ Thi ([`templates/de_thi/chon_che_do.html`](templates/de_thi/chon_che_do.html))

### Đã thêm:

#### Cập nhật badge cho chế độ "Thi thật"
- Thay đổi từ "⭐ Nhận XP (lần đầu)" → "🏆 Tính vào bảng xếp hạng"

#### Thông báo về Bảng Xếp Hạng

🏆 **Lưu ý về Bảng Xếp Hạng**

**Chỉ những bài thi ở chế độ "Thi thật"** mới được tính vào hệ thống bảng xếp hạng. Các chế độ "Luyện tập" và "Luyện từng câu" giúp bạn học tập hiệu quả nhưng không ảnh hưởng đến thứ hạng. Hãy luyện tập kỹ trước khi thi thật để đạt kết quả tốt nhất! 💪

## Lợi Ích

### Cho Người Dùng:
1. **Hiểu rõ cách sử dụng MathJax** - Tạo nội dung học tập chất lượng cao với công thức toán học đẹp
2. **Biết nguyên tắc tạo nội dung** - Đảm bảo nội dung nghiêm túc, chính xác
3. **Hiểu hệ thống xếp hạng** - Biết chế độ nào tính điểm, động lực thi đấu rõ ràng

### Cho Hệ Thống:
1. **Nội dung chất lượng cao hơn** - Người dùng được hướng dẫn tạo nội dung tốt
2. **Giảm spam và nội dung kém** - Nguyên tắc rõ ràng ngăn chặn vi phạm
3. **Tăng tính công bằng** - Mọi người hiểu rõ cách thức tính điểm xếp hạng

## Tệp Đã Chỉnh Sửa

1. [`templates/kien_thuc/tao_bai_viet.html`](templates/kien_thuc/tao_bai_viet.html:176) - Thêm hướng dẫn MathJax và nguyên tắc
2. [`templates/kien_thuc/tao_flashcard_set.html`](templates/kien_thuc/tao_flashcard_set.html:126) - Thêm hướng dẫn tạo flashcard
3. [`templates/kien_thuc/them_flashcard.html`](templates/kien_thuc/them_flashcard.html:236) - Thêm hướng dẫn MathJax chi tiết
4. [`templates/leaderboard/index.html`](templates/leaderboard/index.html:236) - Thêm thông báo về bài thi thật
5. [`templates/de_thi/chon_che_do.html`](templates/de_thi/chon_che_do.html:272) - Thêm thông báo và cập nhật badge

## Ghi Chú Kỹ Thuật

- Tất cả các hướng dẫn được thiết kế với UI/UX nhất quán
- Sử dụng màu sắc phù hợp để phân biệt loại thông tin (xanh lá = hướng dẫn, vàng = cảnh báo)
- Responsive và dễ đọc trên mọi thiết bị
- Không ảnh hưởng đến logic backend hiện tại
