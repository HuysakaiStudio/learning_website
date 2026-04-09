from django.contrib import admin
from .models import Mon, BaiViet, FlashcardSet, Flashcard, FlashcardProgress

@admin.register(Mon)
class MonAdmin(admin.ModelAdmin):
    list_display = ['icon', 'ten', 'mo_ta']

@admin.register(BaiViet)
class BaiVietAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'mon', 'thu_tu', 'ngay_tao']
    list_filter = ['mon']
    search_fields = ['tieu_de', 'noi_dung']
    ordering = ['mon', 'thu_tu']

class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1
    fields = ['thu_tu', 'mat_truoc', 'mat_sau']

@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'mon', 'creator', 'so_luong_the', 'ngay_tao']
    list_filter = ['mon', 'ngay_tao']
    search_fields = ['tieu_de', 'mo_ta']
    inlines = [FlashcardInline]
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat', 'so_luong_the']

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['flashcard_set', 'mat_truoc', 'thu_tu', 'ngay_tao']
    list_filter = ['flashcard_set', 'ngay_tao']
    search_fields = ['mat_truoc', 'mat_sau']
    ordering = ['flashcard_set', 'thu_tu']

@admin.register(FlashcardProgress)
class FlashcardProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'flashcard', 'is_learned']
    list_filter = ['is_learned']
    search_fields = ['user__username', 'flashcard__mat_truoc']
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']