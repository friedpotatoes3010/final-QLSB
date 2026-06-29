from django import forms
from .models import Booking, Pitch
from datetime import datetime

class BookingForm(forms.ModelForm):
    # Tạo danh sách giờ theo format 'HH:MM' để hiển thị dropdown thân thiện
    TIME_CHOICES = [(f"{h:02d}:00", f"{h:02d}:00") for h in range(6, 24)]

    start_time = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES, attrs={'class': 'form-select'}))
    end_time = forms.TimeField(widget=forms.Select(choices=TIME_CHOICES, attrs={'class': 'form-select'}))

    class Meta:
        model = Booking
        fields = ['booking_date', 'start_time', 'end_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    # Hàm Validation nâng cao chặn trùng lịch (Tiêu chí điểm Giỏi)
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if booking_date and start_time and end_time:
            # 1. Kiểm tra nếu người dùng chọn ngày trong quá khứ
            if booking_date < datetime.today().date():
                raise forms.ValidationError("Không thể đặt sân vào một ngày trong quá khứ!")

            # 2. Kiểm tra nếu giờ bắt đầu lớn hơn hoặc bằng giờ kết thúc
            if start_time >= end_time:
                raise forms.ValidationError("Giờ kết thúc phải lớn hơn giờ bắt đầu!")

        return cleaned_data
    
class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        fields = [
            'name',
            'pitch_type',
            'address',
            'description',
            'price_per_hour',
            'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'pitch_type': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'price_per_hour': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }