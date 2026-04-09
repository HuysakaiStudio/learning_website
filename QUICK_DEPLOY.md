# 🚀 Deploy Nhanh - PythonAnywhere

Hướng dẫn deploy nhanh nhất cho người mới bắt đầu.

---

## Bước 1: Đăng Ký PythonAnywhere (2 phút)

1. Truy cập: https://www.pythonanywhere.com/registration/register/beginner/
2. Điền thông tin đăng ký (KHÔNG cần credit card)
3. Xác nhận email

---

## Bước 2: Upload Code (5 phút)

### Cách 1: Từ GitHub (Khuyến nghị)

```bash
# 1. Push code lên GitHub trước
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/learning-web.git
git push -u origin main

# 2. Trên PythonAnywhere, mở Bash console
git clone https://github.com/USERNAME/learning-web.git
cd learning-web
```

### Cách 2: Upload Trực Tiếp

1. Vào tab "Files"
2. Tạo folder `learning-web`
3. Upload tất cả file vào folder đó

---

## Bước 3: Setup Virtual Environment (3 phút)

```bash
# Trong Bash console trên PythonAnywhere
cd learning-web
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Bước 4: Tạo Web App (2 phút)

1. Vào tab "Web"
2. Click "Add a new web app"
3. Chọn domain: `USERNAME.pythonanywhere.com`
4. Chọn "Manual configuration"
5. Chọn "Python 3.11"

---

## Bước 5: Cấu Hình WSGI (3 phút)

1. Trong tab "Web", click vào link "WSGI configuration file"
2. **XÓA TẤT CẢ** nội dung cũ
3. Dán code này vào (thay `USERNAME` bằng username của bạn):

```python
import os
import sys

# Thay USERNAME bằng username PythonAnywhere của bạn
path = '/home/USERNAME/learning-web'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Click "Save"

---

## Bước 6: Cấu Hình Static Files (1 phút)

Trong tab "Web", phần "Static files":

1. Click "Enter URL" và nhập: `/static/`
2. Click "Enter path" và nhập: `/home/USERNAME/learning-web/staticfiles`
   (Thay USERNAME bằng username của bạn)

---

## Bước 7: Chạy Migrations (2 phút)

```bash
# Trong Bash console
cd learning-web
source venv/bin/activate

# Tạo file .env
echo "SECRET_KEY=django-insecure-pythonanywhere-$(date +%s)" > .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=USERNAME.pythonanywhere.com" >> .env

# Chạy migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Tạo superuser
python manage.py createsuperuser
```

---

## Bước 8: Reload & Test (1 phút)

1. Quay lại tab "Web"
2. Click nút **"Reload USERNAME.pythonanywhere.com"** (màu xanh lá)
3. Truy cập: `https://USERNAME.pythonanywhere.com`

---

## ✅ Xong! 

Website của bạn đã online tại: `https://USERNAME.pythonanywhere.com`

---

## 🔄 Cập Nhật Code Sau Này

```bash
# Trên PythonAnywhere Bash console
cd learning-web
git pull  # Nếu dùng GitHub
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput

# Sau đó reload web app từ tab "Web"
```

---

## ❌ Gặp Lỗi?

### Lỗi 502 Bad Gateway
- Kiểm tra lại đường dẫn trong WSGI file
- Đảm bảo đã thay `USERNAME` đúng

### Lỗi Static Files không load
```bash
cd learning-web
source venv/bin/activate
python manage.py collectstatic --noinput
# Reload web app
```

### Lỗi Database
```bash
cd learning-web
source venv/bin/activate
python manage.py migrate
# Reload web app
```

### Xem Logs
- Vào tab "Web"
- Click vào "Error log" hoặc "Server log"

---

## 📞 Cần Trợ Giúp?

- Xem hướng dẫn chi tiết: [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)
- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/

---

**Tổng thời gian: ~20 phút** ⏱️
