from django.urls import path, include
from . import views


urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('log_in/', views.login, name='log_in'),
    path('accounts/', include('django.contrib.auth.urls')),
]

