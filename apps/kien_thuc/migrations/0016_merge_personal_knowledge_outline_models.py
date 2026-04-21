# Generated migration file to merge personal knowledge outline models with existing models
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('kien_thuc', '0015_flashcardstudysession'),
    ]

    operations = [
        # Notebook model
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tên sổ ghi chú')),
                ('description', models.TextField(blank=True, verbose_name='Mô tả')),
                ('visibility', models.CharField(choices=[('private', 'Private')], default='private', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notebooks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sổ ghi chú cá nhân',
                'verbose_name_plural': 'Sổ ghi chú cá nhân',
                'ordering': ['-updated_at'],
            },
        ),
        
        # NoteSection model
        migrations.CreateModel(
            name='NoteSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tiêu đề mục')),
                ('content', models.TextField(help_text='Nội dung hỗ trợ Markdown và MathJax', verbose_name='Nội dung')),
                ('order', models.IntegerField(default=0, verbose_name='Thứ tự')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='kien_thuc.notebook')),
            ],
            options={
                'verbose_name': 'Phần ghi chú',
                'verbose_name_plural': 'Phần ghi chú',
                'ordering': ['order', '-updated_at'],
            },
        ),
        
        # NoteTag model
        migrations.CreateModel(
            name='NoteTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tên thẻ')),
                ('color', models.CharField(default='#007bff', max_length=7, verbose_name='Màu sắc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_tags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Thẻ ghi chú',
                'verbose_name_plural': 'Thẻ ghi chú',
            },
        ),
        
        # NotebookTag model
        migrations.CreateModel(
            name='NotebookTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notebook_tags', to='kien_thuc.notebook')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kien_thuc.notetag')),
            ],
            options={
                'unique_together': {('notebook', 'tag')},
            },
        ),
        
        # Add constraint for NoteTag
        migrations.AddConstraint(
            model_name='notetag',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_user_note_tag'),
        ),
    ]