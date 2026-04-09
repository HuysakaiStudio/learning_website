"""
Views for home page
"""
from django.shortcuts import render
from apps.nguoi_dung.models import UserGamification
from apps.de_thi.models import KetQua


def home_view(request):
    """Home page with gamification data"""
    context = {}
    
    if request.user.is_authenticated:
        # Get or create gamification data
        gamification, created = UserGamification.objects.get_or_create(user=request.user)
        if created:
            gamification.level = gamification.calculate_level()
            gamification.save()
        
        # Get exam count
        exam_count = KetQua.objects.filter(nguoi_dung=request.user).count()
        
        # Pass gamification data directly to template
        context['xp'] = gamification.xp
        context['level'] = gamification.level
        context['current_streak'] = gamification.current_streak
        context['exam_count'] = exam_count
        
        # Also keep the nested structure for JavaScript
        context['gamification_data'] = {
            'xp': gamification.xp,
            'level': gamification.level,
            'current_streak': gamification.current_streak,
        }
    
    return render(request, 'home.html', context)
