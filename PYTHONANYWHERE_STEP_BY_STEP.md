# 🎯 Hướng Dẫn Deploy PythonAnywhere - Từng Bước Chi Tiết

## ✅ Chuẩn Bị Trước Khi Bắt Đầu

### 1. Tạo file .env
```bash
# Copy file mẫu
copy .env.example .env

# Hoặc tạo thủ công với nội dung:
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Push code lên GitHub (nếu chưa có)
```bash
# Khởi tạo Git
git init
git add .
git commit -m "Prepare for PythonAnywhere deployment"

# Tạo repository trên GitHub, sau đó:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/learning-web.git
git push -u origin main
```

---

## 📝 BƯỚC 1: Đăng Ký PythonAnywhere (5 phút)

### 1.1. Truy cập trang đăng ký
- Link: https://www.pythonanywhere.com/registration/register/beginner/

### 1.2. Điền thông tin
- **Username**: Chọn username (sẽ là subdomain của bạn)
- **Email**: Email của bạn
- **Password**: Mật khẩu mạnh

### 1.3. Xác nhận email
- Check email và click link xác nhận

### 1.4. Đăng nhập
- Đăng nhập vào PythonAnywhere

---

## 📦 BƯỚC 2: Upload Code (10 phút)

### Cách 1: Clone từ GitHub (Khuyến nghị)

#### 2.1. Mở Bash Console
- Vào Dashboard → Click "Bash" trong phần "New console"

#### 2.2. Clone repository
```bash
# Thay YOUR_USERNAME và YOUR_REPO
git clone https://github.com/YOUR_USERNAME/learning-web.git
cd learning-web
ls -la  # Kiểm tra files
```

### Cách 2: Upload Trực Tiếp (Nếu không dùng GitHub)

#### 2.1. Vào tab Files
- Click tab "Files" ở menu trên

#### 2.2. Tạo folder
- Click "New directory"
- Tên: `learning-web`

#### 2.3. Upload files
- Vào folder `learning-web`
- Click "Upload a file"
- Upload tất cả files và folders (có thể upload nhiều lần)

---

## 🐍 BƯỚC 3: Tạo Virtual Environment (5 phút)

### 3.1. Trong Bash Console
```bash
cd learning-web
```

### 3.2. Tạo virtual environment
```bash
python3.11 -m venv venv
```

### 3.3. Kích hoạt virtual environment
```bash
source venv/bin/activate
```

Bạn sẽ thấy `(venv)` xuất hiện trước dấu nhắc lệnh.

### 3.4. Cài đặt dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Đợi 2-3 phút để cài đặt xong.

---

## 🌐 BƯỚC 4: Tạo Web App (3 phút)

### 4.1. Vào tab Web
- Click tab "Web" ở menu trên

### 4.2. Add new web app
- Click nút xanh "Add a new web app"

### 4.3. Chọn domain
- Sẽ hiện: `YOUR_USERNAME.pythonanywhere.com`
- Click "Next"

### 4.4. Chọn framework
- Chọn "Manual configuration" (KHÔNG chọn Django)
- Click "Next"

### 4.5. Chọn Python version
- Chọn "Python 3.11"
- Click "Next"

### 4.6. Hoàn tất
- Click "Next" để hoàn tất

---

## ⚙️ BƯỚC 5: Cấu Hình WSGI (5 phút)

### 5.1. Mở WSGI file
- Trong tab "Web", tìm phần "Code"
- Click vào link "WSGI configuration file"
  (Ví dụ: `/var/www/username_pythonanywhere_com_wsgi.py`)

### 5.2. Xóa tất cả nội dung cũ
- Chọn tất cả (Ctrl+A) và xóa

### 5.3. Dán code mới
**QUAN TRỌNG: Thay `YOUR_USERNAME` bằng username PythonAnywhere của bạn**

```python
import os
import sys

# Thay YOUR_USERNAME bằng username của bạn
path = '/home/YOUR_USERNAME/learning-web'
if path not in sys.path:
    sys.path.append(path)

# Thêm virtual environment
venv_path = '/home/YOUR_USERNAME/learning-web/venv/lib/python3.11/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5.4. Lưu file
- Click "Save" ở góc trên bên phải

---

## 📁 BƯỚC 6: Cấu Hình Static Files (2 phút)

### 6.1. Trong tab Web, tìm phần "Static files"

### 6.2. Thêm static files mapping
- Click "Enter URL": `/static/`
- Click "Enter path": `/home/YOUR_USERNAME/learning-web/staticfiles`
  (Thay YOUR_USERNAME)

### 6.3. Thêm media files mapping (optional)
- Click "Enter URL": `/media/`
- Click "Enter path": `/home/YOUR_USERNAME/learning-web/media`
  (Thay YOUR_USERNAME)

---

## 🗄️ BƯỚC 7: Cấu Hình Database & Migrations (5 phút)

### 7.1. Quay lại Bash Console
```bash
cd learning-web
source venv/bin/activate
```

