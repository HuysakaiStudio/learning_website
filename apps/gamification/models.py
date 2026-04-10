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
            try:
                profile = UserProfile.objects.get(user=self.user)
                profile.xp += self.challenge.xp_reward
                profile.save()
            except UserProfile.DoesNotExist:
                pass

            self.save()
            return True
        return False
