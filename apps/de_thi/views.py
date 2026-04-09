from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from apps.kien_thuc.models import Mon
from .models import (DeThi, CauHoi, KetQua, TraLoi, UserAnalytics, SubjectPerformance, QuestionDifficulty,
                     ForumPost, ForumComment, ForumReply, PostVote)
from .forms import DeThiForm, TracNghiemForm, DungSaiForm, DienSoForm, BulkAddQuestionsForm, ImportDeThiForm
from django.core.paginator import Paginator
import json
import csv
import logging
from io import StringIO

logger = logging.getLogger(__name__)

@login_required
def tao_de_thi(request):
    if request.method == 'POST':
        form = DeThiForm(request.POST)
        if form.is_valid():
            de = form.save(commit=False)
            de.creator = request.user
            de.is_custom = True
            de.save()
            messages.success(request, 'Đề thi đã được tạo. Hãy thêm câu hỏi!')
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
        else:
            messages.error(request, 'Có lỗi trong thông tin đề thi. Vui lòng kiểm tra và thử lại.')
    else:
        form = DeThiForm()
    return render(request, 'de_thi/tao_de_thi.html', {'form': form})

@login_required
def them_cau_hoi(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, creator=request.user)
    if request.method == 'POST':
        # Tùy thuộc vào loại câu hỏi mà chọn form tương ứng
        loai = request.POST.get('loai')
        if loai == 'tn':
            form = TracNghiemForm(request.POST)
        elif loai == 'ds':
            form = DungSaiForm(request.POST)
        elif loai == 'dien':
            form = DienSoForm(request.POST)
        else:
            form = None

        if form and form.is_valid():
            cau_hoi = form.save(commit=False)
            cau_hoi.de_thi = de
            cau_hoi.loai = loai
            cau_hoi.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            messages.success(request, 'Câu hỏi đã được thêm!')
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
        elif form:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            else:
                messages.error(request, 'Có lỗi trong thông tin câu hỏi. Vui lòng kiểm tra và thử lại.')
    else:
        # Mặc định là TracNghiemForm nếu không có dữ liệu POST
        cau_hoi_list = de.cau_hoi.all().order_by('id')
        return render(request, 'de_thi/them_cau_hoi.html', {
            'de': de,
            'form_tn': TracNghiemForm(),
            'form_ds': DungSaiForm(),
            'form_dien': DienSoForm(),
            'cau_hoi_list': cau_hoi_list,
            'loai': 'tn'
        })

def danh_sach_de(request):
    selected_mon = request.GET.get('mon')
    search_q = request.GET.get('q')

    selected_mon_id = None
    try:
        selected_mon_id = int(selected_mon) if selected_mon else None
    except (TypeError, ValueError):
        selected_mon_id = None

    de_list = DeThi.objects.filter(an=False)
    mon_list = Mon.objects.filter(de_thi__an=False).distinct()

    if search_q:
        de_list = de_list.filter(ten__icontains=search_q)

    if not request.user.is_staff:
        # Ẩn đề thi không có câu hỏi đối với người dùng bình thường
        de_list = de_list.annotate(q_count=Count('cau_hoi')).filter(q_count__gt=0)

    if selected_mon_id:
        de_list = de_list.filter(mon_id=selected_mon_id)

    paginator = Paginator(de_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'de_thi/danh_sach_de.html', {
        'page_obj': page_obj,
        'mon_list': mon_list,
        'selected_mon': selected_mon_id,
    })

@login_required
def chon_che_do(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, an=False)
    return render(request, 'de_thi/chon_che_do.html', {'de': de})

@login_required
def lich_su_lam_bai(request):
    selected_mon = request.GET.get('mon')

    selected_mon_id = None
    try:
        selected_mon_id = int(selected_mon) if selected_mon else None
    except (TypeError, ValueError):
        selected_mon_id = None

    ket_qua_list = KetQua.objects.filter(nguoi_dung=request.user).select_related('de_thi', 'de_thi__mon')
    mon_list = Mon.objects.filter(de_thi__ketqua__nguoi_dung=request.user).distinct()

    if not request.user.is_staff:
        # Ẩn kết quả không có câu trả lời đối với người dùng bình thường
        ket_qua_list = ket_qua_list.annotate(a_count=Count('tra_loi')).filter(a_count__gt=0)

    if selected_mon_id:
        ket_qua_list = ket_qua_list.filter(de_thi__mon_id=selected_mon_id)

    paginator = Paginator(ket_qua_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'de_thi/lich_su_lam_bai.html', {
        'page_obj': page_obj,
        'mon_list': mon_list,
        'selected_mon': selected_mon_id,
    })

