from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q, F
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Leaderboard, LeaderboardEntry, Achievement
from apps.kien_thuc.models import Mon, FlashcardProgress
from apps.de_thi.models import KetQua, UserAnalytics

def leaderboard_view(request):
    """Main leaderboard page"""
    period = request.GET.get('period', 'weekly')
    category = request.GET.get('category', 'overall')
    mon_id = request.GET.get('mon')
    
    # Get or create leaderboard
    leaderboard_filter = {
        'period': period,
        'category': category,
    }
    
    if category == 'subject' and mon_id:
        mon = get_object_or_404(Mon, id=mon_id)
        leaderboard_filter['mon'] = mon
    else:
        mon = None
    
    leaderboard, created = Leaderboard.objects.get_or_create(**leaderboard_filter)
    
    # Update leaderboard if needed (older than 1 hour)
    if created or (timezone.now() - leaderboard.last_updated) > timedelta(hours=1):
        update_leaderboard(leaderboard)
    
    # Get entries (top 100) - optimized with select_related
    entries = leaderboard.entries.select_related('user').all()[:100]
    
    # Get user's rank if logged in
    user_entry = None
    if request.user.is_authenticated:
        # Check if user is in top 100
        user_entry = leaderboard.entries.filter(user=request.user).first()
    
    # Get all subjects for filter
    mon_list = Mon.objects.all()
    
    context = {
        'leaderboard': leaderboard,
        'entries': entries,
        'user_entry': user_entry,
        'period': period,
        'category': category,
        'selected_mon': mon,
        'mon_list': mon_list,
    }
    
    return render(request, 'leaderboard/index.html', context)


def update_leaderboard(leaderboard):
    """Update leaderboard rankings"""
    period = leaderboard.period
    category = leaderboard.category
    mon = leaderboard.mon
    
    # Calculate date range for period
    now = timezone.now()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:  # all_time
        start_date = None
    
    # Get users and calculate scores based on category
    if category == 'overall':
        users_data = calculate_overall_scores(start_date)
    elif category == 'subject':
        users_data = calculate_subject_scores(start_date, mon)
    elif category == 'flashcard':
        users_data = calculate_flashcard_scores(start_date)
    elif category == 'exam':
        users_data = calculate_exam_scores(start_date)
    else:
        users_data = []
    
    # Sort by score and assign ranks
    users_data.sort(key=lambda x: x['score'], reverse=True)
    
    # Clear old entries
    LeaderboardEntry.objects.filter(leaderboard=leaderboard).delete()
    
    # Create new entries
    entries = []
    rankings = []
    for rank, user_data in enumerate(users_data, 1):
        entry = LeaderboardEntry(
            leaderboard=leaderboard,
            user_id=user_data['user_id'],
            score=user_data['score'],
            rank=rank,
            exams_completed=user_data.get('exams_completed', 0),
            flashcards_learned=user_data.get('flashcards_learned', 0),
            total_time_minutes=user_data.get('total_time_minutes', 0),
        )
        entries.append(entry)
        
        rankings.append({
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'score': user_data['score'],
            'rank': rank,
        })
    
    LeaderboardEntry.objects.bulk_create(entries)
    
    # Update cached rankings
    leaderboard.rankings = rankings[:100]  # Store top 100
    leaderboard.save()
    
    # Note: Achievements and notifications are now sent via management command
    # Run: python manage.py send_leaderboard_notifications --period=daily/weekly/monthly
    # This prevents sending notifications on every page view


def calculate_overall_scores(start_date=None):
    """Calculate overall scores based on exams and flashcards"""
    users = User.objects.filter(is_active=True)
    users_data = []
    
    for user in users:
        # Get exam stats
        exam_filter = Q(nguoi_dung=user, is_official=True)
        if start_date:
            exam_filter &= Q(ngay_lam__gte=start_date)
        
        exam_stats = KetQua.objects.filter(exam_filter).aggregate(
            avg_score=Avg('diem'),
            count=Count('id'),
            total_time=Sum('thoi_gian_lam')
        )
        
        # Get flashcard stats
        flashcard_filter = Q(user=user, is_learned=True)
        if start_date:
            flashcard_filter &= Q(ngay_cap_nhat__gte=start_date)
        
        flashcard_count = FlashcardProgress.objects.filter(flashcard_filter).count()
        
        # Calculate score (weighted average)
        exam_score = (exam_stats['avg_score'] or 0) * (exam_stats['count'] or 0) * 0.7
        flashcard_score = flashcard_count * 0.3
        total_score = exam_score + flashcard_score
        
        if total_score > 0:
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'score': total_score,
                'exams_completed': exam_stats['count'] or 0,
                'flashcards_learned': flashcard_count,
                'total_time_minutes': int((exam_stats['total_time'] or 0) / 60),
            })
    
    return users_data


