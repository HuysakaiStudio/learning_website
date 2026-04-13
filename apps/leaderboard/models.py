from django.db import models
from django.contrib.auth.models import User
from apps.kien_thuc.models import Mon



class Leaderboard(models.Model):
    """Bảng xếp hạng với các period và category khác nhau"""
    PERIOD_CHOICES = [
        ('daily', 'Hàng ngày'),
        ('weekly', 'Hàng tuần'),
        ('monthly', 'Hàng tháng'),
        ('all_time', 'Mọi thời gian'),
    ]
    
    CATEGORY_CHOICES = [
        ('overall', 'Tổng thể'),
        ('subject', 'Theo môn'),
        ('flashcard', 'Flashcard'),
        ('exam', 'Đề thi'),
    ]
    
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    mon = models.ForeignKey(Mon, on_delete=models.CASCADE, null=True, blank=True, 
                           help_text='Chỉ dùng khi category=subject')
    
    # Cached rankings (cập nhật định kỳ)
    rankings = models.JSONField(default=list, help_text='[{user_id, username, score, rank}, ...]')
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Bảng xếp hạng'
        verbose_name_plural = 'Bảng xếp hạng'
        unique_together = ('period', 'category', 'mon')
        ordering = ['period', 'category']
        indexes = [
            models.Index(fields=['period', 'category']),
            models.Index(fields=['last_updated']),
        ]
    
    def __str__(self):
        mon_str = f' - {self.mon.ten}' if self.mon else ''
        return f'{self.get_period_display()} - {self.get_category_display()}{mon_str}'


class LeaderboardEntry(models.Model):
    """Entry cho từng user trong leaderboard"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    score = models.FloatField(default=0)
    total_score = models.FloatField(db_index=True, help_text='Total accumulated score', default=0)
    rank = models.IntegerField(default=0)
    
    # Metadata
    exams_completed = models.IntegerField(default=0)
    flashcards_learned = models.IntegerField(default=0)
    total_time_minutes = models.IntegerField(default=0)
    
    # Flashcard-related fields
    flashcard_avg_score = models.FloatField(default=0.0, help_text='Average score for flashcard learning')
    flashcard_total_cards = models.IntegerField(default=0, help_text='Total number of flashcards studied')
    last_flashcard_study = models.DateTimeField(blank=True, null=True, help_text='Last time user studied flashcards')
    weekly_flashcard_count = models.IntegerField(default=0, help_text='Number of flashcards studied this week')
    flashcard_streak = models.IntegerField(default=0, help_text='Current flashcard study streak')
    
    # Study time tracking
    total_study_time_minutes = models.IntegerField(default=0, help_text='Total study time in minutes (exams + flashcards)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Entry xếp hạng'
        verbose_name_plural = 'Entry xếp hạng'
        unique_together = ('user', 'leaderboard')
        ordering = ['rank']
        indexes = [
            models.Index(fields=['leaderboard', 'rank']),
            models.Index(fields=['user', 'leaderboard']),
            models.Index(fields=['score']),
        ]
    
    def __str__(self):
        return f'#{self.rank} - {self.user.username} ({self.score:.1f})'


class Achievement(models.Model):
    """Thành tựu đặc biệt (Top 10, Top 100, etc.)"""
    ACHIEVEMENT_TYPES = [
        ('top_10_daily', 'Top 10 Hàng ngày'),
        ('top_10_weekly', 'Top 10 Hàng tuần'),
        ('top_10_monthly', 'Top 10 Hàng tháng'),
        ('top_100_all_time', 'Top 100 Mọi thời gian'),
        ('subject_master', 'Bậc thầy môn học'),
        ('flashcard_king', 'Vua Flashcard'),
        ('exam_champion', 'Nhà vô địch Đề thi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPES)
    mon = models.ForeignKey(Mon, on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadata
    rank_achieved = models.IntegerField(null=True, blank=True)
    score_achieved = models.FloatField(null=True, blank=True)
    
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Thành tựu'
        verbose_name_plural = 'Thành tựu'
        ordering = ['-earned_at']
        indexes = [
            models.Index(fields=['user', 'achievement_type']),
            models.Index(fields=['earned_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.get_achievement_type_display()}'
