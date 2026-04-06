from django.db import models

class Mon(models.Model):
    ten = models.CharField(max_length=100)
    mo_ta = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📚')

    class Meta:
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'

    def __str__(self):
        return self.ten


class BaiViet(models.Model):
    mon = models.ForeignKey(Mon, on_delete=models.CASCADE, related_name='bai_viet')
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(auto_now_add=True)
    thu_tu = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering = ['thu_tu', 'ngay_tao']

    def __str__(self):
        return f'{self.mon.ten} — {self.tieu_de}'