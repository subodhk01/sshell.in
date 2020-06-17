from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets

class User(AbstractUser):
    avatar = models.CharField(max_length= 50, verbose_name="Avatar URL")
    is_verified = models.BooleanField(default=False, verbose_name="Email Verfied", help_text="Designates whether User's email address is verified.")
    random_token = models.CharField(max_length=20, editable=False)

    class Meta:
        unique_together = ['email',]

class RandomToken(models.Model):
    token = models.CharField(max_length=20, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    expiry_minutes = models.SmallIntegerField(default=5, help_text="Time after with the token will expire")
    created_at = models.DateTimeField(editable=False)
    expires_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:	
            self.token = secrets.token_urlsafe(16)
            self.created_at = timezone.now()
            self.expires_at = timezone.now() + timezone.timedelta(minutes=self.expiry_minutes)
        super(RandomToken, self).save(*args, **kwargs)

    def clean(self):
        if timezone.now() > self.expires_at:
            self.delete()

    def __str__(self):
        return self.token
