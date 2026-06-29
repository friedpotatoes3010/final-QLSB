from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    # Khai báo các vai trò trong hệ thống
    ROLE_CHOICES = (
        ('customer', 'Khách hàng'),
        ('owner', 'Chủ sân bóng'),
    )
    
    # Kết nối 1-1 với model User mặc định của Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Tạo profile mặc định khi User được tạo bởi admin hoặc đăng ký
        UserProfile.objects.create(user=instance)