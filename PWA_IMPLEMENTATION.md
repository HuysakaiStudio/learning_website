# 📱 PWA Implementation Guide - Ôn Thi THPTQG

## 🎯 Tổng quan

Dự án đã được tích hợp PWA (Progressive Web App) để cải thiện trải nghiệm mobile với các tính năng:

- ✅ Offline support (hoạt động khi mất mạng)
- ✅ Install prompt (cài đặt như app native)
- ✅ Push notifications (thông báo đẩy)
- ✅ Background sync (đồng bộ khi có mạng)
- ✅ Mobile-optimized UI (giao diện tối ưu mobile)
- ✅ Fast loading (tải nhanh với cache)

---

## 📁 Files đã tạo

### 1. Service Worker
**File:** [`static/sw.js`](static/sw.js:1)

Service worker xử lý:
- Cache static files (CSS, JS, images)
- Offline fallback
- Background sync
- Push notifications

**Caching strategies:**
- Static assets: Cache first
- API requests: Network first
- Images: Cache first
- Pages: Network first, fallback to cache

### 2. PWA Manifest
**File:** [`static/manifest.json`](static/manifest.json:1)

Định nghĩa app metadata:
- App name, icons, colors
- Display mode (standalone)
- Start URL
- Shortcuts (quick actions)

### 3. PWA JavaScript
**File:** [`static/js/pwa.js`](static/js/pwa.js:1)

Xử lý:
- Service worker registration
- Install prompt
- Offline detection
- Update notifications
- Background sync

### 4. Mobile CSS
**File:** [`static/css/pwa-mobile.css`](static/css/pwa-mobile.css:1)

Tối ưu mobile:
- Touch-friendly buttons (44x44px minimum)
- Responsive typography
- Safe areas (iPhone X+)
- Swipe gestures
- Performance optimizations

### 5. Offline Page
**File:** [`templates/offline.html`](templates/offline.html:1)

Trang hiển thị khi offline với:
- Status indicator
- Retry button
- List of cached pages

### 6. Updated Base Template
**File:** [`templates/base.html`](templates/base.html:1)

Đã thêm:
- PWA meta tags
- Manifest link
- App icons
- PWA scripts

---

## 🚀 Cách sử dụng

### Bước 1: Tạo App Icons

```bash
# Cài đặt Pillow
pip install Pillow

# Tạo placeholder icons
python generate_icons.py

# Hoặc từ logo của bạn
python generate_icons.py path/to/your/logo.png
```

Icons sẽ được tạo trong `static/icons/`:
- icon-16x16.png đến icon-512x512.png
- apple-touch-icon.png
- favicon.ico

### Bước 2: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Bước 3: Test trên Local

```bash
# Chạy server
python manage.py runserver

# Truy cập: http://localhost:8000
```

**Lưu ý:** PWA chỉ hoạt động trên HTTPS (hoặc localhost)

### Bước 4: Test PWA Features

#### Test Install Prompt:
1. Mở Chrome DevTools (F12)
2. Application tab → Manifest
3. Click "Add to home screen"

#### Test Offline Mode:
1. DevTools → Network tab
2. Chọn "Offline"
3. Reload page → Sẽ thấy offline page

#### Test Service Worker:
1. DevTools → Application → Service Workers
2. Xem status và cache storage

---

## 📱 Mobile Testing

### Android Chrome:
1. Truy cập site trên Chrome mobile
2. Menu → "Add to Home screen"
3. App sẽ xuất hiện như native app

### iOS Safari:
1. Truy cập site trên Safari
2. Share button → "Add to Home Screen"
3. App sẽ xuất hiện trên home screen

---

## 🔧 Configuration

### Customize App Colors

Edit [`static/manifest.json`](static/manifest.json:1):
```json
{
  "theme_color": "#4285f4",
  "background_color": "#ffffff"
}
```

### Customize Cache Strategy

