# Hướng dẫn cài đặt chế độ Luyện từng câu (Wayground-style)

## ✅ Đã hoàn thành

Chế độ luyện tập kiểu Wayground đã được implement thành công với các tính năng:

### 🎯 Tính năng chính
- ✅ Làm từng câu hỏi một (không hiển thị tất cả câu cùng lúc)
- ✅ Phản hồi ngay lập tức sau khi trả lời (đúng/sai + giải thích)
- ✅ Nút "Tiếp tục" để chuyển sang câu tiếp theo
- ✅ Thanh tiến độ hiển thị số câu đã làm / tổng số câu
- ✅ Lưu lịch sử và tính điểm (không tính vào leaderboard)
- ✅ Hỗ trợ đầy đủ 3 loại câu hỏi: Trắc nghiệm, Đúng/Sai, Điền số

### 📁 Files đã tạo/sửa

**Backend:**
- ✅ `apps/de_thi/models.py` - Thêm model `PracticeSession`
- ✅ `apps/de_thi/views.py` - Thêm 3 views mới:
  - `bat_dau_luyen_tung_cau` - Khởi tạo session
  - `hien_thi_cau_hoi` - Hiển thị câu hỏi hiện tại
  - `submit_cau_tra_loi` - AJAX endpoint trả về feedback
- ✅ `apps/de_thi/urls.py` - Thêm 3 URL routes mới
- ✅ `apps/de_thi/migrations/0008_practicesession.py` - Migration file

**Frontend:**
- ✅ `templates/de_thi/luyen_tung_cau.html` - Template câu hỏi đơn với feedback overlay
- ✅ `templates/de_thi/chon_che_do.html` - Cập nhật UI với 3 chế độ đẹp mắt

**Documentation:**
- ✅ `plans/practice-mode-wayground-style.md` - Kế hoạch chi tiết

## 🚀 Cài đặt

### Bước 1: Kích hoạt Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Bước 2: Chạy Migration

```bash
python manage.py migrate de_thi
```

Kết quả mong đợi:
```
Running migrations:
  Applying de_thi.0008_practicesession... OK
```

### Bước 3: Khởi động Server

```bash
python manage.py runserver
```

## 📖 Cách sử dụng

### Cho người dùng:

1. Truy cập trang danh sách đề thi: `http://localhost:8000/de-thi/`
2. Chọn một đề thi bất kỳ
3. Trên trang chọn chế độ, chọn **"🎯 Luyện từng câu"**
4. Làm từng câu hỏi:
   - Đọc câu hỏi và chọn đáp án
   - Click "✓ Kiểm tra đáp án"
   - Xem feedback (đúng/sai + giải thích)
   - Click "→ Câu tiếp theo" để tiếp tục
5. Sau câu cuối cùng, click "🎉 Xem kết quả"
6. Xem tổng kết điểm số và có thể xem lại đáp án chi tiết

### Luồng hoạt động:

```
Chọn đề thi
    ↓
Chọn "Luyện từng câu"
    ↓
Tạo PracticeSession + KetQua
    ↓
Hiển thị câu hỏi 1
    ↓
Người dùng trả lời
    ↓
Submit qua AJAX
    ↓
Lưu TraLoi + Hiển thị feedback
    ↓
Click "Tiếp tục"
    ↓
Câu tiếp theo (lặp lại)
    ↓
Câu cuối cùng → Tính tổng điểm
    ↓
Hiển thị kết quả
```

## 🧪 Testing

### Test Case 1: Câu hỏi Trắc nghiệm (tn)
1. Chọn đề có câu trắc nghiệm ABCD
2. Chọn đáp án và kiểm tra
3. Xác nhận feedback hiển thị đúng/sai
4. Xác nhận đáp án đúng được highlight

### Test Case 2: Câu hỏi Đúng/Sai (ds)
1. Chọn đề có câu đúng/sai 4 ý
2. Chọn đúng/sai cho từng ý
3. Xác nhận điểm được tính theo thang MOET (0.1, 0.25, 0.5, 1.0)
4. Xác nhận bảng đáp án hiển thị đầy đủ 4 ý

