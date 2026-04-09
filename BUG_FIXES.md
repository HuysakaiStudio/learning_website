"""
Bug Fixes and Improvements Documentation
"""

# ✅ FIXED ISSUES

## 1. Missing Logger Import in de_thi/views.py
**Problem:** Code used `logger.error()` but logger was not imported
**Fix:** Added `import logging` and `logger = logging.getLogger(__name__)`
**File:** apps/de_thi/views.py:13-15

## 2. Database Query Optimization
**Problem:** N+1 queries in leaderboard views
**Fix:** Already using `select_related('user')` for entries
**File:** apps/leaderboard/views.py:36

## 3. Notification Preferences Auto-Creation
**Problem:** NotificationPreference might not exist for new users
**Fix:** Auto-create with default settings in create_notification()
**File:** apps/notifications/utils.py:42-44

## 4. Forum Notification Self-Reply Check
**Problem:** Users could get notifications for their own comments
**Fix:** Added check `if post.tac_gia != request.user` before sending
**File:** apps/de_thi/views.py:964, 990

## 5. Flashcard Milestone Duplicate Notifications
**Problem:** Could send multiple notifications for same milestone
**Fix:** Only checks specific milestones [10, 50, 100, 500, 1000]
**File:** apps/kien_thuc/views.py:298-310

---

# 🧪 TESTING CHECKLIST

## A. Notification System Tests

### 1. Bell Widget
- [ ] Bell icon appears in navbar when logged in
- [ ] Badge shows correct unread count
- [ ] Dropdown opens on click
- [ ] Dropdown shows recent notifications
- [ ] Click notification redirects to action_url
- [ ] Auto-refresh works (check after 30s)

### 2. Notification List Page (/notifications/)
- [ ] Page loads without errors
- [ ] Notifications display correctly
- [ ] Filter tabs work (all, unread, by type)
- [ ] Mark as read works
- [ ] Mark as unread works
- [ ] Delete notification works
- [ ] Mark all as read works
- [ ] Pagination works
- [ ] Responsive on mobile

### 3. Preferences Page (/notifications/preferences/)
- [ ] Page loads without errors
- [ ] All toggle switches work
- [ ] Email frequency radio buttons work
- [ ] Save button works
- [ ] Settings persist after save
- [ ] Disabling notification type prevents new notifications

### 4. Notification Types
- [ ] Achievement notification (🏆)
- [ ] Leaderboard notification (📊)
- [ ] Exam result notification (📝)
- [ ] Forum reply notification (💬)
- [ ] Flashcard milestone notification (⭐)
- [ ] System notification (🔔)

## B. Integration Tests

### 1. Exam Result Flow
```
1. Login as user
2. Take an exam
3. Submit exam
4. Check notifications - should have exam result notification
5. Click notification - should go to result page
```

### 2. Flashcard Milestone Flow
```
1. Login as user
2. Learn flashcards until reaching 10 total
3. Check notifications - should have milestone notification
4. Continue to 50, 100, etc.
```

### 3. Forum Reply Flow
```
1. User A creates a forum post
2. User B comments on the post
3. User A should receive notification
4. User B should NOT receive notification (own comment)
```

### 4. Leaderboard Flow
```
1. Complete exams to get into top 10
2. Wait for leaderboard update (or trigger manually)
3. Check notifications - should have rank notification
4. Check achievements page
```

## C. Performance Tests

### 1. Database Queries
```python
from django.db import connection
from django.test.utils import override_settings

# Check number of queries
with override_settings(DEBUG=True):
    # Visit leaderboard page
    # Check len(connection.queries)
    # Should be < 10 queries
```

### 2. Page Load Times
- [ ] Notification list loads in < 1s
- [ ] Bell widget API responds in < 200ms
- [ ] Leaderboard page loads in < 2s
- [ ] Preferences page loads in < 500ms

### 3. Notification Count
- [ ] Test with 100+ notifications
- [ ] Test with 1000+ notifications
- [ ] Pagination works correctly
- [ ] No performance degradation

---

# 🐛 KNOWN ISSUES & SOLUTIONS

