from django.urls import path
from . import views

app_name = 'errors'

urlpatterns = [
    path('401/', views.handler401, name='error_401'),
    path('404/', views.handler404, name='error_404'),
    path('400/', views.error_400, name='error_400'),
]