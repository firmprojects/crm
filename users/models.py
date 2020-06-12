from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def team_leader(self):
        return self.leader_set.all()



class Clocking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    clockin_data = JSONField()

    def __str__(self):
        return self.user.username
def create_clocking(sender, instance,created, **kwargs):
    if created:
        clocking = Clocking(user=instance,clockin_data={})
        clocking.save()
    else:
        try:
            clocking = Clocking.objects.get(user=instance)
        except ObjectDoesNotExist:
            clocking = Clocking(user=instance,clockin_data={})
            clocking.save()
post_save.connect(create_clocking,sender=CustomUser)
