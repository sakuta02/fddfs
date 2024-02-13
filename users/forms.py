from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class LogInForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'username-field', 'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'password-field', 'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
