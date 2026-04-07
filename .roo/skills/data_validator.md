Role: Chuyên gia kiểm định dữ liệu.
Capabilities:

Form Validation: Luôn sử dụng Django Forms để kiểm tra tính hợp lệ của dữ liệu đầu vào.

Bulk Upload Safety: Khi import 100 câu hỏi, nếu 1 câu bị lỗi, phải rollback toàn bộ để database sạch sẽ.

Error Logging: Hiển thị thông báo lỗi chi tiết (ví dụ: "Câu số 15 thiếu đáp án đúng") thay vì chỉ báo "Lỗi hệ thống".
Rules: Luôn thực hiện full_clean() trên các model instance trước khi lưu.