@login_required
def lam_bai(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, an=False)
    che_do = request.GET.get('che_do', 'luyen_tap')
    
    # Sắp xếp câu hỏi theo thứ tự (thu_tu) được thiết lập
    cau_hoi_list = de.cau_hoi.all().order_by('thu_tu', 'id')
    
    # Pre-process choices for TN questions
    for cau in cau_hoi_list:
        if cau.loai == 'tn':
            cau.choices = [('A', cau.dap_an_a), ('B', cau.dap_an_b), ('C', cau.dap_an_c), ('D', cau.dap_an_d)]

    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)
        
        # Ghi nhận hành vi nộp bài
        cheated = request.POST.get('strict_violation') == 'true'
        if cheated:
            logger.warning(f"User {request.user.username} violated exam rules (tab switch/blur) on exam {de.id}")

        # Xác định tư cách Official (Hợp lệ cho Leaderboard)
        # 1. Phải là chế độ 'thi_that'
        # 2. Không vi phạm quy chế (tab switch)
        # 3. Đây phải là lần đầu tiên thi thật HOẶC chưa từng xem đáp án trước đó của đề này
        from django.db.models import Q
        da_thi_that_hoac_xem_dap_an = KetQua.objects.filter(
            nguoi_dung=request.user, 
            de_thi=de
        ).filter(Q(che_do='thi_that') | Q(da_xem_dap_an=True)).exists()

        is_official = False
        if che_do == 'thi_that' and not cheated and not da_thi_that_hoac_xem_dap_an:
            is_official = True

        ket_qua = KetQua.objects.create(
            nguoi_dung=request.user,
            de_thi=de,
            tong_cau=cau_hoi_list.count(),
            thoi_gian_lam=int(request.POST.get('thoi_gian_lam', 0)),
            che_do=che_do,
            is_violated=cheated,
            is_official=is_official
        )

        tong_diem = 0
        tong_cau = cau_hoi_list.count()

        for cau in cau_hoi_list:
            tra_loi = TraLoi(ket_qua=ket_qua, cau_hoi=cau)
            dung = False
            diem = 0

            if cau.loai == 'tn':
                chon = request.POST.get(f'cau_{cau.id}', '').strip().upper()
                tra_loi.chon = chon
                dung = (chon == cau.dap_an_dung.strip().upper())
                diem = 1.0 if dung else 0.0

            elif cau.loai == 'dien':
                so_raw = request.POST.get(f'cau_{cau.id}', '').strip()
                tra_loi.so_dien = so_raw
                try:
                    # So sánh số với sai số 0.001
                    dung = abs(float(so_raw) - float(cau.dap_an_so)) < 0.001
                except (ValueError, TypeError):
                    dung = False
                diem = 1.0 if dung else 0.0

            elif cau.loai == 'ds':
                # Đúng/Sai: 4 ý độc lập
                chon_a = request.POST.get(f'cau_{cau.id}_a') == 'true'
                chon_b = request.POST.get(f'cau_{cau.id}_b') == 'true'
                chon_c = request.POST.get(f'cau_{cau.id}_c') == 'true'
                chon_d = request.POST.get(f'cau_{cau.id}_d') == 'true'
                
                tra_loi.chon_a = chon_a
                tra_loi.chon_b = chon_b
                tra_loi.chon_c = chon_c
                tra_loi.chon_d = chon_d

                so_dung = sum([
                    chon_a == cau.dung_sai_a,
                    chon_b == cau.dung_sai_b,
                    chon_c == cau.dung_sai_c,
                    chon_d == cau.dung_sai_d,
                ])
                
                # Biểu điểm MOET 2025: 1 ý=0.1, 2 ý=0.25, 3 ý=0.5, 4 ý=1.0
                diem_map = {0: 0.0, 1: 0.1, 2: 0.25, 3: 0.5, 4: 1.0}
                diem = diem_map.get(so_dung, 0.0)
                dung = (so_dung == 4)

            tra_loi.dung = dung
            tra_loi.diem_duoc = diem
            tra_loi.save()
            tong_diem += diem

        # Quy về thang điểm 10.0 (Strict rounding)
        if tong_cau > 0:
            diem_10 = round((tong_diem / tong_cau) * 10, 2)
        else:
            diem_10 = 0.0
            
        ket_qua.diem = diem_10
        ket_qua.save()

        # Update stats
        try:
            from .models import UserAnalytics
            analytics, _ = UserAnalytics.objects.get_or_create(nguoi_dung=request.user)
            analytics.cap_nhat_thong_ke()
            
            from apps.nguoi_dung.utils import check_and_award_badges
            check_and_award_badges(request.user)
        except Exception as e:
            logger.error(f"Error updating stats or badges: {e}")
        
        # Send exam result notification
        try:
            from apps.notifications.utils import notify_exam_result
            notify_exam_result(request.user, ket_qua)
        except Exception as e:
            logger.error(f"Error sending exam notification: {e}")

        return redirect('de_thi:ket_qua', kq_id=ket_qua.id)

    return render(request, 'de_thi/lam_bai.html', {
        'de': de,
        'cau_hoi_list': cau_hoi_list,
        'che_do': che_do,
    })

