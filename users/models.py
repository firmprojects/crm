from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from employees.models import Staff
from project.models import Clients
from django.utils.crypto import get_random_string
from django.utils import timezone


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        default='users/default.jpg', upload_to='users', blank=True, null=True)

    def team_leader(self):
        return self.leader_set.all()


def generate_asset_id():
    id = get_random_string(6).upper()
    return "AST-"+str(id)


ASSETS_STATUS = (
    ("approved", "Approved"),
    ("inspect", "Inspect"),
    ("missing", "Missing"),
    ("rejected", "Rejected"),
)


class Assets(models.Model):
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=100)
    asset_id = models.CharField(
        max_length=10, unique=True, default=generate_asset_id, blank=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    assigned_date = models.DateField(blank=True)
    warranty_end = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    asset_amount = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=ASSETS_STATUS, blank=True)
    receipt = models.FileField(
        upload_to='receipts', max_length=100, blank=True)

    def __str__(self):
        return self.asset_name


class Clocking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    clockin_data = JSONField()

    def __str__(self):
        return self.user.username


def create_clocking(sender, instance, created, **kwargs):
    if created:
        clocking = Clocking(user=instance, clockin_data={})
        clocking.save()
    else:
        try:
            clocking = Clocking.objects.get(user=instance)
        except ObjectDoesNotExist:
            clocking = Clocking(user=instance, clockin_data={})
            clocking.save()


def create_staff(sender, instance, created, **kwargs):
    if instance.is_employee:
        try:
            staff = Staff.objects.get(user=instance)
        except ObjectDoesNotExist:
            staff = Staff(user=instance)
            staff.save()
#


def create_client(sender, instance, created, **kwargs):
    if created:
        if instance.is_client:
            client = Clients(user=instance)
            client.save()
    else:
        if instance.is_client:
            try:
                client = Clients.objects.get(user=instance)
            except ObjectDoesNotExist:
                client = Clients(user=instance)
                client.save()


post_save.connect(create_clocking, sender=CustomUser)
post_save.connect(create_staff, sender=CustomUser)
post_save.connect(create_client, sender=CustomUser)
