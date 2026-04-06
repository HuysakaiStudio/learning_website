from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DeThi, CauHoi, KetQua, TraLoi
import json

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

    if request.method == 'POST':
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
                # Đúng/Sai: mỗi ý 0.25 điểm, đúng cả 4 ý = 1 điểm
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
                # Thang điểm: 2 đúng=0.1, 3 đúng=0.25, 4 đúng=1.0
                if so_dung == 4:
                    diem = 1.0
                elif so_dung == 3:
                    diem = 0.25
                elif so_dung == 2:
                    diem = 0.1
                else:
                    diem = 0
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
    kq.da_xem_dap_an = True
    kq.save()
    tra_loi_list = kq.tra_loi.select_related('cau_hoi').all()
    return render(request, 'de_thi/xem_dap_an.html', {'kq': kq, 'tra_loi_list': tra_loi_list})