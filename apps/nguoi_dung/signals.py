from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.de_thi.models import KetQua
from apps.nguoi_dung.models import Badge, UserBadge

@receiver(post_save, sender=KetQua)
def check_for_badges(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.nguoi_dung
    total_exams = KetQua.objects.filter(nguoi_dung=user).count()

    # Define badge logic
    badge_criteria = [
        {'name': 'Novice', 'tier': 'bronze', 'threshold': 1},
        {'name': 'Active Learner', 'tier': 'silver', 'threshold': 10},
        {'name': 'Master', 'tier': 'gold', 'threshold': 50},
    ]

    for criterion in badge_criteria:
        if total_exams >= criterion['threshold']:
            badge, _ = Badge.objects.get_or_create(
                name=criterion['name'],
                tier=criterion['tier'],
                defaults={'description': f'Complete {criterion["threshold"]} exams'}
            )
            UserBadge.objects.get_or_create(nguoi_dung=user, badge=badge)
