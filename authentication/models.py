from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class User(AbstractUser):
    avatar = models.CharField(max_length= 50, verbose_name="Avatar URL")
