from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pitch, Booking
from .forms import BookingForm
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import PitchForm
from apps.accounts.models import UserProfile

# 1. View xem danh sách tất cả sân bóng (Dành cho cả khách vãng lai và thành viên)
class PitchListView(ListView):
    model = Pitch
    template_name = 'pitches/pitch_list.html'
    context_object_name = 'pitches'

# 2. View xem chi tiết sân và xử lý đặt sân
class PitchDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pitch = get_object_or_404(Pitch, pk=pk)
        form = BookingForm()
        # Lấy các lịch đã được duyệt của sân này để hiển thị cho người dùng né khung giờ đó ra
        approved_bookings = pitch.bookings.filter(status='approved').order_by('booking_date', 'start_time')
        
        context = {
            'pitch': pitch,
            'form': form,
            'approved_bookings': approved_bookings
        }
        return render(request, 'pitches/pitch_detail.html', context)

    def post(self, request, pk):
        pitch = get_object_or_404(Pitch, pk=pk)
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.pitch = pitch
            
            # Tính toán tổng tiền dựa trên số giờ thuê
            start_dt = datetime.combine(booking.booking_date, booking.start_time)
            end_dt = datetime.combine(booking.booking_date, booking.end_time)
            duration_hours = Decimal((end_dt - start_dt).total_seconds() / 3600)
            booking.total_price = duration_hours * pitch.price_per_hour
            
            # Kiểm tra trùng lịch trực tiếp trong DB trước khi lưu (Chặn Overbooking tuyệt đối)
            overlapping = Booking.objects.filter(
                pitch=pitch,
                booking_date=booking.booking_date,
                status='approved',
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time
            )
            
            if overlapping.exists():
                form.add_error(None, "Khung giờ này đã có người đặt và được duyệt trước đó! Vui lòng chọn giờ khác.")
            else:
                booking.save()
                return redirect('customer_bookings')
                
        approved_bookings = pitch.bookings.filter(status='approved').order_by('booking_date', 'start_time')
        return render(request, 'pitches/pitch_detail.html', {'pitch': pitch, 'form': form, 'approved_bookings': approved_bookings})

# 3. View hiển thị danh sách đơn đặt của Khách hàng (Customer)
class CustomerBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'pitches/customer_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Chỉ lấy các đơn hàng do chính User đang đăng nhập đặt
        return Booking.objects.filter(customer=self.request.user).order_by('-created_at')

# 4. View Dashboard dành cho Chủ sân (Owner) để duyệt hoặc hủy đơn đặt
class OwnerDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'pitches/owner_dashboard.html'
    context_object_name = 'bookings'

    def test_func(self):
        # Chỉ cho phép user có role 'owner' truy cập
        try:
            return self.request.user.profile.role == 'owner'
        except Exception:
            return False

    def get_queryset(self):
        # Lấy tất cả đơn đặt của các sân thuộc sở hữu của chủ sân này
        return Booking.objects.filter(pitch__owner=self.request.user).order_by('-created_at')

# 5. Xử lý đổi trạng thái đơn hàng nhanh (Duyệt/Hủy)
class UpdateBookingStatusView(LoginRequiredMixin, View):
    def post(self, request, booking_id, action):
        booking = get_object_or_404(Booking, id=booking_id, pitch__owner=request.user)
        if action == 'approve':
            # Trước khi duyệt, kiểm tra xem đã có đơn nào được duyệt trùng khung giờ chưa
            overlapping = Booking.objects.filter(
                pitch=booking.pitch,
                booking_date=booking.booking_date,
                status='approved',
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time
            ).exclude(id=booking.id)

            if overlapping.exists():
                messages.error(request, 'Không thể duyệt đơn: trùng khung giờ với đơn đã được duyệt trước đó.')
                return redirect('owner_dashboard')

            booking.status = 'approved'
        elif action == 'cancel':
            booking.status = 'canceled'
        booking.save()
        return redirect('owner_dashboard')
    
    # Dashboard dành cho Admin hệ thống
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):

        total_users = User.objects.count()

        total_owners = UserProfile.objects.filter(
            role='owner'
        ).count()

        total_customers = UserProfile.objects.filter(
            role='customer'
        ).count()

        total_pitches = Pitch.objects.count()

        total_bookings = Booking.objects.count()

        context = {
            'total_users': total_users,
            'total_owners': total_owners,
            'total_customers': total_customers,
            'total_pitches': total_pitches,
            'total_bookings': total_bookings,
        }

        return render(
            request,
            'admin_panel/dashboard.html',
            context
        )

