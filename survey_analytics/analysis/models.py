# models.py
from django.contrib.auth.models import User
from django.db import models

class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys', null=True, blank=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SurveyFile(models.Model):
    survey = models.ForeignKey(Survey, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='surveys/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