### Test Case 3: Câu hỏi Điền số (dien)
1. Chọn đề có câu điền số
2. Nhập số và kiểm tra
3. Xác nhận so sánh với sai số 0.001
4. Xác nhận đáp án đúng hiển thị

### Test Case 4: Thanh tiến độ
1. Xác nhận thanh tiến độ cập nhật sau mỗi câu
2. Xác nhận % hoàn thành chính xác

### Test Case 5: Kết quả cuối cùng
1. Hoàn thành tất cả câu hỏi
2. Xác nhận điểm được tính đúng (tổng điểm / tổng câu * 10)
3. Xác nhận lưu vào lịch sử với `che_do='luyen_tung_cau'`
4. Xác nhận `is_official=False` (không tính leaderboard)

## 🎨 UI/UX Features

### Trang chọn chế độ:
- ✨ Animation fade-in khi load
- 🎯 Hover effects với gradient backgrounds
- 📱 Responsive design (mobile-friendly)
- 💡 Gợi ý chọn chế độ phù hợp
- 🎨 Header gradient đẹp mắt với thông tin đề thi

### Trang làm bài:
- 📊 Thanh tiến độ real-time
- 🎭 Feedback overlay với animation
- ✅ Highlight đáp án đã chọn
- 💬 Giải thích chi tiết (nếu có)
- 🎯 Icon và màu sắc rõ ràng cho từng loại câu

## 🔧 Troubleshooting

### Lỗi: "No module named 'django'"
**Giải pháp:** Kích hoạt virtual environment trước khi chạy lệnh

### Lỗi: Migration already exists
**Giải pháp:** Migration đã được tạo sẵn, chỉ cần chạy `python manage.py migrate`

### Lỗi: CSRF token missing
**Giải pháp:** Đảm bảo `{% csrf_token %}` có trong form và header AJAX

### Lỗi: 404 Not Found
**Giải pháp:** Kiểm tra URL patterns trong `apps/de_thi/urls.py`

## 📊 Database Schema

### Model: PracticeSession
```python
- nguoi_dung: ForeignKey(User)
- de_thi: ForeignKey(DeThi)
- ket_qua: OneToOneField(KetQua)
- cau_hien_tai: IntegerField (0-based index)
- da_hoan_thanh: BooleanField
- ngay_bat_dau: DateTimeField
- ngay_cap_nhat: DateTimeField
```

### Quan hệ với models hiện có:
- `PracticeSession` → `KetQua` (1-1)
- `KetQua` → `TraLoi` (1-N)
- `KetQua.che_do = 'luyen_tung_cau'`
- `KetQua.is_official = False`

## 🎯 Điểm khác biệt với chế độ khác

| Tính năng | Luyện tập | Luyện từng câu | Thi thật |
|-----------|-----------|----------------|----------|
| Hiển thị | Tất cả câu | Từng câu một | Tất cả câu |
| Feedback | Sau khi nộp | Ngay lập tức | Sau khi nộp |
| Thời gian | Không giới hạn | Không giới hạn | Có giới hạn |
| Xem đáp án | Sau nộp (>6đ) | Ngay lập tức | Sau nộp (>6đ) |
| Leaderboard | ❌ | ❌ | ✅ |
| Lưu lịch sử | ✅ | ✅ | ✅ |

## 📝 Notes

- Chế độ này được thiết kế để học tập hiệu quả, không phải để thi
- Feedback ngay lập tức giúp ghi nhớ tốt hơn
- Phù hợp với học sinh muốn hiểu sâu từng câu hỏi
- Không tạo áp lực thời gian, tập trung vào việc học

## 🎉 Hoàn thành!

Chế độ luyện từng câu đã sẵn sàng sử dụng. Hãy test và báo lỗi nếu có vấn đề!
