from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from apps.de_thi.models import KetQua
from apps.kien_thuc.models import FlashcardProgress, FlashcardSet
from .forms import UserProfileForm
from .models import UserProfile

def dang_ky(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}! Đăng ký thành công 🎉')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'nguoi_dung/dang_ky.html', {'form': form})

def dang_nhap(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Chào mừng trở lại, {user.username}! 👋')
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = AuthenticationForm()
    return render(request, 'nguoi_dung/dang_nhap.html', {'form': form})

def dang_xuat(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        is_own_profile = (user == request.user)
    else:
        user = request.user
        is_own_profile = True

    profile_obj, created = UserProfile.objects.get_or_create(user=user)
    
    if is_own_profile and request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công!')
            return redirect('nguoi_dung:profile')
    else:
        form = UserProfileForm(instance=profile_obj)
    
    # 1. Lịch sử bài làm (Phân trang 8 bản ghi)
    ket_qua_list = KetQua.objects.filter(nguoi_dung=user).order_by('-ngay_lam')
    
    if not request.user.is_staff:
        # Ẩn kết quả không có câu trả lời đối với người xem không phải admin
        ket_qua_list = ket_qua_list.annotate(a_count=Count('tra_loi')).filter(a_count__gt=0)
        
    paginator = Paginator(ket_qua_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 2. Thành tích - Badges và Achievements
    from apps.nguoi_dung.models import Badge
    from apps.nguoi_dung.utils import check_and_award_badges
    from apps.leaderboard.models import Achievement
    
    # Award any missing badges before displaying
    check_and_award_badges(user)
    
    all_badges = Badge.objects.all()
    user_badge_ids = user.badges.values_list('badge_id', flat=True)
    
    display_badges = []
    for b in all_badges:
        display_badges.append({
            'badge': b,
            'achieved': b.id in user_badge_ids
        })
    
    # Lấy achievements từ leaderboard - chỉ hiển thị thành tựu danh giá nhất
    # Thứ tự ưu tiên: top_100_all_time > top_10_monthly > top_10_weekly > top_10_daily > các loại khác
    achievement_priority = {
        'top_100_all_time': 1,
        'top_10_monthly': 2,
        'top_10_weekly': 3,
        'top_10_daily': 4,
        'subject_master': 5,
        'exam_champion': 6,
        'flashcard_king': 7,
    }
    
    all_achievements = Achievement.objects.filter(user=user).select_related('mon')
    
    # Nhóm theo loại và chỉ lấy thành tựu tốt nhất của mỗi loại
    best_achievements = {}
    for ach in all_achievements:
        ach_type = ach.achievement_type
        priority = achievement_priority.get(ach_type, 99)
        
        # Nếu chưa có loại này hoặc thành tựu này tốt hơn (rank thấp hơn)
        if ach_type not in best_achievements:
            best_achievements[ach_type] = (priority, ach)
        elif ach.rank_achieved and best_achievements[ach_type][1].rank_achieved:
            if ach.rank_achieved < best_achievements[ach_type][1].rank_achieved:
                best_achievements[ach_type] = (priority, ach)
    
    # Sắp xếp theo priority và lấy top 6 thành tựu danh giá nhất
    user_achievements = sorted(best_achievements.values(), key=lambda x: (x[0], x[1].rank_achieved or 999))
    user_achievements = [ach for priority, ach in user_achievements[:6]]
    
    # 3. Gamification data từ database
    from apps.nguoi_dung.models import UserGamification
    gamification_data = None
    if is_own_profile:
        gamification, created = UserGamification.objects.get_or_create(user=user)
        if created:
            gamification.level = gamification.calculate_level()
            gamification.save()
        
        xp_progress = gamification.get_xp_for_next_level()
        gamification_data = {
            'xp': gamification.xp,
            'level': gamification.level,
            'current_streak': gamification.current_streak,
            'longest_streak': gamification.longest_streak,
            'xp_progress': xp_progress
        }
        
    analytics = getattr(user, 'analytics', None)
    if analytics:
        analytics.cap_nhat_thong_ke()

    # 4. Tiến độ Flashcard (Gom nhóm theo bộ thẻ)
    # Chỉ lấy bộ thẻ có ít nhất 1 thẻ và người dùng đã có tiến độ
    flashcard_sets = FlashcardSet.objects.filter(
        so_luong_the__gt=0  # Chỉ lấy bộ có thẻ
    ).filter(
        Q(flashcards__flashcardprogress__user=user) | Q(creator=user)  # Đã học hoặc là người tạo
    ).annotate(
        learned_count=Count('flashcards__id', filter=Q(flashcards__flashcardprogress__user=user, flashcards__flashcardprogress__is_learned=True), distinct=True),
        total_count=Count('flashcards__id', distinct=True)
    ).filter(
        total_count__gt=0  # Đảm bảo có thẻ (double check)
    ).order_by('-learned_count')

    return render(request, 'nguoi_dung/profile.html', {
        'form': form,
        'profile': profile_obj,
        'target_user': user,
        'page_obj': page_obj,
        'display_badges': display_badges,
        'user_achievements': user_achievements,
        'analytics': analytics,
        'flashcard_sets': flashcard_sets,
        'is_own_profile': is_own_profile,
        'gamification_data': gamification_data
    })