@login_required
def ket_qua(request, kq_id):
    kq = get_object_or_404(KetQua, id=kq_id, nguoi_dung=request.user)
    return render(request, 'de_thi/ket_qua.html', {'kq': kq})

@login_required
def xem_dap_an(request, kq_id):
    kq = get_object_or_404(KetQua, id=kq_id, nguoi_dung=request.user)
    
    if kq.diem <= 6:
        messages.error(request, 'Bạn cần đạt trên 6 điểm để xem đáp án chi tiết.')
        return redirect('de_thi:ket_qua', kq_id=kq.id)

    kq.da_xem_dap_an = True
    kq.save()
    tra_loi_list = kq.tra_loi.select_related('cau_hoi').all()
    return render(request, 'de_thi/xem_dap_an.html', {'kq': kq, 'tra_loi_list': tra_loi_list})

@login_required
def xoa_de_thi(request, de_id):
    if request.user.is_staff:
        de = get_object_or_404(DeThi, id=de_id)
    else:
        de = get_object_or_404(DeThi, id=de_id, creator=request.user)
    
    if request.method == 'POST':
        de.delete()
        messages.success(request, 'Đề thi đã được xóa!')
        return redirect('de_thi:danh_sach_de')
    return render(request, 'de_thi/xac_nhan_xoa.html', {'de': de})

@login_required
def bulk_add_questions(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, creator=request.user)
    
    if request.method == 'POST':
        form = BulkAddQuestionsForm(request.POST)
        if form.is_valid():
            questions_text = form.cleaned_data['questions_text']
            loai = form.cleaned_data['loai']
            lines = questions_text.strip().split('\n')
            
            success_count = 0
            error_lines = []
            
            for idx, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    if loai == 'tn':  # Trắc nghiệm ABCD
                        parts = line.split('|')
                        if len(parts) < 7:
                            error_lines.append(f"Dòng {idx}: Thiếu trường (cần 7 trường: nội_dung|A|B|C|D|đáp_án|giải_thích)")
                            continue
                        
                        noi_dung = parts[0].strip()
                        dap_an_a = parts[1].strip()
                        dap_an_b = parts[2].strip()
                        dap_an_c = parts[3].strip()
                        dap_an_d = parts[4].strip()
                        dap_an_dung = parts[5].strip().upper()
                        giai_thich = parts[6].strip()
                        
                        if dap_an_dung not in ['A', 'B', 'C', 'D']:
                            error_lines.append(f"Dòng {idx}: Đáp án đúng phải là A, B, C hoặc D")
                            continue
                        
                        CauHoi.objects.create(
                            de_thi=de,
                            loai='tn',
                            noi_dung=noi_dung,
                            dap_an_a=dap_an_a,
                            dap_an_b=dap_an_b,
                            dap_an_c=dap_an_c,
                            dap_an_d=dap_an_d,
                            dap_an_dung=dap_an_dung,
                            giai_thich=giai_thich
                        )
                    
                    elif loai == 'ds':  # Trắc nghiệm Đúng/Sai
                        parts = line.split('|')
                        if len(parts) < 6:
                            error_lines.append(f"Dòng {idx}: Thiếu trường (cần 6 trường: nội_dung|ý_A|ý_B|ý_C|ý_D|DS_A;DS_B;DS_C;DS_D|giải_thích)")
                            continue
                        
                        noi_dung = parts[0].strip()
                        y_a = parts[1].strip()
                        y_b = parts[2].strip()
                        y_c = parts[3].strip()
                        y_d = parts[4].strip()
                        dung_sai = parts[5].strip().upper().split(';')
                        giai_thich = parts[6].strip() if len(parts) > 6 else ''
                        
                        if len(dung_sai) != 4:
                            error_lines.append(f"Dòng {idx}: Đúng/Sai phải có 4 giá trị (D hoặc S), ngăn cách bằng ';'. Ví dụ: D;S;D;S")
                            continue
                        
                        dung_sai_a = dung_sai[0].strip() == 'D'
                        dung_sai_b = dung_sai[1].strip() == 'D'
                        dung_sai_c = dung_sai[2].strip() == 'D'
                        dung_sai_d = dung_sai[3].strip() == 'D'
                        
                        CauHoi.objects.create(
                            de_thi=de,
                            loai='ds',
                            noi_dung=noi_dung,
                            y_a=y_a,
                            y_b=y_b,
                            y_c=y_c,
                            y_d=y_d,
                            dung_sai_a=dung_sai_a,
                            dung_sai_b=dung_sai_b,
                            dung_sai_c=dung_sai_c,
                            dung_sai_d=dung_sai_d,
                            giai_thich=giai_thich
                        )
                    
                    elif loai == 'dien':  # Điền số
                        parts = line.split('|')
                        if len(parts) < 2:
                            error_lines.append(f"Dòng {idx}: Thiếu trường (cần 2-3 trường: nội_dung|đáp_án_số|giải_thích)")
                            continue
                        
                        noi_dung = parts[0].strip()
                        dap_an_so = parts[1].strip()
                        giai_thich = parts[2].strip() if len(parts) > 2 else ''
                        
                        try:
                            float(dap_an_so)
                        except ValueError:
                            error_lines.append(f"Dòng {idx}: Đáp án phải là số")
                            continue
                        
                        CauHoi.objects.create(
                            de_thi=de,
                            loai='dien',
                            noi_dung=noi_dung,
                            dap_an_so=dap_an_so,
                            giai_thich=giai_thich
                        )
                    
                    success_count += 1
                except Exception as e:
                    error_lines.append(f"Dòng {idx}: {str(e)}")
            
            if success_count > 0:
                messages.success(request, f'✅ Đã thêm {success_count} câu hỏi thành công!')
            
            if error_lines:
                error_msg = '\n'.join(error_lines[:5])
                if len(error_lines) > 5:
                    error_msg += f'\n... và {len(error_lines) - 5} lỗi khác'
                messages.error(request, f'⚠️ Lỗi:\n{error_msg}')
            
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
    else:
        form = BulkAddQuestionsForm()
    
    return render(request, 'de_thi/bulk_add_questions.html', {
        'de': de,
        'form': form
    })

