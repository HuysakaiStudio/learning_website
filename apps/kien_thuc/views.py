import json
import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mon, BaiViet, FlashcardSet, Flashcard, FlashcardProgress
from .forms import FlashcardSetForm, FlashcardForm # Giả sử bạn đã có các form này
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

def danh_sach_mon(request):
    mon_list = Mon.objects.all()
    return render(request, 'kien_thuc/danh_sach_mon.html', {'mon_list': mon_list})

def bai_viet_theo_mon(request, mon_id):
    """Hiển thị danh sách bài viết của một môn học."""
    mon = get_object_or_404(Mon, id=mon_id)
    bai_viet_list = mon.bai_viet.filter(status='published').annotate(
        flashcard_count=Count('mon__flashcard_sets', distinct=True)
    ).order_by('thu_tu', 'ngay_tao')
    return render(request, 'kien_thuc/bai_viet_theo_mon.html', {
        'mon': mon,
        'bai_viet_list': bai_viet_list
    })

def chi_tiet_bai_viet(request, bai_id):
    """Hiển thị nội dung chi tiết của một bài viết."""
    bai = get_object_or_404(BaiViet, id=bai_id)

    # Check permissions
    if bai.status != 'published' and not request.user.is_staff and bai.nguoi_dang != request.user:
        messages.error(request, 'Bạn không có quyền xem bài viết này.')
        return redirect('kien_thuc:danh_sach_mon')

    # Increment view count
    bai.view_count += 1
    bai.save(update_fields=['view_count'])

    return render(request, 'kien_thuc/chi_tiet_bai_viet.html', {'bai': bai})

@login_required
def export_flashcards(request, set_id, format):
    flashcard_set = get_object_or_404(FlashcardSet, pk=set_id)
    # Optional: Check ownership here if needed
    
    flashcards = flashcard_set.flashcards.all()
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{flashcard_set.tieu_de}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Front', 'Back'])
        for fc in flashcards:
            writer.writerow([fc.mat_truoc, fc.mat_sau])
        return response
    elif format == 'json':
        data = [{'front': fc.mat_truoc, 'back': fc.mat_sau} for fc in flashcards]
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = f'attachment; filename="{flashcard_set.tieu_de}.json"'
        return response
    else:
        messages.error(request, 'Unsupported format')
        return redirect('kien_thuc:flashcard_dashboard')

def share_flashcards(request, uuid):
    flashcard_set = get_object_or_404(FlashcardSet, uuid=uuid)
    # Implementation for public sharing view
    context = {
        'flashcard_set': flashcard_set,
        'flashcards': flashcard_set.flashcards.all()
    }
    return render(request, 'kien_thuc/share_flashcards.html', context)

@login_required
def flashcard_dashboard(request):
    """
    Dashboard tổng quan về tiến độ học tập của người dùng.
    """
    # 1. Tổng quan - chỉ đếm bộ thẻ có ít nhất 1 thẻ
    all_sets_count = FlashcardSet.objects.filter(so_luong_the__gt=0).count()
    user_progress = FlashcardProgress.objects.filter(user=request.user)
    
    # Bộ thẻ người dùng đã học (có ít nhất 1 thẻ được đánh dấu học/thuộc)
    # Chỉ lấy bộ thẻ có ít nhất 1 thẻ
    user_sets = FlashcardSet.objects.filter(
        flashcards__flashcardprogress__user=request.user,
        so_luong_the__gt=0
    ).distinct()
    user_sets_count = user_sets.count()
    
    # 2. Thống kê bộ thẻ người dùng đã từng tương tác
    # Sử dụng Count với distinct=True và đếm theo ID để tránh duplicate
    sets_stats = user_sets.annotate(
        total=Count('flashcards__id', distinct=True),
        learned=Count('flashcards__id', filter=Q(flashcards__flashcardprogress__user=request.user, flashcards__flashcardprogress__is_learned=True), distinct=True),
        learning=Count('flashcards__id', filter=Q(flashcards__flashcardprogress__user=request.user, flashcards__flashcardprogress__is_learned=False), distinct=True)
    ).filter(total__gt=0)  # Đảm bảo chỉ hiển thị bộ có thẻ
    
    context = {
        'all_sets_count': all_sets_count,
        'user_sets_count': user_sets_count,
        'sets_stats': sets_stats,
    }
    return render(request, 'kien_thuc/flashcard_dashboard.html', context)

