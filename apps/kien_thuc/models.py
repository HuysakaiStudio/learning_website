import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Mon(models.Model):
    ten = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📚')

    class Meta:
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'

    def __str__(self):
        return self.ten


class BaiViet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ duyệt'),
        ('published', 'Đã xuất bản'),
        ('rejected', 'Bị từ chối'),
    ]

    mon = models.ForeignKey(Mon, on_delete=models.CASCADE, related_name='bai_viet')
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    nguoi_dang = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bai_viet')
    ngay_tao = models.DateTimeField(auto_now_add=True)
    thu_tu = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    moderation_note = models.TextField(blank=True, help_text='Ghi chú kiểm duyệt')
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_bai_viet')
    moderated_at = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0, help_text='Số lượt xem bài viết')

    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering = ['thu_tu', 'ngay_tao']

    def __str__(self):
        return f'{self.mon.ten} — {self.tieu_de}'


# ════════════════════════════════════════════════════════════════
# FLASHCARD MODELS
# ════════════════════════════════════════════════════════════════

class Tag(models.Model):
    ten = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.ten

class FlashcardSet(models.Model):
    """
    Bộ flashcard - Tập hợp các thẻ học tập,
    có thể được tạo từ bài viết hoặc tạo riêng
    """
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('pending', 'Đang chờ duyệt'),
        ('published', 'Đã xuất bản'),
        ('rejected', 'Bị từ chối'),
    ]

    mon = models.ForeignKey(Mon, on_delete=models.CASCADE, related_name='flashcard_sets')
    tieu_de = models.CharField(max_length=200)
    mo_ta = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='flashcard_sets', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_flashcard_sets', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    so_luong_the = models.IntegerField(default=0)
    lan_xem = models.IntegerField(default=0, help_text='Số lượt xem bộ flashcard')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    moderation_note = models.TextField(blank=True, help_text='Ghi chú kiểm duyệt')
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_flashcard_sets')
    moderated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Bộ Flashcard'
        verbose_name_plural = 'Bộ Flashcard'
        ordering = ['-ngay_tao']

    def __str__(self):
        return f'{self.tieu_de} ({self.so_luong_the} thẻ)'
    
    def cap_nhat_so_luong(self):
        """Cập nhật số lượng thẻ trong bộ"""
        self.so_luong_the = self.flashcards.count()
        self.save()


class Flashcard(models.Model):
    """
    Thẻ học tập - Một câu hỏi/khái niệm (mặt trước) và câu trả lời (mặt sau)
    Hỗ trợ định dạng Markdown và MathJax
    """
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name='flashcards')
    mat_truoc = models.TextField(help_text='Câu hỏi / Khái niệm (hỗ trợ Markdown & MathJax)')
    mat_sau = models.TextField(help_text='Câu trả lời / Giải thích (hỗ trợ Markdown & MathJax)')
    thu_tu = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Thẻ Flashcard'
        verbose_name_plural = 'Thẻ Flashcard'
        ordering = ['thu_tu']

    def __str__(self):
        return f'{self.flashcard_set.tieu_de} - {self.mat_truoc[:50]}'


class FlashcardProgress(models.Model):
    """
    Theo dõi tiến độ học tập của người dùng cho từng thẻ (Spaced Repetition)
    """
    DIFFICULTY_CHOICES = [
        ('again', 'Lại (< 1 ngày)'),
        ('hard', 'Khó (3 ngày)'),
        ('good', 'Tốt (10 ngày)'),
        ('easy', 'Dễ (21 ngày)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_progress')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    
    # Status
    # is_learned: True = Đã thuộc, False = Đang học
    is_learned = models.BooleanField(default=False)
    
    # Scheduling (Spaced Repetition Data)
    next_review_date = models.DateTimeField(default=timezone.now)
    interval = models.IntegerField(default=0) # Days
    ease_factor = models.FloatField(default=2.5) # Based on SM-2 algorithm
    repetition_count = models.IntegerField(default=0)
    
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'flashcard')
        verbose_name = 'Tiến độ Flashcard'
        verbose_name_plural = 'Tiến độ Flashcard'

    def __str__(self):
        return f'{self.user.username} - {self.flashcard.flashcard_set.tieu_de}'
    
    def cap_nhat_trang_thai(self, is_learned):
        """
        Cập nhật trạng thái học tập của thẻ
        """
        self.is_learned = is_learned
        self.save()


