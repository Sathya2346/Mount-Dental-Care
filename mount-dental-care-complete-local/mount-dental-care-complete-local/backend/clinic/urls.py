from django.urls import path
from .views import *
urlpatterns=[
 path('site/',site_data),path('auth/register/',register),path('auth/login/',login),path('auth/me/',me),
 path('appointments/request-otp/',request_appointment_otp),path('appointments/verify-otp/',verify_appointment_otp),path('user/dashboard/',user_dashboard),path('notifications/<int:pk>/read/',mark_notification_read),
]