@login_required
def tao_bai_viet(request):
    """Xử lý tạo bài viết mới từ phía người dùng."""
    if request.method == 'POST':
        mon_id = request.POST.get('mon')
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        thu_tu = request.POST.get('thu_tu', 0)
        
        mon = get_object_or_404(Mon, id=mon_id)
        
        status = 'published' if request.user.is_staff else 'pending'
        
        bai_viet = BaiViet.objects.create(
            mon=mon,
            tieu_de=tieu_de,
            noi_dung=noi_dung,
            nguoi_dang=request.user,
            thu_tu=thu_tu,
            status=status
        )
        
        if status == 'published':
            messages.success(request, f'Đã tạo bài viết "{tieu_de}" thành công!')
        else:
            messages.success(request, f'Đã gửi bài viết "{tieu_de}" chờ kiểm duyệt!')
            
        return redirect('kien_thuc:chi_tiet_bai_viet', bai_id=bai_viet.id)
    
    mon_list = Mon.objects.all()
    return render(request, 'kien_thuc/tao_bai_viet.html', {'mon_list': mon_list})

def xoa_bai_viet(request, bai_id):
    return render(request, 'kien_thuc/xac_nhan_xoa.html')

from django.core.paginator import Paginator

def danh_sach_flashcard_sets(request):
    """Hiển thị danh sách các bộ Flashcard có lọc theo môn học."""
    mon_list = Mon.objects.all()
    selected_mon = request.GET.get('mon')
    search_q = request.GET.get('q')
    
    flashcard_sets = FlashcardSet.objects.filter(status='published', so_luong_the__gt=0).order_by('-ngay_tao')
    
    if search_q:
        flashcard_sets = flashcard_sets.filter(tieu_de__icontains=search_q)

    if selected_mon:
        flashcard_sets = flashcard_sets.filter(mon_id=selected_mon)
        
    paginator = Paginator(flashcard_sets, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'mon_list': mon_list,
        'selected_mon': selected_mon,
    }
    return render(request, 'kien_thuc/danh_sach_flashcard_sets.html', context)

def hoc_flashcard(request, flashcard_set_id):
    flashcard_set = get_object_or_404(FlashcardSet, pk=flashcard_set_id)

    # Check permissions
    if flashcard_set.status != 'published' and not request.user.is_staff and flashcard_set.creator != request.user:
        messages.error(request, 'Bạn không có quyền xem bộ Flashcard này.')
        return redirect('kien_thuc:danh_sach_flashcard_sets')

    # Increment view count
    flashcard_set.lan_xem += 1
    flashcard_set.save(update_fields=['lan_xem'])

    mode = request.GET.get('mode', 'study') # 'study' hoặc 'review'

    # Lấy TẤT CẢ flashcards để tính tổng số
    all_flashcards = flashcard_set.flashcards.all()
    total_count = all_flashcards.count()

    # Lấy tiến độ của người dùng nếu họ đã đăng nhập
    learned_ids = []
    if request.user.is_authenticated:
        learned_ids = FlashcardProgress.objects.filter(
            user=request.user,
            flashcard__flashcard_set=flashcard_set,
            is_learned=True
        ).values_list('flashcard_id', flat=True)

    # Nếu mode là 'review', chỉ lấy các thẻ chưa thuộc để hiển thị
    flashcards = all_flashcards
    if mode == 'review' and request.user.is_authenticated:
        flashcards = flashcards.exclude(id__in=learned_ids)

    flashcard_data = []
    for fc in flashcards:
        flashcard_data.append({
            'flashcard': {
                'id': fc.id,
                'mat_truoc': fc.mat_truoc,
                'mat_sau': fc.mat_sau
            },
            'is_learned': fc.id in learned_ids
        })

    context = {
        'flashcard_set': flashcard_set,
        'flashcard_data_json': json.dumps(flashcard_data),
        'tong_so': total_count,  # Tổng số thẻ trong set (không đổi)
        'da_thuoc': len(learned_ids),
        'mode': mode,
        'cache_version': '20260410'  # Update this when CSS/JS changes
    }
    return render(request, 'kien_thuc/hoc_flashcard.html', context)

