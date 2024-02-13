from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class Login(LoginView):
    template_name = 'auth.html'
    form_class = LogInForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        print(context)
        return context


def log_out(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('users:log_in'))