@login_required
def import_de_thi(request):
    if request.method == 'POST':
        form = ImportDeThiForm(request.POST, request.FILES)
        if form.is_valid():
            ten_de = form.cleaned_data['ten']
            mon = form.cleaned_data['mon']
            csv_file = request.FILES['csv_file']
            
            try:
                # Tạo đề thi mới
                de = DeThi.objects.create(
                    ten=ten_de,
                    mon=mon,
                    creator=request.user,
                    is_custom=True
                )
                
                # Đọc CSV
                stream = csv_file.read().decode('utf-8')
                csv_reader = csv.reader(StringIO(stream))
                
                success_count = 0
                error_lines = []
                
                for row_idx, row in enumerate(csv_reader, 1):
                    if not row or not row[0].strip():
                        continue
                    
                    try:
                        # Cột đầu tiên là loại câu: tn, ds hoặc dien
                        loai_cau = row[0].strip().lower()
                        
                        # ──────── TRẮC NGHIỆM ABCD ────────
                        if loai_cau == 'tn':
                            if len(row) < 8:
                                error_lines.append(f"Dòng {row_idx}: Loại TN cần 8 cột (loại,nội_dung,A,B,C,D,đáp_án,giải_thích)")
                                continue
                            
                            noi_dung = row[1].strip()
                            dap_an_a = row[2].strip()
                            dap_an_b = row[3].strip()
                            dap_an_c = row[4].strip()
                            dap_an_d = row[5].strip()
                            dap_an_dung = row[6].strip().upper()
                            giai_thich = row[7].strip() if len(row) > 7 else ''
                            
                            if dap_an_dung not in ['A', 'B', 'C', 'D']:
                                error_lines.append(f"Dòng {row_idx}: Đáp án đúng phải là A, B, C hoặc D")
                                continue
                            
                            CauHoi.objects.create(
                                de_thi=de,
                                loai='tn',
                                noi_dung=noi_dung,
                                dap_an_a=dap_an_a,
                                dap_an_b=dap_an_b,
                                dap_an_c=dap_an_c,
                                dap_an_d=dap_an_d,
                                dap_an_dung=dap_an_dung,
                                giai_thich=giai_thich
                            )
                            success_count += 1
                        
                        # ──────── TRẮC NGHIỆM ĐÚNG/SAI ────────
                        elif loai_cau == 'ds':
                            if len(row) < 7:
                                error_lines.append(f"Dòng {row_idx}: Loại DS cần ít nhất 7 cột (loại,nội_dung,Ý_A,Ý_B,Ý_C,Ý_D,D/S,...)")
                                continue
                            
                            noi_dung = row[1].strip()
                            y_a = row[2].strip()
                            y_b = row[3].strip()
                            y_c = row[4].strip()
                            y_d = row[5].strip()
                            dung_sai_str = row[6].strip()
                            giai_thich = row[7].strip() if len(row) > 7 else ''
                            
                            # Parse D/S format: "D;D;S;S"
                            dung_sai_parts = dung_sai_str.split(';')
                            if len(dung_sai_parts) != 4:
                                error_lines.append(f"Dòng {row_idx}: Đáp án Đúng/Sai phải có 4 giá trị (D;D;S;S)")
                                continue
                            
                            try:
                                dung_sai_a = dung_sai_parts[0].strip().upper() == 'D'
                                dung_sai_b = dung_sai_parts[1].strip().upper() == 'D'
                                dung_sai_c = dung_sai_parts[2].strip().upper() == 'D'
                                dung_sai_d = dung_sai_parts[3].strip().upper() == 'D'
                            except:
                                error_lines.append(f"Dòng {row_idx}: Lỗi parsing Đúng/Sai")
                                continue
                            
                            CauHoi.objects.create(
                                de_thi=de,
                                loai='ds',
                                noi_dung=noi_dung,
                                y_a=y_a,
                                y_b=y_b,
                                y_c=y_c,
                                y_d=y_d,
                                dung_sai_a=dung_sai_a,
                                dung_sai_b=dung_sai_b,
                                dung_sai_c=dung_sai_c,
                                dung_sai_d=dung_sai_d,
                                giai_thich=giai_thich
                            )
                            success_count += 1
                        
                        # ──────── ĐIỀN SỐ ────────
                        elif loai_cau == 'dien':
                            if len(row) < 3:
                                error_lines.append(f"Dòng {row_idx}: Loại DIEN cần ít nhất 3 cột (loại,nội_dung,đáp_án,...)")
                                continue
                            
                            noi_dung = row[1].strip()
                            dap_an_so_str = row[2].strip()
                            giai_thich = row[3].strip() if len(row) > 3 else ''
                            
                            try:
                                # Validate và lưu dạng string
                                float(dap_an_so_str)  # Check có phải số không
                            except:
                                error_lines.append(f"Dòng {row_idx}: Đáp án phải là một số")
                                continue
                            
                            CauHoi.objects.create(
                                de_thi=de,
                                loai='dien',
                                noi_dung=noi_dung,
                                dap_an_so=dap_an_so_str,
                                giai_thich=giai_thich
                            )
                            success_count += 1
                        
                        else:
                            error_lines.append(f"Dòng {row_idx}: Loại câu '{loai_cau}' không hợp lệ (tn/ds/dien)")
                    
                    except Exception as e:
                        error_lines.append(f"Dòng {row_idx}: {str(e)}")
                
                if success_count > 0:
                    messages.success(request, f'✅ Import thành công! Đề thi "{ten_de}" với {success_count} câu hỏi')
                
                if error_lines:
                    error_msg = '\n'.join(error_lines[:5])
                    if len(error_lines) > 5:
                        error_msg += f'\n... và {len(error_lines) - 5} lỗi khác'
                    messages.warning(request, f'⚠️ Lỗi import:\n{error_msg}')
                
                return redirect('de_thi:them_cau_hoi', de_id=de.id)
                
            except Exception as e:
                messages.error(request, f'❌ Lỗi: {str(e)}')
    else:
        form = ImportDeThiForm()
    
    return render(request, 'de_thi/import_de_thi.html', {'form': form})


