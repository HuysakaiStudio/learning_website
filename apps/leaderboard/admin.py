from django.contrib import admin
from .models import Leaderboard, LeaderboardEntry, Achievement

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'period', 'category', 'mon', 'last_updated']
    list_filter = ['period', 'category', 'mon']
    search_fields = ['mon__ten']
    readonly_fields = ['last_updated']

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['rank', 'user', 'leaderboard', 'score', 'exams_completed', 'flashcards_learned']
    list_filter = ['leaderboard__period', 'leaderboard__category']
    search_fields = ['user__username']
    ordering = ['leaderboard', 'rank']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement_type', 'mon', 'rank_achieved', 'earned_at']
    list_filter = ['achievement_type', 'mon']
    search_fields = ['user__username']
    ordering = ['-earned_at']
