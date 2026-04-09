# Gamification System - Database Integration

## Tổng quan

Hệ thống gamification đã được tích hợp vào database để:
- ✅ Đồng bộ dữ liệu đa thiết bị
- ✅ Bảo mật và chống cheat
- ✅ Phân tích và thống kê
- ✅ Tạo leaderboard XP
- ✅ Backup tự động

## Cấu trúc Database

### Model: UserGamification

```python
class UserGamification(models.Model):
    user = models.OneToOneField(User, related_name='gamification')
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Công thức tính Level

```python
level = floor((xp / 100) ^ (1 / 1.5))
```

## Migration

### Bước 1: Chạy Migration

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run migration
python manage.py migrate nguoi_dung
```

### Bước 2: Tự động Sync từ localStorage

Khi user đăng nhập lần đầu sau khi update:
- JavaScript tự động đọc dữ liệu từ localStorage
- Gọi API `/nguoi-dung/api/gamification/sync/`
- Server so sánh và lưu giá trị lớn hơn
- Dữ liệu được đồng bộ tự động

## API Endpoints

### 1. Lấy thông tin gamification

```
GET /nguoi-dung/api/gamification/stats/
```

Response:
```json
{
  "success": true,
  "data": {
    "xp": 150,
    "level": 3,
    "current_streak": 5,
    "longest_streak": 10,
    "last_activity_date": "2026-04-09",
    "xp_progress": {
      "current": 50,
      "needed": 200,
      "progress_percent": 25.0
    }
  }
}
```

### 2. Thêm XP

```
POST /nguoi-dung/api/gamification/add-xp/
Content-Type: application/json

{
  "amount": 10,
  "reason": "Hoàn thành bài thi"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "xp_gained": 10,
    "total_xp": 160,
    "old_level": 3,
    "new_level": 3,
    "leveled_up": false,
    "reason": "Hoàn thành bài thi"
  }
}
```

### 3. Cập nhật Streak

```
POST /nguoi-dung/api/gamification/update-streak/
```

Response:
```json
{
  "success": true,
  "data": {
    "updated": true,
    "current_streak": 6,
    "longest_streak": 10,
    "last_activity_date": "2026-04-09"
  }
}
```

### 4. Sync từ localStorage (one-time)

```
POST /nguoi-dung/api/gamification/sync/
Content-Type: application/json

{
  "xp": 200,
  "streak": 7
}
```

## JavaScript Integration

### Tự động Load từ Server

```javascript
// Khi trang load
const gamification = new GamificationSystem();
// Tự động gọi loadFromServer() và sync
```

### Thêm XP

```javascript
// Tự động sync với server
gamification.addXP(10, 'Hoàn thành bài thi');
```

### Cập nhật Streak

```javascript
// Tự động sync với server
gamification.checkStreak();
```

## Offline Mode

Hệ thống vẫn hoạt động khi offline:
- Dữ liệu lưu trong localStorage
- Tự động sync khi online trở lại
- Không mất dữ liệu

## Admin Interface

Truy cập Django Admin để quản lý:
```
/admin/nguoi_dung/usergamification/
```

Có thể:
- Xem danh sách users theo XP/Level
- Tìm kiếm theo username
- Filter theo level, streak
- Chỉnh sửa XP/Level thủ công (nếu cần)

## Leaderboard XP

Tạo leaderboard dựa trên XP:

```python
from apps.nguoi_dung.models import UserGamification

# Top 10 users theo XP
top_users = UserGamification.objects.select_related('user').order_by('-xp')[:10]

# Top 10 users theo Level
top_level = UserGamification.objects.select_related('user').order_by('-level', '-xp')[:10]

# Top 10 users theo Streak
top_streak = UserGamification.objects.select_related('user').order_by('-current_streak')[:10]
```

## Analytics

Phân tích dữ liệu gamification:

```python
from django.db.models import Avg, Max, Min, Count
from apps.nguoi_dung.models import UserGamification

# Thống kê tổng quan
stats = UserGamification.objects.aggregate(
    avg_xp=Avg('xp'),
    max_xp=Max('xp'),
    avg_level=Avg('level'),
    max_level=Max('level'),
    avg_streak=Avg('current_streak'),
    max_streak=Max('longest_streak')
)

# Phân bố level
level_distribution = UserGamification.objects.values('level').annotate(
    count=Count('id')
).order_by('level')
```

## Best Practices

1. **Không chỉnh sửa localStorage trực tiếp** - Luôn dùng API
2. **Kiểm tra response** - Xử lý lỗi khi API fail
3. **Backup định kỳ** - Database được backup tự động
4. **Monitor performance** - Theo dõi query performance với indexes
5. **Rate limiting** - Cân nhắc thêm rate limit cho API endpoints

## Troubleshooting

### Dữ liệu không sync

1. Kiểm tra console log
2. Verify user đã đăng nhập
3. Check network tab trong DevTools
4. Xem Django logs

### Level không đúng

```python
# Recalculate level cho user
gamification = user.gamification
gamification.level = gamification.calculate_level()
gamification.save()
```

### Reset dữ liệu user

```python
# Trong Django shell
from apps.nguoi_dung.models import UserGamification
gamification = UserGamification.objects.get(user__username='username')
gamification.xp = 0
gamification.level = 0
gamification.current_streak = 0
gamification.save()
```

## Future Enhancements

- [ ] XP history tracking
- [ ] Achievement system integration
- [ ] Daily/Weekly challenges
- [ ] XP multipliers
- [ ] Seasonal events
- [ ] Social features (compare with friends)

## Support

Nếu có vấn đề, check:
1. Migration đã chạy chưa
2. API endpoints hoạt động chưa
3. JavaScript console có lỗi không
4. Django logs có error không
