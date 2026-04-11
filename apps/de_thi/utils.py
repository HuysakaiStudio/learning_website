from django.utils import timezone
from .models import PracticeSession
from datetime import timedelta

def get_daily_practice_count(user):
    """Get the number of practice sessions for a user today"""
    today = timezone.now().date()
    return PracticeSession.objects.filter(
        nguoi_dung=user,
        is_practice=True,
        created_at__date=today
    ).count()

def increment_daily_practice(user, de_thi):
    """Increment the daily practice count for a user"""
    session, created = PracticeSession.objects.get_or_create(
        nguoi_dung=user,
        de_thi=de_thi,
        is_practice=True,
        defaults={'created_at': timezone.now()}
    )
    return session

def reset_practice_limits_if_needed(user_profile):
    """Reset practice limits if the reset date has passed"""
    now = timezone.now()
    
    # Reset daily counters if a new day has started
    if user_profile.practice_limit_reset_date.date() < now.date():
        user_profile.current_daily_practice_count = 0
        
        # Reset weekly counter if a new week has started
        if now.date().weekday() == 0:  # Monday
            user_profile.current_weekly_practice_count = 0
        
        user_profile.practice_limit_reset_date = now
        user_profile.save()

def check_practice_limits(user_profile):
    """Check if user has exceeded practice limits"""
    reset_practice_limits_if_needed(user_profile)
    
    daily_exceeded = user_profile.current_daily_practice_count >= user_profile.daily_practice_limit
    weekly_exceeded = user_profile.current_weekly_practice_count >= user_profile.weekly_practice_limit
    
    return {
        'daily_exceeded': daily_exceeded,
        'weekly_exceeded': weekly_exceeded,
        'can_practice': not (daily_exceeded or weekly_exceeded)
    }