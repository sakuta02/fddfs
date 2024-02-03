from django.http import HttpResponseRedirect
from django.shortcuts import render


def main_url(request):
    return HttpResponseRedirect(redirect_to='forum/news')

