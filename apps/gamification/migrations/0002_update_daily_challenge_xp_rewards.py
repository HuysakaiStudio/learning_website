# This migration has been corrected to avoid conflicts with the initial migration
# The original had an issue where it was trying to create UserChallengeProgress again

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamification', '0001_initial'),
    ]

    operations = [
        # Update the DailyChallenge model fields
        migrations.AddField(
            model_name='dailychallenge',
            name='xp_reward',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='dailychallenge',
            name='challenge_type',
            field=models.CharField(
                choices=[
                    ('exam', 'Complete an exam'), 
                    ('flashcard', 'Study flashcards'), 
                    ('streak', 'Maintain login streak'), 
                    ('score', 'Achieve minimum score'), 
                    ('questions', 'Answer questions correctly')
                ], 
                max_length=20,
                default='flashcard'
            ),
        ),
        migrations.AddField(
            model_name='dailychallenge',
            name='target_value',
            field=models.IntegerField(default=5, help_text='Target to achieve for challenge completion'),
        ),
    ]