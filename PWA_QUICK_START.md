# 🚀 Quick Start - PWA Setup

## Bước 1: Cài đặt Pillow (để tạo icons)

```bash
pip install Pillow
```

## Bước 2: Tạo App Icons

```bash
# Tạo placeholder icons
python generate_icons.py

# Hoặc từ logo của bạn
python generate_icons.py path/to/logo.png
```

## Bước 3: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Bước 4: Chạy Server

```bash
python manage.py runserver
```

## Bước 5: Test PWA

1. Mở Chrome: `http://localhost:8000`
2. Mở DevTools (F12) → Application tab
3. Check:
   - ✅ Manifest
   - ✅ Service Worker
   - ✅ Icons

## Bước 6: Test Install

1. Click "Install" button (góc dưới phải)
2. Hoặc: Chrome menu → "Install app"
3. App sẽ mở như native app

## Bước 7: Test Offline

1. DevTools → Network tab → Offline
2. Reload page
3. Sẽ thấy offline page hoặc cached content

---

## 📱 Test trên Mobile

### Android:
1. Deploy lên server HTTPS
2. Mở Chrome mobile
3. Menu → "Add to Home screen"

### iOS:
1. Deploy lên server HTTPS
2. Mở Safari
3. Share → "Add to Home Screen"

---

## ⚠️ Lưu ý

- PWA chỉ hoạt động trên HTTPS (hoặc localhost)
- Cần tạo icons trước khi test
- Service worker cache có thể cần clear khi update

---

Xem chi tiết: [`PWA_IMPLEMENTATION.md`](PWA_IMPLEMENTATION.md:1)
