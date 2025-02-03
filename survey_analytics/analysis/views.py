from django.shortcuts import render

# Create your views here.

def analysisSurveys(request):
    title = "Analysis Surveys"
    return render(request, 'analysis/analysisSurveys.html', {'title': title})

def administrateSurveys(request):
    title = "Administrate Surveys"
    return render(request, 'analysis/administrateSurveys.html', {'title': title})