Edit [`static/sw.js`](static/sw.js:1):
```javascript
const CACHE_VERSION = 'thptqg-v1.0.0';
const MAX_DYNAMIC_CACHE_SIZE = 50;
```

### Customize Install Prompt

Edit [`static/js/pwa.js`](static/js/pwa.js:1):
```javascript
function createFloatingInstallButton() {
  // Customize button appearance
}
```

---

## 🎨 Mobile UI Optimizations

### Touch Targets
Tất cả buttons và links có minimum size 44x44px:
```css
.btn {
  min-height: 44px;
  min-width: 44px;
}
```

### Responsive Typography
Font size tự động scale trên mobile:
```css
@media (max-width: 768px) {
  body {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}
```

### Safe Areas (iPhone X+)
Support notch và home indicator:
```css
@supports (padding: max(0px)) {
  body {
    padding-left: max(0px, env(safe-area-inset-left));
  }
}
```

---

## 🔔 Push Notifications (Optional)

### Setup Backend:

1. Install package:
```bash
pip install pywebpush
```

2. Generate VAPID keys:
```python
from pywebpush import webpush, WebPushException
import json

# Generate keys
vapid_private_key = "YOUR_PRIVATE_KEY"
vapid_public_key = "YOUR_PUBLIC_KEY"
```

3. Add to settings:
```python
# config/settings.py
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "YOUR_PUBLIC_KEY",
    "VAPID_PRIVATE_KEY": "YOUR_PRIVATE_KEY",
    "VAPID_ADMIN_EMAIL": "admin@example.com"
}
```

4. Update [`static/js/pwa.js`](static/js/pwa.js:1):
```javascript
const VAPID_PUBLIC_KEY = 'YOUR_PUBLIC_KEY';
```

---

## 📊 Performance Metrics

### Lighthouse Score Targets:
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+
- PWA: 100

### Test với Lighthouse:
```bash
# Chrome DevTools → Lighthouse tab
# Hoặc CLI:
npm install -g lighthouse
lighthouse http://localhost:8000 --view
```

---

## 🐛 Troubleshooting

### Service Worker không register:
```javascript
// Check console for errors
navigator.serviceWorker.register('/static/sw.js')
  .then(reg => console.log('SW registered:', reg))
  .catch(err => console.error('SW registration failed:', err));
```

### Install prompt không hiện:
- Phải dùng HTTPS (hoặc localhost)
- Phải có manifest.json valid
- Phải có service worker
- Chưa install trước đó

### Offline page không hiện:
- Check service worker đã cache `/offline.html`
- Check fetch handler trong sw.js

### Icons không load:
```bash
# Verify icons exist
ls static/icons/

# Collect static
python manage.py collectstatic
```

---

## 📈 Next Steps

### Phương án 1: Hybrid React Components
Sau khi PWA stable, có thể thêm React cho:
- Flashcard swiper
- Exam interface
- Real-time leaderboard

### Phương án 3: Full SPA
Nếu cần mobile app native:
- Tách frontend React
- Django làm API backend
- React Native Web cho cross-platform

---

## 📚 Resources

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Workbox (Advanced SW)](https://developers.google.com/web/tools/workbox)

---

## ✅ Checklist

- [x] Service Worker created
- [x] Manifest.json configured
- [x] PWA meta tags added
- [x] Mobile CSS optimized
- [x] Offline page created
- [x] Install prompt implemented
- [ ] App icons generated (run `python generate_icons.py`)
- [ ] Test on real mobile devices
- [ ] Push notifications setup (optional)
- [ ] Deploy to production with HTTPS

---

## 🎉 Kết quả

Sau khi hoàn thành, ứng dụng sẽ có:

1. **Install như app native** - Không cần App Store/Play Store
2. **Hoạt động offline** - Xem nội dung đã cache
3. **Tải nhanh** - Cache static assets
4. **Mobile-friendly** - Touch-optimized UI
5. **Push notifications** - Thông báo real-time (nếu setup)

**Trải nghiệm mobile được cải thiện đáng kể! 🚀**
