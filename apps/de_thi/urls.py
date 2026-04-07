from django.urls import path
from . import views

app_name = 'de_thi'

urlpatterns = [
    path('', views.danh_sach_de, name='danh_sach_de'),
    path('tao/', views.tao_de_thi, name='tao_de_thi'),
    path('import/', views.import_de_thi, name='import_de_thi'),
    path('<int:de_id>/sua/', views.sua_de_thi, name='sua_de_thi'),
    path('<int:de_id>/them-cau-hoi/', views.them_cau_hoi, name='them_cau_hoi'),
    path('<int:de_id>/them-cau-hoi-hang-loat/', views.bulk_add_questions, name='bulk_add_questions'),
    path('<int:de_id>/xoa/', views.xoa_de_thi, name='xoa_de_thi'),
    path('<int:de_id>/', views.chon_che_do, name='chon_che_do'),
    path('<int:de_id>/lam/', views.lam_bai, name='lam_bai'),
    path('cau-hoi/<int:cau_id>/sua/', views.sua_cau_hoi, name='sua_cau_hoi'),
    path('cau-hoi/<int:cau_id>/xoa/', views.xoa_cau_hoi, name='xoa_cau_hoi'),
    path('ket-qua/<int:kq_id>/', views.ket_qua, name='ket_qua'),
    path('ket-qua/<int:kq_id>/dap-an/', views.xem_dap_an, name='xem_dap_an'),
]