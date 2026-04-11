from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.gamification.models import DailyChallenge, UserChallengeProgress
# Removed unused import: from apps.nguoi_dung.xp_utils import calculate_xp_gain
from apps.kien_thuc.models import FlashcardProgress
from apps.de_thi.models import KetQua

class Command(BaseCommand):
    help = 'Update daily challenge XP rewards for all users'

    def handle(self, *args, **options):
        self.stdout.write('Updating daily challenge XP rewards...')
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            self.update_user_daily_challenges(user)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated daily challenges for {users.count()} users'
            )
        )

    def update_user_daily_challenges(self, user):
        """Update daily challenges for a specific user"""
        today = timezone.now().date()
        
        # Get today's daily challenges
        daily_challenges = DailyChallenge.objects.filter(
            date=today  # Fixed: use 'date' field instead of non-existent 'start_date' and 'end_date'
        )
        
        for challenge in daily_challenges:
            # Check if user has completed the challenge criteria
            progress, created = UserChallengeProgress.objects.get_or_create(
                user=user,
                challenge=challenge,
                defaults={}  # Removed non-existent 'start_date' field
            )
            
            # Skip if already completed today
            if progress.completed_at and progress.completed_at.date() == today:
                continue
                
            # Calculate completion based on challenge type
            completed = self.check_challenge_completion(user, challenge)
            
            if completed and not progress.completed_at:
                # Award XP for completing the challenge
                xp_reward = challenge.xp_reward
                progress.completed_at = timezone.now()  # Fixed: use correct field name 'completed_at'
                progress.xp_awarded = xp_reward
                progress.save()
                
                # Update user's total XP
                from apps.nguoi_dung.models import UserProfile
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    user_profile.xp += xp_reward
                    user_profile.save()
                except UserProfile.DoesNotExist:
                    pass
                
                self.stdout.write(
                    f'User {user.username} completed challenge: {challenge.title}'  # Fixed: use 'title' instead of 'name'
                )
            elif not completed:
                # Update progress if applicable
                self.update_challenge_progress(user, challenge, progress)

    def check_challenge_completion(self, user, challenge):
        """Check if user has completed the specific challenge"""
        if challenge.challenge_type == 'streak':
            # Check if user has maintained login streak
            return self.check_streak(user, challenge.target_value)
        
        elif challenge.challenge_type == 'flashcard':
            # Check if user has studied X flashcards today
            return self.check_flashcards_today(user, challenge.target_value)
        
        elif challenge.challenge_type == 'exam':
            # Check if user has taken X exams today
            return self.check_exams_today(user, challenge.target_value)
        
        elif challenge.challenge_type == 'score':
            # Check if user has achieved X% correct answers rate
            return self.check_min_score(user, challenge.target_value)
        
        elif challenge.challenge_type == 'questions':
            # Check if user has answered X questions correctly
            return self.check_correct_questions(user, challenge.target_value)
        
        return False

    def check_streak(self, user, target_streak):
        """Check if user has maintained login streak"""
        # Implementation would check user's login history
        # For now, return False as streak tracking logic is not fully implemented
        return False

    def check_min_score(self, user, target_score):
        """Check if user has achieved minimum score in an exam"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        # Check if user has completed an exam with the target score today
        exam_result = KetQua.objects.filter(
            nguoi_dung=user,
            ngay_lam__range=[today_start, today_end],
            diem__gte=target_score,
            is_official=True
        ).first()
        
        return exam_result is not None

    def check_correct_questions(self, user, target_count):
        """Check if user has answered target number of questions correctly today"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        # Count correct answers through TraLoi model
        exam_results = KetQua.objects.filter(
            nguoi_dung=user,
            ngay_lam__range=[today_start, today_end],
            is_official=True
        )
        
        # Count correct answers from TraLoi (answers)
        from apps.de_thi.models import TraLoi
        total_correct = TraLoi.objects.filter(
            ket_qua__in=exam_results,
            dung=True
        ).count()
        
        return total_correct >= target_count

    # The check_flashcard_streak method was removed as it's no longer used

    def check_flashcards_today(self, user, target_count):
        """Check if user has studied target number of flashcards today"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        flashcard_answers = FlashcardProgress.objects.filter(
            user=user,
            ngay_cap_nhat__range=[today_start, today_end]
        ).count()
        
        return flashcard_answers >= target_count

    def check_exams_today(self, user, target_count):
        """Check if user has taken target number of exams today"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        exam_results = KetQua.objects.filter(
            nguoi_dung=user,
            ngay_lam__range=[today_start, today_end],
            is_official=True  # Only count official exam attempts
        ).count()
        
        return exam_results >= target_count

    # The check_correct_answers_rate method was removed as it's no longer used

    def update_challenge_progress(self, user, challenge, progress):
        """Update progress for challenges that track incremental progress"""
        if challenge.challenge_type == 'flashcard':
            current_count = self.get_flashcards_today(user)
            progress.current_value = min(current_count, challenge.target_value)
        elif challenge.challenge_type == 'exam':
            current_count = self.get_exams_today(user)
            progress.current_value = min(current_count, challenge.target_value)
        
        progress.save()

    def get_flashcards_today(self, user):
        """Get count of flashcards studied today"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        return FlashcardProgress.objects.filter(
            user=user,
            ngay_cap_nhat__range=[today_start, today_end]
        ).count()

    def get_exams_today(self, user):
        """Get count of exams taken today"""
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)
        
        return KetQua.objects.filter(
            nguoi_dung=user,
            ngay_lam__range=[today_start, today_end],
            is_official=True
        ).count()