from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    """Hệ thống thông báo cho user"""
    
    NOTIFICATION_TYPES = [
        ('badge', 'Huy hiệu mới'),
        ('forum_reply', 'Trả lời diễn đàn'),
        ('leaderboard', 'Xếp hạng'),
        ('achievement', 'Thành tựu'),
        ('study_reminder', 'Nhắc nhở học tập'),
        ('exam_result', 'Kết quả thi'),
        ('flashcard_milestone', 'Cột mốc flashcard'),
        ('system', 'Hệ thống'),
    ]
    
    # User nhận thông báo
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name='Người nhận'
    )
    
    # Loại thông báo
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES,
        verbose_name='Loại thông báo'
    )
    
    # Nội dung
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    message = models.TextField(verbose_name='Nội dung')
    
    # Link đến object liên quan (generic relation)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # URL để redirect khi click
    action_url = models.CharField(
        max_length=500, 
        blank=True,
        verbose_name='Link hành động'
    )
    
    # Trạng thái
    is_read = models.BooleanField(default=False, verbose_name='Đã đọc')
    is_archived = models.BooleanField(default=False, verbose_name='Đã lưu trữ')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày đọc')
    
    # User gửi (optional, cho forum_reply)
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name='Người gửi'
    )
    
    class Meta:
        verbose_name = 'Thông báo'
        verbose_name_plural = 'Thông báo'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f'{self.recipient.username} - {self.get_notification_type_display()}: {self.title}'
    
    def mark_as_read(self):
        """Đánh dấu đã đọc"""
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_unread(self):
        """Đánh dấu chưa đọc"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=['is_read', 'read_at'])


class NotificationPreference(models.Model):
    """Cài đặt thông báo của user"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name='Người dùng'
    )
    
    # Bật/tắt từng loại thông báo
    enable_badge = models.BooleanField(default=True, verbose_name='Huy hiệu mới')
    enable_forum_reply = models.BooleanField(default=True, verbose_name='Trả lời diễn đàn')
    enable_leaderboard = models.BooleanField(default=True, verbose_name='Xếp hạng')
    enable_achievement = models.BooleanField(default=True, verbose_name='Thành tựu')
    enable_study_reminder = models.BooleanField(default=True, verbose_name='Nhắc nhở học tập')
    enable_exam_result = models.BooleanField(default=True, verbose_name='Kết quả thi')
    enable_flashcard_milestone = models.BooleanField(default=True, verbose_name='Cột mốc flashcard')
    enable_system = models.BooleanField(default=True, verbose_name='Hệ thống')
    
    # Email notifications
    email_notifications = models.BooleanField(default=False, verbose_name='Gửi email')
    
    # Tần suất gửi email
    EMAIL_FREQUENCY = [
        ('instant', 'Ngay lập tức'),
        ('daily', 'Hàng ngày'),
        ('weekly', 'Hàng tuần'),
        ('never', 'Không bao giờ'),
    ]
    email_frequency = models.CharField(
        max_length=10,
        choices=EMAIL_FREQUENCY,
        default='never',
        verbose_name='Tần suất email'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cài đặt thông báo'
        verbose_name_plural = 'Cài đặt thông báo'
    
    def __str__(self):
        return f'Cài đặt thông báo - {self.user.username}'
    
    def is_enabled(self, notification_type):
        """Kiểm tra xem loại thông báo có được bật không"""
        field_map = {
            'badge': self.enable_badge,
            'forum_reply': self.enable_forum_reply,
            'leaderboard': self.enable_leaderboard,
            'achievement': self.enable_achievement,
            'study_reminder': self.enable_study_reminder,
            'exam_result': self.enable_exam_result,
            'flashcard_milestone': self.enable_flashcard_milestone,
            'system': self.enable_system,
        }
        return field_map.get(notification_type, True)
