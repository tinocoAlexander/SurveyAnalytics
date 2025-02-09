from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, AuthenticationForm
from .decorators import anonymous_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

@anonymous_required(redirect_url='errors:error_400')
def login(request):
    title = "Login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

            context = {
                'user': user,
                'login_datetime': timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
                'device_info': request.META.get('HTTP_USER_AGENT', 'Unknown')
            }

            html_content = render_to_string('emails/login_email.html', context)
            subject = 'Alert: Someone recently logged in'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]

            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('users:index')
    else:
        form = AuthenticationForm(request)

    return render(request, 'users/login.html', {'title': title, 'form': form})


@anonymous_required(redirect_url='errors:error_400')
def register(request):
    title = "Register"
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(
                reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
            )

            context = {
                'user': user,
                'activation_link': activation_link,
                'register_datetime': timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
            }

            html_content = render_to_string('emails/register_verification.html', context)
            subject = 'Welcome to our website - Activate your account'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.info(request,
                          "We have sent you an email to activate your account. Please check your email and activate your account before logging in.")
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title': title, 'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated! You can now log in.')
        return redirect('users:login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('users:login')

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been successfully activated! You can now log in.')
        return redirect('users:login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('users:login')

def logout(request):
    auth_logout(request)
    return redirect('users:index')

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class AnonymousPasswordResetView(auth_views.PasswordResetView):
    pass

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class AnonymousPasswordResetDoneView(auth_views.PasswordResetDoneView):
    pass

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class AnonymousPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class AnonymousPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    pass