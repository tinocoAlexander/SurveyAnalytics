from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, AuthenticationForm
from .decorators import anonymous_required
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

@anonymous_required(redirect_url='errors:error_401')
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

            # Enviar correo de inicio de sesión
            subject = 'Inicio de Sesión Exitoso'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            context = {'user': user}
            # Renderizamos la plantilla HTML del correo
            html_content = render_to_string('emails/login_email.html', context)
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('users:index')
    else:
        form = AuthenticationForm(request)

    return render(request, 'users/login.html', {'title': title, 'form': form})


@anonymous_required(redirect_url='errors:error_401')
def register(request):
    title = "Register"
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Enviar correo de registro
            subject = 'Bienvenido a Nuestra App'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            context = {'user': user}
            html_content = render_to_string('users/emails/register_email.html', context)
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