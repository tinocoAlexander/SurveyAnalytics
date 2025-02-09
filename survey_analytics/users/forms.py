# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

# Formulario para el registro de usuarios
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'id': 'password',
            'placeholder': 'Enter your password'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter your email'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False
        if commit:
            user.save()
        return user


# Formulario para el inicio de sesión
class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-input',
            'placeholder': 'Enter your username'
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'id': 'password',
        }),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct username and password. Note that both fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive. Please activate it"),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.fields['username'].label = capfirst(self.fields['username'].label)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.fields['username'].label},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache
