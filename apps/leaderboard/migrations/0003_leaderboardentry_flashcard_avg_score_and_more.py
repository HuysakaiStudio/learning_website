from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0002_achievement_leaderboard_user_id_a93277_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboardentry',
            name='flashcard_avg_score',
            field=models.FloatField(default=0.0, help_text='Average score for flashcard learning'),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='flashcard_total_cards',
            field=models.IntegerField(default=0, help_text='Total number of flashcards studied'),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='last_flashcard_study',
            field=models.DateTimeField(blank=True, help_text='Last time user studied flashcards', null=True),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='weekly_flashcard_count',
            field=models.IntegerField(default=0, help_text='Number of flashcards studied this week'),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='flashcard_streak',
            field=models.IntegerField(default=0, help_text='Current flashcard study streak'),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='total_score',
            field=models.FloatField(db_index=True, help_text='Total accumulated score', default=0),
        ),
    ]