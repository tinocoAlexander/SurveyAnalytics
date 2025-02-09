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
            user = form.save()
            context = {
                'user': user,
                'register_datetime': timezone.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
            html_content = render_to_string('emails/register_email.html', context)
            subject = 'Welcome to our web'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title':title, 'form': form})
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