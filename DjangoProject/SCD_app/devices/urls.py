from django.contrib import admin
from django.urls import path, include
from ..devices import views


app_name = 'devices'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('users/', include('users.urls'), name='users'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


