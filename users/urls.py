from django.urls import path
from .views import Login, log_out
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('log-in/', Login.as_view(), name='log_in'),
    path('log-out/', LogoutView.as_view(), name='log_out')
]
