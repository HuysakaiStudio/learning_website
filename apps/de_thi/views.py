from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DeThi, CauHoi, KetQua, TraLoi
from .forms import DeThiForm, TracNghiemForm, DungSaiForm, DienSoForm, BulkAddQuestionsForm, ImportDeThiForm
import json
import csv
from io import StringIO

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
    de_list = DeThi.objects.filter(an=False)
    return render(request, 'de_thi/danh_sach_de.html', {'de_list': de_list})

@login_required
def chon_che_do(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, an=False)
    return render(request, 'de_thi/chon_che_do.html', {'de': de})

@login_required
def lam_bai(request, de_id):
    de = get_object_or_404(DeThi, id=de_id, an=False)
    che_do = request.GET.get('che_do', 'luyen_tap')
    cau_hoi_list = de.cau_hoi.all()
    # Sắp xếp và tiền xử lý dữ liệu câu hỏi
    sorted_cau_hoi = []
    for loai in ['tn', 'ds', 'dien']:
        cau_list = cau_hoi_list.filter(loai=loai)
        for cau in cau_list:
            if cau.loai == 'tn':
                # Chuẩn bị dữ liệu trắc nghiệm
                choices = [('A', cau.dap_an_a), ('B', cau.dap_an_b), ('C', cau.dap_an_c), ('D', cau.dap_an_d)]
                cau.choices = choices
            sorted_cau_hoi.append(cau)

    if request.method == 'POST':
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"POST data: {request.POST}")

        ket_qua = KetQua.objects.create(
            nguoi_dung=request.user,
            de_thi=de,
            tong_cau=cau_hoi_list.count(),
            thoi_gian_lam=int(request.POST.get('thoi_gian_lam', 0)),
            che_do=che_do,
        )

        tong_diem = 0
        tong_cau = cau_hoi_list.count()

        for cau in cau_hoi_list:
            tra_loi = TraLoi(ket_qua=ket_qua, cau_hoi=cau)
            dung = False
            diem = 0

            if cau.loai == 'tn':
                chon = request.POST.get(f'cau_{cau.id}', '')
                tra_loi.chon = chon
                dung = (chon == cau.dap_an_dung)
                diem = 1 if dung else 0

            elif cau.loai == 'dien':
                so = request.POST.get(f'cau_{cau.id}', '').strip()
                tra_loi.so_dien = so
                try:
                    dung = abs(float(so) - float(cau.dap_an_so)) < 0.001
                except:
                    dung = False
                diem = 1 if dung else 0

            elif cau.loai == 'ds':
                # Đúng/Sai: tính điểm dựa trên số ý đúng (tối đa 1.0)
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
                # Bảng điểm: 1 ý đúng=0.1, 2 ý đúng=0.25, 3 ý đúng=0.5, 4 ý đúng=1.0
                diem_map = {0: 0, 1: 0.1, 2: 0.25, 3: 0.5, 4: 1.0}
                diem = diem_map.get(so_dung, 0)
                dung = (so_dung == 4)

            tra_loi.dung = dung
            tra_loi.diem_duoc = diem
            tra_loi.save()
            tong_diem += diem

        # Quy về thang 10
        diem_10 = round((tong_diem / tong_cau) * 10, 2) if tong_cau > 0 else 0
        ket_qua.diem = diem_10
        ket_qua.save()

        return redirect('de_thi:ket_qua', kq_id=ket_qua.id)

    return render(request, 'de_thi/lam_bai.html', {
        'de': de,
        'cau_hoi_list': sorted_cau_hoi,
        'che_do': che_do,
    })

@login_required
def ket_qua(request, kq_id):
    kq = get_object_or_404(KetQua, id=kq_id, nguoi_dung=request.user)
    return render(request, 'de_thi/ket_qua.html', {'kq': kq})

@login_required
def xem_dap_an(request, kq_id):
    kq = get_object_or_404(KetQua, id=kq_id, nguoi_dung=request.user)
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