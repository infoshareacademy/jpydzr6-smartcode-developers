from django.urls import path, include
from . import views

urlpatterns = [
    path('users/dashboard', views.dashboard),
    path('log_out/', include('users.urls', namespace='log_out')),
    path('change_password/', include('users.urls', namespace='change_password')),
    path('device_form/', include('devices.urls', namespace='device_form')),
    path('device_confirm_delete/', include('devices.urls', namespace='device_confirm_delete')),
    path('device_delete/', include('devices.urls', namespace='device_delete')),
    path('device_detail/', include('devices.urls', namespace='device_detail')),
    path('device_list/', include('devices.urls', namespace='device_list')),
    ]