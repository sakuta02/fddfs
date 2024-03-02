from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def main_url(request):
    return HttpResponseRedirect(redirect_to=reverse('news', args=(1,)))
