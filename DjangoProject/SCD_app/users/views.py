from base64 import urlsafe_b64decode

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

from . forms import CreateUserForm
from .tokens import account_activation_token

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Your account has been confirmed. You can now login.')
        return redirect('login')
    else:
        messages.error(request, 'Activation failed!')

    return redirect('homepage')

def activateEmail(request, user, email):
    mail_subject = 'Activate your account'
    message = render_to_string('activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(request, "Activation email sent.")
    else:
        messages.error(request, "Activation email failed.")


def homepage(request):
    pass


def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data['email'])
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'register_form': form}

    return render(request, "templates/register.html", context=context)


@login_required #(login_url is required)
def dashboard(request):
    return render(request, 'base_templates/dashboard.html')


