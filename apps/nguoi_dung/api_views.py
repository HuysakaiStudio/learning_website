"""
API views for gamification system
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserGamification


@login_required
@require_http_methods(["GET"])
def get_gamification_stats(request):
    """Get user's gamification stats"""
    gamification, created = UserGamification.objects.get_or_create(user=request.user)
    
    if created:
        # Initialize level from XP
        gamification.level = gamification.calculate_level()
        gamification.save()
    
    # Use the enhanced level progress method for better UI display
    level_progress = gamification.get_enhanced_level_progress()
    
    return JsonResponse({
        'success': True,
        'data': {
            'xp': gamification.xp,
            'level': gamification.level,
            'current_streak': gamification.current_streak,
            'longest_streak': gamification.longest_streak,
            'last_activity_date': gamification.last_activity_date.isoformat() if gamification.last_activity_date else None,
            'level_progress': level_progress
        }
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def add_xp(request):
    """Add XP to user"""
    try:
        data = json.loads(request.body)
        amount = int(data.get('amount', 0))
        reason = data.get('reason', '')
        
        if amount <= 0:
            return JsonResponse({
                'success': False,
                'error': 'Amount must be positive'
            }, status=400)
        
        gamification, created = UserGamification.objects.get_or_create(user=request.user)
        result = gamification.add_xp_with_overflow_handling(amount, reason)
        
        # Update streak
        gamification.update_streak()
        
        return JsonResponse({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_streak(request):
    """Update user's streak"""
    try:
        gamification, created = UserGamification.objects.get_or_create(user=request.user)
        updated = gamification.update_streak()
        
        return JsonResponse({
            'success': True,
            'data': {
                'updated': updated,
                'current_streak': gamification.current_streak,
                'longest_streak': gamification.longest_streak,
                'last_activity_date': gamification.last_activity_date.isoformat() if gamification.last_activity_date else None
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def sync_from_localstorage(request):
    """Sync gamification data from localStorage (one-time migration)"""
    try:
        data = json.loads(request.body)
        xp = int(data.get('xp', 0))
        streak = int(data.get('streak', 0))
        
        gamification, created = UserGamification.objects.get_or_create(user=request.user)
        
        # Only sync if DB has less data (avoid overwriting server data)
        if gamification.xp < xp:
            gamification.xp = xp
            gamification.level = gamification.calculate_level()
        
        if gamification.current_streak < streak:
            gamification.current_streak = streak
            if streak > gamification.longest_streak:
                gamification.longest_streak = streak
        
        gamification.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Data synced successfully',
            'data': {
                'xp': gamification.xp,
                'level': gamification.level,
                'current_streak': gamification.current_streak
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
