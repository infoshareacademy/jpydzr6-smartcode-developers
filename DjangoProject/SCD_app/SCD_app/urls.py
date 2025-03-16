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
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/<int:pk>/edit/', views.device_update, name='device_update'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),

# bulb
    path('bulbs/', views.bulb_list, name='bulb_list'),
    path('bulbs/<int:pk>/', views.bulb_detail, name='bulb_detail'),
    path('bulbs/add/', views.bulb_create, name='bulb_create'),
    path('bulbs/<int:pk>/edit/', views.bulb_update, name='bulb_update'),
    path('bulbs/<int:pk>/delete/', views.bulb_delete, name='bulb_delete'),
# plug
    path('plugs/', views.plug_list, name='plug_list'),
    path('plugs/<int:plug_id>/', views.plug_detail, name='plug_detail'),
    path('plugs/add/', views.plug_create, name='plug_create'),
    path('plugs/<int:plug_id>/edit/', views.plug_update, name='plug_update'),
    path('plugs/<int:plug_id>/delete/', views.plug_delete, name='plug_delete'),
# thermostat
    path('thermostat/', views.thermostat_list, name='thermostat_list'),
    path('thermostat/<int:pk>/', views.thermostat_detail, name='thermostat_detail'),
    path('thermostat/add/', views.thermostat_create, name='thermostat_create'),
    path('thermostat/<int:pk>/edit/', views.thermostat_update, name='thermostat_update'),
    path('thermostat/<int:pk>/delete/', views.thermostat_delete, name='thermostat_delete'),
# curtain
    path('curtains/', views.curtain_list, name='curtain_list'),
    path('curtains/<int:pk>/', views.curtain_detail, name='curtain_detail'),
    path('curtains/add/', views.curtain_create, name='curtain_create'),
    path('curtains/<int:pk>/edit/', views.curtain_update, name='curtain_update'),
    path('curtains/<int:pk>/delete/', views.curtain_delete, name='curtain_delete'),
# weather station
    path("weather_stations/", views.weather_station_list, name="weather_station_list"),
    path("weather_stations/<int:pk>/", views.weather_station_detail, name="weather_station_detail"),
    path("weather_stations/add/", views.weather_station_create, name="weather_station_create"),
    path("weather_stations/<int:pk>/edit/", views.weather_station_update, name="weather_station_update"),
    path("weather_stations/<int:pk>/delete/", views.weather_station_delete, name="weather_station_delete"),
# lawn mower
    path('lawn_mowers', views.lawn_mower_list, name='lawn_mower_list'),
    path('lawn_mowers/<int:pk>/', views.lawn_mower_detail, name='lawn_mower_detail'),
    path('lawn_mowers/add/', views.lawn_mower_create, name='lawn_mower_create'),
    path('lawn_mowers/<int:pk>/edit', views.lawn_mower_update, name='lawn_mower_update'),
    path('lawn_mowers/<int:pk>/delete/', views.lawn_mower_delete, name='lawn_mower_delete'),

]



