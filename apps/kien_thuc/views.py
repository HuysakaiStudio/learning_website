from django.shortcuts import render, redirect, get_object_or_404
from .models import Mon, BaiViet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages

def danh_sach_mon(request):
    mon_list = Mon.objects.all()
    return render(request, 'kien_thuc/danh_sach_mon.html', {'mon_list': mon_list})

def bai_viet_theo_mon(request, mon_id):
    mon = get_object_or_404(Mon, id=mon_id)
    bai_viet_list = mon.bai_viet.all()
    return render(request, 'kien_thuc/bai_viet_theo_mon.html', {
        'mon': mon,
        'bai_viet_list': bai_viet_list
    })

def chi_tiet_bai_viet(request, bai_id):
    bai = get_object_or_404(BaiViet, id=bai_id)
    return render(request, 'kien_thuc/chi_tiet_bai_viet.html', {'bai': bai})
def la_admin(user):
    return user.is_authenticated and user.is_staff
@user_passes_test(la_admin, login_url='/nguoi-dung/dang-nhap/')
def tao_bai_viet(request):
    mon_list = Mon.objects.all()
    
    if request.method == 'POST':
        mon_id = request.POST.get('mon')
        tieu_de = request.POST.get('tieu_de', '').strip()
        noi_dung = request.POST.get('noi_dung', '').strip()
        thu_tu = request.POST.get('thu_tu', 0)

        if not mon_id or not tieu_de or not noi_dung:
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
        else:
            mon = get_object_or_404(Mon, id=mon_id)
            BaiViet.objects.create(
                mon=mon,
                tieu_de=tieu_de,
                noi_dung=noi_dung,
                thu_tu=thu_tu
            )
            messages.success(request, f'Đã tạo bài viết "{tieu_de}" thành công! ✅')
            return redirect('kien_thuc:bai_viet_theo_mon', mon_id=mon.id)

    return render(request, 'kien_thuc/tao_bai_viet.html', {'mon_list': mon_list})
@user_passes_test(la_admin, login_url='/nguoi-dung/dang-nhap/')
def xoa_bai_viet(request, bai_id):
    bai = get_object_or_404(BaiViet, id=bai_id)
    mon_id = bai.mon.id
    if request.method == 'POST':
        ten = bai.tieu_de
        bai.delete()
        messages.success(request, f'Đã xóa bài viết "{ten}" ✅')
        return redirect('kien_thuc:bai_viet_theo_mon', mon_id=mon_id)
    return render(request, 'kien_thuc/xac_nhan_xoa.html', {'bai': bai})