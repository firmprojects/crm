from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def team_leader(self):
        return self.leader_set.all()


class Clocking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    clockin_time = models.TimeField(blank=True, null=True)
    clockout_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    week = models.CharField(max_length=50, blank=True, null=True)
    month = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username

    

