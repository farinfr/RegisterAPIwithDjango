from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone_number = models.CharField(max_length=11)
    REQUIRED_FIELDS = ['email', 'phone_number', 'first_name', 'last_name']

class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

class LoginAttempt(models.Model):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    attempts = models.IntegerField(default=0)
    blocked_until = models.DateTimeField(null=True, blank=True)
