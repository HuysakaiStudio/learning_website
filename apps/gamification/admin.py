from django.contrib import admin
from .models import DailyChallenge, UserChallengeProgress


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'target_value', 'xp_reward', 'date', 'is_active']
    list_filter = ['challenge_type', 'date', 'is_active']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'


@admin.register(UserChallengeProgress)
class UserChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'current_value', 'completed', 'completed_at', 'xp_awarded']
    list_filter = ['completed', 'challenge__date', 'challenge__challenge_type']
    search_fields = ['user__username', 'challenge__title']
    date_hierarchy = 'completed_at'
    readonly_fields = ['completed_at', 'xp_awarded']
