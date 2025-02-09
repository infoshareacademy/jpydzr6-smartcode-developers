from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth import login
from .models import CustomUser  # Import modelu użytkownika
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    context = {
        'message': 'Welcome to the Home Page!'
    }
    return render(request, 'home.html', context)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.activation_token = get_random_string(64)
        user.save()
        activation_link = self.request.build_absolute_uri(reverse_lazy('activate', args=[user.activation_token]))
        send_mail('Activate your account', f'Click the link to activate your account: {activation_link}',
                  'noreply@scd.com', [user.email])
        return redirect('login')

class ActivateUserView(View):
    def get(self, request, token):
        user = get_object_or_404(CustomUser, activation_token=token, is_active=False)
        user.is_active = True
        user.activation_token = None
        user.save()
        login(request, user)
        return redirect('home')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')

class UserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Nasza dodatkowa logika (np. wysłanie e-maila)
        user = form.save()
        send_mail('Your profile has been updated', f'Hello {user.username}, your profile has been successfully updated.', 'noreply@scd.com', [user.email])

        # Wywołanie domyślnej logiki UpdateView (zapisanie danych i przekierowanie)
        return super().form_valid(form)