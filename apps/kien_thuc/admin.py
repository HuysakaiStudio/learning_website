from django.contrib import admin
from .models import Mon, BaiViet

@admin.register(Mon)
class MonAdmin(admin.ModelAdmin):
    list_display = ['icon', 'ten', 'mo_ta']

@admin.register(BaiViet)
class BaiVietAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'mon', 'thu_tu', 'ngay_tao']
    list_filter = ['mon']
    search_fields = ['tieu_de', 'noi_dung']
    ordering = ['mon', 'thu_tu']