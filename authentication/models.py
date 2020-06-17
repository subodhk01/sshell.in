from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets

class User(AbstractUser):
    avatar = models.CharField(max_length= 50, verbose_name="Avatar URL")
    is_verified = models.BooleanField(default=False)

    class Meta:
        unique_together = ['email',]
        