def calculate_subject_scores(start_date, mon):
    """Calculate scores for specific subject"""
    if not mon:
        return []
    
    users = User.objects.filter(is_active=True)
    users_data = []
    
    for user in users:
        exam_filter = Q(nguoi_dung=user, de_thi__mon=mon, is_official=True)
        if start_date:
            exam_filter &= Q(ngay_lam__gte=start_date)
        
        exam_stats = KetQua.objects.filter(exam_filter).aggregate(
            avg_score=Avg('diem'),
            count=Count('id')
        )
        
        score = (exam_stats['avg_score'] or 0) * (exam_stats['count'] or 0)
        
        if score > 0:
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'score': score,
                'exams_completed': exam_stats['count'] or 0,
            })
    
    return users_data


def calculate_flashcard_scores(start_date):
    """Calculate flashcard mastery scores"""
    users = User.objects.filter(is_active=True)
    users_data = []
    
    for user in users:
        filter_q = Q(user=user, is_learned=True)
        if start_date:
            filter_q &= Q(ngay_cap_nhat__gte=start_date)
        
        flashcard_count = FlashcardProgress.objects.filter(filter_q).count()
        
        if flashcard_count > 0:
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'score': flashcard_count,
                'flashcards_learned': flashcard_count,
            })
    
    return users_data


def calculate_exam_scores(start_date):
    """Calculate exam performance scores"""
    users = User.objects.filter(is_active=True)
    users_data = []
    
    for user in users:
        filter_q = Q(nguoi_dung=user, is_official=True)
        if start_date:
            filter_q &= Q(ngay_lam__gte=start_date)
        
        exam_stats = KetQua.objects.filter(filter_q).aggregate(
            avg_score=Avg('diem'),
            count=Count('id')
        )
        
        score = (exam_stats['avg_score'] or 0) * (exam_stats['count'] or 0)
        
        if score > 0:
            users_data.append({
                'user_id': user.id,
                'username': user.username,
                'score': score,
                'exams_completed': exam_stats['count'] or 0,
            })
    
    return users_data


def award_achievements(leaderboard, top_entries):
    """Award achievements to top performers"""
    from apps.notifications.utils import notify_new_achievement, notify_leaderboard_rank
    
    period = leaderboard.period
    
    # Determine achievement type
    if period == 'daily':
        achievement_type = 'top_10_daily'
    elif period == 'weekly':
        achievement_type = 'top_10_weekly'
    elif period == 'monthly':
        achievement_type = 'top_10_monthly'
    else:
        achievement_type = 'top_100_all_time'
    
    # Award to top 10 (or top 100 for all_time)
    limit = 100 if period == 'all_time' else 10
    
    for entry in top_entries[:limit]:
        # Check if already has this achievement for this period
        existing = Achievement.objects.filter(
            user=entry.user,
            achievement_type=achievement_type,
            earned_at__gte=timezone.now() - timedelta(days=1)
        ).exists()
        
        if not existing:
            achievement = Achievement.objects.create(
                user=entry.user,
                achievement_type=achievement_type,
                rank_achieved=entry.rank,
                score_achieved=entry.score,
                mon=leaderboard.mon
            )
            
            # Send achievement notification
            notify_new_achievement(entry.user, achievement)
        
        # Send leaderboard rank notification for top 10
        if entry.rank <= 10:
            notify_leaderboard_rank(entry.user, entry.rank, period, leaderboard.category)


@login_required
def user_achievements(request):
    """View user's achievements"""
    achievements = Achievement.objects.filter(user=request.user).order_by('-earned_at')
    
    context = {
        'achievements': achievements,
    }
    
    return render(request, 'leaderboard/achievements.html', context)
