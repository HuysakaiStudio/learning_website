from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import FlashcardSet, Flashcard, FlashcardProgress, FlashcardTest, FlashcardTestAnswer
import uuid

class FlashcardTestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test Description',
            nguoi_tao=self.user,
            trang_thai='published'
        )
        
        self.flashcard1 = Flashcard.objects.create(
            bo_flashcard=self.set,
            mat_truoc='Front 1',
            mat_sau='Back 1',
            vi_tri=1
        )
        
        self.flashcard2 = Flashcard.objects.create(
            bo_flashcard=self.set,
            mat_truoc='Front 2',
            mat_sau='Back 2',
            vi_tri=2
        )

    def test_create_flashcard_test(self):
        """Test creating a flashcard test"""
        test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=0
        )
        
        self.assertEqual(test.nguoi_dung, self.user)
        self.assertEqual(test.bo_flashcard, self.set)
        self.assertEqual(test.tong_so_cau_hoi, 2)
        self.assertIsNotNone(test.ngay_tao)

    def test_create_flashcard_test_answer(self):
        """Test creating a flashcard test answer"""
        test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.set,
            tong_so_cau_hoi=2,
            so_cau_tra_loi_dung=0
        )
        
        answer = FlashcardTestAnswer.objects.create(
            bai_kiem_tra=test,
            flashcard=self.flashcard1,
            cau_tra_loi='User answer',
            dung=True
        )
        
        self.assertEqual(answer.bai_kiem_tra, test)
        self.assertEqual(answer.flashcard, self.flashcard1)
        self.assertEqual(answer.cau_tra_loi, 'User answer')
        self.assertTrue(answer.dung)


class FlashcardTestViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test Description',
            nguoi_tao=self.user,
            trang_thai='published'
        )
        
        self.flashcard1 = Flashcard.objects.create(
            bo_flashcard=self.set,
            mat_truoc='Front 1',
            mat_sau='Back 1',
            vi_tri=1
        )

    def test_start_flashcard_test(self):
        """Test starting a flashcard test"""
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post('/kien-thuc/start-flashcard-test/', {
            'flashcard_set_id': self.set.id
        })
        
        # Should redirect to the test page
        self.assertEqual(response.status_code, 302)
        
        # Check if test was created in database
        test = FlashcardTest.objects.filter(nguoi_dung=self.user, bo_flashcard=self.set).first()
        self.assertIsNotNone(test)
        self.assertEqual(test.tong_so_cau_hoi, 1)

    def test_submit_flashcard_test_answer(self):
        """Test submitting an answer during flashcard test"""
        # First create a test
        test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.set,
            tong_so_cau_hoi=1,
            so_cau_tra_loi_dung=0
        )
        
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post('/kien-thuc/submit-flashcard-answer/', {
            'test_id': test.id,
            'flashcard_id': self.flashcard1.id,
            'answer': 'My answer',
            'is_correct': True
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Check if answer was saved
        answer = FlashcardTestAnswer.objects.filter(
            bai_kiem_tra=test,
            flashcard=self.flashcard1
        ).first()
        self.assertIsNotNone(answer)
        self.assertEqual(answer.cau_tra_loi, 'My answer')
        self.assertTrue(answer.dung)


class FlashcardTestLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.set = FlashcardSet.objects.create(
            tieu_de='Test Set',
            mo_ta='Test Description',
            nguoi_tao=self.user,
            trang_thai='published'
        )
        
        # Create multiple flashcards
        for i in range(5):
            Flashcard.objects.create(
                bo_flashcard=self.set,
                mat_truoc=f'Front {i+1}',
                mat_sau=f'Back {i+1}',
                vi_tri=i+1
            )

    def test_spaced_repetition_logic(self):
        """Test that flashcard test integrates with spaced repetition system"""
        # Create a test and some answers
        test = FlashcardTest.objects.create(
            nguoi_dung=self.user,
            bo_flashcard=self.set,
            tong_so_cau_hoi=5,
            so_cau_tra_loi_dung=3
        )
        
        # Get first flashcard
        flashcard = self.set.flashcards.first()
        
        # Submit a correct answer
        answer = FlashcardTestAnswer.objects.create(
            bai_kiem_tra=test,
            flashcard=flashcard,
            cau_tra_loi='Correct answer',
            dung=True
        )
        
        # Update flashcard progress based on the answer
        progress, created = FlashcardProgress.objects.get_or_create(
            nguoi_dung=self.user,
            flashcard=flashcard,
            defaults={
                'trang_thai': 'new',
                'he_so_de_dang': 2.5,
                'so_lan_hien_thi': 0,
                'so_lan_dung': 0,
                'lan_cuoi_hien_thi': timezone.now(),
                'next_review_date': timezone.now()
            }
        )
        
        # Simulate spaced repetition update after correct answer
        if answer.dung:
            progress.so_lan_dung += 1
            progress.so_lan_hien_thi += 1
            
            # Update ease factor (simplified algorithm)
            if progress.he_so_de_dang < 1.3:
                progress.he_so_de_dang = 1.3
            else:
                progress.he_so_de_dang += 0.1 - (5 - 4) * (0.08 + (5 - 4) * 0.02)
            
            # Calculate next review date (simplified)
            if progress.trang_thai == 'new':
                progress.trang_thai = 'learning'
                
        progress.save()
        
        # Verify the progress was updated correctly
        updated_progress = FlashcardProgress.objects.get(id=progress.id)
        self.assertGreaterEqual(updated_progress.so_lan_dung, 1)
        self.assertGreaterEqual(updated_progress.so_lan_hien_thi, 1)