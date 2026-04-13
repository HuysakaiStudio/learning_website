from django.db import models
from django.db.models import Count, Avg, Sum
from django.contrib.auth.models import User
from apps.kien_thuc.models import Mon

class DeThi(models.Model):
    ten = models.CharField(max_length=200)
    mon = models.ForeignKey(Mon, on_delete=models.SET_NULL, null=True, related_name='de_thi')
    mo_ta = models.TextField(blank=True)
    thoi_gian_phut = models.IntegerField(default=50)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    an = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_de_thi')
    is_custom = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Đề thi'
        verbose_name_plural = 'Đề thi'
        ordering = ['-ngay_tao']

    def __str__(self):
        return self.ten

    def tong_cau(self):
        return self.cau_hoi.count()


class CauHoi(models.Model):
    LOAI_CAU = [
        ('tn', 'Trắc nghiệm ABCD'),
        ('ds', 'Trắc nghiệm Đúng/Sai'),
        ('dien', 'Điền số'),
    ]

    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE, related_name='cau_hoi')
    loai = models.CharField(max_length=10, choices=LOAI_CAU, default='tn')
    noi_dung = models.TextField()
    hinh_anh = models.ImageField(upload_to='cau_hoi_images/', blank=True, null=True, verbose_name='Hình ảnh minh họa')
    giai_thich = models.TextField(blank=True)
    thu_tu = models.IntegerField(default=0)

    # Trắc nghiệm ABCD
    dap_an_a = models.CharField(max_length=500, blank=True)
    dap_an_b = models.CharField(max_length=500, blank=True)
    dap_an_c = models.CharField(max_length=500, blank=True)
    dap_an_d = models.CharField(max_length=500, blank=True)
    dap_an_dung = models.CharField(max_length=10, blank=True)  # 'A','B','C','D'

    # Đúng/Sai — 4 ý a,b,c,d mỗi ý là True/False
    y_a = models.CharField(max_length=500, blank=True)
    y_b = models.CharField(max_length=500, blank=True)
    y_c = models.CharField(max_length=500, blank=True)
    y_d = models.CharField(max_length=500, blank=True)
    dung_sai_a = models.BooleanField(default=False)
    dung_sai_b = models.BooleanField(default=False)
    dung_sai_c = models.BooleanField(default=False)
    dung_sai_d = models.BooleanField(default=False)

    # Điền số
    dap_an_so = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['thu_tu']
        verbose_name = 'Câu hỏi'
        verbose_name_plural = 'Câu hỏi'

    def __str__(self):
        return f'[{self.get_loai_display()}] {self.noi_dung[:60]}'


class KetQua(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ket_qua')
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    diem = models.FloatField(default=0)
    tong_cau = models.IntegerField(default=0)
    thoi_gian_lam = models.IntegerField(default=0)  # giây
    che_do = models.CharField(max_length=20, default='luyen_tap')  # luyen_tap / thi_that
    ngay_lam = models.DateTimeField(auto_now_add=True)
    da_xem_dap_an = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)  # Chỉ những bài official mới được tính vào leaderboard
    is_violated = models.BooleanField(default=False)  # Đánh dấu bài thi có hành vi gian lận (ra khỏi tab, ẩn trang)
    danh_dau_khong_chinh_thuc = models.BooleanField(default=False)  # Đánh dấu bài thi không chính thức vì đã luyện từng câu

    class Meta:
        ordering = ['-ngay_lam']

    def __str__(self):
        return f'{self.nguoi_dung.username} — {self.de_thi.ten} — {self.diem}'


class TraLoi(models.Model):
    ket_qua = models.ForeignKey(KetQua, on_delete=models.CASCADE, related_name='tra_loi')
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)

    # Trắc nghiệm
    chon = models.CharField(max_length=10, blank=True)

    # Đúng/Sai
    chon_a = models.BooleanField(null=True, blank=True)
    chon_b = models.BooleanField(null=True, blank=True)
    chon_c = models.BooleanField(null=True, blank=True)
    chon_d = models.BooleanField(null=True, blank=True)

    # Điền số
    so_dien = models.CharField(max_length=100, blank=True)

    dung = models.BooleanField(default=False)
    diem_duoc = models.FloatField(default=0)


class QuestionDifficulty(models.Model):
    """Tracks difficulty of each question based on class-wide performance"""
    cau_hoi = models.OneToOneField(CauHoi, on_delete=models.CASCADE, related_name='difficulty')
    tong_lan_hoi = models.IntegerField(default=0)  # Total times answered
    so_lan_dung = models.IntegerField(default=0)   # Times answered correctly
    do_kho = models.FloatField(default=0.5)  # Difficulty (0=easy, 1=hard), calculated as 1 - (correct_rate)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Độ khó câu hỏi'
        verbose_name_plural = 'Độ khó câu hỏi'

    def __str__(self):
        return f'{self.cau_hoi.de_thi.ten} - Độ khó: {self.do_kho:.2f}'

    def tinh_do_kho(self):
        """Recalculate difficulty based on correct rate"""
        if self.tong_lan_hoi == 0:
            self.do_kho = 0.5
        else:
            correct_rate = self.so_lan_dung / self.tong_lan_hoi
            self.do_kho = 1 - correct_rate
        self.save()