@login_required
def sua_de_thi(request, de_id):
    """Sửa thông tin đề thi"""
    if request.user.is_staff:
        de = get_object_or_404(DeThi, id=de_id)
    else:
        de = get_object_or_404(DeThi, id=de_id, creator=request.user)
    
    if request.method == 'POST':
        form = DeThiForm(request.POST, instance=de)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Cập nhật đề thi thành công!')
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
        else:
            messages.error(request, f'❌ Lỗi: {form.errors}')
    else:
        form = DeThiForm(instance=de)
    
    return render(request, 'de_thi/sua_de_thi.html', {'form': form, 'de': de})


@login_required
def sua_cau_hoi(request, cau_id):
    """Sửa câu hỏi"""
    cau = get_object_or_404(CauHoi, id=cau_id)
    de = cau.de_thi
    
    if request.user.is_staff:
        pass
    else:
        if request.user != de.creator:
            messages.error(request, 'Bạn không có quyền sửa câu hỏi này')
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
    
    if request.method == 'POST':
        loai = request.POST.get('loai', cau.loai)
        
        try:
            # Cập nhật thông tin chung
            cau.loai = loai
            cau.noi_dung = request.POST.get('noi_dung', '')
            cau.giai_thich = request.POST.get('giai_thich', '')
            
            if loai == 'tn':
                form = TracNghiemForm(request.POST, instance=cau)
                if form.is_valid():
                    form.save()
                    messages.success(request, '✅ Cập nhật câu hỏi trắc nghiệm thành công!')
                else:
                    messages.error(request, f'❌ Lỗi: {form.errors}')
                    return render(request, 'de_thi/sua_cau_hoi.html', {'cau': cau, 'de': de, 'form_tn': form})
            
            elif loai == 'ds':
                form = DungSaiForm(request.POST, instance=cau)
                if form.is_valid():
                    form.save()
                    messages.success(request, '✅ Cập nhật câu hỏi Đúng/Sai thành công!')
                else:
                    messages.error(request, f'❌ Lỗi: {form.errors}')
                    return render(request, 'de_thi/sua_cau_hoi.html', {'cau': cau, 'de': de, 'form_ds': form})
            
            elif loai == 'dien':
                form = DienSoForm(request.POST, instance=cau)
                if form.is_valid():
                    form.save()
                    messages.success(request, '✅ Cập nhật câu hỏi điền số thành công!')
                else:
                    messages.error(request, f'❌ Lỗi: {form.errors}')
                    return render(request, 'de_thi/sua_cau_hoi.html', {'cau': cau, 'de': de, 'form_dien': form})
            
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
        
        except Exception as e:
            messages.error(request, f'❌ Lỗi: {str(e)}')
    
    # GET request - show form
    form_tn = TracNghiemForm(instance=cau) if cau.loai == 'tn' else None
    form_ds = DungSaiForm(instance=cau) if cau.loai == 'ds' else None
    form_dien = DienSoForm(instance=cau) if cau.loai == 'dien' else None
    
    return render(request, 'de_thi/sua_cau_hoi.html', {
        'cau': cau,
        'de': de,
        'form_tn': form_tn,
        'form_ds': form_ds,
        'form_dien': form_dien
    })


