# 🔔 Leaderboard Notification Setup Guide

## Overview
Thông báo bảng xếp hạng giờ được gửi tự động theo lịch trình thay vì mỗi khi người dùng xem bảng xếp hạng.

## Changes Made

### 1. Created Management Command
**File:** [`apps/leaderboard/management/commands/send_leaderboard_notifications.py`](apps/leaderboard/management/commands/send_leaderboard_notifications.py:1)

Command này sẽ:
- Lấy top 10 users từ leaderboard
- Tạo achievements cho users chưa có
- Gửi thông báo xếp hạng
- Chỉ gửi 1 lần cho mỗi period

### 2. Updated Leaderboard Views
**File:** [`apps/leaderboard/views.py`](apps/leaderboard/views.py:1)

- Removed `award_achievements()` call from view
- Prevents sending notifications on every page view
- Added comment explaining new approach

## Setup Instructions

### Option 1: Cron Jobs (Linux/Mac)

Edit crontab:
```bash
crontab -e
```

Add these lines:
```bash
# Daily leaderboard notifications (midnight)
0 0 * * * cd /path/to/project && /path/to/venv/bin/python manage.py send_leaderboard_notifications --period=daily

# Weekly leaderboard notifications (Sunday midnight)
0 0 * * 0 cd /path/to/project && /path/to/venv/bin/python manage.py send_leaderboard_notifications --period=weekly

# Monthly leaderboard notifications (1st of month)
0 0 1 * * cd /path/to/project && /path/to/venv/bin/python manage.py send_leaderboard_notifications --period=monthly
```

### Option 2: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (Daily/Weekly/Monthly)
4. Action: Start a program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `manage.py send_leaderboard_notifications --period=daily`
7. Start in: `C:\path\to\project`

### Option 3: Django-Crontab (Recommended)

Install:
```bash
pip install django-crontab
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django_crontab',
]

CRONJOBS = [
    # Daily at midnight
    ('0 0 * * *', 'django.core.management.call_command', ['send_leaderboard_notifications', '--period=daily']),
    
    # Weekly on Sunday at midnight
    ('0 0 * * 0', 'django.core.management.call_command', ['send_leaderboard_notifications', '--period=weekly']),
    
    # Monthly on 1st at midnight
    ('0 0 1 * *', 'django.core.management.call_command', ['send_leaderboard_notifications', '--period=monthly']),
]
```

Add cron jobs:
```bash
python manage.py crontab add
```

View active cron jobs:
```bash
python manage.py crontab show
```

Remove cron jobs:
```bash
python manage.py crontab remove
```

### Option 4: Celery Beat (Production)

Install:
```bash
pip install celery redis
```

Create `celery.py`:
```python
from celery import Celery
from celery.schedules import crontab

app = Celery('learning_web')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'daily-leaderboard': {
        'task': 'apps.leaderboard.tasks.send_daily_notifications',
        'schedule': crontab(hour=0, minute=0),
    },
    'weekly-leaderboard': {
        'task': 'apps.leaderboard.tasks.send_weekly_notifications',
        'schedule': crontab(hour=0, minute=0, day_of_week=0),
    },
    'monthly-leaderboard': {
        'task': 'apps.leaderboard.tasks.send_monthly_notifications',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),
    },
}
```

## Manual Testing

Test the command manually:

```bash
# Test daily notifications
python manage.py send_leaderboard_notifications --period=daily

# Test weekly notifications
python manage.py send_leaderboard_notifications --period=weekly

# Test monthly notifications
python manage.py send_leaderboard_notifications --period=monthly
```

## Expected Output

```
Processing daily leaderboard notifications...
  ✓ Achievement for user1 (Rank 1)
  ✓ Rank notification for user1 (Rank 1)
  ✓ Achievement for user2 (Rank 2)
  ✓ Rank notification for user2 (Rank 2)
  ...
Successfully processed daily notifications
```

## Notification Logic

### Daily Leaderboard
- Runs at midnight every day
- Notifies top 10 users
- Achievement type: `top_10_daily`
- Checks for existing achievements in last 24 hours

### Weekly Leaderboard
- Runs at midnight every Sunday
- Notifies top 10 users
- Achievement type: `top_10_weekly`
- Checks for existing achievements in last 7 days

### Monthly Leaderboard
- Runs at midnight on 1st of each month
- Notifies top 10 users
- Achievement type: `top_10_monthly`
- Checks for existing achievements in last 30 days

## Benefits

✅ **No spam**: Users only get notified once per period
✅ **Predictable**: Notifications sent at consistent times
✅ **Scalable**: Doesn't slow down page views
✅ **Fair**: All users notified at same time
✅ **Efficient**: Batch processing instead of per-view

## Troubleshooting

### Notifications not sending?

1. Check cron job is running:
```bash
crontab -l  # Linux/Mac
```

2. Check Django logs:
```bash
tail -f logs/django.log
```

3. Test command manually:
```bash
python manage.py send_leaderboard_notifications --period=daily
```

4. Verify notification preferences:
```python
from apps.notifications.models import NotificationPreference
prefs = NotificationPreference.objects.all()
for p in prefs:
    print(f"{p.user.username}: leaderboard={p.leaderboard_notifications}")
```

### Duplicate notifications?

- Check if cron job is running multiple times
- Verify achievement check logic
- Check time threshold in command

## Migration from Old System

The old system sent notifications on every page view. The new system:

1. **Before**: `award_achievements()` called in view → notifications sent immediately
2. **After**: Management command runs periodically → notifications sent in batch

No database migration needed - the Achievement model remains the same.

## Monitoring

Add logging to track notification sends:

```python
import logging
logger = logging.getLogger(__name__)

# In management command
logger.info(f'Sent {count} leaderboard notifications for {period}')
```

View logs:
```bash
grep "leaderboard notifications" logs/django.log
```

## Future Enhancements

- [ ] Email notifications for top 3
- [ ] Push notifications via Firebase
- [ ] Customizable notification times per user
- [ ] Notification history dashboard
- [ ] A/B test notification timing

---

**Created:** 2026-04-09  
**Status:** Active  
**Maintainer:** Development Team
