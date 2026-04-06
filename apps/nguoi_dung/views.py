from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def dang_ky(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}! Đăng ký thành công 🎉')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'nguoi_dung/dang_ky.html', {'form': form})

def dang_nhap(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Chào mừng trở lại, {user.username}! 👋')
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = AuthenticationForm()
    return render(request, 'nguoi_dung/dang_nhap.html', {'form': form})

def dang_xuat(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('home')