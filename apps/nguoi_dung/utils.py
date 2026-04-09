from django.db.models import Avg, Count, Sum
from apps.nguoi_dung.models import Badge, UserBadge
from apps.de_thi.models import KetQua
from apps.kien_thuc.models import FlashcardProgress

def check_and_award_badges(user):
    """
    Kểm tra và cấp huy hiệu cho user dựa trên điều kiện.
    """
    if not user.is_authenticated:
        return

    # Cache user badges to avoid issuing if already owned
    owned_badge_names = list(UserBadge.objects.filter(nguoi_dung=user).values_list('badge__name', flat=True))
    
    # Get all official results
    official_results = KetQua.objects.filter(nguoi_dung=user, is_official=True)
    tong_bai = official_results.count()
    
    if tong_bai > 0:
        diem_tb = official_results.aggregate(Avg('diem'))['diem__avg'] or 0
        tong_thoi_gian = official_results.aggregate(Sum('thoi_gian_lam'))['thoi_gian_lam__sum'] or 0
        tong_phut = tong_thoi_gian / 60.0
    else:
        diem_tb = 0
        tong_phut = 0

    # 1. Lính Mới (Hoàn thành bài thi hợp lệ đầu tiên)
    if 'Lính Mới' not in owned_badge_names and tong_bai >= 1:
        badge = Badge.objects.filter(name='Lính Mới').first()
        if badge: UserBadge.objects.create(nguoi_dung=user, badge=badge)

    # 2. Học Bá (Điểm TB >= 8.0 trên ít nhất 5 bài)
    if 'Học Bá' not in owned_badge_names and tong_bai >= 5 and diem_tb >= 8.0:
        badge = Badge.objects.filter(name='Học Bá').first()
        if badge: UserBadge.objects.create(nguoi_dung=user, badge=badge)

    # 3. Thợ Săn Điểm 10 (Điểm 10 tuyệt đối bài Official)
    if 'Thợ Săn Điểm 10' not in owned_badge_names:
        has_perfect = official_results.filter(diem=10.0).exists()
        if has_perfect:
            badge = Badge.objects.filter(name='Thợ Săn Điểm 10').first()
            if badge: UserBadge.objects.create(nguoi_dung=user, badge=badge)

    # 4. Trí Nhớ Siêu Phàm (Thuộc lòng >= 50 cards)
    if 'Trí Nhớ Siêu Phàm' not in owned_badge_names:
        learned_cards = FlashcardProgress.objects.filter(user=user, is_learned=True).count()
        if learned_cards >= 50:
            badge = Badge.objects.filter(name='Trí Nhớ Siêu Phàm').first()
            if badge: UserBadge.objects.create(nguoi_dung=user, badge=badge)

    # 5. Chăm Chỉ (Tổng thời gian làm bài hợp lệ >= 60 phút)
    if 'Chăm Chỉ' not in owned_badge_names and tong_phut >= 60:
        badge = Badge.objects.filter(name='Chăm Chỉ').first()
        if badge: UserBadge.objects.create(nguoi_dung=user, badge=badge)
