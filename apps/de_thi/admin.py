from django.contrib import admin
from .models import DeThi, CauHoi, KetQua

class CauHoiInline(admin.StackedInline):
    model = CauHoi
    extra = 1
    fields = [
        'loai', 'noi_dung', 'thu_tu',
        ('dap_an_a', 'dap_an_b'), ('dap_an_c', 'dap_an_d'),
        'dap_an_dung',
        ('y_a', 'dung_sai_a'), ('y_b', 'dung_sai_b'),
        ('y_c', 'dung_sai_c'), ('y_d', 'dung_sai_d'),
        'dap_an_so', 'giai_thich',
    ]

@admin.register(DeThi)
class DeThiAdmin(admin.ModelAdmin):
    list_display = ['ten', 'mon', 'thoi_gian_phut', 'tong_cau', 'an', 'ngay_tao']
    list_filter = ['mon', 'an']
    inlines = [CauHoiInline]

@admin.register(KetQua)
class KetQuaAdmin(admin.ModelAdmin):
    list_display = ['nguoi_dung', 'de_thi', 'diem', 'che_do', 'ngay_lam']
    list_filter = ['che_do', 'de_thi']