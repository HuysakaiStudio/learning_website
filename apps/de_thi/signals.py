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
    When an exam result is saved, update all related analytics and award XP.
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
    
    # 4. Award XP for completing exam
    award_exam_xp(instance)


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


def award_exam_xp(ket_qua):
    """
    Award XP based on exam score
    """
    from apps.nguoi_dung.xp_utils import award_xp, get_exam_xp_reward
    from django.utils import timezone
    from django.db.models import Count
    from datetime import datetime
    # KetQua is already imported at the top of the file
    
    # Determine XP reward based on exam type
    # For official exams that are not violated, award full XP
    if ket_qua.is_official and not ket_qua.is_violated:
        # Check if this is the first official submission for this exam to prevent duplicate XP
        first_official_submission = KetQua.objects.filter(
            nguoi_dung=ket_qua.nguoi_dung,
            de_thi=ket_qua.de_thi,
            is_official=True
        ).order_by('ngay_lam').first()
        
        # Only award XP if this is the first official submission for this exam
        if first_official_submission and first_official_submission.id == ket_qua.id:
            xp_amount, reason = get_exam_xp_reward(ket_qua.diem)
            # Award XP for official exams
            result = award_xp(ket_qua.nguoi_dung, xp_amount, reason)
            
            if result:
                # Send XP notification if XP was actually awarded
                try:
                    from apps.notifications.utils import create_notification
                    xp_message = f'Bạn đã nhận được {xp_amount} XP từ bài thi "{ket_qua.de_thi.tieu_de}"'
                    if result.get('leveled_up'):
                        # User leveled up!
                        xp_message += f'. Chúc mừng bạn đã lên cấp {result["new_level"]}!'
                    
                    create_notification(
                        recipient=ket_qua.nguoi_dung,
                        notification_type='xp_award',
                        title=f'+{xp_amount} XP!',
                        message=xp_message,
                        action_url=f'/de-thi/ket-qua/{ket_qua.id}/',
                        content_object=ket_qua
                    )
                except ImportError:
                    pass  # Notifications not available
        else:
            # For subsequent official submissions, don't award XP but could send a different notification
            try:
                from apps.notifications.utils import create_notification
                create_notification(
                    recipient=ket_qua.nguoi_dung,
                    notification_type='exam_result',
                    title='📋 Kết quả thi',
                    message=f'Bạn đã hoàn thành lại bài thi "{ket_qua.de_thi.tieu_de}" nhưng không nhận thêm XP (XP chỉ được tính 1 lần duy nhất)',
                    action_url=f'/de-thi/ket-qua/{ket_qua.id}/',
                    content_object=ket_qua
                )
            except ImportError:
                pass  # Notifications not available
    # For practice modes, award XP only for first 5 attempts per day
    elif ket_qua.che_do in ['luyen_tap', 'luyen_tung_cau']:
        # Check if the user has already earned XP for this exam today (first 5 attempts)
        today = timezone.now().date()
        user = ket_qua.nguoi_dung
        exam = ket_qua.de_thi
        
        # Count how many times the user has earned XP for this exam today (BEFORE this attempt)
        # Only count attempts that resulted in XP gain
        xp_earned_today = KetQua.objects.filter(
            nguoi_dung=user,
            de_thi=exam,
            ngay_lam__date=today,
            che_do=ket_qua.che_do,  # Same mode (practice or question-by-question)
            is_official=False  # Practice attempts
        ).exclude(id=ket_qua.id).count()  # Exclude current attempt
        
        # Only award XP for first 5 attempts per exam per day per mode
        if xp_earned_today < 5:
            # Reduced XP for practice modes
            xp_amount, reason = get_exam_xp_reward(ket_qua.diem)
            # Reduce XP by 50% for practice modes
            xp_amount = max(1, int(xp_amount * 0.5))  # Minimum 1 XP
            reason = f"Luyện tập - {reason}"
            
            # Award XP
            result = award_xp(user, xp_amount, reason)
            
            if result and result.get('leveled_up'):
                # User leveled up! Could send notification here
                pass
        # If user has already earned XP 5 times today, don't award XP but allow the attempt
    # No XP for violated exams
