from django.urls import path
from .views import Login, log_out, RegisterView

app_name = 'users'

urlpatterns = [
    path('log-in/', Login.as_view(), name='log_in'),
    path('log-out/', log_out, name='log_out'),
    path('register/', RegisterView.as_view(), name='register')
]
