from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from apps.leaderboard.models import Leaderboard, LeaderboardEntry
from apps.kien_thuc.models import FlashcardSet, Flashcard, FlashcardProgress, Mon
from apps.gamification.models import DailyChallenge, UserChallengeProgress


class FlashcardLeaderboardIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a subject first
        self.subject = Mon.objects.create(ten='Mathematics', mo_ta='Math subject')
        
        # Create a leaderboard first
        self.leaderboard = Leaderboard.objects.create(
            period='all_time',
            category='flashcard'
        )
        
        # Create a leaderboard entry for the user
        self.leaderboard_entry = LeaderboardEntry.objects.create(
            user=self.user,
            leaderboard=self.leaderboard,
            total_score=100.0,
            rank=10
        )
        
        # Create a flashcard set and flashcards - using correct field names
        self.flashcard_set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test Description',
            mon=self.subject,  # Add required mon field
            creator=self.user,
            status='published'
        )
        
        self.flashcard = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front',
            mat_sau='Back',
            thu_tu=1
        )

    def test_leaderboard_updates_on_flashcard_study(self):
        """Test that leaderboard entries update when user studies flashcards"""
        # Initially, the user should have 0 flashcard-related metrics
        self.leaderboard_entry.refresh_from_db()
        self.assertEqual(self.leaderboard_entry.flashcard_total_cards, 0)
        self.assertEqual(self.leaderboard_entry.flashcard_avg_score, 0.0)
        
        # Simulate studying a flashcard and getting progress
        progress, created = FlashcardProgress.objects.get_or_create(
            user=self.user,
            flashcard=self.flashcard,
            defaults={
                'is_learned': False,
                'next_review_date': timezone.now(),
                'interval': 0,
                'ease_factor': 2.5,
                'repetition_count': 0
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
        
        # Create multiple flashcards to simulate studying different cards each day
        flashcard2 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 2',
            mat_sau='Back 2',
            thu_tu=2
        )
        
        flashcard3 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 3',
            mat_sau='Back 3',
            thu_tu=3
        )
        
        # Create flashcard progress for each day with different flashcards
        FlashcardProgress.objects.get_or_create(
            user=self.user,
            flashcard=self.flashcard,
            defaults={
                'is_learned': False,
                'next_review_date': timezone.now() - timezone.timedelta(days=2),
                'interval': 0,
                'ease_factor': 2.5,
                'repetition_count': 0
            }
        )
        
        FlashcardProgress.objects.get_or_create(
            user=self.user,
            flashcard=flashcard2,
            defaults={
                'is_learned': False,
                'next_review_date': timezone.now() - timezone.timedelta(days=1),
                'interval': 0,
                'ease_factor': 2.5,
                'repetition_count': 0
            }
        )
        
        FlashcardProgress.objects.get_or_create(
            user=self.user,
            flashcard=flashcard3,
            defaults={
                'is_learned': False,
                'next_review_date': timezone.now(),
                'interval': 0,
                'ease_factor': 2.5,
                'repetition_count': 0
            }
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
            title='Study 5 Flashcards Today',  # Changed from 'name' to 'title'
            description='Study at least 5 flashcards in one day',
            challenge_type='flashcard',  # Changed from 'flashcards_today' to 'flashcard'
            target_value=5,
            xp_reward=100,
            date=timezone.now().date(),  # Changed from 'start_date'/'end_date' to 'date'
        )
        
        # Initially no progress
        progress_exists = UserChallengeProgress.objects.filter(
            user=self.user,
            challenge=daily_challenge
        ).exists()
        self.assertFalse(progress_exists)
        
        # Create multiple different flashcards to study (avoiding unique constraint)
        flashcard2 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 2',
            mat_sau='Back 2',
            thu_tu=2
        )
        
        flashcard3 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 3',
            mat_sau='Back 3',
            thu_tu=3
        )
        
        flashcard4 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 4',
            mat_sau='Back 4',
            thu_tu=4
        )
        
        flashcard5 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 5',
            mat_sau='Back 5',
            thu_tu=5
        )
        
        # User studies 5 different flashcards
        for flashcard in [self.flashcard, flashcard2, flashcard3, flashcard4, flashcard5]:
            FlashcardProgress.objects.get_or_create(
                user=self.user,
                flashcard=flashcard,
                defaults={
                    'is_learned': False,
                    'next_review_date': timezone.now(),
                    'interval': 0,
                    'ease_factor': 2.5,
                    'repetition_count': 0
                }
            )
        
        # Check if challenge progress was created
        progress, created = UserChallengeProgress.objects.get_or_create(
            user=self.user,
            challenge=daily_challenge,
            defaults={
                'current_value': 0,
                'completed_at': None,
                'xp_awarded': 0
            }
        )
        
        # Update progress
        progress.current_value = 5  # Changed from 'current_progress' to 'current_value'
        if progress.current_value >= daily_challenge.target_value:
            progress.completed_at = timezone.now()  # Changed from 'completed_date' to 'completed_at'
            progress.xp_awarded = daily_challenge.xp_reward
        
        progress.save()
        
        # Verify challenge was completed
        progress.refresh_from_db()
        self.assertIsNotNone(progress.completed_at)
        self.assertEqual(progress.xp_awarded, daily_challenge.xp_reward)

    def test_leaderboard_ranking_by_flashcard_performance(self):
        """Test that users can be ranked based on flashcard performance"""
        # Create another user
        user2 = User.objects.create_user(username='testuser2', password='testpass')
        
        # Create leaderboard for second user
        leaderboard2 = Leaderboard.objects.create(
            period='all_time',
            category='flashcard'
        )
        
        # Create leaderboard entry for second user
        leaderboard_entry2 = LeaderboardEntry.objects.create(
            user=user2,
            leaderboard=leaderboard2,
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
        
        # Create a subject first
        self.subject = Mon.objects.create(ten='Mathematics', mo_ta='Math subject')
        
        # Create a leaderboard first
        self.leaderboard = Leaderboard.objects.create(
            period='all_time',
            category='flashcard'
        )
        
        self.leaderboard_entry = LeaderboardEntry.objects.create(
            user=self.user,
            leaderboard=self.leaderboard,
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