# Quản lý người dùng dành cho Admin
class AdminUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'admin_panel/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, user_id):

        user = get_object_or_404(User, id=user_id)

        # Không cho admin tự xóa chính mình
        if user == request.user:
            messages.error(
                request,
                'Không thể xóa chính tài khoản Admin đang đăng nhập.'
            )
            return redirect('admin_users')

        user.delete()

        messages.success(
            request,
            'Đã xóa tài khoản thành công.'
        )

        return redirect('admin_users')
    
class CreatePitchView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        profile = getattr(request.user, 'profile', None)

        if not profile or profile.role != 'owner':
            messages.error(
                request,
                'Chỉ chủ sân mới được đăng sân.'
            )
            return redirect('pitch_list')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        form = PitchForm()

        return render(
            request,
            'pitches/create_pitch.html',
            {'form': form}
        )

    def post(self, request):

        form = PitchForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            pitch = form.save(commit=False)
            pitch.owner = request.user
            pitch.save()

            messages.success(
                request,
                'Đăng sân thành công.'
            )

            return redirect('my_pitches')

        print(form.errors)

        messages.error(
            request,
            'Có lỗi xảy ra khi đăng sân.'
        )

        return render(
            request,
            'pitches/create_pitch.html',
            {'form': form}
        )

class MyPitchesView(LoginRequiredMixin, View):

    def get(self, request):

        # Admin xem tất cả sân
        if request.user.is_superuser:
            pitches = Pitch.objects.all().order_by("-id")

        else:
            profile = getattr(request.user, 'profile', None)

            if not profile or profile.role != 'owner':
                messages.error(request, 'Bạn không có quyền truy cập.')
                return redirect('pitch_list')

            pitches = Pitch.objects.filter(owner=request.user)

        return render(
            request,
            'pitches/my_pitches.html',
            {
                'pitches': pitches
            }
        )
    
class UpdatePitchView(LoginRequiredMixin, View):

    def get(self, request, pk):
        if request.user.is_superuser:
            pitch = get_object_or_404(Pitch, pk=pk)
        else:
            pitch = get_object_or_404(
                Pitch,
                pk=pk,
                owner=request.user
           )

        form = PitchForm(instance=pitch)

        return render(
            request,
            'pitches/edit_pitch.html',
            {
                'form': form,
                'pitch': pitch
            }
        )

    def post(self, request, pk):

        pitch = get_object_or_404(
            Pitch,
            pk=pk,
            owner=request.user
        )

        form = PitchForm(
            request.POST,
            request.FILES,
            instance=pitch
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Cập nhật sân thành công.'
            )

            return redirect('my_pitches')

        return render(
            request,
            'pitches/edit_pitch.html',
            {
                'form': form,
                'pitch': pitch
            }
        )
    
class DeletePitchView(LoginRequiredMixin, View):

    def post(self, request, pk):

        if request.user.is_superuser:
            pitch = get_object_or_404(Pitch, pk=pk)
        else:
            pitch = get_object_or_404(
                Pitch,
                pk=pk,
                owner=request.user
            )

        pitch.delete()

        messages.success(
            request,
            'Đã xóa sân.'
        )

        return redirect('my_pitches')
    
class AdminPitchListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Pitch
    template_name = "pitches/my_pitches.html"
    context_object_name = "pitches"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return Pitch.objects.all().order_by("-id")