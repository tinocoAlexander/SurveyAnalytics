from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users.views import (
    AnonymousPasswordResetView,
    AnonymousPasswordResetDoneView,
    AnonymousPasswordResetConfirmView,
    AnonymousPasswordResetCompleteView,
)
app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', AnonymousPasswordResetView.as_view(
        template_name='users/forgot_password.html',
        email_template_name='users/password_reset_email.html',
        html_email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url='password-reset-done/'
    ), name='password_reset'),

    path('forgot-password/password-reset-done/', AnonymousPasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', AnonymousPasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', AnonymousPasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]