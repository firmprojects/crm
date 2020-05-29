from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def team_leader(self):
        return self.leader_set.all()


    

