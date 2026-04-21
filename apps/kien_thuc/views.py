import json
import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mon, BaiViet, FlashcardSet, Flashcard, FlashcardProgress, FlashcardTest, FlashcardTestAnswer, Notebook, NoteSection, NoteTag, NotebookTag, Note
from .forms import FlashcardSetForm, FlashcardForm # Giả sử bạn đã có các form này
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import re

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

    # Process content to render markdown-like formatting
    processed_content = render_markdown_content(bai.noi_dung)
    bai.processed_content = processed_content

    return render(request, 'kien_thuc/chi_tiet_bai_viet.html', {'bai': bai})


def render_markdown_content(text):
    """
    Render markdown-like content with HTML formatting
    Handles: headers, bold, italic, horizontal rules, and preserves formulas
    """
    # Temporarily protect formulas from processing
    formulas = []
    def replace_formula(match):
        nonlocal formulas
        formulas.append(match.group(0))
        return f'%%FORMULA_{len(formulas)-1}%%'
    
    # Find and temporarily replace formulas
    text = re.sub(r'(\$\$[\s\S]*?\$\$|\$[^\$]*?\$)', replace_formula, text)
    
    # Escape HTML characters to prevent XSS (but preserve our formula placeholders)
    text = text.replace('&', '&').replace('<', '<').replace('>', '>')
    
    # Process markdown syntax
    # Headers
    text = re.sub(r'^# (.+)$', r'<h2 style="font-size:22px;font-weight:600;margin:24px 0 12px;color:#2980b9">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h3 style="font-size:20px;font-weight:500;margin:20px 0 10px;color:#3498db">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h4 style="font-size:18px;font-weight:500;margin:18px 0 8px;color:#3498db">\1</h4>', text, flags=re.MULTILINE)
    
    # Bold text
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight:600;">\1</strong>', text)
    
    # Italic text
    text = re.sub(r'\*(.+?)\*', r'<em style="font-style:italic;">\1</em>', text)
    
    # Horizontal rules
    text = re.sub(r'^──+$', r'<hr style="border:none;border-top:1px solid #eee;margin:16px 0">', text, flags=re.MULTILINE)
    
    # Preserve line breaks
    text = text.replace('\n', '<br>')
    
    # Restore formulas
    for i, formula in enumerate(formulas):
        text = text.replace(f'%%FORMULA_{i}%%', formula)
    
    return text


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
        mon = get_object_or_404(Mon, id=mon_id)
        
        status = 'published' if request.user.is_staff else 'pending'
        
        bai_viet = BaiViet.objects.create(
            mon=mon,
            tieu_de=tieu_de,
            noi_dung=noi_dung,
            nguoi_dang=request.user,
            thu_tu=0,  # Default to 0 since field is removed
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
    sort_by = request.GET.get('sort', 'moi_nhat')  # Default sort by newest
    
    flashcard_sets = FlashcardSet.objects.filter(status='published', so_luong_the__gt=0)
    
    if search_q:
        flashcard_sets = flashcard_sets.filter(tieu_de__icontains=search_q)

    if selected_mon:
        flashcard_sets = flashcard_sets.filter(mon_id=selected_mon)
    
    # Apply sorting based on user selection
    if sort_by == 'luot_xem_giam_dan':
        flashcard_sets = flashcard_sets.order_by('-lan_xem', '-ngay_tao')
    elif sort_by == 'luot_xem_tang_dan':
        flashcard_sets = flashcard_sets.order_by('lan_xem', '-ngay_tao')
    elif sort_by == 'so_the_giam_dan':
        flashcard_sets = flashcard_sets.order_by('-so_luong_the', '-ngay_tao')
    elif sort_by == 'so_the_tang_dan':
        flashcard_sets = flashcard_sets.order_by('so_luong_the', '-ngay_tao')
    elif sort_by == 'ten_az':
        flashcard_sets = flashcard_sets.order_by('tieu_de', '-ngay_tao')
    elif sort_by == 'ten_za':
        flashcard_sets = flashcard_sets.order_by('-tieu_de', '-ngay_tao')
    else:  # 'moi_nhat' or default
        flashcard_sets = flashcard_sets.order_by('-ngay_tao')
        
    paginator = Paginator(flashcard_sets, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'mon_list': mon_list,
        'selected_mon': selected_mon,
        'sort_by': sort_by,
    }
    return render(request, 'kien_thuc/danh_sach_flashcard_sets.html', context)

def hoc_flashcard(request, flashcard_set_id):
    flashcard_set = get_object_or_404(FlashcardSet, pk=flashcard_set_id)

    # Check permissions
    if flashcard_set.status != 'published' and not request.user.is_staff and flashcard_set.creator != request.user:
        messages.error(request, 'Bạn không có quyền xem bộ Flashcard này.')
        return redirect('kien_thuc:danh_sach_flashcard_sets')

    # Implement view count with session-based limiting to prevent inflation
    session_key = f'flashcard_view_{flashcard_set_id}_{request.session.session_key}'
    last_view_time = request.session.get(session_key)
    
    from django.utils import timezone
    from datetime import timedelta
    
    # Only increment view count if it's been at least 5 minutes since last view
    if not last_view_time or (timezone.now() - timezone.datetime.fromisoformat(last_view_time)).total_seconds() > 300:
        flashcard_set.lan_xem += 1
        flashcard_set.save(update_fields=['lan_xem'])
        request.session[session_key] = timezone.now().isoformat()

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
    # Create a new study session for this flashcard set
    from .models import FlashcardStudySession
    study_session = FlashcardStudySession.objects.create(
        nguoi_dung=request.user,
        bo_flashcard=flashcard_set,
        che_do=mode
    )
    
    context = {
        'flashcard_set': flashcard_set,
        'flashcard_data_json': json.dumps(flashcard_data),
        'tong_so': total_count,  # Tổng số thẻ trong set (không đổi)
        'da_thuoc': len(learned_ids),
        'mode': mode,
        'cache_version': '20260410',  # Update this when CSS/JS changes
        'study_session_id': study_session.id
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
            import_file = request.FILES.get('import_file')
            imported_count = 0

            if import_file:
                # Handle CSV file upload
                try:
                    # Use utf-8-sig to handle BOM if present
                    decoded_file = import_file.read().decode('utf-8-sig').splitlines()
                    reader = csv.reader(decoded_file, delimiter=';')
                    for row in reader:
                        if len(row) >= 2:
                            Flashcard.objects.create(
                                flashcard_set=flashcard_set,
                                mat_truoc=row[0].strip(),
                                mat_sau=row[1].strip()
                            )
                            imported_count += 1
                except Exception as e:
                    messages.error(request, f'Lỗi khi đọc file CSV: {e}')
            else:
                # Handle text-based import
                bulk_data = request.POST.get('bulk_data', '')
                if bulk_data:
                    lines = bulk_data.strip().split('\n')
                    for line in lines:
                        if '|' in line:
                            front, back = line.split(';', 1)
                            Flashcard.objects.create(
                                flashcard_set=flashcard_set,
                                mat_truoc=front.strip(),
                                mat_sau=back.strip()
                            )
                            imported_count += 1
            
            if imported_count > 0:
                flashcard_set.cap_nhat_so_luong()
                messages.success(request, f'Đã nhập thành công {imported_count} thẻ!')
            elif not import_file and not request.POST.get('bulk_data'):
                messages.warning(request, 'Vui lòng cung cấp file hoặc nội dung để nhập.')
            else:
                messages.warning(request, 'Không tìm thấy dữ liệu hợp lệ để nhập. Hãy kiểm tra lại định dạng.')
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


@login_required
def start_flashcard_test(request, flashcard_set_id):
    """
    Bắt đầu một bài kiểm tra flashcard mới (dưới dạng trắc nghiệm 4 lựa chọn)
    """
    flashcard_set = get_object_or_404(FlashcardSet, pk=flashcard_set_id)
    
    # Kiểm tra quyền truy cập
    if flashcard_set.status != 'published' and not request.user.is_staff and flashcard_set.creator != request.user:
        messages.error(request, 'Bạn không có quyền làm bài kiểm tra này.')
        return redirect('kien_thuc:danh_sach_flashcard_sets')
    
    # Lấy tất cả flashcards trong bộ
    all_flashcards = list(flashcard_set.flashcards.all())
    
    if not all_flashcards:
        messages.error(request, 'Bộ flashcard này không có thẻ nào để kiểm tra.')
        return redirect('kien_thuc:hoc_flashcard', flashcard_set_id=flashcard_set_id)
    
    # Kiểm tra xem có đủ thẻ để tạo câu hỏi trắc nghiệm không (ít nhất 4 thẻ để có 1 đúng + 3 sai)
    if len(all_flashcards) < 4:
        messages.error(request, 'Không thể truy cập chế độ kiểm tra của flashcard khi chưa đủ 4 thẻ.')
        return redirect('kien_thuc:hoc_flashcard', flashcard_set_id=flashcard_set_id)
    
    # Trộn ngẫu nhiên các thẻ để tạo câu hỏi
    import random
    random.shuffle(all_flashcards)
    
    # Giới hạn số lượng câu hỏi (ví dụ: tối đa 20 câu)
    selected_flashcards = all_flashcards[:20]  # Giới hạn số lượng câu hỏi

    # Tạo dữ liệu câu hỏi trắc nghiệm
    multiple_choice_data = []
    for i, main_card in enumerate(selected_flashcards):
        # Lấy 3 thẻ khác làm đáp án sai
        other_cards = [card for j, card in enumerate(selected_flashcards) if j != i]
        wrong_choices = random.sample(other_cards, min(3, len(other_cards)))
        
        # Tạo danh sách lựa chọn
        choices = [
            {'id': main_card.id, 'content': main_card.mat_sau, 'is_correct': True}
        ]
        
        for wrong_card in wrong_choices:
            choices.append({
                'id': wrong_card.id,
                'content': wrong_card.mat_sau,
                'is_correct': False
            })
        
        # Trộn ngẫu nhiên thứ tự các lựa chọn
        random.shuffle(choices)
        
        multiple_choice_data.append({
            'id': main_card.id,
            'question': main_card.mat_truoc,  # Câu hỏi từ mặt trước
            'choices': choices,  # Các lựa chọn (1 đúng + 3 sai)
            'correct_answer_id': main_card.id  # ID của đáp án đúng
        })
    
    # Tạo bài kiểm tra mới
    test = FlashcardTest.objects.create(
        nguoi_dung=request.user,
        bo_flashcard=flashcard_set,
        tong_so_cau_hoi=len(multiple_choice_data)
    )
    
    # Check if there are enough cards to show quiz controls
    has_min_cards_for_quiz = len(multiple_choice_data) >= 1  # Since we already checked above
    
    context = {
        'test': test,
        'flashcard_set': flashcard_set,
        'flashcard_data_json': json.dumps(multiple_choice_data),
        'total_questions': len(multiple_choice_data),
        'has_min_cards_for_quiz': has_min_cards_for_quiz
    }
    
    return render(request, 'kien_thuc/flashcard_test.html', context)


@login_required
def submit_flashcard_test_answer(request):
    """
    Gửi câu trả lời cho một câu hỏi trong bài kiểm tra
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'})
    
    try:
        data = json.loads(request.body)
        test_id = data.get('test_id')
        flashcard_id = data.get('flashcard_id')
        is_correct = data.get('is_correct')
        user_answer = data.get('user_answer', '')
        response_time = data.get('response_time', 0)
        
        test = FlashcardTest.objects.get(id=test_id, nguoi_dung=request.user)
        
        # Kiểm tra xem câu hỏi này đã được trả lời chưa
        existing_answer, created = FlashcardTestAnswer.objects.get_or_create(
            bai_kiem_tra=test,
            flashcard_id=flashcard_id,
            defaults={
                'cau_tra_loi': user_answer,
                'dung': is_correct,
                'thoi_gian_tra_loi_thuc_te': response_time
            }
        )
        
        if not created:
            # Nếu đã tồn tại câu trả lời, cập nhật
            existing_answer.cau_tra_loi = user_answer
            existing_answer.dung = is_correct
            existing_answer.thoi_gian_tra_loi_thuc_te = response_time
            existing_answer.save()
        
        # Cập nhật số câu trả lời đúng trong bài kiểm tra
        if is_correct:
            test.so_cau_tra_loi_dung += 1
            test.save()
        
        # Cập nhật điểm
        test.cap_nhat_diem()
        
        return JsonResponse({
            'success': True,
            'correct_answers': test.so_cau_tra_loi_dung,
            'total_questions': test.tong_so_cau_hoi,
            'current_score': test.diem
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def finish_flashcard_test(request, test_id):
    """
    Kết thúc bài kiểm tra và hiển thị kết quả
    """
    test = get_object_or_404(FlashcardTest, id=test_id, nguoi_dung=request.user)
    
    # Đánh dấu là hoàn thành
    test.hoan_thanh = True
    test.thoi_gian_hoan_thanh = timezone.now()
    test.save()
    
    # Tính điểm cuối cùng
    test.cap_nhat_diem()
    
    # Lấy các câu trả lời để hiển thị kết quả chi tiết
    answers = test.cac_cau_tra_loi.select_related('flashcard').all()
    
    context = {
        'test': test,
        'answers': answers
    }
    
    return render(request, 'kien_thuc/flashcard_test_results.html', context)


def api_reset_flashcard(request, set_id):
    """
    API endpoint để đặt lại tiến độ flashcard
    """
    if request.method == 'POST':
        flashcard_set = get_object_or_404(FlashcardSet, pk=set_id)
        FlashcardProgress.objects.filter(user=request.user, flashcard__flashcard_set=flashcard_set).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def end_flashcard_session(request):
    """
    API endpoint to end a flashcard study session and record time spent
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({'success': False, 'error': 'Session ID is required'})
        
        from .models import FlashcardStudySession
        session = get_object_or_404(FlashcardStudySession, id=session_id, nguoi_dung=request.user)
        
        # Update session end time
        session.ngay_ket_thuc = timezone.now()
        session.cap_nhat_thoi_gian_hoc()  # Calculate time spent
        
        # Update card counters if provided
        cards_seen = data.get('cards_seen', 0)
        cards_studied = data.get('cards_studied', 0)
        if cards_seen > 0:
            session.so_the_da_xem = cards_seen
        if cards_studied > 0:
            session.so_the_da_hoc = cards_studied
        
        session.save()
        
        # Update user analytics with the time spent
        try:
            from apps.de_thi.models import UserAnalytics
            analytics, created = UserAnalytics.objects.get_or_create(nguoi_dung=request.user)
            time_spent_minutes = session.thoi_gian_hoc // 60  # Convert seconds to minutes
            analytics.cap_nhat_thoi_gian_hoc(time_spent_minutes, 'flashcard')
        except ImportError:
            pass  # Analytics not available
        
        return JsonResponse({
            'success': True,
            'time_spent': session.thoi_gian_hoc,
            'time_spent_minutes': time_spent_minutes
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Personal Knowledge Outline Feature Views

@login_required
def notebook_dashboard(request):
    """
    Dashboard showing all user's notebooks
    """
    notebooks = Notebook.objects.filter(user=request.user).select_related('user').prefetch_related('sections', 'notebook_tags__tag')
    
    # Get all user's tags for filtering
    user_tags = NoteTag.objects.filter(user=request.user)
    
    # Apply tag filter if provided
    tag_filter = request.GET.get('tag')
    if tag_filter:
        notebooks = notebooks.filter(notebook_tags__tag__id=tag_filter)
    
    context = {
        'notebooks': notebooks,
        'user_tags': user_tags,
        'selected_tag': tag_filter
    }
    return render(request, 'kien_thuc/notebook_dashboard.html', context)


@login_required
def api_notebooks(request):
    """
    API endpoint for managing notebooks
    """
    if request.method == 'GET':
        # Get all user's notebooks
        notebooks = Notebook.objects.filter(user=request.user).select_related('user').prefetch_related('sections', 'notebook_tags__tag')
        
        data = []
        for notebook in notebooks:
            notebook_data = {
                'id': notebook.id,
                'title': notebook.title,
                'description': notebook.description,
                'visibility': notebook.visibility,
                'created_at': notebook.created_at.isoformat(),
                'updated_at': notebook.updated_at.isoformat(),
                'sections': [
                    {
                        'id': section.id,
                        'title': section.title,
                        'order': section.order,
                        'created_at': section.created_at.isoformat(),
                        'updated_at': section.updated_at.isoformat()
                    } for section in notebook.sections.all()
                ],
                'tags': [
                    {
                        'id': tag.tag.id,
                        'name': tag.tag.name,
                        'color': tag.tag.color
                    } for tag in notebook.notebook_tags.all()
                ]
            }
            data.append(notebook_data)
        
        return JsonResponse({'notebooks': data})
    
    elif request.method == 'POST':
        # Create a new notebook
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            description = data.get('description', '')
            visibility = data.get('visibility', 'private')
            tag_ids = data.get('tag_ids', [])
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            notebook = Notebook.objects.create(
                user=request.user,
                title=title,
                description=description,
                visibility=visibility
            )
            
            # Associate tags if provided
            for tag_id in tag_ids:
                try:
                    tag = NoteTag.objects.get(id=tag_id, user=request.user)
                    NotebookTag.objects.create(notebook=notebook, tag=tag)
                except NoteTag.DoesNotExist:
                    # Skip invalid tag IDs
                    continue
            
            return JsonResponse({
                'id': notebook.id,
                'title': notebook.title,
                'description': notebook.description,
                'visibility': notebook.visibility,
                'created_at': notebook.created_at.isoformat(),
                'updated_at': notebook.updated_at.isoformat()
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_notebook_detail(request, notebook_id):
    """
    API endpoint for managing a specific notebook
    """
    try:
        notebook = Notebook.objects.get(id=notebook_id, user=request.user)
    except Notebook.DoesNotExist:
        return JsonResponse({'error': 'Notebook not found'}, status=404)
    
    if request.method == 'GET':
        # Get notebook with sections
        data = {
            'id': notebook.id,
            'title': notebook.title,
            'description': notebook.description,
            'visibility': notebook.visibility,
            'created_at': notebook.created_at.isoformat(),
            'updated_at': notebook.updated_at.isoformat(),
            'sections': [
                {
                    'id': section.id,
                    'title': section.title,
                    'content': section.content,
                    'order': section.order,
                    'created_at': section.created_at.isoformat(),
                    'updated_at': section.updated_at.isoformat()
                } for section in notebook.sections.all().order_by('order', 'created_at')
            ],
            'tags': [
                {
                    'id': tag.tag.id,
                    'name': tag.tag.name,
                    'color': tag.tag.color
                } for tag in notebook.notebook_tags.all()
            ]
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        # Update notebook
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            description = data.get('description', '')
            visibility = data.get('visibility', 'private')
            tag_ids = data.get('tag_ids', [])
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            notebook.title = title
            notebook.description = description
            notebook.visibility = visibility
            notebook.save()
            
            # Update tags - first remove all existing tags
            NotebookTag.objects.filter(notebook=notebook).delete()
            
            # Then add new tags
            for tag_id in tag_ids:
                try:
                    tag = NoteTag.objects.get(id=tag_id, user=request.user)
                    NotebookTag.objects.create(notebook=notebook, tag=tag)
                except NoteTag.DoesNotExist:
                    # Skip invalid tag IDs
                    continue
            
            return JsonResponse({
                'id': notebook.id,
                'title': notebook.title,
                'description': notebook.description,
                'visibility': notebook.visibility,
                'created_at': notebook.created_at.isoformat(),
                'updated_at': notebook.updated_at.isoformat()
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        # Delete notebook
        notebook.delete()
        return JsonResponse({'success': True})


@login_required
def api_notebook_sections(request, notebook_id):
    """
    API endpoint for managing sections within a notebook
    """
    try:
        notebook = Notebook.objects.get(id=notebook_id, user=request.user)
    except Notebook.DoesNotExist:
        return JsonResponse({'error': 'Notebook not found'}, status=404)
    
    if request.method == 'GET':
        # Get all sections for the notebook
        sections = NoteSection.objects.filter(notebook=notebook).order_by('order', 'created_at')
        data = [
            {
                'id': section.id,
                'title': section.title,
                'content': section.content,
                'order': section.order,
                'created_at': section.created_at.isoformat(),
                'updated_at': section.updated_at.isoformat()
            } for section in sections
        ]
        return JsonResponse({'sections': data})
    
    elif request.method == 'POST':
        # Create a new section
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '')
            order = data.get('order', 0)
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            section = NoteSection.objects.create(
                notebook=notebook,
                title=title,
                content=content,
                order=order
            )
            
            return JsonResponse({
                'id': section.id,
                'title': section.title,
                'content': section.content,
                'order': section.order,
                'created_at': section.created_at.isoformat(),
                'updated_at': section.updated_at.isoformat()
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_section_detail(request, section_id):
    """
    API endpoint for managing a specific section
    """
    try:
        section = NoteSection.objects.get(id=section_id, notebook__user=request.user)
    except NoteSection.DoesNotExist:
        return JsonResponse({'error': 'Section not found'}, status=404)
    
    if request.method == 'GET':
        # Get section
        data = {
            'id': section.id,
            'title': section.title,
            'content': section.content,
            'order': section.order,
            'created_at': section.created_at.isoformat(),
            'updated_at': section.updated_at.isoformat(),
            'notebook_id': section.notebook.id
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        # Update section
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '')
            order = data.get('order', section.order)
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            section.title = title
            section.content = content
            section.order = order
            section.save()
            
            return JsonResponse({
                'id': section.id,
                'title': section.title,
                'content': section.content,
                'order': section.order,
                'created_at': section.created_at.isoformat(),
                'updated_at': section.updated_at.isoformat(),
                'notebook_id': section.notebook.id
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        # Delete section
        section.delete()
        return JsonResponse({'success': True})


@login_required
def api_note_tags(request):
    """
    API endpoint for managing note tags
    """
    if request.method == 'GET':
        # Get all user's tags
        tags = NoteTag.objects.filter(user=request.user)
        data = [
            {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color
            } for tag in tags
        ]
        return JsonResponse({'tags': data})
    
    elif request.method == 'POST':
        # Create a new tag
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            color = data.get('color', '#007bff')
            
            if not name:
                return JsonResponse({'error': 'Tag name is required'}, status=400)
            
            # Check if tag already exists for this user
            existing_tag = NoteTag.objects.filter(user=request.user, name=name).first()
            if existing_tag:
                return JsonResponse({'error': 'Tag already exists'}, status=400)
            
            tag = NoteTag.objects.create(
                user=request.user,
                name=name,
                color=color
            )
            
            return JsonResponse({
                'id': tag.id,
                'name': tag.name,
                'color': tag.color
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_note_search(request):
    """
    API endpoint for searching user's notebooks and sections
    """
    query = request.GET.get('q', '').strip()
    tag_id = request.GET.get('tag')
    
    if not query:
        return JsonResponse({'results': []})
    
    # Search in notebooks and sections
    notebooks = Notebook.objects.filter(user=request.user)
    sections = NoteSection.objects.filter(notebook__user=request.user)
    
    # Apply tag filter if provided
    if tag_id:
        try:
            tag = NoteTag.objects.get(id=tag_id, user=request.user)
            notebooks = notebooks.filter(notebook_tags__tag=tag)
            sections = sections.filter(notebook__notebook_tags__tag=tag)
        except NoteTag.DoesNotExist:
            # If tag doesn't exist, return empty results
            return JsonResponse({'results': []})
    
    # Search in titles and content
    notebooks = notebooks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    sections = sections.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    results = []
    
    # Add notebooks to results
    for notebook in notebooks:
        results.append({
            'type': 'notebook',
            'id': notebook.id,
            'title': notebook.title,
            'description': notebook.description,
            'url': f'/notebooks/{notebook.id}/',
            'updated_at': notebook.updated_at.isoformat()
        })
    
    # Add sections to results
    for section in sections:
        results.append({
            'type': 'section',
            'id': section.id,
            'title': section.title,
            'content_preview': section.content[:100] + '...' if len(section.content) > 100 else section.content,
            'notebook_id': section.notebook.id,
            'notebook_title': section.notebook.title,
            'url': f'/notebooks/{section.notebook.id}/#section-{section.id}',
            'updated_at': section.updated_at.isoformat()
        })
    
    # Sort results by updated_at (most recent first)
    results.sort(key=lambda x: x['updated_at'], reverse=True)
    
    return JsonResponse({'results': results})


# Smart Notes API Views

@login_required
def api_notes(request):
    """
    API endpoint for managing user notes
    """
    if request.method == 'GET':
        # Get all user's notes with optional filtering
        note_type = request.GET.get('type')
        is_pinned = request.GET.get('pinned')
        
        notes = Note.objects.filter(user=request.user).select_related('question', 'flashcard', 'article')
        
        if note_type:
            notes = notes.filter(note_type=note_type)
        if is_pinned:
            notes = notes.filter(is_pinned=(is_pinned.lower() == 'true'))
        
        data = []
        for note in notes:
            note_data = {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'note_type': note.note_type,
                'is_pinned': note.is_pinned,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'associated_id': None,
                'associated_title': None,
            }
            
            # Add associated content info
            if note.question:
                note_data['associated_id'] = note.question.id
                note_data['associated_title'] = note.question.noi_dung[:50] + '...' if len(note.question.noi_dung) > 50 else note.question.noi_dung
            elif note.flashcard:
                note_data['associated_id'] = note.flashcard.id
                note_data['associated_title'] = note.flashcard.mat_truoc
            elif note.article:
                note_data['associated_id'] = note.article.id
                note_data['associated_title'] = note.article.tieu_de
            
            data.append(note_data)
        
        return JsonResponse({'notes': data})
    
    elif request.method == 'POST':
        # Create a new note
        try:
            data = json.loads(request.body)
            note_type = data.get('note_type', '').strip()
            title = data.get('title', '').strip()
            content = data.get('content', '')
            is_pinned = data.get('is_pinned', False)
            associated_id = data.get('associated_id')
            
            if not note_type or not associated_id:
                return JsonResponse({'error': 'Note type and associated ID are required'}, status=400)
            
            # Create note with proper associations
            note = Note.objects.create(
                user=request.user,
                note_type=note_type,
                title=title,
                content=content,
                is_pinned=is_pinned
            )
            
            # Set the appropriate association based on note_type
            if note_type == 'question':
                from apps.de_thi.models import CauHoi
                try:
                    question = CauHoi.objects.get(id=associated_id)
                    note.question = question
                except CauHoi.DoesNotExist:
                    return JsonResponse({'error': 'Question not found'}, status=404)
            elif note_type == 'flashcard':
                try:
                    flashcard = Flashcard.objects.get(id=associated_id)
                    note.flashcard = flashcard
                except Flashcard.DoesNotExist:
                    return JsonResponse({'error': 'Flashcard not found'}, status=404)
            elif note_type == 'article':
                try:
                    article = BaiViet.objects.get(id=associated_id)
                    note.article = article
                except BaiViet.DoesNotExist:
                    return JsonResponse({'error': 'Article not found'}, status=404)
            else:
                return JsonResponse({'error': 'Invalid note type'}, status=400)
            
            note.save()
            
            return JsonResponse({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'note_type': note.note_type,
                'is_pinned': note.is_pinned,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'associated_id': associated_id,
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def api_note_detail(request, note_id):
    """
    API endpoint for managing a specific note
    """
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return JsonResponse({'error': 'Note not found'}, status=404)
    
    if request.method == 'GET':
        # Get note
        note_data = {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'note_type': note.note_type,
            'is_pinned': note.is_pinned,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat(),
            'associated_id': None,
        }
        
        if note.question:
            note_data['associated_id'] = note.question.id
        elif note.flashcard:
            note_data['associated_id'] = note.flashcard.id
        elif note.article:
            note_data['associated_id'] = note.article.id
        
        return JsonResponse(note_data)
    
    elif request.method == 'PUT':
        # Update note
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '')
            is_pinned = data.get('is_pinned', note.is_pinned)
            
            note.title = title
            note.content = content
            note.is_pinned = is_pinned
            note.save()
            
            return JsonResponse({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'note_type': note.note_type,
                'is_pinned': note.is_pinned,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'associated_id': data.get('associated_id'),
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'DELETE':
        # Delete note
        note.delete()
        return JsonResponse({'success': True})


@login_required
def api_notes_context(request, note_type, obj_id):
    """
    API endpoint for getting notes associated with specific content
    """
    if note_type not in ['question', 'flashcard', 'article']:
        return JsonResponse({'error': 'Invalid note type'}, status=400)
    
    try:
        # Get all notes for this user associated with the specific content
        notes = Note.objects.filter(user=request.user)
        
        if note_type == 'question':
            notes = notes.filter(question_id=obj_id)
        elif note_type == 'flashcard':
            notes = notes.filter(flashcard_id=obj_id)
        elif note_type == 'article':
            notes = notes.filter(article_id=obj_id)
        
        notes = notes.select_related('question', 'flashcard', 'article').order_by('-is_pinned', '-updated_at')
        
        data = []
        for note in notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'is_pinned': note.is_pinned,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
            })
        
        return JsonResponse({'notes': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
