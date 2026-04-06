from django.urls import path
from . import views

app_name = 'kien_thuc'

urlpatterns = [
    path('', views.danh_sach_mon, name='danh_sach_mon'),
    path('<int:mon_id>/', views.bai_viet_theo_mon, name='bai_viet_theo_mon'),
    path('bai/<int:bai_id>/', views.chi_tiet_bai_viet, name='chi_tiet_bai_viet'),
    path('tao-bai/', views.tao_bai_viet, name='tao_bai_viet'),
    path('bai/<int:bai_id>/xoa/', views.xoa_bai_viet, name='xoa_bai_viet'),
]