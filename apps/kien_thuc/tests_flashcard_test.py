from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from apps.kien_thuc.models import FlashcardSet, Flashcard, FlashcardProgress, FlashcardTest, FlashcardTestAnswer, Mon
from apps.gamification.models import DailyChallenge, UserChallengeProgress

class FlashcardTestFunctionalityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a subject first
        self.subject = Mon.objects.create(ten='Mathematics', mo_ta='Math subject')
        
        # Create a flashcard set - using correct field names and required mon field
        self.flashcard_set = FlashcardSet.objects.create(
            tieu_de='Test Flashcard Set',
            mo_ta='Description for testing',
            mon=self.subject,  # Added required mon field
            creator=self.user,
            status='published'
        )
        
        # Create some flashcards
        self.flashcard1 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 1',
            mat_sau='Back 1',
            thu_tu=1
        )
        
        self.flashcard2 = Flashcard.objects.create(
            flashcard_set=self.flashcard_set,
            mat_truoc='Front 2',
            mat_sau='Back 2',
            thu_tu=2
        )

    def test_flashcard_test_creation(self):
        """Test creating a flashcard test"""
        flashcard_test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,  # Changed from tong_so_flashcard to tong_so_cau_hoi
            so_cau_tra_loi_dung=1,
            diem=50.0
        )
        
        self.assertEqual(flashcard_test.nguoi_dung, self.user)
        self.assertEqual(flashcard_test.bo_flashcard, self.flashcard_set)
        self.assertEqual(flashcard_test.tong_so_cau_hoi, 2)
        self.assertEqual(flashcard_test.so_cau_tra_loi_dung, 1)
        self.assertEqual(flashcard_test.diem, 50.0)

    def test_flashcard_test_answer_creation(self):
        """Test creating answers for flashcard test"""
        flashcard_test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=1,
            diem=50.0
        )
        
        # Create test answers
        answer1 = FlashcardTestAnswer.objects.create(
            bai_kiem_tra=flashcard_test,
            flashcard=self.flashcard1,
            cau_tra_loi='Back 1',  # Changed from da_lua_chon to cau_tra_loi
            dung=True  # Changed from ket_qua to dung
        )
        
        answer2 = FlashcardTestAnswer.objects.create(
            bai_kiem_tra=flashcard_test,
            flashcard=self.flashcard2,
            cau_tra_loi='Wrong answer',
            dung=False  # Changed from ket_qua to dung
        )
        
        self.assertEqual(answer1.bai_kiem_tra, flashcard_test)
        self.assertEqual(answer1.flashcard, self.flashcard1)
        self.assertTrue(answer1.dung)
        
        self.assertEqual(answer2.bai_kiem_tra, flashcard_test)
        self.assertEqual(answer2.flashcard, self.flashcard2)
        self.assertFalse(answer2.dung)

    def test_flashcard_test_scoring(self):
        """Test that flashcard test scoring works correctly"""
        flashcard_test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=0,
            diem=0.0
        )
        
        # Create answers
        FlashcardTestAnswer.objects.create(
            bai_kiem_tra=flashcard_test,
            flashcard=self.flashcard1,
            cau_tra_loi='Back 1',
            dung=True  # Changed from ket_qua to dung
        )
        
        FlashcardTestAnswer.objects.create(
            bai_kiem_tra=flashcard_test,
            flashcard=self.flashcard2,
            cau_tra_loi='Wrong answer',
            dung=False  # Changed from ket_qua to dung
        )
        
        # Update test scores
        correct_answers = FlashcardTestAnswer.objects.filter(
            bai_kiem_tra=flashcard_test,
            dung=True  # Changed from ket_qua to dung
        ).count()
        
        flashcard_test.so_cau_tra_loi_dung = correct_answers
        flashcard_test.diem = (correct_answers / flashcard_test.tong_so_cau_hoi) * 100
        flashcard_test.save()
        
        self.assertEqual(flashcard_test.so_cau_tra_loi_dung, 1)
        self.assertEqual(flashcard_test.diem, 50.0)  # 1 out of 2 correct

    def test_flashcard_test_history(self):
        """Test that users can have multiple flashcard test histories"""
        # Create multiple tests
        test1 = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=2,
            diem=100.0
        )
        
        test2 = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=1,
            diem=50.0
        )
        
        # Check that both tests exist for the user
        user_tests = FlashcardTest.objects.filter(nguoi_dung=self.user)
        self.assertEqual(user_tests.count(), 2)
        
        # Check that tests are associated with the same flashcard set
        set_tests = FlashcardTest.objects.filter(bo_flashcard=self.flashcard_set)
        self.assertEqual(set_tests.count(), 2)

    def test_flashcard_test_progress_integration(self):
        """Test integration between flashcard tests and regular flashcard progress"""
        # First, create regular flashcard progress - using correct field names
        progress1 = FlashcardProgress.objects.create(
            user=self.user,
            flashcard=self.flashcard1,
            is_learned=False,
            next_review_date=timezone.now(),
            interval=0,
            ease_factor=2.5,
            repetition_count=0
        )
        
        # Then create a test
        flashcard_test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=1,
            diem=50.0
        )
        
        FlashcardTestAnswer.objects.create(
            bai_kiem_tra=flashcard_test,
            flashcard=self.flashcard1,
            cau_tra_loi='Back 1',
            dung=True
        )
        
        # Both regular progress and test results should coexist
        self.assertTrue(FlashcardProgress.objects.filter(id=progress1.id).exists())
        self.assertTrue(FlashcardTest.objects.filter(id=flashcard_test.id).exists())

    def test_flashcard_test_xp_integration(self):
        """Test integration between flashcard tests and XP/daily challenges"""
        from apps.nguoi_dung.models import UserGamification
        
        # Create user gamification data
        user_gamification, created = UserGamification.objects.get_or_create(user=self.user)
        
        # Create a flashcard test
        flashcard_test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.flashcard_set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=2,  # All correct
            diem=100.0
        )
        
        # Check if daily challenge progress is affected
        # Create a flashcard-related daily challenge
        daily_challenge = DailyChallenge.objects.create(
            title='Take a Flashcard Test',
            description='Complete a flashcard test with high score',
            challenge_type='flashcard',
            target_value=1,  # Take 1 test
            xp_reward=50,
            date=timezone.now().date()
        )
        
        # Check if progress is made toward the challenge
        progress, created = UserChallengeProgress.objects.get_or_create(
            user=self.user,
            challenge=daily_challenge
        )
        
        # Initially, progress should be 0
        self.assertEqual(progress.current_value, 0)  # Changed from current_progress to current_value
        
        # Update progress based on test completion
        progress.current_value = 1  # Changed from current_progress to current_value
        if progress.current_value >= daily_challenge.target_value:
            progress.completed_at = timezone.now()  # Changed from completed_date to completed_at
            progress.xp_awarded = daily_challenge.xp_reward
        
        progress.save()
        
        # Refresh and verify
        progress.refresh_from_db()
        self.assertGreaterEqual(progress.current_value, 1)  # Changed from current_progress to current_value
        if progress.current_value >= daily_challenge.target_value:
            self.assertIsNotNone(progress.completed_at)  # Changed from completed_date to completed_at
            self.assertEqual(progress.xp_awarded, daily_challenge.xp_reward)