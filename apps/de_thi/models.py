from django.db import models
from django.contrib.auth.models import User

class DeThi(models.Model):
    ten = models.CharField(max_length=200)
    mon = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True)
    thoi_gian_phut = models.IntegerField(default=50)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    an = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Đề thi'
        verbose_name_plural = 'Đề thi'
        ordering = ['-ngay_tao']

    def __str__(self):
        return self.ten

    def tong_cau(self):
        return self.cau_hoi.count()


class CauHoi(models.Model):
    LOAI_CAU = [
        ('tn', 'Trắc nghiệm ABCD'),
        ('ds', 'Trắc nghiệm Đúng/Sai'),
        ('dien', 'Điền số'),
    ]

    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE, related_name='cau_hoi')
    loai = models.CharField(max_length=10, choices=LOAI_CAU, default='tn')
    noi_dung = models.TextField()
    giai_thich = models.TextField(blank=True)
    thu_tu = models.IntegerField(default=0)

    # Trắc nghiệm ABCD
    dap_an_a = models.CharField(max_length=500, blank=True)
    dap_an_b = models.CharField(max_length=500, blank=True)
    dap_an_c = models.CharField(max_length=500, blank=True)
    dap_an_d = models.CharField(max_length=500, blank=True)
    dap_an_dung = models.CharField(max_length=10, blank=True)  # 'A','B','C','D'

    # Đúng/Sai — 4 ý a,b,c,d mỗi ý là True/False
    y_a = models.CharField(max_length=500, blank=True)
    y_b = models.CharField(max_length=500, blank=True)
    y_c = models.CharField(max_length=500, blank=True)
    y_d = models.CharField(max_length=500, blank=True)
    dung_sai_a = models.BooleanField(default=False)
    dung_sai_b = models.BooleanField(default=False)
    dung_sai_c = models.BooleanField(default=False)
    dung_sai_d = models.BooleanField(default=False)

    # Điền số
    dap_an_so = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['thu_tu']

    def __str__(self):
        return f'[{self.get_loai_display()}] {self.noi_dung[:60]}'


class KetQua(models.Model):
    nguoi_dung = models.ForeignKey(User, on_delete=models.CASCADE)
    de_thi = models.ForeignKey(DeThi, on_delete=models.CASCADE)
    diem = models.FloatField(default=0)
    tong_cau = models.IntegerField(default=0)
    thoi_gian_lam = models.IntegerField(default=0)  # giây
    che_do = models.CharField(max_length=20, default='luyen_tap')  # luyen_tap / thi_that
    ngay_lam = models.DateTimeField(auto_now_add=True)
    da_xem_dap_an = models.BooleanField(default=False)

    class Meta:
        ordering = ['-ngay_lam']

    def __str__(self):
        return f'{self.nguoi_dung.username} — {self.de_thi.ten} — {self.diem}'


class TraLoi(models.Model):
    ket_qua = models.ForeignKey(KetQua, on_delete=models.CASCADE, related_name='tra_loi')
    cau_hoi = models.ForeignKey(CauHoi, on_delete=models.CASCADE)

    # Trắc nghiệm
    chon = models.CharField(max_length=10, blank=True)

    # Đúng/Sai
    chon_a = models.BooleanField(null=True, blank=True)
    chon_b = models.BooleanField(null=True, blank=True)
    chon_c = models.BooleanField(null=True, blank=True)
    chon_d = models.BooleanField(null=True, blank=True)

    # Điền số
    so_dien = models.CharField(max_length=100, blank=True)

    dung = models.BooleanField(default=False)
    diem_duoc = models.FloatField(default=0)