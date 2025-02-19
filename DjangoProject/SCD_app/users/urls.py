from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('signup', views.signup),
    path('login', views.login),
]