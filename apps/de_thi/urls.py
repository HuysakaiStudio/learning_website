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
    path('lich-su/', views.lich_su_lam_bai, name='lich_su_lam_bai'),
    path('ket-qua/<int:kq_id>/', views.ket_qua, name='ket_qua'),
    path('ket-qua/<int:kq_id>/dap-an/', views.xem_dap_an, name='xem_dap_an'),
    
    # Analytics URLs
    path('phan-tich/', views.phan_tich_hoc_tap, name='phan_tich_hoc_tap'),
    path('api/analytics/', views.api_analytics_data, name='api_analytics_data'),
    path('mon/<int:mon_id>/chi-tiet/', views.chi_tiet_mon_hoc, name='chi_tiet_mon_hoc'),
    
    # Forum URLs
    path('cau-hoi/<int:cau_id>/forum/', views.danh_sach_forum, name='danh_sach_forum'),
    path('cau-hoi/<int:cau_id>/forum/tao/', views.tao_post_forum, name='tao_post_forum'),
    path('forum/<int:post_id>/', views.chi_tiet_forum, name='chi_tiet_forum'),
    path('forum/<int:post_id>/binh-luan/', views.them_binh_luan, name='them_binh_luan'),
    path('forum/binh-luan/<int:comment_id>/tra-loi/', views.them_tra_loi, name='them_tra_loi'),
    path('forum/binh-luan/<int:comment_id>/chon-tot/', views.chon_cau_tra_loi_tot, name='chon_cau_tra_loi_tot'),
    path('api/forum/binh-chon/', views.binh_chon, name='api_binh_chon'),
]