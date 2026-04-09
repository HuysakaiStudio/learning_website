from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.notifications.models import Notification, NotificationPreference
from apps.notifications.utils import *


class NotificationModelTest(TestCase):
    """Test Notification model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_notification_creation(self):
        """Test creating a notification"""
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        self.assertEqual(notif.recipient, self.user)
        self.assertEqual(notif.notification_type, 'system')
        self.assertFalse(notif.is_read)
    
    def test_mark_as_read(self):
        """Test marking notification as read"""
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        notif.mark_as_read()
        self.assertTrue(notif.is_read)
        self.assertIsNotNone(notif.read_at)
    
    def test_mark_as_unread(self):
        """Test marking notification as unread"""
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message',
            is_read=True
        )
        notif.mark_as_unread()
        self.assertFalse(notif.is_read)
        self.assertIsNone(notif.read_at)


class NotificationPreferenceTest(TestCase):
    """Test NotificationPreference model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_preference_creation(self):
        """Test creating notification preferences"""
        prefs = NotificationPreference.objects.create(user=self.user)
        self.assertEqual(prefs.user, self.user)
        self.assertTrue(prefs.enable_achievement)
        self.assertTrue(prefs.enable_system)
    
    def test_is_enabled(self):
        """Test checking if notification type is enabled"""
        prefs = NotificationPreference.objects.create(
            user=self.user,
            enable_achievement=False
        )
        self.assertFalse(prefs.is_enabled('achievement'))
        self.assertTrue(prefs.is_enabled('system'))


class NotificationUtilsTest(TestCase):
    """Test notification utility functions"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_notification(self):
        """Test create_notification function"""
        notif = create_notification(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        self.assertIsNotNone(notif)
        self.assertEqual(notif.recipient, self.user)
    
    def test_create_notification_disabled_type(self):
        """Test creating notification when type is disabled"""
        prefs = NotificationPreference.objects.create(
            user=self.user,
            enable_system=False
        )
        notif = create_notification(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        self.assertIsNone(notif)
    
    def test_notify_system(self):
        """Test notify_system function"""
        notif = notify_system(
            user=self.user,
            title='System Test',
            message='System message'
        )
        self.assertIsNotNone(notif)
        self.assertEqual(notif.notification_type, 'system')
    
    def test_notify_flashcard_milestone(self):
        """Test notify_flashcard_milestone function"""
        notif = notify_flashcard_milestone(self.user, 10)
        self.assertIsNotNone(notif)
        self.assertEqual(notif.notification_type, 'flashcard_milestone')
        self.assertIn('10', notif.message)
    
    def test_bulk_notify(self):
        """Test bulk_notify function"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        users = [self.user, user2]
        notifications = bulk_notify(
            users=users,
            notification_type='system',
            title='Bulk Test',
            message='Bulk message'
        )
        self.assertEqual(len(notifications), 2)


class NotificationViewTest(TestCase):
    """Test notification views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_notification_list_view(self):
        """Test notification list view"""
        response = self.client.get(reverse('notifications:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/list.html')
    
    def test_notification_preferences_view(self):
        """Test notification preferences view"""
        response = self.client.get(reverse('notifications:preferences'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/preferences.html')
    
    def test_mark_as_read_view(self):
        """Test mark as read view"""
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        response = self.client.post(
            reverse('notifications:mark_as_read', args=[notif.id])
        )
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)
    
    def test_delete_notification_view(self):
        """Test delete notification view"""
        notif = Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        response = self.client.post(
            reverse('notifications:delete', args=[notif.id])
        )
        notif.refresh_from_db()
        self.assertTrue(notif.is_archived)
    
    def test_api_unread_count(self):
        """Test unread count API"""
        Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test 1',
            message='Test message 1'
        )
        Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test 2',
            message='Test message 2'
        )
        response = self.client.get(reverse('notifications:api_unread_count'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 2)
    
    def test_api_recent_notifications(self):
        """Test recent notifications API"""
        Notification.objects.create(
            recipient=self.user,
            notification_type='system',
            title='Test',
            message='Test message'
        )
        response = self.client.get(reverse('notifications:api_recent'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['notifications']), 1)


class NotificationIntegrationTest(TestCase):
    """Test notification integration with other features"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_notification_count_after_creation(self):
        """Test notification count increases after creation"""
        initial_count = Notification.objects.filter(recipient=self.user).count()
        
        notify_system(self.user, 'Test', 'Test message')
        
        final_count = Notification.objects.filter(recipient=self.user).count()
        self.assertEqual(final_count, initial_count + 1)
    
    def test_unread_count_after_read(self):
        """Test unread count decreases after marking as read"""
        notif1 = notify_system(self.user, 'Test 1', 'Message 1')
        notif2 = notify_system(self.user, 'Test 2', 'Message 2')
        
        initial_unread = Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).count()
        self.assertEqual(initial_unread, 2)
        
        notif1.mark_as_read()
        
        final_unread = Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).count()
        self.assertEqual(final_unread, 1)
