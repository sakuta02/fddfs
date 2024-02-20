from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True, verbose_name='Фотография')

    def get_absolute_url(self):
        return reverse('profile', args=(self.pk, ))