class UserAnalytics(models.Model):
    """Tracks user's performance metrics across all exams"""
    nguoi_dung = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    tong_bai_lam = models.IntegerField(default=0)  # Total exams taken (official only)
    tong_bai_da_lam = models.IntegerField(default=0)  # Total exams completed (all exams)
    diem_trung_binh = models.FloatField(default=0)  # Average score across all exams
    tong_gio_lam = models.IntegerField(default=0)  # Total minutes spent on exams
    tong_gio_hoc = models.IntegerField(default=0)  # Total minutes spent studying (including flashcards)
    dem_tien_tro = models.IntegerField(default=0)  # Streak count
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Phân tích người dùng'
        verbose_name_plural = 'Phân tích người dùng'

    def __str__(self):
        return f'{self.nguoi_dung.username} - Trung bình: {self.diem_trung_binh:.2f}'

    def cap_nhat_thong_ke(self):
        """Update user statistics from KetQua records"""
        from django.db.models import Avg, Sum, Count, Q
        
        # Update official exams count (only valid official exams)
        official_stats = KetQua.objects.filter(
            nguoi_dung=self.nguoi_dung,
            tra_loi__isnull=False,
            is_official=True
        ).distinct().aggregate(
            total=Count('id'),
            avg_score=Avg('diem'),
            total_time=Sum('thoi_gian_lam')
        )
        
        # Update all completed exams count (regardless of official status)
        all_exams_stats = KetQua.objects.filter(
            nguoi_dung=self.nguoi_dung,
            tra_loi__isnull=False  # Only exams with at least one answer
        ).distinct().aggregate(
            total=Count('id')
        )
        
        self.tong_bai_lam = official_stats['total'] or 0
        self.tong_bai_da_lam = all_exams_stats['total'] or 0
        self.diem_trung_binh = official_stats['avg_score'] or 0
        self.tong_gio_lam = int((official_stats['total_time'] or 0) / 60)  # Convert seconds to minutes
        
        # Import here to avoid circular imports
        from django.utils import timezone
        try:
            from apps.leaderboard.models import LeaderboardEntry
            # Get the user's overall leaderboard entry to combine times
            overall_entry = LeaderboardEntry.objects.filter(
                user=self.nguoi_dung,
                leaderboard__category='overall'
            ).first()
            
            if overall_entry:
                self.tong_gio_hoc = self.tong_gio_lam + overall_entry.total_time_minutes
            else:
                self.tong_gio_hoc = self.tong_gio_lam
        except ImportError:
            # If leaderboard app is not available, just use exam time
            self.tong_gio_hoc = self.tong_gio_lam
            
        self.save()

    def cap_nhat_thoi_gian_hoc(self, time_spent_minutes, activity_type='general'):
        """
        Update study time tracking for different activities
        activity_type: 'exam', 'flashcard', 'general'
        """
        from django.utils import timezone
        if activity_type == 'exam':
            self.tong_gio_lam += time_spent_minutes
        elif activity_type == 'flashcard':
            # Update flashcard-specific tracking in leaderboard entry if available
            try:
                from apps.leaderboard.models import LeaderboardEntry
                from apps.leaderboard.models import Leaderboard  # Import Leaderboard model
                
                # Get or create a flashcard-specific leaderboard for the user
                flashcard_lb, created = Leaderboard.objects.get_or_create(
                    period='all_time',
                    category='flashcard',
                    defaults={'period': 'all_time', 'category': 'flashcard'}
                )
                
                leaderboard_entry, created = LeaderboardEntry.objects.get_or_create(
                    user=self.nguoi_dung,
                    leaderboard=flashcard_lb,
                    defaults={
                        'score': 0,
                        'total_score': 0,
                        'rank': 999999,
                        'exams_completed': 0,
                        'flashcards_learned': 0,
                        'total_time_minutes': 0,
                        'flashcard_avg_score': 0.0,
                        'flashcard_total_cards': 0,
                        'weekly_flashcard_count': 0,
                        'flashcard_streak': 0
                    }
                )
                
                if leaderboard_entry:
                    leaderboard_entry.total_time_minutes += time_spent_minutes
                    leaderboard_entry.last_flashcard_study = timezone.now()
                    leaderboard_entry.save()
                    
            except (ImportError, Exception):
                pass  # Leaderboard app not available or other error
                
        # Update total study time
        self.tong_gio_hoc = self.tong_gio_lam + time_spent_minutes
        self.save()
        
        # Update leaderboard entries with the new total study time
        try:
            from apps.leaderboard.models import LeaderboardEntry, Leaderboard
            # Update overall leaderboard entry
            overall_lb, created = Leaderboard.objects.get_or_create(
                period='all_time',
                category='overall'
            )
            
            overall_entry, created = LeaderboardEntry.objects.get_or_create(
                user=self.nguoi_dung,
                leaderboard=overall_lb,
                defaults={
                    'score': 0,
                    'total_score': 0,
                    'rank': 999999,
                    'exams_completed': 0,
                    'flashcards_learned': 0,
                    'total_time_minutes': 0,
                    'total_study_time_minutes': 0,
                    'flashcard_avg_score': 0.0,
                    'flashcard_total_cards': 0,
                    'weekly_flashcard_count': 0,
                    'flashcard_streak': 0
                }
            )
            
            overall_entry.total_study_time_minutes = self.tong_gio_hoc
            overall_entry.total_time_minutes += time_spent_minutes  # Add to existing time
            overall_entry.save()
            
            # Update flashcard leaderboard entry
            flashcard_lb, created = Leaderboard.objects.get_or_create(
                period='all_time',
                category='flashcard'
            )
            
            flashcard_entry, created = LeaderboardEntry.objects.get_or_create(
                user=self.nguoi_dung,
                leaderboard=flashcard_lb,
                defaults={
                    'score': 0,
                    'total_score': 0,
                    'rank': 999999,
                    'exams_completed': 0,
                    'flashcards_learned': 0,
                    'total_time_minutes': 0,
                    'total_study_time_minutes': 0,
                    'flashcard_avg_score': 0.0,
                    'flashcard_total_cards': 0,
                    'weekly_flashcard_count': 0,
                    'flashcard_streak': 0
                }
            )
            
            flashcard_entry.total_study_time_minutes = self.tong_gio_hoc
            flashcard_entry.total_time_minutes += time_spent_minutes
            flashcard_entry.save()
            
        except ImportError:
            pass  # Leaderboard app not available
    
    def get_detailed_statistics(self):
        """Get detailed statistics for the profile page"""
        from django.db.models import Avg, Count, Sum, Max, Min
        from datetime import timedelta, datetime
        
        # Get all official exam results
        exam_results = KetQua.objects.filter(
            nguoi_dung=self.nguoi_dung,
            is_official=True
        )
        
        # Overall statistics
        total_exams = exam_results.count()
        avg_score = exam_results.aggregate(Avg('diem'))['diem__avg'] or 0
        total_time = exam_results.aggregate(Sum('thoi_gian_lam'))['thoi_gian_lam__sum'] or 0
        highest_score = exam_results.aggregate(Max('diem'))['diem__max'] or 0
        lowest_score = exam_results.aggregate(Min('diem'))['diem__min'] or 0
        
        # Recent statistics (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_exams = exam_results.filter(ngay_lam__gte=thirty_days_ago)
        recent_count = recent_exams.count()
        recent_avg = recent_exams.aggregate(Avg('diem'))['diem__avg'] or 0
        
        # Subject-wise statistics
        subject_stats = []
        from apps.kien_thuc.models import Mon
        subjects = Mon.objects.filter(de_thi__ket_qua__nguoi_dung=self.nguoi_dung).distinct()
        
        for subject in subjects:
            subject_exams = exam_results.filter(de_thi__mon=subject)
            subject_avg = subject_exams.aggregate(Avg('diem'))['diem__avg'] or 0
            subject_count = subject_exams.count()
            
            subject_stats.append({
                'subject': subject.ten,
                'average_score': subject_avg,
                'exam_count': subject_count
            })
        
        return {
            'overall': {
                'total_exams': total_exams,
                'average_score': round(avg_score, 2),
                'total_time_minutes': int(total_time / 60) if total_time else 0,
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
            },
            'recent': {
                'recent_30_days': recent_count,
                'recent_average': round(recent_avg, 2),
            },
            'by_subject': subject_stats
        }
    


