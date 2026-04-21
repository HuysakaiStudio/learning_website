from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from apps.kien_thuc.models import Mon, BaiViet, FlashcardSet, Flashcard
from apps.kien_thuc.forms import FlashcardForm
from django.db.models import Count
from apps.notifications.utils import create_notification
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    """Tổng quan Studio."""
    articles_count = BaiViet.objects.filter(nguoi_dang=request.user).count()
    # Chỉ đếm bộ flashcard có ít nhất 1 thẻ
    flashcards_count = FlashcardSet.objects.filter(creator=request.user, so_luong_the__gt=0).count()
    
    # Hiệu suất
    recent_articles = BaiViet.objects.filter(nguoi_dang=request.user).order_by('-ngay_tao')[:5]
    
    context = {
        'articles_count': articles_count,
        'flashcards_count': flashcards_count,
        'recent_articles': recent_articles,
    }
    return render(request, 'studio/dashboard.html', context)

@login_required
def content_list(request):
    """Quản lý nội dung."""
    tab = request.GET.get('tab', 'articles')
    
    if tab == 'articles':
        items = BaiViet.objects.filter(nguoi_dang=request.user).order_by('-ngay_tao')
    else:
        items = FlashcardSet.objects.filter(creator=request.user).order_by('-ngay_tao')
        
    context = {
        'tab': tab,
        'items': items,
    }
    return render(request, 'studio/content.html', context)

@login_required
def edit_article(request, bai_id):
    bai_viet = get_object_or_404(BaiViet, id=bai_id, nguoi_dang=request.user)
    
    if request.method == 'POST':
        mon_id = request.POST.get('mon')
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        
        mon = get_object_or_404(Mon, id=mon_id)
        
        bai_viet.mon = mon
        bai_viet.tieu_de = tieu_de
        bai_viet.noi_dung = noi_dung
        # Skip thu_tu update since field is removed
        
        # Re-moderation: Reset to pending if published content is edited by non-staff
        if bai_viet.status == 'rejected':
            bai_viet.status = 'pending'
        elif bai_viet.status == 'published' and not request.user.is_staff:
            bai_viet.status = 'pending'
            messages.info(request, 'Bài viết đã được gửi lại để kiểm duyệt.')
        
        bai_viet.save()
        
        messages.success(request, 'Đã cập nhật bài viết.')
        return redirect('studio:content_list')
    
    mon_list = Mon.objects.all()
    return render(request, 'studio/edit_article.html', {'bai_viet': bai_viet, 'mon_list': mon_list})

@login_required
def delete_article(request, bai_id):
    bai_viet = get_object_or_404(BaiViet, id=bai_id, nguoi_dang=request.user)
    if request.method == 'POST':
        bai_viet.delete()
        messages.success(request, 'Đã xóa bài viết vĩnh viễn.')
        return redirect('studio:content_list')
    return render(request, 'studio/confirm_delete.html', {'item_title': bai_viet.tieu_de})

