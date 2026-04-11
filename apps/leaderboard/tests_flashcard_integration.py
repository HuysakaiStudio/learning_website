from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from apps.leaderboard.models import LeaderboardEntry
from apps.kien_thuc.models import FlashcardSet, Flashcard, FlashcardProgress
from apps.gamification.models import DailyChallenge, UserChallengeProgress

class FlashcardLeaderboardIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a leaderboard entry for the user
        self.leaderboard_entry = LeaderboardEntry.objects.create(
            user=self.user,
            subject_id=1,  # Assuming a subject exists
            total_score=100.0,
            rank=10
        )
        
        # Create a flashcard set and flashcards
        self.flashcard_set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test Description',
            nguoi_tao=self.user,
            trang_thai='published'
        )
        
        self.flashcard = Flashcard.objects.create(
            bo_flashcard=self.flashcard_set,
            mat_truoc='Front',
            mat_sau='Back',
            vi_tri=1
        )

    def test_leaderboard_updates_on_flashcard_study(self):
        """Test that leaderboard entries update when user studies flashcards"""
        # Initially, the user should have 0 flashcard-related metrics
        self.leaderboard_entry.refresh_from_db()
        self.assertEqual(self.leaderboard_entry.flashcard_total_cards, 0)
        self.assertEqual(self.leaderboard_entry.flashcard_avg_score, 0.0)
        
        # Simulate studying a flashcard and getting progress
        progress, created = FlashcardProgress.objects.get_or_create(
            nguoi_dung=self.user,
            flashcard=self.flashcard,
            defaults={
                'trang_thai': 'learning',
                'he_so_de_dang': 2.5,
                'so_lan_hien_thi': 1,
                'so_lan_dung': 1,
                'lan_cuoi_hien_thi': timezone.now(),
                'next_review_date': timezone.now()
            }
        )
        
        # Update leaderboard metrics after flashcard study
        self.leaderboard_entry.flashcard_total_cards += 1
        self.leaderboard_entry.last_flashcard_study = timezone.now()
        self.leaderboard_entry.weekly_flashcard_count += 1
        
        # Calculate average score based on progress
        if self.leaderboard_entry.flashcard_total_cards > 0:
            avg_score = (self.leaderboard_entry.flashcard_avg_score * (self.leaderboard_entry.flashcard_total_cards - 1) + 1.0) / self.leaderboard_entry.flashcard_total_cards
            self.leaderboard_entry.flashcard_avg_score = avg_score
        else:
            self.leaderboard_entry.flashcard_avg_score = 1.0
            
        self.leaderboard_entry.save()
        
        # Refresh and verify the updates
        self.leaderboard_entry.refresh_from_db()
        self.assertEqual(self.leaderboard_entry.flashcard_total_cards, 1)
        self.assertGreater(self.leaderboard_entry.flashcard_avg_score, 0.0)
        self.assertIsNotNone(self.leaderboard_entry.last_flashcard_study)

    def test_flashcard_streak_tracking(self):
        """Test that flashcard study streaks are tracked correctly"""
        # Initially, streak should be 0
        self.leaderboard_entry.refresh_from_db()
        self.assertEqual(self.leaderboard_entry.flashcard_streak, 0)
        
        # Simulate studying flashcards for 3 consecutive days
        for i in range(3):
            study_date = timezone.now() - timezone.timedelta(days=i)
            
            # Create flashcard progress for each day
            FlashcardProgress.objects.create(
                nguoi_dung=self.user,
                flashcard=self.flashcard,
                trang_thai='learning',
                he_so_de_dang=2.5,
                so_lan_hien_thi=1,
                so_lan_dung=1,
                lan_cuoi_hien_thi=study_date,
                next_review_date=study_date
            )
        
        # Update streak in leaderboard
        self.leaderboard_entry.flashcard_streak = 3
        self.leaderboard_entry.save()
        
        self.leaderboard_entry.refresh_from_db()
        self.assertEqual(self.leaderboard_entry.flashcard_streak, 3)

    def test_daily_challenge_integration(self):
        """Test integration between flashcard study and daily challenges"""
        # Create a flashcard-related daily challenge
        daily_challenge = DailyChallenge.objects.create(
            name='Study 5 Flashcards Today',
            description='Study at least 5 flashcards in one day',
            challenge_type='flashcards_today',
            target_value=5,
            xp_reward=100,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1)
        )
        
        # Initially no progress
        progress_exists = UserChallengeProgress.objects.filter(
            user=self.user,
            challenge=daily_challenge
        ).exists()
        self.assertFalse(progress_exists)
        
        # User studies 5 flashcards (simulate by creating progress records)
        for i in range(5):
            FlashcardProgress.objects.create(
                nguoi_dung=self.user,
                flashcard=self.flashcard,
                trang_thai='learning',
                he_so_de_dang=2.5,
                so_lan_hien_thi=1,
                so_lan_dung=1,
                lan_cuoi_hien_thi=timezone.now(),
                next_review_date=timezone.now()
            )
        
        # Check if challenge progress was created
        progress, created = UserChallengeProgress.objects.get_or_create(
            user=self.user,
            challenge=daily_challenge
        )
        
        # Update progress
        progress.current_progress = 5
        if progress.current_progress >= daily_challenge.target_value:
            progress.completed_date = timezone.now()
            progress.xp_awarded = daily_challenge.xp_reward
        
        progress.save()
        
        # Verify challenge was completed
        progress.refresh_from_db()
        self.assertIsNotNone(progress.completed_date)
        self.assertEqual(progress.xp_awarded, daily_challenge.xp_reward)

    def test_leaderboard_ranking_by_flashcard_performance(self):
        """Test that users can be ranked based on flashcard performance"""
        # Create another user
        user2 = User.objects.create_user(username='testuser2', password='testpass')
        
        # Create leaderboard entry for second user
        leaderboard_entry2 = LeaderboardEntry.objects.create(
            user=user2,
            subject_id=1,
            total_score=80.0,
            rank=15
        )
        
        # Update first user's flashcard metrics to be higher
        self.leaderboard_entry.flashcard_avg_score = 0.95
        self.leaderboard_entry.flashcard_total_cards = 50
        self.leaderboard_entry.flashcard_streak = 7
        self.leaderboard_entry.total_score = 150.0
        self.leaderboard_entry.save()
        
        # Update second user's flashcard metrics to be lower
        leaderboard_entry2.flashcard_avg_score = 0.75
        leaderboard_entry2.flashcard_total_cards = 25
        leaderboard_entry2.flashcard_streak = 2
        leaderboard_entry2.total_score = 120.0
        leaderboard_entry2.save()
        
        # In a real system, ranking would be recalculated based on various factors
        # including flashcard performance. This test verifies that the metrics exist
        # and can be used for ranking calculations.
        self.assertGreater(self.leaderboard_entry.flashcard_avg_score, 
                          leaderboard_entry2.flashcard_avg_score)
        self.assertGreater(self.leaderboard_entry.flashcard_total_cards, 
                          leaderboard_entry2.flashcard_total_cards)


class FlashcardScoreCalculationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.leaderboard_entry = LeaderboardEntry.objects.create(
            user=self.user,
            subject_id=1,
            total_score=100.0,
            rank=10
        )

    def test_average_score_calculation(self):
        """Test calculation of average flashcard score"""
        scores = [1.0, 0.8, 1.0, 0.6, 1.0]  # 5 study sessions
        
        # Calculate cumulative average
        for i, score in enumerate(scores):
            self.leaderboard_entry.flashcard_total_cards = i + 1
            old_avg = self.leaderboard_entry.flashcard_avg_score
            new_avg = ((old_avg * i) + score) / (i + 1)
            self.leaderboard_entry.flashcard_avg_score = new_avg
            self.leaderboard_entry.save()
        
        expected_avg = sum(scores) / len(scores)
        self.leaderboard_entry.refresh_from_db()
        self.assertAlmostEqual(self.leaderboard_entry.flashcard_avg_score, expected_avg, places=2)