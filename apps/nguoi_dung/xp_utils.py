"""
Utility functions for awarding XP
"""
from apps.nguoi_dung.models import UserGamification


def award_xp(user, amount, reason=''):
    """
    Award XP to user and return result
    
    Args:
        user: User object
        amount: XP amount to award
        reason: Reason for awarding XP
        
    Returns:
        dict with xp_gained, total_xp, old_level, new_level, leveled_up
    """
    if not user or not user.is_authenticated:
        return None
    
    gamification, created = UserGamification.objects.get_or_create(user=user)
    result = gamification.add_xp(amount, reason)
    
    # Update streak when user is active
    gamification.update_streak()
    
    return result


# XP Rewards Configuration
XP_REWARDS = {
    # Exam completion
    'exam_completed': 10,
    'exam_perfect_score': 50,  # Score = 10
    'exam_high_score': 30,     # Score >= 8
    'exam_pass': 15,           # Score >= 5
    
    # Flashcard learning
    'flashcard_learned': 2,
    'flashcard_set_completed': 20,
    'flashcard_review': 1,
    
    # Daily activities
    'daily_login': 5,
    'study_streak_3': 10,
    'study_streak_7': 30,
    'study_streak_30': 200,
    'study_streak_100': 1000,
    
    # Forum activities
    'forum_post_created': 5,
    'forum_comment': 3,
    'forum_helpful_answer': 10,
    
    # Content creation
    'article_published': 25,
    'flashcard_set_created': 15,
}


def get_exam_xp_reward(score):
    """Calculate XP reward based on exam score"""
    if score >= 10:
        return XP_REWARDS['exam_perfect_score'], 'Điểm 10 hoàn hảo!'
    elif score >= 8:
        return XP_REWARDS['exam_high_score'], 'Điểm cao xuất sắc!'
    elif score >= 5:
        return XP_REWARDS['exam_pass'], 'Hoàn thành bài thi'
    else:
        return XP_REWARDS['exam_completed'], 'Hoàn thành bài thi'
