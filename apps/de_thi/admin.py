from django.contrib import admin
from .models import (DeThi, CauHoi, KetQua, QuestionDifficulty, UserAnalytics, SubjectPerformance,
                     ForumPost, ForumComment, ForumReply, PostVote)

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

@admin.register(QuestionDifficulty)
class QuestionDifficultyAdmin(admin.ModelAdmin):
    list_display = ['cau_hoi', 'tong_lan_hoi', 'so_lan_dung', 'do_kho', 'ngay_cap_nhat']
    list_filter = ['do_kho', 'ngay_cap_nhat']
    readonly_fields = ['ngay_cap_nhat']
    search_fields = ['cau_hoi__noi_dung']

@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['nguoi_dung', 'tong_bai_lam', 'diem_trung_binh', 'tong_gio_lam', 'ngay_cap_nhat']
    list_filter = ['ngay_cap_nhat']
    readonly_fields = ['ngay_cap_nhat']
    search_fields = ['nguoi_dung__username']

@admin.register(SubjectPerformance)
class SubjectPerformanceAdmin(admin.ModelAdmin):
    list_display = ['nguoi_dung', 'mon', 'tong_bai_lam', 'diem_trung_binh', 'so_dan_dung', 'ngay_cap_nhat']
    list_filter = ['mon', 'ngay_cap_nhat']
    readonly_fields = ['ngay_cap_nhat']
    search_fields = ['nguoi_dung__username', 'mon__ten']


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 0
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']
    fields = ['tac_gia', 'noi_dung', 'vote_count', 'ngay_tao']


class ForumCommentInline(admin.TabularInline):
    model = ForumComment
    extra = 0
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']
    fields = ['tac_gia', 'noi_dung', 'vote_count', 'ngay_tao']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'cau_hoi', 'tac_gia', 'is_solved', 'vote_count', 'so_binh_luan', 'ngay_tao']
    list_filter = ['is_solved', 'ngay_tao']
    search_fields = ['tieu_de', 'noi_dung']
    readonly_fields = ['vote_count', 'so_binh_luan', 'ngay_tao', 'ngay_cap_nhat']
    inlines = [ForumCommentInline]
    fieldsets = (
        ('Bài viết', {
            'fields': ('cau_hoi', 'tieu_de', 'tac_gia')
        }),
        ('Nội dung', {
            'fields': ('noi_dung',)
        }),
        ('Trạng thái', {
            'fields': ('is_solved', 'best_answer_comment')
        }),
        ('Thống kê', {
            'fields': ('vote_count', 'so_binh_luan', 'ngay_tao', 'ngay_cap_nhat'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ['bai_dang', 'tac_gia', 'vote_count', 'ngay_tao']
    list_filter = ['ngay_tao']
    search_fields = ['noi_dung']
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']
    inlines = [ForumReplyInline]


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['binh_luan', 'tac_gia', 'vote_count', 'ngay_tao']
    list_filter = ['ngay_tao']
    search_fields = ['noi_dung']
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    list_display = ['nguoi_dung', 'loai_bau', 'bai_dang', 'binh_luan', 'tra_loi', 'ngay_tao']
    list_filter = ['loai_bau', 'ngay_tao']
    readonly_fields = ['ngay_tao']
    search_fields = ['nguoi_dung__username']