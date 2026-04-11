from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kien_thuc', '0011_baiviet_view_count_flashcardset_lan_xem'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashcardTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('tong_so_cau_hoi', models.IntegerField()),
                ('so_cau_tra_loi_dung', models.IntegerField(default=0)),
                ('bo_flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kien_thuc.flashcardset')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FlashcardTestAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cau_tra_loi', models.TextField()),
                ('dung', models.BooleanField()),
                ('thoi_gian_tra_loi', models.DateTimeField(auto_now_add=True)),
                ('bai_kiem_tra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kien_thuc.flashcardtest')),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kien_thuc.flashcard')),
            ],
        ),
    ]