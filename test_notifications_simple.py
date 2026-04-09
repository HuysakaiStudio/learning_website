"""
Simple Test Script for Notification System (No Emoji)
Run: python manage.py shell < test_notifications_simple.py
"""

from django.contrib.auth.models import User
from apps.notifications.models import Notification, NotificationPreference
from apps.notifications.utils import *

print("=" * 60)
print("TESTING NOTIFICATION SYSTEM")
print("=" * 60)

# Get or create test user
try:
    user = User.objects.first()
    if not user:
        print("No users found. Creating test user...")
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"[OK] Created test user: {user.username}")
    else:
        print(f"[OK] Using existing user: {user.username}")
except Exception as e:
    print(f"[ERROR] Error getting user: {e}")
    exit(1)

print("\n" + "=" * 60)
print("TEST 1: System Notification")
print("=" * 60)
try:
    notif = notify_system(
        user=user,
        title='Test System Notification',
        message='This is a test system notification',
        action_url='/kien-thuc/'
    )
    if notif:
        print(f"[OK] Created system notification: {notif.id}")
        print(f"     Title: {notif.title}")
        print(f"     Type: {notif.notification_type}")
    else:
        print("[WARN] Notification not created (user may have disabled this type)")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 2: Flashcard Milestone Notification")
print("=" * 60)
try:
    notif = notify_flashcard_milestone(user=user, count=10)
    if notif:
        print(f"[OK] Created flashcard milestone notification: {notif.id}")
        print(f"     Message: {notif.message}")
    else:
        print("[WARN] Notification not created")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 3: Leaderboard Rank Notification")
print("=" * 60)
try:
    notif = notify_leaderboard_rank(
        user=user,
        rank=5,
        period='weekly',
        category='overall'
    )
    if notif:
        print(f"[OK] Created leaderboard notification: {notif.id}")
        print(f"     Message: {notif.message}")
    else:
        print("[WARN] Notification not created")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 4: Check Notification Preferences")
print("=" * 60)
try:
    prefs, created = NotificationPreference.objects.get_or_create(user=user)
    if created:
        print("[OK] Created notification preferences")
    else:
        print("[OK] Notification preferences exist")
    
    print(f"   - Achievement: {prefs.enable_achievement}")
    print(f"   - Leaderboard: {prefs.enable_leaderboard}")
    print(f"   - Exam Result: {prefs.enable_exam_result}")
    print(f"   - Forum Reply: {prefs.enable_forum_reply}")
    print(f"   - Flashcard Milestone: {prefs.enable_flashcard_milestone}")
    print(f"   - Study Reminder: {prefs.enable_study_reminder}")
    print(f"   - Badge: {prefs.enable_badge}")
    print(f"   - System: {prefs.enable_system}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 5: Count Notifications")
print("=" * 60)
try:
    total = Notification.objects.filter(recipient=user).count()
    unread = Notification.objects.filter(recipient=user, is_read=False).count()
    print(f"[OK] Total notifications: {total}")
    print(f"[OK] Unread notifications: {unread}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 6: Test Mark as Read")
print("=" * 60)
try:
    notif = Notification.objects.filter(recipient=user, is_read=False).first()
    if notif:
        notif.mark_as_read()
        print(f"[OK] Marked notification {notif.id} as read")
        print(f"     Read at: {notif.read_at}")
    else:
        print("[WARN] No unread notifications to test")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 7: Bulk Notification")
print("=" * 60)
try:
    users = User.objects.all()[:3]
    notifications = bulk_notify(
        users=users,
        notification_type='system',
        title='Bulk Test',
        message='This is a bulk notification test'
    )
    print(f"[OK] Created {len(notifications)} bulk notifications")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("TEST 8: Notification Types")
print("=" * 60)
try:
    types = Notification.objects.filter(recipient=user).values_list('notification_type', flat=True).distinct()
    print(f"[OK] Notification types in database:")
    for t in types:
        count = Notification.objects.filter(recipient=user, notification_type=t).count()
        print(f"   - {t}: {count}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 60)
print("[OK] TESTING COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Visit /notifications/ to see the notification list")
print("2. Check the bell icon on the navbar")
print("3. Visit /notifications/preferences/ to test settings")
print("4. Try creating real notifications by:")
print("   - Taking an exam")
print("   - Learning flashcards")
print("   - Commenting on forum posts")
print("   - Getting into top 10 leaderboard")
print("=" * 60)
