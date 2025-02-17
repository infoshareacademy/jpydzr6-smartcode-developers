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

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
# device
    path('devices/', views.devices, name='devices'),
    path('devices/list/', views.device_list, name='device_list'),
    path('devices/<int:device_id>/', views.device_detail, name='device_detail'),
    path('devices/add/', views.add_device, name='add_device'),
# bulb
    path('bulbs/', views.bulb_list, name='bulb_list'),
    path('bulbs/<int:pk>/', views.bulb_detail, name='bulb_detail'),
    path('bulbs/add/', views.bulb_create, name='bulb_create'),
    path('bulbs/<int:pk>/edit/', views.bulb_update, name='bulb_update'),
    path('bulbs/<int:pk>/delete/', views.bulb_delete, name='bulb_delete'),
# plug
    path('plugs/', views.plug_list, name='plug_list'),
    path('plugs/add/', views.plug_create, name='plug_create'),
    path('plugs/<int:plug_id>/', views.plug_detail, name='plug_detail'),
    path('plugs/<int:plug_id>/edit/', views.plug_update, name='plug_update'),
    path('plugs/<int:plug_id>/delete/', views.plug_delete, name='plug_delete'),
# thermostat
    path('thermostat/', views.thermostat_status_list, name='thermostat_list'),
    path('thermostat/add/', views.thermostat_status_create, name='thermostat_create'),
    path('thermostat/edit/<int:pk>/', views.thermostat_status_edit, name='thermostat_edit'),
    path('thermostat/delete/<int:pk>/', views.thermostat_status_delete, name='thermostat_delete'),

]



