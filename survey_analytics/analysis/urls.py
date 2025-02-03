from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('analysisSurveys/', views.analysisSurveys, name='analysisSurveys'),
    path('administrateSurveys/', views.administrateSurveys, name='administrateSurveys'),
]