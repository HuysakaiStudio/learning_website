from django.urls import path
from . import views

app_name = 'de_thi'

urlpatterns = [
    path('', views.danh_sach_de, name='danh_sach_de'),
    path('<int:de_id>/', views.chon_che_do, name='chon_che_do'),
    path('<int:de_id>/lam/', views.lam_bai, name='lam_bai'),
    path('ket-qua/<int:kq_id>/', views.ket_qua, name='ket_qua'),
    path('ket-qua/<int:kq_id>/dap-an/', views.xem_dap_an, name='xem_dap_an'),
]