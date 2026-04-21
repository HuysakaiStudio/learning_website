from django.urls import path
from . import views

app_name = 'kien_thuc'

urlpatterns = [
    path('', views.danh_sach_mon, name='danh_sach_mon'),
    path('<int:mon_id>/', views.bai_viet_theo_mon, name='bai_viet_theo_mon'),
    path('bai/<int:bai_id>/', views.chi_tiet_bai_viet, name='chi_tiet_bai_viet'),
    path('tao-bai/', views.tao_bai_viet, name='tao_bai_viet'),
    path('bai/<int:bai_id>/xoa/', views.xoa_bai_viet, name='xoa_bai_viet'),
    
    # Flashcard URLs
    path('flashcard/', views.danh_sach_flashcard_sets, name='danh_sach_flashcard_sets'),
    path('flashcard/<int:flashcard_set_id>/hoc/', views.hoc_flashcard, name='hoc_flashcard'),
    path('flashcard/<int:flashcard_set_id>/them/', views.them_flashcard, name='them_flashcard'),
    path('flashcard/reset/<int:set_id>/', views.reset_flashcard_progress, name='api_reset_flashcard'),
    path('flashcard/tao-bo/', views.tao_flashcard_set, name='tao_flashcard_set'),
    path('flashcard/dashboard/', views.flashcard_dashboard, name='flashcard_dashboard'),
    path('flashcard/<int:set_id>/export/<str:format>/', views.export_flashcards, name='export_flashcards'),
    path('flashcard/share/<uuid:uuid>/', views.share_flashcards, name='share_flashcards'),
    path('api/flashcard/progress/', views.api_flashcard_progress, name='api_flashcard_progress'),
    
    # Flashcard Test URLs
    path('flashcard/<int:flashcard_set_id>/test/', views.start_flashcard_test, name='start_flashcard_test'),
    path('api/flashcard/test/answer/', views.submit_flashcard_test_answer, name='submit_flashcard_test_answer'),
    path('flashcard/test/<int:test_id>/finish/', views.finish_flashcard_test, name='finish_flashcard_test'),
    path('api/flashcard/session/end/', views.end_flashcard_session, name='end_flashcard_session'),
    
    # Personal Knowledge Outline URLs
    path('notebooks/', views.notebook_dashboard, name='notebook_dashboard'),
    path('api/notebooks/', views.api_notebooks, name='api_notebooks'),
    path('api/notebooks/<int:notebook_id>/', views.api_notebook_detail, name='api_notebook_detail'),
    path('api/notebooks/<int:notebook_id>/sections/', views.api_notebook_sections, name='api_notebook_sections'),
    path('api/sections/<int:section_id>/', views.api_section_detail, name='api_section_detail'),
    path('api/note-tags/', views.api_note_tags, name='api_note_tags'),
    path('api/note-search/', views.api_note_search, name='api_note_search'),
    
    # Smart Notes API URLs
    path('api/notes/', views.api_notes, name='api_notes'),
    path('api/notes/<int:note_id>/', views.api_note_detail, name='api_note_detail'),
    path('api/notes/<str:note_type>/<int:obj_id>/', views.api_notes_context, name='api_notes_context'),
]