"""Custom template tags for Studio app"""
from django import template
from apps.kien_thuc.models import BaiViet, FlashcardSet

register = template.Library()


@register.simple_tag
def get_pending_count():
    """Get total count of pending items for moderation."""
    pending_articles = BaiViet.objects.filter(status='pending').count()
    pending_flashcards = FlashcardSet.objects.filter(status='pending').count()
    return pending_articles + pending_flashcards
