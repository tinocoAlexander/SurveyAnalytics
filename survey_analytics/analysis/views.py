from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Survey, SurveyFile
# Create your views here.
@login_required(login_url='errors:error_401')
def lastSurveys(request):
    title = "Last Surveys"
    surveys = Survey.objects.filter(user=request.user).prefetch_related('files')
    for survey in surveys:
        last_modified = None
        total_size = 0
        for survey_file in survey.files.all():
            if last_modified is None or survey_file.uploaded_at > last_modified:
                last_modified = survey_file.uploaded_at
            if survey_file.file:
                total_size += survey_file.file.size
        survey.last_modified = last_modified
        survey.total_size_mb = total_size / (1024 * 1024)

    sorted_surveys = sorted(
        surveys,
        key=lambda s: s.last_modified if s.last_modified is not None else s.created_at,
        reverse=True
    )
    recent_surveys = sorted_surveys[:5]
    all_surveys = sorted_surveys

    context = {
        'title': title,
        'recent_surveys': recent_surveys,
        'all_surveys': all_surveys,
    }
    return render(request, 'analysis/lastSurveys.html', context)

@login_required(login_url='errors:error_401')
def resultSurveys(request):
    title = "Results Surveys"
    return render(request, 'analysis/resultSurveys.html', {'title': title})

@login_required(login_url='errors:error_401')
def analysisSurveys(request):
    title = "Add Surveys"
    if request.method == 'POST':
        survey_name = request.POST.get('survey_name')
        uploaded_files = request.FILES.getlist('upload_files')
        if not survey_name:
            messages.error(request, 'Please enter a survey name')
            return render(request, 'analysis/analysisSurveys.html', {'title': title})
        if not uploaded_files:
            messages.error(request, 'You must upload at least one file')
            return render(request, 'analysis/analysisSurveys.html', {'title': title})
        survey = Survey.objects.create(user=request.user, name=survey_name)

        for file in uploaded_files:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['csv', 'xlsx', 'xls']:
                messages.error(request, 'The file {file.name} has an unsupported extension ')
                continue
            SurveyFile.objects.create(survey=survey, file=file)
        messages.success(request, 'Survey added successfully')
        return redirect('users:index') # Este lo tengo que cambiar cuando tenga la vista de las graficas
    return render(request, 'analysis/analysisSurveys.html', {'title': title})