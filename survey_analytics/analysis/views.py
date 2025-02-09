from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='errors:error_401')
def analysisSurveys(request):
    title = "Analysis Surveys"
    return render(request, 'analysis/analysisSurveys.html', {'title': title})

@login_required(login_url='errors:error_401')
def lastSurveys(request):
    title = "Last Surveys"
    return render(request, 'analysis/lastSurveys.html', {'title': title})

@login_required(login_url='errors:error_401')
def resultSurveys(request):
    title = "Results Surveys"
    return render(request, 'analysis/resultSurveys.html', {'title': title})