from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class UserGamification(models.Model):
    """
    Gamification system: XP, Level, Streak tracking
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gamification')
    
    # XP and Level
    xp = models.IntegerField(default=0, help_text='Total experience points')
    level = models.IntegerField(default=0, help_text='Current level (calculated from XP)')
    
    # Streak tracking
    current_streak = models.IntegerField(default=0, help_text='Current consecutive study days')
    longest_streak = models.IntegerField(default=0, help_text='Longest streak ever achieved')
    last_activity_date = models.DateField(null=True, blank=True, help_text='Last day user was active')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Gamification'
        verbose_name_plural = 'User Gamifications'
        indexes = [
            models.Index(fields=['xp']),
            models.Index(fields=['level']),
            models.Index(fields=['current_streak']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - Level {self.level} ({self.xp} XP)'
    
    def calculate_level(self):
        """Calculate level from XP using formula: level = floor((xp/100)^(1/1.5))"""
        import math
        if self.xp <= 0:
            return 0
        return math.floor(math.pow(self.xp / 100, 1 / 1.5))
    
    def add_xp(self, amount, reason=''):
        """Add XP and update level"""
        old_level = self.level
        self.xp += amount
        self.level = self.calculate_level()
        self.save()
        
        # Check if leveled up
        leveled_up = self.level > old_level
        return {
            'xp_gained': amount,
            'total_xp': self.xp,
            'old_level': old_level,
            'new_level': self.level,
            'leveled_up': leveled_up,
            'reason': reason
        }
    
    def update_streak(self):
        """Update streak based on last activity date"""
        today = timezone.now().date()
        
        if self.last_activity_date is None:
            # First time activity
            self.current_streak = 1
            self.last_activity_date = today
        elif self.last_activity_date == today:
            # Already counted today
            return False
        elif self.last_activity_date == today - timedelta(days=1):
            # Continuing streak
            self.current_streak += 1
            self.last_activity_date = today
            
            # Update longest streak
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Streak broken
            self.current_streak = 1
            self.last_activity_date = today
        
        self.save()
        return True
    
    def get_xp_for_next_level(self):
        """Calculate XP needed for next level"""
        import math
        current_level_xp = math.pow(self.level * 100, 1.5)
        next_level_xp = math.pow((self.level + 1) * 100, 1.5)
        xp_in_current_level = self.xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        
        return {
            'current': int(xp_in_current_level),
            'needed': int(xp_needed),
            'progress_percent': min(100, (xp_in_current_level / xp_needed) * 100) if xp_needed > 0 else 0
        }

class Badge(models.Model):
    TIER_CHOICES = [
        ('bronze', 'Đồng'),
        ('silver', 'Bạc'),
        ('gold', 'Vàng'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    
    def __str__(self):
        return f'{self.name} ({self.get_tier_display()})'
    
    def get_vietnamese_name(self):
        """Trả về tên tiếng Việt của huy hiệu"""
        vietnamese_names = {
            'Lính Mới': 'Lính Mới',
            'Học Bá': 'Học Bá',
            'Thợ Săn Điểm 10': 'Thợ Săn Điểm 10',
            'Trí Nhớ Siêu Phàm': 'Trí Nhớ Siêu Phàm',
            'Chăm Chỉ': 'Chăm Chỉ',
            'Novice': 'Người Mới',
            'Expert': 'Chuyên Gia',
            'Master': 'Bậc Thầy',
        }
        return vietnamese_names.get(self.name, self.name)

class UserBadge(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    ngay_dat_duoc = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('nguoi_dung', 'badge')

