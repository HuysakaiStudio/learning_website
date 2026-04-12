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
    result = gamification.add_xp_with_overflow_handling(amount, reason)
    
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


def get_practice_xp_reward(score):
    """Calculate XP reward for practice mode (50% of normal XP)"""
    base_xp, reason = get_exam_xp_reward(score)
    practice_xp = max(1, int(base_xp * 0.5))  # Minimum 1 XP, 50% of base XP
    return practice_xp, f"Luyện tập - {reason}"


def calculate_xp_for_level(level):
    """Calculate total XP needed to reach a specific level"""
    import math
    if level <= 0:
        return 0
    # More consistent formula: XP = (level^2) * 100
    return int(level * level * 100)


def get_level_from_xp(xp):
    """Get level from XP (inverse of calculate_xp_for_level)"""
    import math
    if xp <= 0:
        return 0
    # Inverse of XP = level^2 * 100 -> level = sqrt(XP / 100)
    return int(math.sqrt(max(0, xp / 100)))


def get_xp_progress_in_level(xp, level=None):
    """Get progress information for the current level"""
    import math
    
    if level is None:
        level = get_level_from_xp(xp)
    
    level_start_xp = calculate_xp_for_level(level)
    next_level_start_xp = calculate_xp_for_level(level + 1)
    
    xp_in_current_level = xp - level_start_xp
    xp_needed_for_next_level = next_level_start_xp - level_start_xp
    
    # Ensure xp_in_current_level doesn't go negative
    xp_in_current_level = max(0, xp_in_current_level)
    
    return {
        'level_start_xp': int(level_start_xp),
        'next_level_start_xp': int(next_level_start_xp),
        'xp_in_current_level': int(xp_in_current_level),
        'xp_needed_for_next_level': int(xp_needed_for_next_level),
        'progress_percentage': min(100, (xp_in_current_level / xp_needed_for_next_level) * 100) if xp_needed_for_next_level > 0 else 0,
        'xp_remaining': int(xp_needed_for_next_level - xp_in_current_level) if xp_needed_for_next_level > 0 else 0
    }


def validate_xp_system_consistency():
    """Validate that the XP calculation formulas are consistent"""
    import math
    
    # Test a few levels to ensure consistency between XP -> Level and Level -> XP functions
    test_levels = [0, 1, 5, 10, 25, 50, 100]
    results = []
    
    for level in test_levels:
        xp_needed = calculate_xp_for_level(level)
        calculated_level = get_level_from_xp(xp_needed)
        results.append({
            'target_level': level,
            'xp_needed': xp_needed,
            'calculated_level': calculated_level,
            'consistent': level == calculated_level
        })
    
    return results