def them_flashcard(request, flashcard_set_id):
    flashcard_set = get_object_or_404(FlashcardSet, pk=flashcard_set_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            card_id = request.POST.get('card_id')
            Flashcard.objects.filter(id=card_id, flashcard_set=flashcard_set).delete()
            flashcard_set.cap_nhat_so_luong()
            messages.success(request, 'Đã xóa thẻ!')
        elif action == 'import':
            bulk_data = request.POST.get('bulk_data', '')
            lines = bulk_data.strip().split('\n')
            for line in lines:
                if '|' in line:
                    front, back = line.split('|', 1)
                    Flashcard.objects.create(
                        flashcard_set=flashcard_set,
                        mat_truoc=front.strip(),
                        mat_sau=back.strip()
                    )
            flashcard_set.cap_nhat_so_luong()
            messages.success(request, 'Đã nhập thẻ thành công!')
        else:
            form = FlashcardForm(request.POST)
            if form.is_valid():
                flashcard = form.save(commit=False)
                flashcard.flashcard_set = flashcard_set
                flashcard.save()
                flashcard_set.cap_nhat_so_luong()
                messages.success(request, 'Đã thêm thẻ mới!')
        
        return redirect('kien_thuc:them_flashcard', flashcard_set_id=flashcard_set_id)
    
    else:
        form = FlashcardForm()
        flashcards = flashcard_set.flashcards.all()
    
    return render(request, 'kien_thuc/them_flashcard.html', {
        'flashcard_set': flashcard_set,
        'form': form,
        'flashcards': flashcards
    })

@login_required
def tao_flashcard_set(request):
    if request.method == 'POST':
        form = FlashcardSetForm(request.POST)
        if form.is_valid():
            set_moi = form.save(commit=False)
            set_moi.creator = request.user
            set_moi.status = 'draft'  # Always start as draft
            set_moi.save()
            
            messages.success(request, 'Bộ flashcard đã được tạo. Hãy thêm thẻ và gửi kiểm duyệt.')
            return redirect('studio:edit_flashcard_set', set_id=set_moi.id)
    else:
        form = FlashcardSetForm()
    
    mon_list = Mon.objects.all()
    return render(request, 'kien_thuc/tao_flashcard_set.html', {'form': form, 'mon_list': mon_list})

def api_flashcard_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            flashcard_id = data.get('flashcard_id')
            is_learned = data.get('is_learned')
            
            # Cập nhật hoặc tạo tiến độ
            progress, created = FlashcardProgress.objects.get_or_create(
                user=request.user,
                flashcard_id=flashcard_id
            )
            progress.is_learned = is_learned
            progress.save()
            
            # Tính lại số lượng đã thuộc trong bộ để trả về
            flashcard = Flashcard.objects.get(id=flashcard_id)
            da_thuoc = FlashcardProgress.objects.filter(
                user=request.user,
                flashcard__flashcard_set=flashcard.flashcard_set,
                is_learned=True
            ).count()
            
            # Check for milestones and send notification
            if is_learned:
                total_learned = FlashcardProgress.objects.filter(
                    user=request.user,
                    is_learned=True
                ).count()
                
                # Send notification for milestones
                if total_learned in [10, 50, 100, 500, 1000]:
                    try:
                        from apps.notifications.utils import notify_flashcard_milestone
                        notify_flashcard_milestone(request.user, total_learned)
                    except Exception as e:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Error sending flashcard milestone notification: {e}")
            
            return JsonResponse({'success': True, 'da_thuoc': da_thuoc})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def reset_flashcard_progress(request, set_id):
    if request.method == 'POST':
        flashcard_set = get_object_or_404(FlashcardSet, pk=set_id)
        FlashcardProgress.objects.filter(user=request.user, flashcard__flashcard_set=flashcard_set).delete()
        messages.success(request, 'Đã đặt lại tiến độ bộ thẻ!')
        return redirect('kien_thuc:hoc_flashcard', flashcard_set_id=set_id)
    return redirect('kien_thuc:danh_sach_flashcard_sets')
