from django.shortcuts import render

# Create your views here.

def handler404(request, exception):
    title = "Error 404"
    return render(request, 'errors/404.html', {'title': title}, status=404)

def handler401(request, exception):
    title = "Error 401"
    return render(request, 'errors/401.html', {'title': title}, status=401)