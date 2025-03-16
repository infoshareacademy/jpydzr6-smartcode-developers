from django.contrib import admin
from django.urls import path, include
from ..devices import views
from . import views
from ..devices.views import bulb_list

app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home'), name='home'),
    path('devices/', include('devices.urls'), name='devices'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about_us/', views.about_us, name='about_us'),
    path('instruction', views.instruction, name='instruction'),
    path('registration/edit_profile/', views.UserEditView.as_view(template_name="registration/edit_profile.html"), name='edit_profile'),
    path('bulbs/bulb_list/', include('devices.urls'), name='bulb_list'),
]


