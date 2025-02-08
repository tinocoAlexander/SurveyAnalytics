from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from .forms import UserRegisterForm, AuthenticationForm
from .decorators import anonymous_required
def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

@anonymous_required(redirect_url='errors:error_401')
def login(request):
    title = "Login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

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
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title':title, 'form': form})
def logout(request):
    auth_logout(request)
    return redirect('users:index')