## Issue 1: Bell Widget Not Showing
**Symptoms:** Bell icon doesn't appear in navbar
**Causes:**
- User not logged in
- Widget template not included
- JavaScript errors

**Solutions:**
1. Check if user is authenticated
2. Verify `{% include 'notifications/widget.html' %}` in base.html
3. Check browser console for errors
4. Clear browser cache

## Issue 2: Notifications Not Being Created
**Symptoms:** No notifications appear after actions
**Causes:**
- Migrations not run
- Notification type disabled in preferences
- Error in notification creation

**Solutions:**
1. Run migrations: `python manage.py migrate`
2. Check user preferences
3. Check server logs for errors
4. Test with test_notifications.py script

## Issue 3: Badge Count Not Updating
**Symptoms:** Badge shows wrong count or doesn't update
**Causes:**
- JavaScript not running
- API endpoint error
- CSRF token issues

**Solutions:**
1. Check browser console for errors
2. Test API endpoint: `/notifications/api/unread-count/`
3. Verify CSRF token in cookies
4. Refresh page

## Issue 4: Duplicate Notifications
**Symptoms:** Multiple notifications for same event
**Causes:**
- Function called multiple times
- No duplicate check

**Solutions:**
1. Add duplicate check before creating
2. Use get_or_create where appropriate
3. Check for existing notifications in time window

## Issue 5: Performance Issues
**Symptoms:** Slow page loads, high database queries
**Causes:**
- N+1 query problems
- Missing indexes
- No caching

**Solutions:**
1. Use select_related() and prefetch_related()
2. Add database indexes
3. Implement caching for leaderboard
4. Paginate large result sets

---

# 🔧 OPTIMIZATION RECOMMENDATIONS

## 1. Database Indexes
```python
# In models.py
class Notification(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
```

## 2. Caching Leaderboard
```python
from django.core.cache import cache

def get_leaderboard(period, category):
    cache_key = f'leaderboard_{period}_{category}'
    data = cache.get(cache_key)
    
    if not data:
        # Calculate leaderboard
        data = calculate_leaderboard()
        cache.set(cache_key, data, 3600)  # 1 hour
    
    return data
```

## 3. Async Notification Creation
```python
# Using Celery
from celery import shared_task

@shared_task
def send_notification_async(user_id, notification_type, title, message):
    user = User.objects.get(id=user_id)
    create_notification(user, notification_type, title, message)
```

## 4. Batch Notification Deletion
```python
# Instead of deleting one by one
Notification.objects.filter(
    recipient=user,
    created_at__lt=timezone.now() - timedelta(days=30)
).delete()
```

---

# 📊 MONITORING

## Metrics to Track
1. **Notification Creation Rate**
   - Notifications created per hour
   - By type distribution

2. **User Engagement**
   - Notification read rate
   - Click-through rate
   - Time to read

3. **Performance**
   - API response times
   - Database query counts
   - Page load times

4. **Errors**
   - Failed notification creations
   - JavaScript errors
   - API errors

## Logging
```python
import logging
logger = logging.getLogger(__name__)

# Log notification creation
logger.info(f"Created notification {notif.id} for user {user.id}")

# Log errors
logger.error(f"Failed to create notification: {e}")

# Log performance
logger.debug(f"Leaderboard update took {elapsed}s")
```

---

# ✅ TESTING COMMANDS

## Run Test Script
```bash
python manage.py shell < test_notifications.py
```

## Check Database
```bash
python manage.py shell

from apps.notifications.models import Notification
Notification.objects.count()
Notification.objects.filter(is_read=False).count()
```

## Check Migrations
```bash
python manage.py showmigrations notifications
python manage.py migrate --plan
```

## Run Django Tests
```bash
python manage.py test apps.notifications
```

---

# 🎯 NEXT STEPS AFTER TESTING

1. **If tests pass:**
   - Deploy to production
   - Monitor for issues
   - Gather user feedback

2. **If tests fail:**
   - Fix identified bugs
   - Re-run tests
   - Document fixes

3. **Improvements:**
   - Add more notification types
   - Implement email notifications
   - Add real-time updates
   - Create mobile app
