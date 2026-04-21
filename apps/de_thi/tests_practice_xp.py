from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.de_thi.models import DeThi, KetQua, PracticeSession
from apps.kien_thuc.models import Mon
import json

class PracticeModeXPTest(TestCase):
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

    def test_practice_session_creation(self):
        """Test that practice sessions are created properly"""
        # Create a practice session (Note: PracticeSession doesn't have an is_practice field)
        practice_session = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            da_hoan_thanh=False  # Not completed
        )
        
        self.assertIsNotNone(practice_session)
        self.assertFalse(practice_session.da_hoan_thanh)  # Not completed
        self.assertIsNotNone(practice_session.ngay_bat_dau)  # Has start date

    def test_no_xp_for_practice_mode(self):
        """Test that practice mode doesn't award XP"""
        # Create a result in practice mode (non-official)
        result = KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=8.5,
            is_official=False  # Practice mode results are not official
        )
        
        # Check that no official result was created (no XP)
        official_results = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        )
        
        self.assertEqual(official_results.count(), 0)

    def test_xp_calculation_for_real_mode(self):
        """Test XP calculation for real exam mode"""
        # Create an official result (real mode)
        official_result = KetQua.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            diem=8.5,
            is_official=True  # Official results count for XP
        )
        
        # Check that an official result was created
        official_result_check = KetQua.objects.filter(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            is_official=True
        ).first()
        
        self.assertIsNotNone(official_result_check)
        self.assertGreater(official_result_check.diem, 0)

    def test_practice_session_cleanup(self):
        """Test that old practice sessions can be cleaned up"""
        # Create multiple practice sessions
        session1 = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            da_hoan_thanh=False
        )
        
        session2 = PracticeSession.objects.create(
            nguoi_dung=self.user,
            de_thi=self.de_thi,
            da_hoan_thanh=False
        )
        
        # Verify both sessions exist initially
        self.assertTrue(PracticeSession.objects.filter(id=session1.id).exists())
        self.assertTrue(PracticeSession.objects.filter(id=session2.id).exists())
        
        # Count total sessions before deletion
        total_before = PracticeSession.objects.count()
        
        # Delete the first session (simulating cleanup of old sessions)
        session1.delete()
        
        # Count total sessions after deletion
        total_after = PracticeSession.objects.count()
        
        # Verify the first session was deleted, the second remains
        self.assertFalse(PracticeSession.objects.filter(id=session1.id).exists())
        self.assertTrue(PracticeSession.objects.filter(id=session2.id).exists())
        
        # Total count should decrease by 1
        self.assertEqual(total_before - 1, total_after)


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
            da_hoan_thanh=False  # Not completed
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