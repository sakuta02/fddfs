from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm, RegisterForm, PasswordChangeCustomForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView
from django.urls import reverse_lazy


class Login(LoginView):
    template_name = 'auth.html'
    form_class = LogInForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


def log_out(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('users:log_in'))


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:log_in')


class PasswordChangeCustomView(PasswordChangeView):
    form_class = PasswordChangeCustomForm
    success_url = reverse_lazy("users:log_out")
    template_name = "change_password.html"
