# ✅ Checklist Deploy PythonAnywhere

In ra và tick vào mỗi bước khi hoàn thành!

---

## 📋 CHUẨN BỊ

- [ ] Đã có tài khoản GitHub
- [ ] Đã push code lên GitHub
- [ ] Đã tạo file `.env` từ `.env.example`
- [ ] Đã test ứng dụng chạy được ở local

---

## 🚀 DEPLOY

### Bước 1: Đăng Ký (5 phút)
- [ ] Truy cập: https://www.pythonanywhere.com/registration/register/beginner/
- [ ] Điền username: ________________
- [ ] Điền email: ________________
- [ ] Tạo password
- [ ] Xác nhận email
- [ ] Đăng nhập thành công

### Bước 2: Upload Code (10 phút)
- [ ] Mở Bash Console
- [ ] Clone repository: `git clone https://github.com/USERNAME/learning-web.git`
- [ ] Vào folder: `cd learning-web`
- [ ] Kiểm tra files: `ls -la`

### Bước 3: Virtual Environment (5 phút)
- [ ] Tạo venv: `python3.11 -m venv venv`
- [ ] Kích hoạt: `source venv/bin/activate`
- [ ] Upgrade pip: `pip install --upgrade pip`
- [ ] Cài dependencies: `pip install -r requirements.txt`
- [ ] Đợi cài đặt xong (2-3 phút)

### Bước 4: Tạo Web App (3 phút)
- [ ] Vào tab "Web"
- [ ] Click "Add a new web app"
- [ ] Chọn domain: `USERNAME.pythonanywhere.com`
- [ ] Chọn "Manual configuration"
- [ ] Chọn "Python 3.11"
- [ ] Hoàn tất

### Bước 5: Cấu Hình WSGI (5 phút)
- [ ] Click vào "WSGI configuration file"
- [ ] Xóa tất cả nội dung cũ
- [ ] Dán code mới (nhớ thay `YOUR_USERNAME`)
- [ ] Kiểm tra lại đường dẫn
- [ ] Click "Save"

### Bước 6: Static Files (2 phút)
- [ ] Trong tab "Web", phần "Static files"
- [ ] URL: `/static/`
- [ ] Path: `/home/USERNAME/learning-web/staticfiles`
- [ ] (Optional) URL: `/media/`, Path: `/home/USERNAME/learning-web/media`

### Bước 7: Database (5 phút)
- [ ] Quay lại Bash Console
- [ ] `cd learning-web`
- [ ] `source venv/bin/activate`
- [ ] Tạo `.env` với SECRET_KEY
- [ ] Thêm DEBUG=False vào `.env`
- [ ] Thêm ALLOWED_HOSTS vào `.env`
- [ ] Chạy: `python manage.py migrate`
- [ ] Chạy: `python manage.py collectstatic --noinput`
- [ ] Chạy: `python manage.py createsuperuser`
- [ ] Nhập username admin: ________________
- [ ] Nhập email: ________________
- [ ] Nhập password

### Bước 8: Reload & Test (2 phút)
- [ ] Vào tab "Web"
- [ ] Click nút "Reload USERNAME.pythonanywhere.com"
- [ ] Đợi 10-20 giây
- [ ] Truy cập: `https://USERNAME.pythonanywhere.com`
- [ ] Kiểm tra trang chủ hiển thị
- [ ] Kiểm tra CSS/JS load được
- [ ] Thử đăng nhập
- [ ] Truy cập admin: `/admin/`
- [ ] Đăng nhập admin thành công

---

## ✅ HOÀN TẤT!

- [ ] Website online: https://________________.pythonanywhere.com
- [ ] Admin hoạt động: https://________________.pythonanywhere.com/admin/
- [ ] Đã test các chức năng chính
- [ ] Đã lưu thông tin đăng nhập

---

## 📝 THÔNG TIN QUAN TRỌNG

**PythonAnywhere Username:** ________________

**Website URL:** https://________________.pythonanywhere.com

**Admin Username:** ________________

**Admin Password:** ________________ (lưu ở nơi an toàn!)

**GitHub Repo:** https://github.com/________________/learning-web

---

## 🔄 CẬP NHẬT SAU NÀY

Mỗi khi cập nhật code:

- [ ] Push code lên GitHub
- [ ] Mở Bash Console trên PythonAnywhere
- [ ] `cd learning-web`
- [ ] `git pull`
- [ ] `source venv/bin/activate`
- [ ] `python manage.py migrate` (nếu có migrations mới)
- [ ] `python manage.py collectstatic --noinput` (nếu có static files mới)
- [ ] Vào tab "Web" → Click "Reload"
- [ ] Test website

---

## ❌ NẾU GẶP LỖI

### Lỗi 502 Bad Gateway
- [ ] Kiểm tra WSGI file
- [ ] Kiểm tra đường dẫn trong WSGI
- [ ] Kiểm tra đã thay `YOUR_USERNAME` đúng chưa
- [ ] Reload web app

### Static Files Không Load
- [ ] Chạy: `python manage.py collectstatic --noinput`
- [ ] Kiểm tra Static files mapping trong tab Web
- [ ] Reload web app

### DisallowedHost Error
- [ ] Kiểm tra file `.env`
- [ ] Sửa ALLOWED_HOSTS=USERNAME.pythonanywhere.com
- [ ] Reload web app

### Xem Logs
- [ ] Tab "Web" → "Error log"
- [ ] Tab "Web" → "Server log"

---

## 📞 TRỢ GIÚP

- Hướng dẫn chi tiết: [`PYTHONANYWHERE_STEP_BY_STEP.md`](PYTHONANYWHERE_STEP_BY_STEP.md)
- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/

---

**Tổng thời gian dự kiến: ~35 phút**

**Chúc bạn deploy thành công! 🎉**
