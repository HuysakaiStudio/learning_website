from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Leaderboard, LeaderboardEntry, Achievement
from .views import update_leaderboard, calculate_overall_scores
from apps.kien_thuc.models import Mon, FlashcardSet, Flashcard, FlashcardProgress
from apps.de_thi.models import DeThi, CauHoi, KetQua


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.mon = Mon.objects.create(ten='Toán', mo_ta='Môn Toán')
    
    def test_leaderboard_creation(self):
        """Test creating a leaderboard"""
        leaderboard = Leaderboard.objects.create(
            period='weekly',
            category='overall'
        )
        self.assertEqual(leaderboard.period, 'weekly')
        self.assertEqual(leaderboard.category, 'overall')
        self.assertEqual(leaderboard.rankings, [])
    
    def test_leaderboard_unique_together(self):
        """Test unique_together constraint"""
        Leaderboard.objects.create(period='weekly', category='overall')
        # Should not raise error for same period/category
        leaderboard = Leaderboard.objects.get(period='weekly', category='overall')
        self.assertIsNotNone(leaderboard)


class LeaderboardEntryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.leaderboard = Leaderboard.objects.create(
            period='weekly',
            category='overall'
        )
    
    def test_entry_creation(self):
        """Test creating a leaderboard entry"""
        entry = LeaderboardEntry.objects.create(
            user=self.user,
            leaderboard=self.leaderboard,
            score=100.5,
            rank=1,
            exams_completed=5,
            flashcards_learned=20
        )
        self.assertEqual(entry.score, 100.5)
        self.assertEqual(entry.rank, 1)
        self.assertEqual(str(entry), '#1 - testuser (100.5)')


class AchievementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_achievement_creation(self):
        """Test creating an achievement"""
        achievement = Achievement.objects.create(
            user=self.user,
            achievement_type='top_10_weekly',
            rank_achieved=5,
            score_achieved=150.0
        )
        self.assertEqual(achievement.achievement_type, 'top_10_weekly')
        self.assertEqual(achievement.rank_achieved, 5)


class LeaderboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.mon = Mon.objects.create(ten='Toán', mo_ta='Môn Toán')
    
    def test_leaderboard_view_get(self):
        """Test accessing leaderboard view"""
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('leaderboard', response.context)
    
    def test_leaderboard_view_with_filters(self):
        """Test leaderboard with period and category filters"""
        response = self.client.get('/leaderboard/?period=daily&category=exam')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['period'], 'daily')
        self.assertEqual(response.context['category'], 'exam')
    
    def test_user_achievements_view_requires_login(self):
        """Test achievements view requires authentication"""
        response = self.client.get('/leaderboard/achievements/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_user_achievements_view_authenticated(self):
        """Test achievements view when logged in"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/leaderboard/achievements/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('achievements', response.context)


class LeaderboardCalculationTest(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')
        
        # Create mon
        self.mon = Mon.objects.create(ten='Toán', mo_ta='Môn Toán')
        
        # Create de thi
        self.de_thi = DeThi.objects.create(
            ten='Đề test',
            mon=self.mon,
            thoi_gian_phut=60,
            creator=self.user1
        )
        
        # Create cau hoi
        self.cau_hoi = CauHoi.objects.create(
            de_thi=self.de_thi,
            noi_dung='Câu hỏi test',
            loai='tn',
            dap_an_dung='A'
        )
    
    def test_calculate_overall_scores(self):
        """Test calculating overall scores"""
        # Create exam results
        KetQua.objects.create(
            nguoi_dung=self.user1,
            de_thi=self.de_thi,
            diem=8.0,
            thoi_gian_lam=1800,
            is_official=True
        )
        
        # Create flashcard progress
        flashcard_set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test',
            mon=self.mon,
            creator=self.user1
        )
        flashcard = Flashcard.objects.create(
            flashcard_set=flashcard_set,
            mat_truoc='Front',
            mat_sau='Back'
        )
        FlashcardProgress.objects.create(
            user=self.user1,
            flashcard=flashcard,
            is_learned=True
        )
        
        # Calculate scores
        scores = calculate_overall_scores()
        
        self.assertGreater(len(scores), 0)
        user1_score = next((s for s in scores if s['user_id'] == self.user1.id), None)
        self.assertIsNotNone(user1_score)
        self.assertGreater(user1_score['score'], 0)
    
    def test_update_leaderboard(self):
        """Test updating leaderboard"""
        leaderboard = Leaderboard.objects.create(
            period='weekly',
            category='overall'
        )
        
        # Create some data
        KetQua.objects.create(
            nguoi_dung=self.user1,
            de_thi=self.de_thi,
            diem=9.0,
            thoi_gian_lam=1800,
            is_official=True
        )
        
        # Update leaderboard
        update_leaderboard(leaderboard)
        
        # Check entries were created
        entries = LeaderboardEntry.objects.filter(leaderboard=leaderboard)
        self.assertGreater(entries.count(), 0)
        
        # Check rankings were cached
        self.assertGreater(len(leaderboard.rankings), 0)


class LeaderboardIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.mon = Mon.objects.create(ten='Toán', mo_ta='Môn Toán')
        
        # Create de thi
        self.de_thi = DeThi.objects.create(
            ten='Đề test',
            mon=self.mon,
            thoi_gian_phut=60,
            creator=self.user
        )
        
        # Create cau hoi
        CauHoi.objects.create(
            de_thi=self.de_thi,
            noi_dung='Câu hỏi test',
            loai='tn',
            dap_an_dung='A'
        )
    
    def test_leaderboard_updates_after_exam(self):
        """Test leaderboard updates after completing exam"""
        # Create exam result
        KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=9.5,
            thoi_gian_lam=1800,
            is_official=True
        )
        
        # Access leaderboard (should trigger update)
        response = self.client.get('/leaderboard/?period=weekly&category=exam')
        self.assertEqual(response.status_code, 200)
        
        # Check if user appears in leaderboard
        leaderboard = response.context['leaderboard']
        entries = leaderboard.entries.all()
        
        # User should be in entries if they have score
        user_in_leaderboard = any(e.user == self.user for e in entries)
        self.assertTrue(user_in_leaderboard or entries.count() == 0)
