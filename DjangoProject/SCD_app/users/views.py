from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.template.response import TemplateResponse
from validators import domain
from django.urls import reverse

from . forms import CreateUserForm
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        login(request, user)

        messages.success(request, 'Your account has been confirmed. You can now login.')
        return redirect(reverse('login'))
    else:
        messages.error(request, 'Activation failed!')
        return redirect('homepage')


def homepage(request):
    pass
    #return render(request, 'base_templates/homepage.html')


def log_in(request):
    pass


def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, "homepage.html", {'messages': messages_to_display})


def register(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('templates/activate_account.html',{"user": user,
                                                                           "domain": current_site.domain,
                                                                           "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                                           "token": account_activation_token.make_token(user)})
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Check your email to complete the registration.')
            return redirect(index)
    return render(request, "templates/register.html", {'form': form})


@login_required #(login_url needs to be added)
def dashboard(request):
    pass
    #return render(request, 'base_templates/dashboard.html')


