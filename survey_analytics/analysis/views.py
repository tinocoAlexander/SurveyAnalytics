from django.shortcuts import render

# Create your views here.

def analysisSurveys(request):
    title = "Analysis Surveys"
    return render(request, 'analysis/analysisSurveys.html', {'title': title})

def lastSurveys(request):
    title = "Last Surveys"
    return render(request, 'analysis/lastSurveys.html', {'title': title})