@login_required
def edit_flashcard_set(request, set_id):
    fs = get_object_or_404(FlashcardSet, id=set_id, creator=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Xóa thẻ
        if action == 'delete_card':
            card_id = request.POST.get('card_id')
            Flashcard.objects.filter(id=card_id, flashcard_set=fs).delete()
            fs.cap_nhat_so_luong()
            messages.success(request, 'Đã xóa thẻ!')
            return redirect('studio:edit_flashcard_set', set_id=set_id)
        
        # Thêm thẻ mới
        elif action == 'add_card':
            mat_truoc = request.POST.get('mat_truoc', '').strip()
            mat_sau = request.POST.get('mat_sau', '').strip()
            
            if mat_truoc and mat_sau:
                Flashcard.objects.create(
                    flashcard_set=fs,
                    mat_truoc=mat_truoc,
                    mat_sau=mat_sau
                )
                fs.cap_nhat_so_luong()
                messages.success(request, 'Đã thêm thẻ mới!')
            else:
                messages.error(request, 'Vui lòng điền đầy đủ mặt trước và mặt sau!')
            return redirect('studio:edit_flashcard_set', set_id=set_id)
        
        # Sửa thẻ
        elif action == 'edit_card':
            card_id = request.POST.get('card_id')
            mat_truoc = request.POST.get('mat_truoc', '').strip()
            mat_sau = request.POST.get('mat_sau', '').strip()
            
            if mat_truoc and mat_sau:
                card = Flashcard.objects.filter(id=card_id, flashcard_set=fs).first()
                if card:
                    card.mat_truoc = mat_truoc
                    card.mat_sau = mat_sau
                    card.save()
                    messages.success(request, 'Đã cập nhật thẻ!')
            else:
                messages.error(request, 'Vui lòng điền đầy đủ mặt trước và mặt sau!')
            return redirect('studio:edit_flashcard_set', set_id=set_id)
        
        # Cập nhật thông tin bộ flashcard
        else:
            mon_id = request.POST.get('mon')
            tieu_de = request.POST.get('tieu_de')
            mo_ta = request.POST.get('mo_ta')
            
            mon = get_object_or_404(Mon, id=mon_id)
            
            fs.mon = mon
            fs.tieu_de = tieu_de
            fs.mo_ta = mo_ta
            
            # Re-moderation: Reset to pending if published content is edited by non-staff
            # Keep draft/rejected status until user explicitly submits for review
            if fs.status == 'published' and not request.user.is_staff:
                fs.status = 'pending'
                messages.info(request, 'Bộ flashcard đã được gửi lại để kiểm duyệt.')
                
            fs.save()
            
            messages.success(request, 'Đã cập nhật bộ Flashcard.')
            return redirect('studio:content_list')
        
    mon_list = Mon.objects.all()
    flashcards = fs.flashcards.all().order_by('thu_tu', 'id')
    form = FlashcardForm()
    
    return render(request, 'studio/edit_flashcard_set.html', {
        'flashcard_set': fs,
        'mon_list': mon_list,
        'flashcards': flashcards,
        'form': form
    })

@login_required
def delete_flashcard_set(request, set_id):
    fs = get_object_or_404(FlashcardSet, id=set_id, creator=request.user)
    if request.method == 'POST':
        fs.delete()
        messages.success(request, 'Đã xóa bộ Flashcard vĩnh viễn.')
        return redirect('studio:content_list')
    return render(request, 'studio/confirm_delete.html', {'item_title': fs.tieu_de})

@login_required
def submit_flashcard_for_review(request, pk):
    """Submit flashcard set for moderation review."""
    flashcard_set = get_object_or_404(FlashcardSet, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        # Validate: Must have at least 1 card
        if flashcard_set.flashcards.count() == 0:
            messages.error(request, 'Bạn phải thêm ít nhất 1 thẻ trước khi gửi kiểm duyệt.')
            return redirect('studio:edit_flashcard_set', set_id=pk)
        
        # Validate: Cannot submit if already published
        if flashcard_set.status == 'published':
            messages.warning(request, 'Bộ flashcard này đã được xuất bản.')
            return redirect('studio:content_list')
        
        # Change status to pending
        flashcard_set.status = 'pending'
        flashcard_set.save()
        
        messages.success(request, 'Bộ flashcard đã được gửi để kiểm duyệt.')
        return redirect('studio:content_list')
    
    return redirect('studio:edit_flashcard_set', set_id=pk)

def staff_check(user):
    """Check if user is admin (superuser or staff with moderation permission)."""
    return user.is_superuser or (user.is_staff and user.has_perm('kien_thuc.can_moderate'))

@user_passes_test(staff_check)
def moderation_list(request):
    """Admin only moderation queue."""
    pending_articles = BaiViet.objects.filter(status='pending').order_by('ngay_tao')
    pending_flashcards = FlashcardSet.objects.filter(status='pending').order_by('ngay_tao')
    
    context = {
        'pending_articles': pending_articles,
        'pending_flashcards': pending_flashcards,
        'total_pending': pending_articles.count() + pending_flashcards.count()
    }
    return render(request, 'studio/moderation_list.html', context)

@user_passes_test(staff_check)
def moderation_action(request):
    """Handle approve/reject actions with validation and notifications."""
    if request.method == 'POST':
        item_type = request.POST.get('type', '').strip()
        item_id = request.POST.get('id', '').strip()
        action = request.POST.get('action', '').strip()
        note = request.POST.get('note', '').strip()
        
        # Validation: item_type
        if item_type not in ['article', 'flashcard']:
            messages.error(request, 'Loại nội dung không hợp lệ.')
            return redirect('studio:moderation_list')
        
        # Validation: action
        if action not in ['approve', 'reject']:
            messages.error(request, 'Hành động không hợp lệ.')
            return redirect('studio:moderation_list')
        
        # Validation: item_id
        try:
            item_id = int(item_id)
        except (ValueError, TypeError):
            messages.error(request, 'ID không hợp lệ.')
            return redirect('studio:moderation_list')
        
        # Get item
        if item_type == 'article':
            item = get_object_or_404(BaiViet, id=item_id)
            creator = item.nguoi_dang
            item_title = item.tieu_de
            item_url = f'/kien-thuc/bai-viet/{item.id}/'
        else:
            item = get_object_or_404(FlashcardSet, id=item_id)
            creator = item.creator
            item_title = item.tieu_de
            item_url = f'/kien-thuc/hoc-flashcard/{item.id}/'
        
        # Check if already moderated
        if item.status != 'pending':
            messages.warning(request, 'Nội dung này đã được kiểm duyệt trước đó.')
            return redirect('studio:moderation_list')
        
        # Update status
        status = 'published' if action == 'approve' else 'rejected'
        item.status = status
        item.moderation_note = note
        item.moderated_by = request.user
        item.moderated_at = timezone.now()
        item.save()
        
        # Audit logging
        logger.info(f"Admin {request.user.username} {action} {item_type} #{item_id}")
        
        # Send notification to creator
        if creator:
            if action == 'approve':
                create_notification(
                    recipient=creator,
                    notification_type='content_approved',
                    title='✅ Nội dung đã được duyệt',
                    message=f'Nội dung "{item_title}" của bạn đã được phê duyệt và xuất bản.',
                    action_url=item_url,
                    sender=request.user
                )
            else:
                create_notification(
                    recipient=creator,
                    notification_type='content_rejected',
                    title='❌ Nội dung bị từ chối',
                    message=f'Nội dung "{item_title}" của bạn bị từ chối. Lý do: {note if note else "Không có ghi chú"}',
                    action_url=item_url,
                    sender=request.user
                )
        
        msg = 'được phê duyệt' if action == 'approve' else 'bị từ chối'
        messages.success(request, f'Đã xử lý thành công. Nội dung {msg}.')
        
    return redirect('studio:moderation_list')
