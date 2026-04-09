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

    # 2. Thành tích
    from apps.nguoi_dung.models import Badge
    from apps.nguoi_dung.utils import check_and_award_badges
    
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
        
    analytics = getattr(user, 'analytics', None)
    if analytics:
        analytics.cap_nhat_thong_ke()

    # 3. Tiến độ Flashcard (Gom nhóm theo bộ thẻ)
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
        'analytics': analytics,
        'flashcard_sets': flashcard_sets,
        'is_own_profile': is_own_profile
    })

