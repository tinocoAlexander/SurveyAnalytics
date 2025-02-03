from django.shortcuts import render

def index(request):
    title = "Homepage"
    return render(request, 'users/index.html', {'title': title})
