from django.contrib import admin
from .models import UserProfile, Badge, UserBadge, UserGamification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'description']
    list_filter = ['tier']
    search_fields = ['name']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['nguoi_dung', 'badge', 'ngay_dat_duoc']
    list_filter = ['badge__tier', 'ngay_dat_duoc']
    search_fields = ['nguoi_dung__username', 'badge__name']
    date_hierarchy = 'ngay_dat_duoc'


@admin.register(UserGamification)
class UserGamificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'xp', 'current_streak', 'longest_streak', 'last_activity_date', 'updated_at']
    list_filter = ['level', 'last_activity_date']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-xp']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Experience & Level', {
            'fields': ('xp', 'level')
        }),
        ('Streak Information', {
            'fields': ('current_streak', 'longest_streak', 'last_activity_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
