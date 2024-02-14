from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


class LogInForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'username-field', 'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'password-field', 'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'username-field', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'password-field', 'placeholder': 'Придумайте надежный пароль'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'password-field', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'Адрес электронной почты'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Адреса не могут повторяться'})
        }

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом уже существует")
        return email
