# Generated migration for adding draft status to FlashcardSet

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kien_thuc', '0009_alter_baiviet_status_alter_flashcardset_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcardset',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'Nháp'),
                    ('pending', 'Đang chờ duyệt'),
                    ('published', 'Đã xuất bản'),
                    ('rejected', 'Bị từ chối')
                ],
                default='pending',
                max_length=20
            ),
        ),
    ]
