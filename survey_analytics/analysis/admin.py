from django.contrib import admin
from .models import Survey, SurveyFile

class SurveyFileInline(admin.TabularInline):
    model = SurveyFile
    extra = 1  #

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [SurveyFileInline]

admin.site.register(Survey, SurveyAdmin)
