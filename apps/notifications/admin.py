from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_archived', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('recipient', 'sender', 'notification_type')
        }),
        ('Nội dung', {
            'fields': ('title', 'message', 'action_url')
        }),
        ('Liên kết', {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_read', 'is_archived', 'created_at', 'read_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('recipient', 'sender', 'content_type')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'email_frequency']
    search_fields = ['user__username']
    
    fieldsets = (
        ('Người dùng', {
            'fields': ('user',)
        }),
        ('Loại thông báo', {
            'fields': (
                'enable_badge',
                'enable_forum_reply',
                'enable_leaderboard',
                'enable_achievement',
                'enable_study_reminder',
                'enable_exam_result',
                'enable_flashcard_milestone',
                'enable_system',
            )
        }),
        ('Email', {
            'fields': ('email_notifications', 'email_frequency')
        }),
    )
