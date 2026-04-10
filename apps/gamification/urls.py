from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('challenges/', views.daily_challenges, name='daily_challenges'),
]
