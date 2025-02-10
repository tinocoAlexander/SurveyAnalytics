from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login
from .forms import UserRegisterForm, AuthenticationForm
from .decorators import anonymous_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

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

def logout(request):
    auth_logout(request)
    return redirect('users:index')

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/forgot_password.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

@method_decorator(anonymous_required(redirect_url='errors:error_400'), name='dispatch')
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_logout(self.request)
        messages.success(
            self.request,
            "Your password has been changed and your session has been ended. Please log in again with your new password."
        )
        return response

@method_decorator(login_required(login_url='errors:error_401'), name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):

    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_logout(self.request)
        messages.success(
            self.request,
            "Your password has been changed successfully. Please log in again."
        )
        return response