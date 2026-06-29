Football Pitch Project

Hướng dẫn nhanh — Clone & chạy dự án

Yêu cầu
- Python 3.x
- pip

Các bước

1. Clone repository
```
git clone https://github.com/23110182vju/football-booking-system.git
cd football-booking-system
```

2. Tạo virtual environment và kích hoạt
```
python3 -m venv .venv
source .venv/bin/activate
```

3. Cài dependencies
```
pip install -r requirements.txt
```

4. Áp migrations
```
python manage.py migrate
```

5. (Tùy chọn) Tạo superuser
```
python manage.py createsuperuser
```

6. Chạy server
```
python manage.py runserver
```

tk mk admin: admin123 - 12345678 (đang để cả role owner)
tk test (khách hàng): 123 - 123
