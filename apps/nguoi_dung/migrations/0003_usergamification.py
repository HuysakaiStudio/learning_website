# Generated manually for UserGamification model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nguoi_dung', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGamification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xp', models.IntegerField(default=0, help_text='Total experience points')),
                ('level', models.IntegerField(default=0, help_text='Current level (calculated from XP)')),
                ('current_streak', models.IntegerField(default=0, help_text='Current consecutive study days')),
                ('longest_streak', models.IntegerField(default=0, help_text='Longest streak ever achieved')),
                ('last_activity_date', models.DateField(blank=True, help_text='Last day user was active', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gamification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Gamification',
                'verbose_name_plural': 'User Gamifications',
            },
        ),
        migrations.AddIndex(
            model_name='usergamification',
            index=models.Index(fields=['xp'], name='nguoi_dung_xp_idx'),
        ),
        migrations.AddIndex(
            model_name='usergamification',
            index=models.Index(fields=['level'], name='nguoi_dung_level_idx'),
        ),
        migrations.AddIndex(
            model_name='usergamification',
            index=models.Index(fields=['current_streak'], name='nguoi_dung_streak_idx'),
        ),
    ]
