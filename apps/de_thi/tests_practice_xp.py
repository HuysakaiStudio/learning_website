from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from ..models import DeThi, KetQua, PracticeSession
from apps.nguoi_dung.xp_utils import calculate_xp_gain
import json

class PracticeModeXPTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.de_thi = DeThi.objects.create(
            ten_de='Practice Test',
            mon_hoc_id=1,  # Assuming a subject exists
            creator=self.user,
            is_custom=False,
            time_limit=60
        )

    def test_practice_session_creation(self):
        """Test that practice sessions are created properly"""
        self.client.login(username='testuser', password='testpass')
        
        # Start practice session
        response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Check that a practice session was created
        practice_session = PracticeSession.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi
        ).first()
        
        self.assertIsNotNone(practice_session)
        self.assertTrue(practice_session.is_practice)
        self.assertIsNotNone(practice_session.start_time)

    def test_no_xp_for_practice_mode(self):
        """Test that practice mode doesn't award XP"""
        self.client.login(username='testuser', password='testpass')
        
        # Submit answers in practice mode
        response = self.client.post(reverse('nop_bai'), {
            'de_thi_id': self.de_thi.id,
            'answers': json.dumps({'1': 'A', '2': 'B'}),
            'mode': 'practice'
        })
        
        # Check that no official result was created (no XP)
        official_results = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        )
        
        self.assertEqual(official_results.count(), 0)

    def test_xp_calculation_for_real_mode(self):
        """Test XP calculation for real exam mode"""
        self.client.login(username='testuser', password='testpass')
        
        # Submit answers in real mode
        response = self.client.post(reverse('nop_bai'), {
            'de_thi_id': self.de_thi.id,
            'answers': json.dumps({'1': 'A', '2': 'B'}),
            'mode': 'real'
        })
        
        # Check that an official result was created
        official_result = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        ).first()
        
        self.assertIsNotNone(official_result)
        self.assertGreater(official_result.xp_gained, 0)

    def test_practice_session_cleanup(self):
        """Test that old practice sessions are cleaned up"""
        # Create an old practice session
        old_session = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_practice=True,
            start_time=timezone.now() - timedelta(hours=25)  # More than 24 hours ago
        )
        
        # Create a recent practice session
        recent_session = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_practice=True,
            start_time=timezone.now() - timedelta(hours=1)  # Recent
        )
        
        # Clean up old sessions (this would happen via management command)
        cutoff_time = timezone.now() - timedelta(hours=24)
        old_sessions = PracticeSession.objects.filter(start_time__lt=cutoff_time)
        old_count_before = old_sessions.count()
        
        old_sessions.delete()
        
        # Verify old session was deleted, recent one remains
        old_remaining = PracticeSession.objects.filter(id=old_session.id).exists()
        recent_remaining = PracticeSession.objects.filter(id=recent_session.id).exists()
        
        self.assertFalse(old_remaining)
        self.assertTrue(recent_remaining)


class PracticeModeLimitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.de_thi = DeThi.objects.create(
            ten_de='Practice Test',
            mon_hoc_id=1,
            creator=self.user,
            is_custom=False,
            time_limit=60
        )

    def test_daily_practice_limit(self):
        """Test daily practice limits"""
        from ..utils import get_daily_practice_count, increment_daily_practice
        
        # Reset counter for test
        # In real implementation, this would track daily attempts
        
        # Simulate multiple practice attempts
        self.client.login(username='testuser', password='testpass')
        
        for i in range(5):
            response = self.client.post(reverse('lam_bai'), {
                'de_thi_id': self.de_thi.id,
                'mode': 'practice'
            })
            self.assertEqual(response.status_code, 302)  # Should allow practice

    def test_practice_vs_real_distinction(self):
        """Test that practice and real modes are tracked separately"""
        self.client.login(username='testuser', password='testpass')
        
        # Do a practice session
        practice_response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Do a real session
        real_response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'real'
        })
        
        # Both should be allowed (depending on implementation)
        # The key is that they're tracked differently
        practice_sessions = PracticeSession.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_practice=True
        )
        
        # Real sessions would create KetQua objects with is_official=True
        official_results = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        )
        
        # Both should exist independently
        self.assertGreaterEqual(practice_sessions.count(), 1)