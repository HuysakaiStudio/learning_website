# 🚀 Hướng Dẫn Deploy Web Lên Host Miễn Phí

Tài liệu này hướng dẫn chi tiết cách deploy ứng dụng Django Learning Web lên các nền tảng hosting miễn phí phổ biến.

---

## 📋 Mục Lục

1. [Chuẩn Bị](#chuẩn-bị)
2. [PythonAnywhere (Khuyến Nghị)](#1-pythonanywhere-khuyến-nghị)
3. [Render.com](#2-rendercom)
4. [Railway.app](#3-railwayapp)
5. [Vercel (Giới Hạn)](#4-vercel-giới-hạn)
6. [So Sánh Các Nền Tảng](#so-sánh-các-nền-tảng)

---

## Chuẩn Bị

### 1. Kiểm tra các file cần thiết đã được tạo:
- ✅ [`requirements.txt`](requirements.txt) - Dependencies
- ✅ [`runtime.txt`](runtime.txt) - Python version
- ✅ [`Procfile`](Procfile) - Process commands
- ✅ [`vercel.json`](vercel.json) - Vercel config
- ✅ [`render.yaml`](render.yaml) - Render config
- ✅ [`build_files.sh`](build_files.sh) - Build script

### 2. Cập nhật file `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url-if-using-postgres
```

### 3. Push code lên GitHub:
```bash
git init
git add .
git commit -m "Prepare for deployment"
git branch -M main
git remote add origin https://github.com/yourusername/learning-web.git
git push -u origin main
```

---

## 1. PythonAnywhere (Khuyến Nghị) ⭐

**Ưu điểm:**
- ✅ Miễn phí vĩnh viễn
- ✅ Hỗ trợ Django tốt nhất
- ✅ Có database MySQL miễn phí
- ✅ Dễ setup nhất
- ✅ Không cần credit card

**Giới hạn:**
- ⚠️ 512MB disk space
- ⚠️ 1 web app
- ⚠️ Subdomain: yourusername.pythonanywhere.com

### Các Bước Deploy:

#### Bước 1: Đăng ký tài khoản
1. Truy cập: https://www.pythonanywhere.com/registration/register/beginner/
2. Đăng ký tài khoản miễn phí (không cần credit card)

#### Bước 2: Upload code
**Cách 1: Từ GitHub (Khuyến nghị)**
```bash
# Mở Bash console trên PythonAnywhere
git clone https://github.com/yourusername/learning-web.git
cd learning-web
```

**Cách 2: Upload trực tiếp**
- Vào tab "Files"
- Upload từng file/folder

#### Bước 3: Tạo Virtual Environment
```bash
# Trong Bash console
cd learning-web
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Bước 4: Cấu hình Web App
1. Vào tab "Web"
2. Click "Add a new web app"
3. Chọn "Manual configuration"
4. Chọn Python 3.11

#### Bước 5: Cấu hình WSGI
1. Click vào file WSGI configuration
2. Xóa nội dung cũ, thay bằng:

```python
import os
import sys

# Đường dẫn đến project
path = '/home/yourusername/learning-web'
if path not in sys.path:
    sys.path.append(path)

# Đường dẫn đến virtual environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Bước 6: Cấu hình Static Files
Trong tab "Web", phần "Static files":
- URL: `/static/`
- Directory: `/home/yourusername/learning-web/staticfiles`

#### Bước 7: Chạy migrations
```bash
cd learning-web
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Bước 8: Reload Web App
- Click nút "Reload" màu xanh
- Truy cập: https://yourusername.pythonanywhere.com

### Cập nhật code sau này:
```bash
cd learning-web
git pull
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
# Reload web app từ dashboard
```

---

## 2. Render.com

**Ưu điểm:**
- ✅ Miễn phí 750 giờ/tháng
- ✅ Hỗ trợ PostgreSQL miễn phí
- ✅ Auto deploy từ GitHub
- ✅ SSL miễn phí

**Giới hạn:**
- ⚠️ Sleep sau 15 phút không hoạt động
- ⚠️ Khởi động lại chậm (30-60s)
- ⚠️ Cần credit card để verify

### Các Bước Deploy:

#### Bước 1: Đăng ký
1. Truy cập: https://render.com/
2. Đăng ký bằng GitHub

#### Bước 2: Tạo PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Đặt tên: `learning-web-db`
3. Chọn Free plan
4. Click "Create Database"
5. Copy "Internal Database URL"

#### Bước 3: Tạo Web Service
1. Click "New +" → "Web Service"
2. Connect repository GitHub
3. Cấu hình:
   - **Name**: learning-web
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`

#### Bước 4: Thêm Environment Variables
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=paste-internal-database-url-here
PYTHON_VERSION=3.11.0
```

#### Bước 5: Deploy
- Click "Create Web Service"
- Đợi 5-10 phút để build
- Truy cập URL được cung cấp

### Auto Deploy:
- Mỗi khi push code lên GitHub, Render tự động deploy lại

---

## 3. Railway.app

**Ưu điểm:**
- ✅ $5 credit miễn phí/tháng
- ✅ Không sleep
- ✅ Deploy nhanh
- ✅ PostgreSQL miễn phí

**Giới hạn:**
- ⚠️ Hết credit sau ~500 giờ
- ⚠️ Cần credit card

### Các Bước Deploy:

#### Bước 1: Đăng ký
1. Truy cập: https://railway.app/
2. Đăng nhập bằng GitHub

#### Bước 2: Tạo Project
1. Click "New Project"
2. Chọn "Deploy from GitHub repo"
3. Chọn repository của bạn

#### Bước 3: Thêm PostgreSQL
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway tự động tạo DATABASE_URL

#### Bước 4: Cấu hình Variables
Vào Settings → Variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHON_VERSION=3.11.0
```

#### Bước 5: Cấu hình Deploy
Vào Settings:
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- **Start Command**: `gunicorn config.wsgi:application`

#### Bước 6: Generate Domain
- Vào Settings → Networking
- Click "Generate Domain"
- Truy cập domain được tạo

---

## 4. Vercel (Giới Hạn)

**Lưu ý:** Vercel chủ yếu cho frontend, Django có thể gặp vấn đề với database và file uploads.

**Ưu điểm:**
- ✅ Deploy cực nhanh
- ✅ Miễn phí không giới hạn
- ✅ SSL tự động

**Giới hạn:**
- ⚠️ Không hỗ trợ SQLite
- ⚠️ Serverless (không phù hợp Django)
- ⚠️ Không lưu file uploads

### Các Bước Deploy (Nếu muốn thử):

#### Bước 1: Cài Vercel CLI
```bash
npm install -g vercel
```

#### Bước 2: Login
```bash
vercel login
```

#### Bước 3: Deploy
```bash
vercel --prod
```

**Khuyến nghị:** Không nên dùng Vercel cho Django app phức tạp như này.

---

## So Sánh Các Nền Tảng

| Tiêu Chí | PythonAnywhere | Render | Railway | Vercel |
|----------|----------------|--------|---------|--------|
| **Giá** | Miễn phí vĩnh viễn | Miễn phí có giới hạn | $5/tháng | Miễn phí |
| **Database** | MySQL | PostgreSQL | PostgreSQL | Không có |
| **Sleep** | Không | Có (15 phút) | Không | Không |
| **Credit Card** | Không cần | Cần | Cần | Không cần |
| **Phù hợp Django** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Dễ setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 Khuyến Nghị

### Cho người mới bắt đầu:
**→ PythonAnywhere** - Dễ nhất, miễn phí vĩnh viễn, không cần credit card

### Cho production nhỏ:
**→ Render.com** - Tốt hơn về performance, auto deploy

### Cho production lớn:
**→ Railway.app** hoặc **DigitalOcean** (trả phí)

---

## 🔧 Troubleshooting

### Lỗi Static Files không load:
```bash
python manage.py collectstatic --noinput
# Kiểm tra STATIC_ROOT trong settings.py
```

### Lỗi Database:
```bash
python manage.py migrate
# Kiểm tra DATABASE_URL
```

### Lỗi 500 Internal Server Error:
1. Kiểm tra logs trên hosting platform
2. Đảm bảo DEBUG=False
3. Kiểm tra ALLOWED_HOSTS

### Lỗi Module not found:
```bash
pip install -r requirements.txt
# Đảm bảo tất cả dependencies đã được cài
```

---

## 📚 Tài Liệu Tham Khảo

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Render Django Guide](https://render.com/docs/deploy-django)
- [Railway Django Guide](https://docs.railway.app/guides/django)

---

## ✅ Checklist Trước Khi Deploy

- [ ] Đã test ứng dụng local
- [ ] Đã tạo requirements.txt
- [ ] Đã set DEBUG=False
- [ ] Đã cấu hình ALLOWED_HOSTS
- [ ] Đã tạo SECRET_KEY mới
- [ ] Đã test collectstatic
- [ ] Đã push code lên GitHub
- [ ] Đã tạo .gitignore (không commit .env, db.sqlite3)
- [ ] Đã chạy migrations
- [ ] Đã tạo superuser

---

**Chúc bạn deploy thành công! 🚀**

Nếu gặp vấn đề, hãy kiểm tra logs của hosting platform hoặc tham khảo documentation của họ.
