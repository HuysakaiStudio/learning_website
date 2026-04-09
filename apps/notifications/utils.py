"""Utility functions để tạo notifications"""
from django.contrib.auth.models import User
from .models import Notification, NotificationPreference


def create_notification(
    recipient,
    notification_type,
    title,
    message,
    action_url='',
    sender=None,
    content_object=None
):
    """
    Tạo notification mới
    
    Args:
        recipient: User object hoặc user_id
        notification_type: Loại thông báo (badge, forum_reply, etc.)
        title: Tiêu đề
        message: Nội dung
        action_url: URL để redirect
        sender: User gửi (optional)
        content_object: Object liên quan (optional)
    
    Returns:
        Notification object hoặc None nếu user tắt loại thông báo này
    """
    # Get user object
    if isinstance(recipient, int):
        try:
            recipient = User.objects.get(id=recipient)
        except User.DoesNotExist:
            return None
    
    # Check preferences
    try:
        prefs = NotificationPreference.objects.get(user=recipient)
        if not prefs.is_enabled(notification_type):
            return None
    except NotificationPreference.DoesNotExist:
        # Nếu chưa có preferences, tạo mới với default settings
        NotificationPreference.objects.create(user=recipient)
    
    # Create notification
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        sender=sender,
        content_object=content_object
    )
    
    return notification


def notify_new_achievement(user, achievement):
    """Thông báo khi đạt thành tựu mới"""
    return create_notification(
        recipient=user,
        notification_type='achievement',
        title='🏆 Thành tựu mới!',
        message=f'Chúc mừng! Bạn đã đạt thành tựu: {achievement.get_achievement_type_display()}',
        action_url='/leaderboard/achievements/',
        content_object=achievement
    )


def notify_leaderboard_rank(user, rank, period, category):
    """Thông báo khi lên hạng trong leaderboard"""
    period_map = {
        'daily': 'hàng ngày',
        'weekly': 'hàng tuần',
        'monthly': 'hàng tháng',
        'all_time': 'mọi thời gian'
    }
    
    return create_notification(
        recipient=user,
        notification_type='leaderboard',
        title=f'📊 Xếp hạng #{rank}',
        message=f'Bạn đang ở vị trí #{rank} trong bảng xếp hạng {period_map.get(period, period)}!',
        action_url='/leaderboard/'
    )


def notify_forum_reply(user, reply, post):
    """Thông báo khi có người reply bài viết"""
    return create_notification(
        recipient=user,
        notification_type='forum_reply',
        title='💬 Trả lời mới',
        message=f'{reply.nguoi_dung.username} đã trả lời bài viết của bạn',
        action_url=f'/de-thi/forum/{post.id}/',
        sender=reply.nguoi_dung,
        content_object=reply
    )


def notify_exam_result(user, ket_qua):
    """Thông báo kết quả thi"""
    diem = ket_qua.diem
    emoji = '🎉' if diem >= 8 else '👍' if diem >= 5 else '💪'
    
    return create_notification(
        recipient=user,
        notification_type='exam_result',
        title=f'{emoji} Kết quả thi',
        message=f'Bạn đã hoàn thành đề thi "{ket_qua.de_thi.tieu_de}" với điểm {diem:.1f}',
        action_url=f'/de-thi/ket-qua/{ket_qua.id}/',
        content_object=ket_qua
    )


def notify_flashcard_milestone(user, count):
    """Thông báo cột mốc flashcard"""
    milestones = {
        10: '🌱',
        50: '🌿',
        100: '🌳',
        500: '🏆',
        1000: '👑'
    }
    
    emoji = milestones.get(count, '⭐')
    
    return create_notification(
        recipient=user,
        notification_type='flashcard_milestone',
        title=f'{emoji} Cột mốc {count} flashcard!',
        message=f'Chúc mừng! Bạn đã học được {count} flashcard',
        action_url='/kien-thuc/'
    )


def notify_study_reminder(user):
    """Nhắc nhở học tập"""
    return create_notification(
        recipient=user,
        notification_type='study_reminder',
        title='📚 Đã đến giờ học!',
        message='Hãy dành chút thời gian để ôn tập hôm nay nhé!',
        action_url='/kien-thuc/'
    )


def notify_system(user, title, message, action_url=''):
    """Thông báo hệ thống"""
    return create_notification(
        recipient=user,
        notification_type='system',
        title=title,
        message=message,
        action_url=action_url
    )


def bulk_notify(users, notification_type, title, message, action_url=''):
    """Gửi thông báo hàng loạt cho nhiều users"""
    notifications = []
    
    for user in users:
        notif = create_notification(
            recipient=user,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=action_url
        )
        if notif:
            notifications.append(notif)
    
    return notifications
