from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

class Badge(models.Model):
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    
    def __str__(self):
        return f'{self.name} ({self.get_tier_display()})'

class UserBadge(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    ngay_dat_duoc = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('nguoi_dung', 'badge')