@login_required
def xoa_cau_hoi(request, cau_id):
    """Xóa câu hỏi"""
    cau = get_object_or_404(CauHoi, id=cau_id)
    de = cau.de_thi
    
    if request.user.is_staff:
        pass
    else:
        if request.user != de.creator:
            messages.error(request, 'Bạn không có quyền xóa câu hỏi này')
            return redirect('de_thi:them_cau_hoi', de_id=de.id)
    
    if request.method == 'POST':
        cau.delete()
        messages.success(request, '✅ Xóa câu hỏi thành công!')
        return redirect('de_thi:them_cau_hoi', de_id=de.id)
    
    return render(request, 'de_thi/xac_nhan_xoa_cau.html', {'cau': cau, 'de': de})


# ════════════════════════════════════════════════════════════════
# ╔══════════════════════════════════════════════════════════════╗
# ║        LEARNING ANALYTICS VIEWS                             ║
# ╚══════════════════════════════════════════════════════════════╝
# ════════════════════════════════════════════════════════════════


@login_required
def phan_tich_hoc_tap(request):
    """
    Learning Analytics Dashboard - Chính
    Hiển thị đồ thị phân tích hiệu suất học tập của người dùng
    """
    # Get or create user analytics
    analytics, _ = UserAnalytics.objects.get_or_create(nguoi_dung=request.user)
    analytics.cap_nhat_thong_ke()
    
    # Get subject performance data
    subject_performance = SubjectPerformance.objects.filter(
        nguoi_dung=request.user
    ).select_related('mon').order_by('-diem_trung_binh')
    
    # Get exam history for linear chart
    exam_history = KetQua.objects.filter(
        nguoi_dung=request.user
    ).select_related('de_thi', 'de_thi__mon').order_by('ngay_lam')[:20]
    
    # Get question difficulty data
    question_difficulties = QuestionDifficulty.objects.filter(
        cau_hoi__de_thi__an=False
    ).select_related('cau_hoi', 'cau_hoi__de_thi').order_by('-do_kho')[:10]
    
    # Prepare data for charts
    exam_scores = [{'exam': exam.de_thi.ten[:20], 'score': exam.diem} for exam in exam_history]
    subject_scores = [{'subject': sp.mon.ten, 'score': sp.diem_trung_binh, 'count': sp.tong_bai_lam} 
                      for sp in subject_performance]
    
    context = {
        'analytics': analytics,
        'subject_performance': subject_performance,
        'exam_history': exam_history,
        'question_difficulties': question_difficulties,
        'exam_scores_json': json.dumps(exam_scores),
        'subject_scores_json': json.dumps(subject_scores),
        'total_exams': analytics.tong_bai_lam,
        'avg_score': round(analytics.diem_trung_binh, 2),
        'total_time_hours': analytics.tong_gio_lam // 60,
        'total_time_mins': analytics.tong_gio_lam % 60,
    }
    
    return render(request, 'de_thi/phan_tich_hoc_tap.html', context)