class SubjectPerformance(models.Model):
    """Tracks user's performance for each subject/Mon"""
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_performance')
    mon = models.ForeignKey(Mon, on_delete=models.CASCADE)
    tong_bai_lam = models.IntegerField(default=0)
    diem_trung_binh = models.FloatField(default=0)
    so_dan_dung = models.IntegerField(default=0)  # Questions answered correctly
    tong_dan_tra_loi = models.IntegerField(default=0)  # Total questions attempted
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('nguoi_dung', 'mon')
        verbose_name = 'Hiệu suất theo môn'
        verbose_name_plural = 'Hiệu suất theo môn'

    def __str__(self):
        return f'{self.nguoi_dung.username} - {self.mon.ten}: {self.diem_trung_binh:.2f}'

    def cap_nhat_hieu_suat(self):
        """Update subject performance from exam results"""
        # Chỉ tính những kết quả official
        exams = KetQua.objects.filter(
            nguoi_dung=self.nguoi_dung,
            de_thi__mon=self.mon,
            tra_loi__isnull=False,
            is_official=True
        ).distinct()
        
        stats = exams.aggregate(
            total=Count('id'),
            avg_score=Avg('diem')
        )
        
        self.tong_bai_lam = stats['total'] or 0
        self.diem_trung_binh = stats['avg_score'] or 0
        
        # Count total correct/total answers
        tra_loi_stats = TraLoi.objects.filter(
            ket_qua__in=exams
        ).aggregate(
            total_correct=Sum(models.Case(
                models.When(dung=True, then=1),
                default=0,
                output_field=models.IntegerField()
            )),
            total_attempts=Count('id')
        )
        
        self.so_dan_dung = tra_loi_stats['total_correct'] or 0
        self.tong_dan_tra_loi = tra_loi_stats['total_attempts'] or 0
        self.save()


