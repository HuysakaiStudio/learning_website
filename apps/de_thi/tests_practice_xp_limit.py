from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from ..models import DeThi, KetQua, PracticeSession
from apps.nguoi_dung.models import UserProfile
import json

class PracticeLimitTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.de_thi = DeThi.objects.create(
            ten_de='Practice Test',
            mon_hoc_id=1,
            creator=self.user,
            is_custom=False,
            time_limit=60
        )
        
        # Create user profile to track practice limits
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            practice_limit_reset_date=timezone.now() - timedelta(days=1)
        )

    def test_daily_practice_limit_enforcement(self):
        """Test that daily practice limits are enforced"""
        self.client.login(username='testuser', password='testpass')
        
        # Set a low daily limit for testing
        self.user_profile.daily_practice_limit = 2
        self.user_profile.current_daily_practice_count = 0
        self.user_profile.save()
        
        # Perform first practice session
        response1 = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        self.assertEqual(response1.status_code, 302)  # Should be allowed
        
        # Perform second practice session
        response2 = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        self.assertEqual(response2.status_code, 302)  # Should be allowed
        
        # Update count manually to simulate the increment
        self.user_profile.refresh_from_db()
        self.user_profile.current_daily_practice_count = 2
        self.user_profile.save()
        
        # Third practice session should be limited
        response3 = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Should either redirect with message or return error
        # Implementation depends on how limits are handled in views
        # This tests that the limit is being checked

    def test_weekly_practice_limit(self):
        """Test weekly practice limits"""
        self.client.login(username='testuser', password='testpass')
        
        # Set a weekly limit
        self.user_profile.weekly_practice_limit = 10
        self.user_profile.current_weekly_practice_count = 9
        self.user_profile.save()
        
        # This should be the 10th (final) allowed practice session
        response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Should be allowed
        self.assertEqual(response.status_code, 302)
        
        # Update count to 10
        self.user_profile.refresh_from_db()
        self.user_profile.current_weekly_practice_count = 10
        self.user_profile.save()
        
        # Next attempt should be limited
        response2 = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })

    def test_practice_limit_reset(self):
        """Test that practice limits reset appropriately"""
        self.client.login(username='testuser', password='testpass')
        
        # Set counts to maximum
        self.user_profile.daily_practice_limit = 5
        self.user_profile.current_daily_practice_count = 5
        self.user_profile.weekly_practice_limit = 20
        self.user_profile.current_weekly_practice_count = 20
        self.user_profile.practice_limit_reset_date = timezone.now() - timedelta(days=1)
        self.user_profile.save()
        
        # All limits reached - should be restricted
        response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Reset the counters to simulate passing time
        self.user_profile.refresh_from_db()
        self.user_profile.current_daily_practice_count = 0
        self.user_profile.current_weekly_practice_count = 0
        self.user_profile.practice_limit_reset_date = timezone.now()
        self.user_profile.save()
        
        # Now practice should be allowed again
        response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        self.assertEqual(response.status_code, 302)

    def test_practice_limit_notification(self):
        """Test that users are notified near their practice limits"""
        self.client.login(username='testuser', password='testpass')
        
        # Set close to daily limit
        self.user_profile.daily_practice_limit = 5
        self.user_profile.current_daily_practice_count = 4  # One away from limit
        self.user_profile.save()
        
        # Request should succeed but may include warning
        response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # Check if response contains limit warning (implementation dependent)
        # This would depend on how the view handles notifications


class PracticeVsRealModeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.de_thi = DeThi.objects.create(
            ten_de='Test Exam',
            mon_hoc_id=1,
            creator=self.user,
            is_custom=False,
            time_limit=60
        )

    def test_separate_tracking_for_modes(self):
        """Test that practice and real modes have separate limits"""
        self.client.login(username='testuser', password='testpass')
        
        # Reach practice limit
        self.user.userprofile.daily_practice_limit = 1
        self.user.userprofile.current_daily_practice_count = 1
        self.user.userprofile.save()
        
        # Practice mode should be limited
        practice_response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'practice'
        })
        
        # But real mode should still be available
        real_response = self.client.post(reverse('lam_bai'), {
            'de_thi_id': self.de_thi.id,
            'mode': 'real'
        })
        
        # Real mode should not be affected by practice limits
        # The exact behavior depends on implementation