"""
Management command to send periodic leaderboard notifications
Run this via cron job:
- Daily: 0 0 * * * (midnight)
- Weekly: 0 0 * * 0 (Sunday midnight)
- Monthly: 0 0 1 * * (1st of month)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.leaderboard.models import Leaderboard, LeaderboardEntry, Achievement
from apps.notifications.utils import notify_new_achievement, notify_leaderboard_rank


class Command(BaseCommand):
    help = 'Send leaderboard notifications for completed periods'

    def add_arguments(self, parser):
        parser.add_argument(
            '--period',
            type=str,
            choices=['daily', 'weekly', 'monthly'],
            help='Period to process (daily, weekly, or monthly)',
        )

    def handle(self, *args, **options):
        period = options.get('period')
        
        if not period:
            self.stdout.write(self.style.ERROR('Please specify --period (daily, weekly, or monthly)'))
            return
        
        self.stdout.write(f'Processing {period} leaderboard notifications...')
        
        # Get leaderboards for this period
        leaderboards = Leaderboard.objects.filter(period=period)
        
        for leaderboard in leaderboards:
            self.process_leaderboard(leaderboard, period)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {period} notifications'))

    def process_leaderboard(self, leaderboard, period):
        """Process a single leaderboard and send notifications"""
        # Get top entries
        entries = LeaderboardEntry.objects.filter(
            leaderboard=leaderboard
        ).order_by('-score', 'updated_at')[:10]
        
        if not entries:
            return
        
        # Determine achievement type
        achievement_map = {
            'daily': 'top_10_daily',
            'weekly': 'top_10_weekly',
            'monthly': 'top_10_monthly'
        }
        achievement_type = achievement_map.get(period)
        
        # Get time threshold for checking existing achievements
        time_threshold = {
            'daily': timezone.now() - timedelta(days=1),
            'weekly': timezone.now() - timedelta(days=7),
            'monthly': timezone.now() - timedelta(days=30)
        }
        threshold = time_threshold.get(period)
        
        for entry in entries:
            # Check if already notified for this period
            existing = Achievement.objects.filter(
                user=entry.user,
                achievement_type=achievement_type,
                earned_at__gte=threshold
            ).exists()
            
            if not existing:
                # Create achievement
                achievement = Achievement.objects.create(
                    user=entry.user,
                    achievement_type=achievement_type,
                    rank_achieved=entry.rank,
                    score_achieved=entry.score,
                    mon=leaderboard.mon
                )
                
                # Send achievement notification
                notify_new_achievement(entry.user, achievement)
                self.stdout.write(f'  ✓ Achievement for {entry.user.username} (Rank {entry.rank})')
            
            # Send leaderboard rank notification
            notify_leaderboard_rank(entry.user, entry.rank, period, leaderboard.category)
            self.stdout.write(f'  ✓ Rank notification for {entry.user.username} (Rank {entry.rank})')
