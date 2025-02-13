from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('analysisSurveys/', views.analysisSurveys, name='analysisSurveys'),
    path('lastSurveys/', views.lastSurveys, name='lastSurveys'),
    path('graphs/<int:survey_id>/', views.analysisGraphs, name='analysis_graphs'),
    path('download_pdf/<int:survey_id>/', views.downloadPDF, name='download_pdf'),
    path('delete_survey/<int:survey_id>/', views.deleteSurvey, name='delete_survey'),
]