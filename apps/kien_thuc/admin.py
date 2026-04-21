from django.contrib import admin
from .models import Mon, BaiViet, FlashcardSet, Flashcard, FlashcardProgress, Notebook, NoteSection, NoteTag, NotebookTag, Note

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

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'visibility', 'created_at']
    list_filter = ['visibility', 'created_at', 'user']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

class NoteSectionInline(admin.TabularInline):
    model = NoteSection
    extra = 1
    fields = ['title', 'order', 'content']

@admin.register(NoteSection)
class NoteSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'notebook', 'order', 'updated_at']
    list_filter = ['notebook', 'updated_at']
    search_fields = ['title', 'content', 'notebook__title']
    ordering = ['notebook', 'order']

@admin.register(NoteTag)
class NoteTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color']
    list_filter = ['user']
    search_fields = ['name', 'user__username']
    list_per_page = 20

@admin.register(NotebookTag)
class NotebookTagAdmin(admin.ModelAdmin):
    list_display = ['notebook', 'tag']
    list_filter = ['tag']
    search_fields = ['notebook__title', 'tag__name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'note_type', 'created_at', 'is_pinned')
    list_filter = ('note_type', 'is_pinned', 'created_at', 'user')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content Association', {
            'fields': ('user', 'note_type', 'question', 'flashcard', 'article')
        }),
        ('Note Content', {
            'fields': ('title', 'content', 'is_pinned')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )