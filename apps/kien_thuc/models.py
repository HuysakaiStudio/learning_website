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