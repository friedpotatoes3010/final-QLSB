from django.contrib import admin
from .models import Pitch, Booking

@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'price_per_hour'
    )

    search_fields = (
        'name',
        'address'
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'pitch',
        'booking_date',
        'status'
    )

    list_filter = (
        'status',
        'booking_date'
    )