@login_required
def api_analytics_data(request):
    """
    API endpoint để lấy dữ liệu analytics cho chart.js updates
    """
    data_type = request.GET.get('type', 'overview')
    
    if data_type == 'exam_progress':
        # Lấy 30 bài thi gần nhất để biểu thị tiến độ
        exams = KetQua.objects.filter(
            nguoi_dung=request.user
        ).select_related('de_thi').order_by('-ngay_lam')[:30]
        
        data = {
            'labels': [e.de_thi.ten[:15] for e in reversed(exams)],
            'scores': [e.diem for e in reversed(exams)],
            'dates': [e.ngay_lam.strftime('%d/%m') for e in reversed(exams)],
        }
        return JsonResponse(data)
    
    elif data_type == 'subject_performance':
        # Performance by subject
        subjects = SubjectPerformance.objects.filter(
            nguoi_dung=request.user
        ).select_related('mon').order_by('-diem_trung_binh')
        
        data = {
            'labels': [s.mon.ten for s in subjects],
            'scores': [s.diem_trung_binh for s in subjects],
            'attempts': [s.tong_bai_lam for s in subjects],
        }
        return JsonResponse(data)
    
    elif data_type == 'question_difficulty':
        # Question difficulty distribution
        difficulties = QuestionDifficulty.objects.filter(
            cau_hoi__de_thi__an=False
        ).order_by('-do_kho')[:10]
        
        data = {
            'labels': [f'{d.cau_hoi.de_thi.ten[:12]} - Q{d.cau_hoi.id}' for d in difficulties],
            'difficulties': [round(d.do_kho, 2) for d in difficulties],
            'attempts': [d.tong_lan_hoi for d in difficulties],
        }
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid data type'}, status=400)


@login_required
def chi_tiet_mon_hoc(request, mon_id):
    """
    Subject Performance Details - Chi tiết hiệu suất theo từng môn học
    """
    mon = get_object_or_404(Mon, id=mon_id)
    
    # Get user's performance for this subject
    subject_perf, _ = SubjectPerformance.objects.get_or_create(
        nguoi_dung=request.user,
        mon=mon
    )
    subject_perf.cap_nhat_hieu_suat()
    
    # Get all exams taken for this subject
    exams = KetQua.objects.filter(
        nguoi_dung=request.user,
        de_thi__mon=mon
    ).select_related('de_thi').order_by('-ngay_lam')
    
    # Get questions and their difficulty
    questions = CauHoi.objects.filter(
        de_thi__mon=mon,
        de_thi__an=False
    ).select_related('difficulty', 'de_thi')
    
    # Calculate performance by question
    question_stats = []
    for q in questions:
        correct = TraLoi.objects.filter(
            cau_hoi=q,
            ket_qua__nguoi_dung=request.user,
            dung=True
        ).count()
        total = TraLoi.objects.filter(
            cau_hoi=q,
            ket_qua__nguoi_dung=request.user
        ).count()
        
        if total > 0:
            difficulty = q.difficulty if hasattr(q, 'difficulty') else None
            question_stats.append({
                'question': q,
                'correct': correct,
                'total': total,
                'rate': round((correct / total) * 100, 1),
                'difficulty': difficulty.do_kho if difficulty else 0.5,
            })
    
    # Sort by accuracy (worst first)
    question_stats.sort(key=lambda x: x['rate'])
    
    context = {
        'mon': mon,
        'subject_perf': subject_perf,
        'exams': exams,
        'questions_stats': question_stats,
        'total_score': subject_perf.diem_trung_binh,
        'total_exams': subject_perf.tong_bai_lam,
        'total_correct': subject_perf.so_dan_dung,
        'total_attempts': subject_perf.tong_dan_tra_loi,
    }
    
    return render(request, 'de_thi/chi_tiet_mon_hoc.html', context)


# ==================== FORUM VIEWS ====================

@login_required
def danh_sach_forum(request, cau_id):
    """List all discussion posts for a specific question"""
    cau_hoi = get_object_or_404(CauHoi, id=cau_id)
    posts = ForumPost.objects.filter(cau_hoi=cau_hoi).select_related(
        'tac_gia', 'best_answer_comment'
    ).prefetch_related(
        'comments', 'comments__replies'
    ).order_by('-ngay_tao')
    
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cau_hoi': cau_hoi,
        'page_obj': page_obj,
    }
    return render(request, 'de_thi/danh_sach_forum.html', context)


@login_required
def chi_tiet_forum(request, post_id):
    """View a single forum post with all comments and replies"""
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.select_related('tac_gia').prefetch_related('replies').order_by('-vote_count', 'ngay_tao')
    
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'de_thi/chi_tiet_forum.html', context)


@login_required
def tao_post_forum(request, cau_id):
    """Create a new forum discussion post for a question"""
    cau_hoi = get_object_or_404(CauHoi, id=cau_id)
    
    if request.method == 'POST':
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        
        if tieu_de and noi_dung:
            post = ForumPost.objects.create(
                cau_hoi=cau_hoi,
                tac_gia=request.user,
                tieu_de=tieu_de,
                noi_dung=noi_dung
            )
            messages.success(request, 'Bài viết đã được đăng!')
            return redirect('de_thi:chi_tiet_forum', post_id=post.id)
        else:
            messages.error(request, 'Vui lòng điền đầy đủ tiêu đề và nội dung.')
    
    context = {
        'cau_hoi': cau_hoi,
    }
    return render(request, 'de_thi/form_forum.html', context)


@login_required
def them_binh_luan(request, post_id):
    """Add a comment to a forum post"""
    post = get_object_or_404(ForumPost, id=post_id)
    
    if request.method == 'POST':
        noi_dung = request.POST.get('noi_dung')
        
        if noi_dung:
            comment = ForumComment.objects.create(
                bai_dang=post,
                tac_gia=request.user,
                noi_dung=noi_dung
            )
            # Update comment count
            post.so_binh_luan = post.comments.count()
            post.save()
            
            # Send notification to post author
            if post.tac_gia != request.user:
                try:
                    from apps.notifications.utils import notify_forum_reply
                    notify_forum_reply(post.tac_gia, comment, post)
                except Exception as e:
                    logger.error(f"Error sending forum notification: {e}")
            
            messages.success(request, 'Bình luận đã được thêm!')
            return redirect('de_thi:chi_tiet_forum', post_id=post.id)
        else:
            messages.error(request, 'Vui lòng nhập nội dung bình luận.')
    
    return redirect('de_thi:chi_tiet_forum', post_id=post.id)


@login_required
def them_tra_loi(request, comment_id):
    """Add a reply to a forum comment"""
    comment = get_object_or_404(ForumComment, id=comment_id)
    
    if request.method == 'POST':
        noi_dung = request.POST.get('noi_dung')
        
        if noi_dung:
            reply = ForumReply.objects.create(
                binh_luan=comment,
                tac_gia=request.user,
                noi_dung=noi_dung
            )
            
            # Send notification to comment author
            if comment.tac_gia != request.user:
                try:
                    from apps.notifications.utils import notify_forum_reply
                    notify_forum_reply(comment.tac_gia, reply, comment.bai_dang)
                except Exception as e:
                    logger.error(f"Error sending forum notification: {e}")
            
            messages.success(request, 'Trả lời đã được thêm!')
            return redirect('de_thi:chi_tiet_forum', post_id=comment.bai_dang.id)
        else:
            messages.error(request, 'Vui lòng nhập nội dung trả lời.')
    
    return redirect('de_thi:chi_tiet_forum', post_id=comment.bai_dang.id)


@login_required
def binh_chon(request):
    """AJAX endpoint for voting on posts, comments, and replies"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=400)
    
    try:
        data = json.loads(request.body)
        item_type = data.get('type')  # 'post', 'comment', 'reply'
        item_id = data.get('id')
        vote = data.get('vote')  # 1 or -1
        
        if vote not in (1, -1):
            return JsonResponse({'success': False, 'error': 'Invalid vote'})
        
        if item_type == 'post':
            item = get_object_or_404(ForumPost, id=item_id)
            vote_obj, created = PostVote.objects.get_or_create(
                nguoi_dung=request.user,
                bai_dang=item,
                defaults={'loai_bau': vote}
            )
            if not created:
                vote_obj.loai_bau = vote
                vote_obj.save()
            
            # Recalculate vote count
            item.vote_count = PostVote.objects.filter(bai_dang=item).aggregate(
                total=Sum('loai_bau')
            )['total'] or 0
            item.save()
        
        elif item_type == 'comment':
            item = get_object_or_404(ForumComment, id=item_id)
            vote_obj, created = PostVote.objects.get_or_create(
                nguoi_dung=request.user,
                binh_luan=item,
                defaults={'loai_bau': vote}
            )
            if not created:
                vote_obj.loai_bau = vote
                vote_obj.save()
            
            # Recalculate vote count
            item.vote_count = PostVote.objects.filter(binh_luan=item).aggregate(
                total=Sum('loai_bau')
            )['total'] or 0
            item.save()
        
        elif item_type == 'reply':
            item = get_object_or_404(ForumReply, id=item_id)
            vote_obj, created = PostVote.objects.get_or_create(
                nguoi_dung=request.user,
                tra_loi=item,
                defaults={'loai_bau': vote}
            )
            if not created:
                vote_obj.loai_bau = vote
                vote_obj.save()
            
            # Recalculate vote count
            item.vote_count = PostVote.objects.filter(tra_loi=item).aggregate(
                total=Sum('loai_bau')
            )['total'] or 0
            item.save()
        
        else:
            return JsonResponse({'success': False, 'error': 'Invalid type'})
        
        return JsonResponse({
            'success': True,
            'vote_count': item.vote_count
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def chon_cau_tra_loi_tot(request, comment_id):
    """Mark a comment as best answer (only post creator can do this)"""
    comment = get_object_or_404(ForumComment, id=comment_id)
    post = comment.bai_dang
    
    # Only post creator can mark best answer
    if post.tac_gia != request.user:
        messages.error(request, 'Chỉ có tác giả bài viết mới có thể chọn câu trả lời tốt nhất.')
        return redirect('de_thi:chi_tiet_forum', post_id=post.id)
    
    post.best_answer_comment = comment
    post.is_solved = True
    post.save()
    
    messages.success(request, 'Câu trả lời này đã được đánh dấu là tốt nhất!')
    return redirect('de_thi:chi_tiet_forum', post_id=post.id)