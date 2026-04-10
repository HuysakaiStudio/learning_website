# Daily Challenges System

## Overview
Implement a daily challenge system to increase user engagement through gamification. Users complete daily goals to earn bonus XP and maintain streaks.

## Database Models

### Challenge Model
```python
# apps/gamification/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyChallenge(models.Model):
    """Daily challenges that rotate"""
    CHALLENGE_TYPES = [
        ('exam', 'Complete an exam'),
        ('flashcard', 'Study flashcards'),
        ('streak', 'Maintain login streak'),
        ('score', 'Achieve minimum score'),
        ('questions', 'Answer questions correctly'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    target_value = models.IntegerField(help_text="Target to complete (e.g., 10 flashcards, 80% score)")
    xp_reward = models.IntegerField(default=50)
    date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['challenge_type', 'date']
    
    def __str__(self):
        return f"{self.title} ({self.date})"


class UserChallengeProgress(models.Model):
    """Track user progress on daily challenges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_progress')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    current_value = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    xp_awarded = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'challenge']
        ordering = ['-challenge__date']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"
    
    @property
    def progress_percentage(self):
        if self.challenge.target_value == 0:
            return 0
        return min(100, int((self.current_value / self.challenge.target_value) * 100))
    
    def check_completion(self):
        """Check if challenge is completed and award XP"""
        if not self.completed and self.current_value >= self.challenge.target_value:
            self.completed = True
            self.completed_at = timezone.now()
            self.xp_awarded = self.challenge.xp_reward
            
            # Award XP to user profile
            from apps.nguoi_dung.models import UserProfile
            profile = UserProfile.objects.get(user=self.user)
            profile.xp += self.challenge.xp_reward
            profile.save()
            
            self.save()
            return True
        return False
```

## Views

### Challenge Dashboard View
```python
# apps/gamification/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DailyChallenge, UserChallengeProgress

@login_required
def daily_challenges(request):
    """Display today's challenges and user progress"""
    today = timezone.now().date()
    
    # Get today's active challenges
    challenges = DailyChallenge.objects.filter(date=today, is_active=True)
    
    # Get or create user progress for each challenge
    challenge_data = []
    for challenge in challenges:
        progress, created = UserChallengeProgress.objects.get_or_create(
            user=request.user,
            challenge=challenge
        )
        challenge_data.append({
            'challenge': challenge,
            'progress': progress,
        })
    
    # Calculate daily stats
    total_challenges = challenges.count()
    completed_challenges = UserChallengeProgress.objects.filter(
        user=request.user,
        challenge__date=today,
        completed=True
    ).count()
    
    total_xp_today = UserChallengeProgress.objects.filter(
        user=request.user,
        challenge__date=today,
        completed=True
    ).aggregate(models.Sum('xp_awarded'))['xp_awarded__sum'] or 0
    
    context = {
        'challenge_data': challenge_data,
        'total_challenges': total_challenges,
        'completed_challenges': completed_challenges,
        'total_xp_today': total_xp_today,
        'completion_rate': int((completed_challenges / total_challenges * 100)) if total_challenges > 0 else 0,
    }
    
    return render(request, 'gamification/daily_challenges.html', context)
```

## Management Command

### Generate Daily Challenges
```python
# apps/gamification/management/commands/generate_daily_challenges.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.gamification.models import DailyChallenge
import random

class Command(BaseCommand):
    help = 'Generate daily challenges for today'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Check if challenges already exist for today
        if DailyChallenge.objects.filter(date=today).exists():
            self.stdout.write(self.style.WARNING('Challenges already exist for today'))
            return
        
        # Challenge templates
        challenge_templates = [
            {
                'title': 'Hoàn thành 1 đề thi',
                'description': 'Làm và nộp bài một đề thi bất kỳ',
                'challenge_type': 'exam',
                'target_value': 1,
                'xp_reward': 100,
            },
            {
                'title': 'Học 20 flashcards',
                'description': 'Ôn tập ít nhất 20 thẻ flashcard',
                'challenge_type': 'flashcard',
                'target_value': 20,
                'xp_reward': 50,
            },
            {
                'title': 'Đạt điểm 8.0+',
                'description': 'Hoàn thành một bài thi với điểm từ 8.0 trở lên',
                'challenge_type': 'score',
                'target_value': 80,
                'xp_reward': 150,
            },
            {
                'title': 'Trả lời đúng 30 câu',
                'description': 'Trả lời đúng tổng cộng 30 câu hỏi trong ngày',
                'challenge_type': 'questions',
                'target_value': 30,
                'xp_reward': 75,
            },
            {
                'title': 'Duy trì streak',
                'description': 'Đăng nhập liên tiếp để duy trì chuỗi ngày học',
                'challenge_type': 'streak',
                'target_value': 1,
                'xp_reward': 25,
            },
        ]
        
        # Select 3 random challenges for today
        selected = random.sample(challenge_templates, 3)
        
        for template in selected:
            DailyChallenge.objects.create(
                date=today,
                **template
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(selected)} challenges for {today}'))
```

