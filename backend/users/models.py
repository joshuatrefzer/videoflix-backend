
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)
    custom = models.CharField(max_length=1000, default='')
    adress = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
