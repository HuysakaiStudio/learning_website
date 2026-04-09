from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Notification, NotificationPreference


@login_required
def notification_list(request):
    """Danh sách thông báo của user"""
    # Lấy filter từ query params
    filter_type = request.GET.get('type', 'all')
    
    # Base queryset
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_archived=False
    )
    
    # Apply filters
    if filter_type == 'unread':
        notifications = notifications.filter(is_read=False)
    elif filter_type == 'read':
        notifications = notifications.filter(is_read=True)
    elif filter_type != 'all':
        notifications = notifications.filter(notification_type=filter_type)
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Count unread
    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_archived=False
    ).count()
    
    context = {
        'notifications': page_obj,
        'filter_type': filter_type,
        'unread_count': unread_count,
        'page_obj': page_obj,
    }
    
    return render(request, 'notifications/list.html', context)


@login_required
@require_POST
def mark_as_read(request, notification_id):
    """Đánh dấu thông báo đã đọc"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')


@login_required
@require_POST
def mark_as_unread(request, notification_id):
    """Đánh dấu thông báo chưa đọc"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.mark_as_unread()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')


@login_required
@require_POST
def mark_all_as_read(request):
    """Đánh dấu tất cả thông báo đã đọc"""
    from django.utils import timezone
    
    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_archived=False
    ).update(is_read=True, read_at=timezone.now())
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')


@login_required
@require_POST
def delete_notification(request, notification_id):
    """Xóa thông báo (archive)"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    notification.is_archived = True
    notification.save(update_fields=['is_archived'])
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')


@login_required
def get_unread_count(request):
    """API endpoint để lấy số thông báo chưa đọc"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        is_archived=False
    ).count()
    
    return JsonResponse({'count': count})


@login_required
def get_recent_notifications(request):
    """API endpoint để lấy thông báo gần đây (cho dropdown)"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_archived=False
    )[:10]
    
    data = [{
        'id': n.id,
        'type': n.notification_type,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'action_url': n.action_url,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]
    
    return JsonResponse({'notifications': data})


@login_required
def notification_preferences(request):
    """Cài đặt thông báo"""
    # Get or create preferences
    prefs, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        # Update preferences
        prefs.enable_badge = request.POST.get('enable_badge') == 'on'
        prefs.enable_forum_reply = request.POST.get('enable_forum_reply') == 'on'
        prefs.enable_leaderboard = request.POST.get('enable_leaderboard') == 'on'
        prefs.enable_achievement = request.POST.get('enable_achievement') == 'on'
        prefs.enable_study_reminder = request.POST.get('enable_study_reminder') == 'on'
        prefs.enable_exam_result = request.POST.get('enable_exam_result') == 'on'
        prefs.enable_flashcard_milestone = request.POST.get('enable_flashcard_milestone') == 'on'
        prefs.enable_system = request.POST.get('enable_system') == 'on'
        prefs.email_notifications = request.POST.get('email_notifications') == 'on'
        prefs.email_frequency = request.POST.get('email_frequency', 'never')
        prefs.save()
        
        return redirect('notifications:preferences')
    
    context = {
        'prefs': prefs,
    }
    
    return render(request, 'notifications/preferences.html', context)
