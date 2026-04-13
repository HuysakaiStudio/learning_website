# Patch for apps/de_thi/views.py - lam_bai function

The following changes need to be made to the lam_bai function in apps/de_thi/views.py to properly implement the practice-disables-leaderboard logic:

## Current problematic code around lines 245-267:
```python
# Xác định tư cách Official (Hợp lệ cho Leaderboard)
# 1. Phải là chế độ 'thi_that'
# 2. Không vi phạm quy chế (tab switch)
# 3. Đây phải là lần đầu tiên thi thật HOẶC chưa từng xem đáp án trước đó của đề này
from django.db.models import Q
da_thi_that_hoac_xem_dap_an = KetQua.objects.filter(
    nguoi_dung=request.user,
    de_thi=de
).filter(Q(che_do='thi_that') | Q(da_xem_dap_an=True)).exists()

is_official = False
if che_do == 'thi_that' and not cheated and not da_thi_that_hoac_xem_dap_an:
    is_official = True

ket_qua = KetQua.objects.create(
    nguoi_dung=request.user,
    de_thi=de,
    tong_cau=cau_hoi_list.count(),
    thoi_gian_lam=max(int(request.POST.get('thi_gian_lam', 0)), 1),  # Ensure at least 1 second to avoid 0 time
    che_do=che_do,
    is_violated=cheated,
    is_official=is_official
)
```

## Should be replaced with:
```python
# Check if user has practiced this exam before
da_da_luyen_tung_cau = PracticeSession.objects.filter(
    nguoi_dung=request.user,
    de_thi=de
).exists()

# Xác định tư cách Official (Hợp lệ cho Leaderboard)
# 1. Phải là chế độ 'thi_that'
# 2. Không vi phạm quy chế (tab switch)
# 3. Người dùng chưa từng luyện từng câu với đề này (practice-disables-leaderboard approach)
is_official = False
if che_do == 'thi_that' and not cheated and not da_da_luyen_tung_cau:
    is_official = True
elif che_do == 'thi_that' and da_da_luyen_tung_cau:
    # User has practiced this exam, so real exam won't be official
    # But they can still take it for self-assessment
    is_official = False

ket_qua = KetQua.objects.create(
    nguoi_dung=request.user,
    de_thi=de,
    tong_cau=cau_hoi_list.count(),
    thoi_gian_lam=max(int(request.POST.get('thi_gian_lam', 0)), 1),  # Ensure at least 1 second to avoid 0 time
    che_do=che_do,
    is_violated=cheated,
    is_official=is_official,
    danh_dau_khong_chinh_thuc=da_da_luyen_tung_cau  # Mark why it's unofficial
)
```

Note: This manual update needs to be performed as the apply_diff tool had difficulty with the complexity of this function replacement.