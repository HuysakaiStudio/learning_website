"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from django.views.static import serve
from apps.kien_thuc import views_search as kien_thuc_search
from apps.home_views import home_view
import os
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('nguoi-dung/', include('apps.nguoi_dung.urls')),
    path('kien-thuc/', include('apps.kien_thuc.urls')),
    path('de-thi/', include('apps.de_thi.urls')),
    path('leaderboard/', include('apps.leaderboard.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('gamification/', include('apps.gamification.urls')),
    path('search/', include([
        path('', kien_thuc_search.global_search_results, name='global_search'),
        path('api/suggestions/', kien_thuc_search.api_search_suggestions, name='api_search_suggestions'),
    ])),
    path('studio/', include('apps.studio.urls', namespace='studio')),

    # PWA files - serve from root
    path('sw.js', lambda r: serve(r, 'sw.js', document_root=os.path.join(settings.BASE_DIR, 'static'))),
    path('manifest.json', lambda r: serve(r, 'manifest.json', document_root=os.path.join(settings.BASE_DIR, 'static'))),
    path('offline.html', TemplateView.as_view(template_name='offline.html'), name='offline'),

    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: HttpResponseNotFound()),
]
