"""
URL configuration for SCD_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from devices import views
from users.views import UserRegisterView, ActivateUserView, UserEditView, home, DeleteUserAccount, dashboard
from django.contrib.auth import views as auth_views, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
# User views
    path('', home, name='home'),  # Ścieżka o nazwie 'home'
    path('register/', UserRegisterView.as_view(), name='register'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html'), name='change_password'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'), name='password_change_done'),
    path('accounts/delete-user', DeleteUserAccount.as_view(), name='delete_user'),
    path('edit-profile/', UserEditView.as_view(), name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_password.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_done.html'), name='password_reset_complete'),
    path('dashboard/', dashboard, name='dashboard'),

# device

     path('devices/', views.devices, name='devices'),
     path('devices/list/', views.device_list, name='device_list'),
     path('devices/create/success/', views.device_create_success, name='device_create_success'),
     path('devices/update/success/', views.device_update_success, name='device_update_success'),
     path('devices/delete/success/', views.device_delete_success, name='device_delete_success'),
     path('devices/create/<str:device_type>/', views.DeviceCreateView.as_view(), name='device_create'),
     path('device/update/<str:device_type>/<int:pk>/', views.DeviceUpdateView.as_view(), name='device_update'),
     path('devices/details/<str:device_type>/<int:device_id>/', views.DeviceDetailView.as_view(), name='device_detail'),
     path('devices/delete/<str:device_type>/<int:device_id>/', views.DeviceDeleteView.as_view(), name='device_delete'),
     path('devices/schedule/<str:device_type>/<int:device_id>/', views.device_schedule, name='device_schedule'),


# bulb
    path('bulbs/', views.bulb_list, name='bulb_list'),

# plug
    path('plugs/', views.plug_list, name='plug_list'),

# thermostat
    path('thermostat/', views.thermostat_list, name='thermostat_list'),

# curtain
    path('curtains/', views.curtain_list, name='curtain_list'),

# weather station
    path("weather_stations/", views.weather_station_list, name="weather_station_list"),

# lawn mower
    path('lawn_mowers', views.lawn_mower_list, name='lawn_mower_list'),

]



