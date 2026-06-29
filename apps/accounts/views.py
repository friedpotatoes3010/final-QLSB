from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from .models import UserProfile

# View xử lý Đăng ký tài khoản
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Lưu tài khoản User trước (chưa commit vào DB để ẩn mật khẩu)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Tạo hoặc cập nhật UserProfile để lưu vai trò (Role) và SĐT
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = form.cleaned_data.get('role', profile.role)
            profile.phone_number = form.cleaned_data.get('phone_number', profile.phone_number)
            profile.save()
            
            # Đăng nhập luôn sau khi đăng ký thành công
            login(request, user)
            return redirect('pitch_list') # Sau này sẽ nhảy về trang danh sách sân bóng
        return render(request, 'accounts/register.html', {'form': form})

# View xử lý Đăng nhập tài khoản
class LoginView(View):
    def get(self, request):
        form = LoginForm(request)
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pitch_list')
        return render(request, 'accounts/login.html', {'form': form})

# View xử lý Đăng xuất
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')