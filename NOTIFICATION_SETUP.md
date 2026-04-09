# 🔔 Notification System - Setup Guide

## ✅ Đã Hoàn Thành

### 1. App Structure
- ✓ Created [`apps/notifications/`](apps/notifications/) directory
- ✓ Created [`models.py`](apps/notifications/models.py) with Notification & NotificationPreference models
- ✓ Created [`views.py`](apps/notifications/views.py) with all views
- ✓ Created [`urls.py`](apps/notifications/urls.py) with URL patterns
- ✓ Created [`admin.py`](apps/notifications/admin.py) for admin interface
- ✓ Created [`utils.py`](apps/notifications/utils.py) with helper functions

### 2. Templates
- ✓ [`templates/notifications/list.html`](templates/notifications/list.html) - Main notification list
- ✓ [`templates/notifications/preferences.html`](templates/notifications/preferences.html) - Settings page
- ✓ [`templates/notifications/widget.html`](templates/notifications/widget.html) - Bell widget for navbar

### 3. Configuration
- ✓ Added `'apps.notifications'` to [`INSTALLED_APPS`](config/settings.py:47)
- ✓ Added URL pattern to [`config/urls.py`](config/urls.py:30)

## 📋 Cần Làm Tiếp

### Step 1: Chạy Migrations (QUAN TRỌNG!)

```bash
# Trong virtual environment (venv)
python manage.py makemigrations notifications
python manage.py migrate
```

### Step 2: Thêm Notification Widget vào Base Template

Mở file `templates/base.html` và thêm widget vào navbar:

```html
<!-- Trong navbar, bên cạnh user menu -->
{% include 'notifications/widget.html' %}
```

### Step 3: Tích Hợp Notifications vào Các Chức Năng

#### A. Khi user đạt thành tựu mới (trong leaderboard views)

```python
from apps.notifications.utils import notify_new_achievement

# Sau khi tạo achievement
achievement = Achievement.objects.create(...)
notify_new_achievement(user, achievement)
```

#### B. Khi có kết quả thi mới (trong de_thi views)

```python
from apps.notifications.utils import notify_exam_result

# Sau khi lưu kết quả
ket_qua = KetQuaLamBai.objects.create(...)
notify_exam_result(user, ket_qua)
```

#### C. Khi có reply trong forum

```python
from apps.notifications.utils import notify_forum_reply

# Sau khi tạo reply
reply = ForumReply.objects.create(...)
# Notify post author
notify_forum_reply(post.nguoi_dung, reply, post)
```

#### D. Khi đạt cột mốc flashcard

```python
from apps.notifications.utils import notify_flashcard_milestone

# Sau khi học flashcard
total_learned = user.flashcard_progress.count()
if total_learned in [10, 50, 100, 500, 1000]:
    notify_flashcard_milestone(user, total_learned)
```

#### E. Khi lên hạng trong leaderboard

```python
from apps.notifications.utils import notify_leaderboard_rank

# Sau khi update leaderboard
if entry.rank <= 10:
    notify_leaderboard_rank(user, entry.rank, period, category)
```

## 🎯 8 Loại Thông Báo

1. **badge** (🎖️) - Huy hiệu mới
2. **forum_reply** (💬) - Trả lời diễn đàn
3. **leaderboard** (📊) - Xếp hạng
4. **achievement** (🏆) - Thành tựu
5. **study_reminder** (📚) - Nhắc nhở học tập
6. **exam_result** (📝) - Kết quả thi
7. **flashcard_milestone** (⭐) - Cột mốc flashcard
8. **system** (🔔) - Hệ thống

## 📡 API Endpoints

- `GET /notifications/` - Danh sách thông báo
- `GET /notifications/preferences/` - Cài đặt
- `POST /notifications/<id>/read/` - Đánh dấu đã đọc
- `POST /notifications/<id>/unread/` - Đánh dấu chưa đọc
- `POST /notifications/<id>/delete/` - Xóa thông báo
- `POST /notifications/mark-all-read/` - Đọc tất cả
- `GET /notifications/api/unread-count/` - Số thông báo chưa đọc
- `GET /notifications/api/recent/` - 10 thông báo gần nhất

## 🔧 Sử dụng Utils

```python
from apps.notifications.utils import (
    create_notification,
    notify_new_achievement,
    notify_leaderboard_rank,
    notify_forum_reply,
    notify_exam_result,
    notify_flashcard_milestone,
    notify_study_reminder,
    notify_system,
    bulk_notify
)

# Tạo notification tùy chỉnh
create_notification(
    recipient=user,
    notification_type='system',
    title='Chào mừng!',
    message='Chào mừng bạn đến với hệ thống',
    action_url='/kien-thuc/'
)

# Gửi thông báo hàng loạt
users = User.objects.filter(is_active=True)
bulk_notify(
    users=users,
    notification_type='system',
    title='Cập nhật hệ thống',
    message='Hệ thống đã được cập nhật phiên bản mới'
)
```

## 🎨 Features

### User Features
- ✓ Xem danh sách thông báo
- ✓ Filter theo loại (all, unread, achievement, etc.)
- ✓ Đánh dấu đã đọc/chưa đọc
- ✓ Xóa thông báo
- ✓ Đọc tất cả cùng lúc
- ✓ Cài đặt bật/tắt từng loại thông báo
- ✓ Cài đặt email notifications
- ✓ Bell widget với dropdown
- ✓ Real-time unread count
- ✓ Pagination

### Admin Features
- ✓ Quản lý notifications
- ✓ Filter by type, read status
- ✓ Search by user, title, message
- ✓ Bulk actions

## 🧪 Testing

Sau khi chạy migrations, test các chức năng:

1. Truy cập `/notifications/` - Xem danh sách
2. Truy cập `/notifications/preferences/` - Cài đặt
3. Tạo notification test trong Django shell:

```python
python manage.py shell

from django.contrib.auth.models import User
from apps.notifications.utils import notify_system

user = User.objects.first()
notify_system(user, 'Test', 'Đây là thông báo test', '/kien-thuc/')
```

4. Kiểm tra bell widget trên navbar
5. Test mark as read/unread
6. Test preferences

## 📝 Next Steps

1. ✅ Run migrations
2. ✅ Add widget to base.html
3. ✅ Integrate notifications into existing features
4. ✅ Test all functionality
5. ✅ (Optional) Setup email notifications
6. ✅ (Optional) Add push notifications

## 🐛 Troubleshooting

### Lỗi: No module named 'django'
→ Activate virtual environment: `venv\Scripts\activate`

### Lỗi: No installed app with label 'notification'
→ App name là 'notifications' (có 's'), không phải 'notification'

### Widget không hiện
→ Kiểm tra đã include widget.html trong base.html chưa
→ Kiểm tra user đã login chưa (widget chỉ hiện khi authenticated)

### Không có thông báo
→ Chạy test script ở trên để tạo notification mẫu
→ Kiểm tra preferences có bật loại notification đó không
