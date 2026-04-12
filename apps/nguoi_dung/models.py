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
        """Calculate level from XP using formula: level = sqrt(xp/100)"""
        import math
        if self.xp <= 0:
            return 0
        # Inverse of XP = level^2 * 100 -> level = sqrt(XP / 100)
        return int(math.sqrt(max(0, self.xp / 100)))
    
    def add_xp(self, amount, reason=''):
        """Add XP and update level with proper overflow handling"""
        old_level = self.level
        old_xp = self.xp
        
        # Add the new XP
        self.xp += amount
        
        # Calculate the new level based on total XP
        new_level = self.calculate_level()
        
        # Check if level increased
        leveled_up = new_level > old_level
        
        # If level increased, we need to handle XP overflow
        if leveled_up:
            # Calculate the XP threshold for the old level
            from apps.nguoi_dung.xp_utils import calculate_xp_for_level
            xp_for_old_level = calculate_xp_for_level(old_level)
            xp_for_new_level = calculate_xp_for_level(new_level)
            
            # The XP that belongs to the new level
            xp_in_new_level = self.xp - xp_for_old_level
            
            # Update to the new level
            self.level = new_level
        else:
            # Level didn't change, just update the level in case it should have
            self.level = new_level
        
        self.save()
        
        return {
            'xp_gained': amount,
            'total_xp': self.xp,
            'old_level': old_level,
            'new_level': self.level,
            'leveled_up': leveled_up,
            'reason': reason
        }
    
    def add_xp_with_overflow_handling(self, amount, reason=''):
        """Add XP with proper overflow handling to the next level"""
        old_level = self.level
        old_xp = self.xp
        
        # Add the new XP
        temp_total_xp = old_xp + amount
        
        # Calculate what the new level should be
        new_level = self._calculate_level_from_xp(temp_total_xp)
        
        # Check if level increased
        leveled_up = new_level > old_level
        
        # Update both XP and level
        self.xp = temp_total_xp
        self.level = new_level
        
        self.save()
        
        return {
            'xp_gained': amount,
            'total_xp': self.xp,
            'old_level': old_level,
            'new_level': self.level,
            'leveled_up': leveled_up,
            'reason': reason
        }
    
    def _calculate_level_from_xp(self, xp):
        """Calculate level from XP using the same formula"""
        import math
        if xp <= 0:
            return 0
        # Inverse of XP = level^2 * 100 -> level = sqrt(XP / 100)
        return int(math.sqrt(max(0, xp / 100)))
    
    def get_xp_for_level(self, level_num):
        """Get the XP required to reach a specific level"""
        if level_num <= 0:
            return 0
        # XP = level^2 * 100
        return level_num * level_num * 100
    
    def get_current_level_max_xp(self):
        """Get the maximum XP required to complete the current level"""
        return self.get_xp_for_level(self.level + 1)
    
    def get_current_level_min_xp(self):
        """Get the minimum XP required to be at the current level"""
        return self.get_xp_for_level(self.level)
    
    def get_xp_into_current_level(self):
        """Get how much XP the user has accumulated in their current level"""
        level_min_xp = self.get_current_level_min_xp()
        return max(0, self.xp - level_min_xp)
    
    def get_xp_needed_for_next_level(self):
        """Get how much XP is needed to reach the next level"""
        if self.level == 0:
            # Special case for level 0
            xp_for_level_1 = self.get_xp_for_level(1)
            return max(0, xp_for_level_1 - self.xp)
        else:
            xp_for_next_level = self.get_xp_for_level(self.level + 1)
            return max(0, xp_for_next_level - self.xp)
    
    def get_level_progress_percentage(self):
        """Get the percentage progress to the next level"""
        if self.level == 0:
            xp_for_level_1 = self.get_xp_for_level(1)
            if xp_for_level_1 == 0:
                return 0
            return min(100, (self.xp / xp_for_level_1) * 100)
        else:
            level_min_xp = self.get_current_level_min_xp()
            xp_for_next_level = self.get_xp_for_level(self.level + 1)
            
            if xp_for_next_level <= level_min_xp:
                return 100  # Already at max level theoretically
               
            xp_in_current_level = self.xp - level_min_xp
            xp_needed_in_level = xp_for_next_level - level_min_xp
            
            if xp_needed_in_level == 0:
                return 100
                
            return min(100, (xp_in_current_level / xp_needed_in_level) * 100)

    def get_enhanced_level_progress(self):
        """Get comprehensive level progress information for UI display"""
        current_level_start_xp = self.level * self.level * 100
        next_level_start_xp = (self.level + 1) * (self.level + 1) * 100
        
        xp_in_current_level = max(0, self.xp - current_level_start_xp)
        xp_needed_for_next_level = next_level_start_xp - current_level_start_xp
        
        progress_percent = 0
        if xp_needed_for_next_level > 0:
            progress_percent = min(100, (xp_in_current_level / xp_needed_for_next_level) * 100)
        
        return {
            'current_level': self.level,
            'current_xp': self.xp,
            'xp_in_current_level': int(xp_in_current_level),
            'xp_for_current_level': int(current_level_start_xp),
            'xp_for_next_level': int(next_level_start_xp),
            'xp_needed_for_next_level': int(xp_needed_for_next_level),
            'progress_percent': round(progress_percent, 1),
            'xp_remaining': int(xp_needed_for_next_level - xp_in_current_level) if xp_needed_for_next_level > 0 else 0,
            'level_name': self.get_level_name(),
            'next_level_name': self.get_level_name(self.level + 1)
        }

    def get_level_name(self, level=None):
        """Get a descriptive name for a level"""
        if level is None:
            level = self.level
            
        # Define level tiers with Vietnamese names
        if level < 5:
            return "Mầm Non"
        elif level < 10:
            return "Học Sinh"
        elif level < 20:
            return "Sinh Viên"
        elif level < 30:
            return "Cử Nhân"
        elif level < 50:
            return "Thạc Sĩ"
        elif level < 75:
            return "Tiến Sĩ"
        elif level < 100:
            return "Giáo Sư"
        else:
            return "Bậc Thầy"
    
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
        current_level_xp = self.level * self.level * 100 if self.level > 0 else 0
        next_level_xp = (self.level + 1) * (self.level + 1) * 100
        xp_in_current_level = self.xp - current_level_xp
        xp_needed = next_level_xp - current_level_xp
        
        # Ensure xp_in_current_level doesn't go negative
        xp_in_current_level = max(0, xp_in_current_level)
        
        return {
            'current': int(xp_in_current_level),
            'needed': int(xp_needed),
            'progress_percent': min(100, (xp_in_current_level / xp_needed) * 100) if xp_needed > 0 else 0
        }
    
    def get_level_progress_info(self):
        """Get comprehensive level progress information"""
        import math
        from apps.nguoi_dung.xp_utils import calculate_xp_for_level
        
        current_level_start_xp = calculate_xp_for_level(self.level)
        next_level_start_xp = calculate_xp_for_level(self.level + 1)
        
        xp_in_current_level = self.xp - current_level_start_xp
        xp_needed_for_next_level = next_level_start_xp - current_level_start_xp
        
        # Ensure xp_in_current_level doesn't go negative
        xp_in_current_level = max(0, xp_in_current_level)
        
        return {
            'current_level': self.level,
            'current_xp': self.xp,
            'xp_in_current_level': int(xp_in_current_level),
            'xp_for_current_level': int(current_level_start_xp),
            'xp_for_next_level': int(next_level_start_xp),
            'xp_needed_for_next_level': int(xp_needed_for_next_level),
            'progress_percent': min(100, (xp_in_current_level / xp_needed_for_next_level) * 100) if xp_needed_for_next_level > 0 else 0,
            'xp_remaining': int(xp_needed_for_next_level - xp_in_current_level) if xp_needed_for_next_level > 0 else 0
        }
    
    def get_accurate_level_progress(self):
        """Get accurate progress information that handles edge cases"""
        import math
        
        if self.level == 0:
            # For level 0, calculate based on XP needed to reach level 1
            xp_for_level_1 = math.pow(100, 1.5)  # This is the XP needed for level 1
            progress_percent = min(100, (self.xp / xp_for_level_1) * 100) if xp_for_level_1 > 0 else 0
            return {
                'current_level': 0,
                'current_xp': self.xp,
                'xp_in_current_level': self.xp,
                'xp_for_next_level': int(xp_for_level_1),
                'progress_percent': progress_percent,
                'xp_remaining': int(xp_for_level_1 - self.xp) if self.xp < xp_for_level_1 else 0
            }
        else:
            # For higher levels, calculate normally
            current_level_start_xp = math.pow(self.level * 100, 1.5)
            next_level_start_xp = math.pow((self.level + 1) * 100, 1.5)
            
            # Ensure the user's XP is at least at the start of the current level
            actual_xp_in_level = max(0, self.xp - current_level_start_xp)
            xp_needed_for_next_level = next_level_start_xp - current_level_start_xp
            
            progress_percent = min(100, (actual_xp_in_level / xp_needed_for_next_level) * 100) if xp_needed_for_next_level > 0 else 0
            
            return {
                'current_level': self.level,
                'current_xp': self.xp,
                'xp_in_current_level': int(actual_xp_in_level),
                'xp_for_current_level': int(current_level_start_xp),
                'xp_for_next_level': int(next_level_start_xp),
                'xp_needed_for_next_level': int(xp_needed_for_next_level),
                'progress_percent': progress_percent,
                'xp_remaining': int(xp_needed_for_next_level - actual_xp_in_level) if xp_needed_for_next_level > 0 else 0
            }
    
    def get_max_xp_for_level(self, level):
        """Get the maximum XP required to reach the given level"""
        if level <= 0:
            return 0
        # XP = level^2 * 100
        return level * level * 100
    
    def get_level_range(self, level=None):
        """Get XP range for a specific level (min and max XP needed)"""
        if level is None:
            level = self.level
        
        min_xp = level * level * 100 if level > 0 else 0
        max_xp = (level + 1) * (level + 1) * 100
        
        return {
            'min_xp': int(min_xp),
            'max_xp': int(max_xp),
            'range': int(max_xp - min_xp)
        }
    
    def get_xp_towards_next_level(self):
        """Get the XP progress towards the next level"""
        current_level_start_xp = self.level * self.level * 100
        next_level_start_xp = (self.level + 1) * (self.level + 1) * 100
        
        xp_in_current_level = self.xp - current_level_start_xp
        xp_needed_for_next_level = next_level_start_xp - current_level_start_xp
        
        return {
            'current_in_level': int(xp_in_current_level),
            'needed_for_next_level': int(xp_needed_for_next_level),
            'percentage_complete': min(100, (xp_in_current_level / xp_needed_for_next_level) * 100) if xp_needed_for_next_level > 0 else 0,
            'remaining_xp': int(xp_needed_for_next_level - xp_in_current_level) if xp_needed_for_next_level > 0 else 0
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

