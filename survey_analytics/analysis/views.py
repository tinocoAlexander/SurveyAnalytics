from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Survey, SurveyFile
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse

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
                messages.error(request, f'The file {file.name} has an unsupported extension')
                continue
            SurveyFile.objects.create(survey=survey, file=file)
        messages.success(request, 'Survey added successfully')

        redirect_url = reverse_lazy('analysis:analysis_graphs', kwargs={'survey_id': survey.id})

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': str(redirect_url)})
        else:
            return redirect(redirect_url)
    return render(request, 'analysis/analysisSurveys.html', {'title': title})


@login_required
def analysisGraphs(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    survey_file = survey.files.first()
    if not survey_file:
        messages.error(request, "No file associated with this survey.")
        return redirect('analysis:analysisSurveys')

    file_path = survey_file.file.path
    ext = survey_file.file.name.split('.')[-1].lower()

    try:
        if ext == 'csv':
            df = pd.read_csv(file_path)
        elif ext in ['xls', 'xlsx']:
            df = pd.read_excel(file_path)
        else:
            messages.error(request, "Unsupported file extension.")
            return redirect('analysis:analysisSurveys')
    except Exception as e:
        messages.error(request, f"Error reading file: {e}")
        df = pd.DataFrame()

    graphs = []
    if not df.empty:
        for col in df.columns:
            plt.figure(figsize=(6, 4))
            if df[col].dtype == 'object' or df[col].nunique() < 10:
                counts = df[col].value_counts()
                counts.plot(kind='bar', color='#4f46e5')
            else:
                df[col].plot(kind='hist', color='#4f46e5', bins=10)
            plt.title(col, fontsize=14, fontfamily='DejaVu Sans')
            plt.xlabel("Response", fontsize=12, fontfamily='DejaVu Sans')
            plt.ylabel("Frequency", fontsize=12, fontfamily='DejaVu Sans')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            graphs.append({'column': col, 'image': image_base64})
            plt.close()
    else:
        messages.error(request, "No data available to generate graphs.")

    context = {
        'survey': survey,
        'graphs': graphs,
    }
    return render(request, 'analysis/analysisGraphs.html', context)