from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

def login(request):
    title = "Login"
    return render(request, 'users/login.html', {'title': title})

def register(request):
    title = "Register"
    return render(request, 'users/register.html', {'title': title})

def logout(request):
    auth_logout(request)
    return redirect('users:index')