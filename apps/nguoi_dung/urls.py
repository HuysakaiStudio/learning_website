from django.urls import path
from . import views, api_views

app_name = 'nguoi_dung'

urlpatterns = [
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/', views.profile, name='user_profile'),
    
    # Gamification API endpoints
    path('api/gamification/stats/', api_views.get_gamification_stats, name='api_gamification_stats'),
    path('api/gamification/add-xp/', api_views.add_xp, name='api_add_xp'),
    path('api/gamification/update-streak/', api_views.update_streak, name='api_update_streak'),
    path('api/gamification/sync/', api_views.sync_from_localstorage, name='api_sync_gamification'),
]