from django.urls import path, include
from . import views


urlpatterns = [
    path('homepage/', views.dashboard, name='homepage'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