class ForumPost(models.Model):
    """Discussion threads linked to specific exam questions"""
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE, related_name='forum_posts')
    tac_gia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forum_posts')
    tieu_de = models.CharField(max_length=300)
    noi_dung = models.TextField()  # Markdown format
    is_solved = models.BooleanField(default=False)  # Mark as solved
    best_answer_comment = models.ForeignKey('ForumComment', on_delete=models.SET_NULL, null=True, blank=True, related_name='best_answer_for_post')
    vote_count = models.IntegerField(default=0)  # Total votes (upvote - downvote)
    so_binh_luan = models.IntegerField(default=0)  # Comment count
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ngay_tao']
        verbose_name = 'Bài diễn đàn'
        verbose_name_plural = 'Bài diễn đàn'
    
    def __str__(self):
        return f'[{self.cau_hoi.de_thi.ten}] {self.tieu_de}'


class ForumComment(models.Model):
    """Top-level replies to forum posts"""
    bai_dang = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    tac_gia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forum_comments')
    noi_dung = models.TextField()  # Markdown format
    vote_count = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-vote_count', 'ngay_tao']
        verbose_name = 'Bình luận diễn đàn'
        verbose_name_plural = 'Bình luận diễn đàn'
    
    def __str__(self):
        return f'Re: {self.bai_dang.tieu_de} - {self.tac_gia.username}'


class ForumReply(models.Model):
    """Nested replies to comments (threading)"""
    binh_luan = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='replies')
    tac_gia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='forum_replies')
    noi_dung = models.TextField()  # Markdown format
    vote_count = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['ngay_tao']
        verbose_name = 'Trả lời bình luận'
        verbose_name_plural = 'Trả lời bình luận'
    
    def __str__(self):
        return f'Reply by {self.tac_gia.username}'


class PostVote(models.Model):
    """Track upvotes/downvotes on posts and comments"""
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Post voting
    bai_dang = models.ForeignKey(ForumPost, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    
    # Comment voting
    binh_luan = models.ForeignKey(ForumComment, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    
    # Reply voting
    tra_loi = models.ForeignKey(ForumReply, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    
    # Vote value
    loai_bau = models.IntegerField(choices=VOTE_CHOICES)  # 1 or -1
    ngay_tao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Bầu chọn'
        verbose_name_plural = 'Bầu chọn'
        # Prevent duplicate votes from same user
        unique_together = [
            ('nguoi_dung', 'bai_dang'),
            ('nguoi_dung', 'binh_luan'),
            ('nguoi_dung', 'tra_loi'),
        ]
    
    def __str__(self):
        vote_str = 'Upvote' if self.loai_bau == 1 else 'Downvote'
        return f'{self.nguoi_dung.username} - {vote_str}'


class PracticeSession(models.Model):
    """Tracks question-by-question practice sessions (Wayground-style)"""
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_sessions')
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE, related_name='practice_sessions')
    ket_qua = models.OneToOneField(KetQua, on_delete=models.CASCADE, null=True, blank=True, related_name='practice_session')
    
    # Session tracking
    cau_hien_tai = models.IntegerField(default=0)  # Index of current question (0-based)
    da_hoan_thanh = models.BooleanField(default=False)
    
    # Timestamps
    ngay_bat_dau = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ngay_bat_dau']
        verbose_name = 'Phiên luyện tập'
        verbose_name_plural = 'Phiên luyện tập'
    
    def __str__(self):
        status = 'Hoàn thành' if self.da_hoan_thanh else f'Câu {self.cau_hien_tai + 1}'
        return f'{self.nguoi_dung.username} - {self.de_thi.ten} ({status})'