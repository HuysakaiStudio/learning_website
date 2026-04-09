from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Main views
    path('', views.notification_list, name='list'),
    path('preferences/', views.notification_preferences, name='preferences'),
    
    # Actions
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('<int:notification_id>/unread/', views.mark_as_unread, name='mark_as_unread'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_as_read'),
    
    # API endpoints
    path('api/unread-count/', views.get_unread_count, name='api_unread_count'),
    path('api/recent/', views.get_recent_notifications, name='api_recent'),
]