### 7.2. Tạo file .env
```bash
# Tạo SECRET_KEY ngẫu nhiên
echo "SECRET_KEY=django-insecure-pythonanywhere-$(date +%s)-$(openssl rand -hex 20)" > .env

# Thêm các config khác
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com" >> .env

# Xem file .env
cat .env
```

**Thay YOUR_USERNAME bằng username của bạn**

### 7.3. Chạy migrations
```bash
python manage.py migrate
```

Bạn sẽ thấy các migrations được apply.

### 7.4. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 7.5. Tạo superuser
```bash
python manage.py createsuperuser
```

Nhập:
- Username: (tên admin của bạn)
- Email: (email của bạn)
- Password: (mật khẩu mạnh)
- Password (again): (nhập lại)

---

## 🚀 BƯỚC 8: Reload & Test (2 phút)

### 8.1. Reload web app
- Quay lại tab "Web"
- Scroll lên trên
- Click nút xanh lá **"Reload YOUR_USERNAME.pythonanywhere.com"**

### 8.2. Đợi 10-20 giây

### 8.3. Truy cập website
- Click vào link: `https://YOUR_USERNAME.pythonanywhere.com`
- Hoặc mở trình duyệt mới và truy cập

### 8.4. Kiểm tra
- ✅ Trang chủ hiển thị đúng
- ✅ Static files (CSS, JS) load được
- ✅ Có thể đăng nhập
- ✅ Các chức năng hoạt động

### 8.5. Truy cập Admin
- URL: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- Đăng nhập bằng superuser vừa tạo

---

## ✅ HOÀN TẤT!

Website của bạn đã online tại:
**https://YOUR_USERNAME.pythonanywhere.com**

---

## 🔄 Cập Nhật Code Sau Này

### Nếu dùng GitHub:
```bash
# Mở Bash Console
cd learning-web
git pull
source venv/bin/activate
pip install -r requirements.txt  # Nếu có thêm dependencies
python manage.py migrate
python manage.py collectstatic --noinput
```

### Nếu upload thủ công:
1. Vào tab "Files"
2. Upload files mới (ghi đè files cũ)
3. Chạy migrations trong Bash Console

### Sau đó:
- Vào tab "Web"
- Click "Reload"

---

## ❌ Xử Lý Lỗi Thường Gặp

### Lỗi 1: 502 Bad Gateway

**Nguyên nhân:** WSGI file cấu hình sai

**Giải pháp:**
1. Kiểm tra lại WSGI file
2. Đảm bảo đã thay `YOUR_USERNAME` đúng
3. Kiểm tra đường dẫn: `/home/YOUR_USERNAME/learning-web`
4. Reload web app

### Lỗi 2: Static files không load (CSS, JS không hiển thị)

**Giải pháp:**
```bash
cd learning-web
source venv/bin/activate
python manage.py collectstatic --noinput
```

Kiểm tra Static files mapping trong tab Web:
- URL: `/static/`
- Path: `/home/YOUR_USERNAME/learning-web/staticfiles`

Reload web app.

### Lỗi 3: DisallowedHost at /

**Nguyên nhân:** ALLOWED_HOSTS chưa đúng

**Giải pháp:**
```bash
cd learning-web
nano .env  # Hoặc dùng editor trên web

# Sửa dòng ALLOWED_HOSTS
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
```

Reload web app.

### Lỗi 4: ImportError / ModuleNotFoundError

**Nguyên nhân:** Thiếu dependencies

**Giải pháp:**
```bash
cd learning-web
source venv/bin/activate
pip install -r requirements.txt
```

Reload web app.

### Lỗi 5: Database errors

**Giải pháp:**
```bash
cd learning-web
source venv/bin/activate
python manage.py migrate
```

Reload web app.

---

## 📊 Xem Logs

### Error Log
- Tab "Web" → Click "Error log"
- Xem lỗi gần nhất

### Server Log
- Tab "Web" → Click "Server log"
- Xem requests

### Access Log
- Tab "Web" → Click "Access log"
- Xem traffic

---

## 🎓 Tips & Tricks

### 1. Tự động reload khi có lỗi
- Mỗi khi sửa code, nhớ reload web app

### 2. Kiểm tra logs thường xuyên
- Logs giúp debug nhanh hơn

### 3. Backup database
```bash
cd learning-web
python manage.py dumpdata > backup.json
```

### 4. Restore database
```bash
python manage.py loaddata backup.json
```

### 5. Chạy Django shell
```bash
cd learning-web
source venv/bin/activate
python manage.py shell
```

### 6. Xem cron jobs (scheduled tasks)
- Tab "Tasks" để setup scheduled tasks

---

## 📞 Cần Trợ Giúp?

### PythonAnywhere Help
- Help: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Wiki: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

### Django Documentation
- Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/

---

## 🎉 Chúc Mừng!

Bạn đã deploy thành công Django app lên PythonAnywhere!

**Website:** https://YOUR_USERNAME.pythonanywhere.com
**Admin:** https://YOUR_USERNAME.pythonanywhere.com/admin/

Chia sẻ link với bạn bè và thầy cô! 🚀
