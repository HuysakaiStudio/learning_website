from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.gamification.models import DailyChallenge
import random


class Command(BaseCommand):
    help = 'Generate daily challenges for today'

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Check if challenges already exist for today
        if DailyChallenge.objects.filter(date=today).exists():
            self.stdout.write(self.style.WARNING('Challenges already exist for today'))
            return

        # Challenge templates
        challenge_templates = [
            {
                'title': 'Hoàn thành 1 đề thi',
                'description': 'Làm và nộp bài một đề thi bất kỳ',
                'challenge_type': 'exam',
                'target_value': 1,
                'xp_reward': 100,
            },
            {
                'title': 'Học 20 flashcards',
                'description': 'Ôn tập ít nhất 20 thẻ flashcard',
                'challenge_type': 'flashcard',
                'target_value': 20,
                'xp_reward': 50,
            },
            {
                'title': 'Đạt điểm 8.0+',
                'description': 'Hoàn thành một bài thi với điểm từ 8.0 trở lên',
                'challenge_type': 'score',
                'target_value': 80,
                'xp_reward': 150,
            },
            {
                'title': 'Trả lời đúng 30 câu',
                'description': 'Trả lời đúng tổng cộng 30 câu hỏi trong ngày',
                'challenge_type': 'questions',
                'target_value': 30,
                'xp_reward': 75,
            },
            {
                'title': 'Duy trì streak',
                'description': 'Đăng nhập liên tiếp để duy trì chuỗi ngày học',
                'challenge_type': 'streak',
                'target_value': 1,
                'xp_reward': 25,
            },
        ]

        # Select 3 random challenges for today
        selected = random.sample(challenge_templates, 3)

        for template in selected:
            DailyChallenge.objects.create(
                date=today,
                **template
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(selected)} challenges for {today}'))
