from django.urls import path
from . import views

app_name = 'studio'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('content/', views.content_list, name='content_list'),
    path('article/<int:bai_id>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:bai_id>/delete/', views.delete_article, name='delete_article'),
    path('flashcard/<int:set_id>/edit/', views.edit_flashcard_set, name='edit_flashcard_set'),
    path('flashcard/<int:set_id>/delete/', views.delete_flashcard_set, name='delete_flashcard_set'),
    path('flashcard/<int:pk>/submit-review/', views.submit_flashcard_for_review, name='submit_flashcard_review'),
    
    # Moderation (Staff Only)
    path('moderation/', views.moderation_list, name='moderation_list'),
    path('moderation/action/', views.moderation_action, name='moderation_action'),
]
