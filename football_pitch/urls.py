from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Trang quản trị tối cao của hệ thống
    path('admin/', admin.site.urls),
    
    # Kết nối các đường dẫn URL của từng app chức năng
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.pitches.urls')), # Để trống '' để app pitches làm trang chủ mặc định
]

# Cấu hình giúp Django đọc và hiển thị được file ảnh trong thư mục media khi phát triển dưới local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)