# ════════════════════════════════════════════════════════════════
# FLASHCARD TEST MODELS (NEW)
# ════════════════════════════════════════════════════════════════

class FlashcardTest(models.Model):
    """
    Bài kiểm tra flashcard - Theo dõi một phiên kiểm tra cụ thể
    để đánh giá mức độ hiểu của người dùng với bộ flashcard
    """
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    bo_flashcard = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    tong_so_cau_hoi = models.IntegerField()
    so_cau_tra_loi_dung = models.IntegerField(default=0)
    diem = models.FloatField(default=0.0)  # Tính theo phần trăm
    hoan_thanh = models.BooleanField(default=False)
    thoi_gian_hoan_thanh = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Bài kiểm tra Flashcard'
        verbose_name_plural = 'Bài kiểm tra Flashcard'
        ordering = ['-ngay_tao']

    def __str__(self):
        return f'{self.nguoi_dung.username} - {self.bo_flashcard.tieu_de}'

    def cap_nhat_diem(self):
        """Cập nhật điểm dựa trên số câu trả lời đúng"""
        if self.tong_so_cau_hoi > 0:
            self.diem = (self.so_cau_tra_loi_dung / self.tong_so_cau_hoi) * 100
        else:
            self.diem = 0.0
        self.save()


class FlashcardTestAnswer(models.Model):
    """
    Câu trả lời trong bài kiểm tra flashcard
    """
    bai_kiem_tra = models.ForeignKey(FlashcardTest, on_delete=models.CASCADE, related_name='cac_cau_tra_loi')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    cau_tra_loi = models.TextField()  # Câu trả lời của người dùng (nếu cần lưu)
    dung = models.BooleanField()  # Đúng hay sai
    thoi_gian_tra_loi = models.DateTimeField(auto_now_add=True)
    thoi_gian_tra_loi_thuc_te = models.FloatField(null=True, blank=True)  # Thời gian trả lời (giây)

    class Meta:
        verbose_name = 'Câu trả lời kiểm tra Flashcard'
        verbose_name_plural = 'Câu trả lời kiểm tra Flashcard'
        unique_together = ('bai_kiem_tra', 'flashcard')

    def __str__(self):
        return f'{self.bai_kiem_tra.nguoi_dung.username} - {self.flashcard.id} - {"Đúng" if self.dung else "Sai"}'


class FlashcardStudySession(models.Model):
    """
    Tracks individual flashcard study sessions with time spent
    """
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_sessions')
    bo_flashcard = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name='study_sessions')
    
    # Session details
    ngay_bat_dau = models.DateTimeField(auto_now_add=True)
    ngay_ket_thuc = models.DateTimeField(null=True, blank=True)
    thoi_gian_hoc = models.IntegerField(default=0)  # Total time spent in seconds
    so_the_da_xem = models.IntegerField(default=0)  # Number of cards viewed
    so_the_da_hoc = models.IntegerField(default=0)  # Number of cards studied/reviewed
    ty_le_dung = models.FloatField(default=0.0)  # Accuracy rate
    
    # Session type
    CHE_DO_CHOICES = [
        ('study', 'Học mới'),
        ('review', 'Ôn tập'),
        ('test', 'Kiểm tra'),
    ]
    che_do = models.CharField(max_length=20, choices=CHE_DO_CHOICES, default='study')
    
    class Meta:
        verbose_name = 'Phiên học Flashcard'
        verbose_name_plural = 'Phiên học Flashcard'
        ordering = ['-ngay_bat_dau']

    def __str__(self):
        return f'{self.nguoi_dung.username} - {self.bo_flashcard.tieu_de} - {self.thoi_gian_hoc}s'

    def cap_nhat_thoi_gian_hoc(self):
        """Update total study time in seconds"""
        if self.ngay_bat_dau and self.ngay_ket_thuc:
            self.thoi_gian_hoc = int((self.ngay_ket_thuc - self.ngay_bat_dau).total_seconds())
            self.save()

    def tinh_ty_le_dung(self):
        """Calculate accuracy rate"""
        if self.so_the_da_hoc > 0:
            self.ty_le_dung = (self.so_the_da_xem / self.so_the_da_hoc) * 100
        else:
            self.ty_le_dung = 0.0
        self.save()