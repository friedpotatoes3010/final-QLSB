from django.db import models
from django.contrib.auth.models import User

class Pitch(models.Model):
    PITCH_TYPE_CHOICES = (
        ('5', '5 người'),
        ('7', '7 người'),
        ('11', '11 người'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pitches', verbose_name="Chủ sân")
    name = models.CharField(max_length=100, verbose_name="Tên sân bóng")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")
    pitch_type = models.CharField(max_length=2, choices=PITCH_TYPE_CHOICES, default='5', verbose_name="Loại sân")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá thuê (VND/Giờ)")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả chi tiết")
    image = models.ImageField(upload_to='pitch_images/', blank=True, null=True, verbose_name="Hình ảnh sân")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_pitch_type_display()})"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('canceled', 'Đã hủy'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Khách hàng")
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE, related_name='bookings', verbose_name="Sân bóng")
    booking_date = models.DateField(verbose_name="Ngày đặt")
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng tiền thanh toán")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} đặt {self.pitch.name} ngày {self.booking_date}"