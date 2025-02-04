from django.shortcuts import render

def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})

def login(request):
    title = "Login"
    return render(request, 'users/login.html', {'title': title})

def register(request):
    title = "Register"
    return render(request, 'users/register.html', {'title': title})