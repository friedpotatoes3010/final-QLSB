from django.urls import path
from .views import AdminDashboardView
from .views import (
    PitchListView, PitchDetailView, CustomerBookingsView, 
    OwnerDashboardView, UpdateBookingStatusView,
    AdminUserListView, DeleteUserView, MyPitchesView,
    UpdatePitchView, DeletePitchView, CreatePitchView,
)


urlpatterns = [
    path('', PitchListView.as_view(), name='pitch_list'),
    path('pitch/<int:pk>/', PitchDetailView.as_view(), name='pitch_detail'),
    path('my-bookings/', CustomerBookingsView.as_view(), name='customer_bookings'),
    path('dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('booking/<int:booking_id>/<str:action>/', UpdateBookingStatusView.as_view(), name='update_booking'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/users/', AdminUserListView.as_view(), name='admin_users'), 
    path('admin-dashboard/users/delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user') ,
    path(
    'my-pitches/',
    MyPitchesView.as_view(),
    name='my_pitches'
),

path(
    'pitch/<int:pk>/edit/',
    UpdatePitchView.as_view(),
    name='edit_pitch'
),

path(
    'pitch/<int:pk>/delete/',
    DeletePitchView.as_view(),
    name='delete_pitch'
),
path(
    'pitch/create/',
    CreatePitchView.as_view(),
    name='create_pitch'
),
]