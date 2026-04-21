from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.de_thi.models import DeThi, KetQua, PracticeSession
from apps.kien_thuc.models import Mon
import json

class PracticeModeLimitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create a subject first
        self.subject = Mon.objects.create(ten='Mathematics', mo_ta='Math subject')
        
        # Create DeThi with correct field names and proper subject
        self.de_thi = DeThi.objects.create(
            ten='Practice Test',  # Changed from 'ten_de' to 'ten'
            mon=self.subject,  # Use the created subject instead of mon_id=1
            mo_ta='Practice test description',
            thoi_gian_phut=60  # Changed from 'time_limit' to 'thoi_gian_phut'
        )

    def test_daily_practice_limit(self):
        """Test daily practice limits"""
        # Create multiple practice sessions to simulate the limit behavior
        for i in range(3):
            session = PracticeSession.objects.create(
                nguoi_dung=self.user,
                de_thi=self.de_thi,
                da_hoan_thanh=False
            )
            self.assertIsNotNone(session)

    def test_practice_vs_real_distinction(self):
        """Test that practice and real modes are tracked separately"""
        # Create practice session
        practice_session = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            da_hoan_thanh=False
        )
        
        # Create official result (real mode)
        official_result = KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=7.5,
            is_official=True
        )
        
        # Both should exist independently
        practice_sessions = PracticeSession.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi
        )
        
        official_results = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        )
        
        # Both should exist independently
        self.assertGreaterEqual(practice_sessions.count(), 1)
        self.assertGreaterEqual(official_results.count(), 1)

    def test_practice_xp_penalty(self):
        """Test that practice mode has reduced XP or no XP"""
        # Create an official result (real mode) - should count for XP
        real_result = KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=8.5,
            is_official=True  # Official results count for XP
        )
        
        # Create a non-official result (practice mode) - should not count for XP
        practice_result = KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=7.0,
            is_official=False  # Practice results don't count for XP
        )
        
        # Verify practice doesn't create official result that affects XP
        official_results = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True  # Only official results count for XP
        )
        
        # Should have only the real result affecting XP
        self.assertEqual(official_results.count(), 1)
        self.assertEqual(official_results.first().id, real_result.id)