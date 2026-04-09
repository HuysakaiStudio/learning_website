"""
Signal handlers to automatically update analytics when exam results are saved
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count, Sum, Case, When, IntegerField
from .models import KetQua, TraLoi, QuestionDifficulty, UserAnalytics, SubjectPerformance, CauHoi


@receiver(post_save, sender=KetQua)
def update_analytics_on_exam_submit(sender, instance, created, **kwargs):
    """
    When an exam result is saved, update all related analytics.
    Skip initial creation (diem=0), only update after score is set
    """
    # Skip if it's the very first save with diem=0
    if created and instance.diem == 0:
        return
    
    # Only process if there are answer records (meaning exam is complete)
    if not instance.tra_loi.exists():
        return
    
    # 1. Update QuestionDifficulty for each question in this exam
    update_question_difficulty(instance)
    
    # 2. Update UserAnalytics
    update_user_analytics(instance.nguoi_dung)
    
    # 3. Update SubjectPerformance
    update_subject_performance(instance.nguoi_dung, instance.de_thi.mon)


def update_question_difficulty(ket_qua):
    """
    Update difficulty score for each question based on this new exam result
    """
    tra_loi_records = ket_qua.tra_loi.select_related('cau_hoi').all()
    
    for tra_loi in tra_loi_records:
        cau_hoi = tra_loi.cau_hoi
        
        # Get or create QuestionDifficulty
        difficulty, _ = QuestionDifficulty.objects.get_or_create(cau_hoi=cau_hoi)
        
        # Update counters
        difficulty.tong_lan_hoi += 1
        if tra_loi.dung:
            difficulty.so_lan_dung += 1
        
        # Recalculate difficulty
        difficulty.tinh_do_kho()


def update_user_analytics(user):
    """
    Update user's overall analytics
    """
    analytics, _ = UserAnalytics.objects.get_or_create(nguoi_dung=user)
    analytics.cap_nhat_thong_ke()


def update_subject_performance(user, mon):
    """
    Update user's performance for a specific subject
    """
    if not mon:
        return
    
    perf, _ = SubjectPerformance.objects.get_or_create(
        nguoi_dung=user,
        mon=mon
    )
    perf.cap_nhat_hieu_suat()
