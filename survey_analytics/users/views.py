from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from .forms import UserRegisterForm

def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

def login(request):
    title = "Login"
    return render(request, 'users/login.html', {'title': title})

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