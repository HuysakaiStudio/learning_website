from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
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
