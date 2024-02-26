from django.urls import path
from .views import Login, log_out, RegisterView, PasswordChangeCustomView

app_name = 'users'

urlpatterns = [
    path('login/', Login.as_view(), name='log_in'),
    path('logout/', log_out, name='log_out'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', PasswordChangeCustomView.as_view(), name='password_change'),
]
