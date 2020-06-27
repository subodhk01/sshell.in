from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets

class User(AbstractUser):
    avatar = models.CharField(max_length= 50, verbose_name="Avatar URL", default="/static/images/logos/avatar.png")
    country = models.CharField(max_length= 50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name="Email Verfied", help_text="Designates whether User's email address is verified.")
    has_password = models.BooleanField(default=True)
    last_send_verification_link = models.DateTimeField(null=True, blank=True)
    random_token = models.CharField(max_length=20, editable=False)

    class Meta:
        unique_together = ['email',]

class RandomToken(models.Model):
    token = models.CharField(max_length=40, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    expiry_minutes = models.SmallIntegerField(default=5, help_text="Time after with the token will expire")
    created_at = models.DateTimeField(editable=False)
    expires_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:	
            self.token = secrets.token_urlsafe(32)
            self.created_at = timezone.now()
            self.expires_at = timezone.now() + timezone.timedelta(minutes=self.expiry_minutes)
        super(RandomToken, self).save(*args, **kwargs)

    def clean(self):
        if timezone.now() > self.expires_at:
            self.delete()

    def __str__(self):
        return self.token

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
