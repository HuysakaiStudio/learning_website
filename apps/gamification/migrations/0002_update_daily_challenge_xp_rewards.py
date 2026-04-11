from django.db import migrations, models
from django.db import models as django_models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailychallenge',
            name='xp_reward',
            field=models.IntegerField(default=50, help_text='XP reward for completing the challenge'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailychallenge',
            name='challenge_type',
            field=models.CharField(choices=[('flashcard_streak', 'Flashcard Streak'), ('flashcards_today', 'Flashcards Today'), ('exams_today', 'Exams Today'), ('correct_answers_rate', 'Correct Answers Rate')], default='flashcards_today', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailychallenge',
            name='target_value',
            field=models.IntegerField(default=5, help_text='Target value to achieve for challenge completion'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserChallengeProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('current_progress', models.IntegerField(default=0)),
                ('xp_awarded', models.IntegerField(default=0)),
                ('challenge', models.ForeignKey(on_delete=models.CASCADE, to='gamification.dailychallenge')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to='auth.user')),
            ],
        ),
    ]