## URLs

```python
# apps/gamification/urls.py

from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('challenges/', views.daily_challenges, name='daily_challenges'),
]
```

## Template

```html
<!-- templates/gamification/daily_challenges.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}Thử thách hàng ngày{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/daily-challenges.css' %}">
{% endblock %}

{% block content %}
<div class="challenges-container">
  <div class="challenges-header">
    <h1>🎯 Thử thách hàng ngày</h1>
    <p class="text-muted">Hoàn thành thử thách để nhận XP thưởng</p>
  </div>

  <!-- Daily Stats -->
  <div class="daily-stats">
    <div class="stat-card">
      <div class="stat-icon">✅</div>
      <div class="stat-value">{{ completed_challenges }}/{{ total_challenges }}</div>
      <div class="stat-label">Hoàn thành</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">⭐</div>
      <div class="stat-value">{{ total_xp_today }}</div>
      <div class="stat-label">XP hôm nay</div>
    </div>
    <div class="stat-card">
      <div class="stat-icon">📊</div>
      <div class="stat-value">{{ completion_rate }}%</div>
      <div class="stat-label">Tỷ lệ hoàn thành</div>
    </div>
  </div>

  <!-- Challenge List -->
  <div class="challenges-list">
    {% for item in challenge_data %}
    <div class="challenge-card {% if item.progress.completed %}completed{% endif %}">
      <div class="challenge-header">
        <h3>{{ item.challenge.title }}</h3>
        {% if item.progress.completed %}
        <span class="badge-completed">✓ Hoàn thành</span>
        {% endif %}
      </div>
      
      <p class="challenge-description">{{ item.challenge.description }}</p>
      
      <div class="challenge-progress">
        <div class="progress-bar">
          <div class="progress-fill" style="width: {{ item.progress.progress_percentage }}%"></div>
        </div>
        <div class="progress-text">
          {{ item.progress.current_value }}/{{ item.challenge.target_value }}
        </div>
      </div>
      
      <div class="challenge-reward">
        <span class="xp-badge">+{{ item.challenge.xp_reward }} XP</span>
      </div>
    </div>
    {% empty %}
    <div class="empty-state">
      <p>Chưa có thử thách nào cho hôm nay</p>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

## Integration Points

### Update exam completion
```python
# In apps/de_thi/views.py - after exam submission

# Update challenge progress
from apps.gamification.models import DailyChallenge, UserChallengeProgress
from django.utils import timezone

today = timezone.now().date()
exam_challenges = DailyChallenge.objects.filter(
    date=today,
    challenge_type='exam',
    is_active=True
)

for challenge in exam_challenges:
    progress, created = UserChallengeProgress.objects.get_or_create(
        user=request.user,
        challenge=challenge
    )
    progress.current_value += 1
    progress.save()
    progress.check_completion()
```

### Update flashcard study
```python
# In apps/kien_thuc/views.py - after flashcard study

# Update challenge progress
progress_obj, created = UserChallengeProgress.objects.get_or_create(
    user=request.user,
    challenge__date=today,
    challenge__challenge_type='flashcard'
)
progress_obj.current_value += cards_studied
progress_obj.save()
progress_obj.check_completion()
```

## Cron Job Setup

Add to crontab to generate challenges daily at midnight:
```bash
0 0 * * * cd /path/to/project && python manage.py generate_daily_challenges
```

## Next Steps
1. Create CSS file for challenges UI
2. Add challenge notification system
3. Create admin interface for managing challenges
4. Add weekly/monthly challenge variants
