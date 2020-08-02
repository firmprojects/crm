import django
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres import fields
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(default='default.jpg', upload_to='users')
    staff_id = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    on_leave = models.BooleanField(default=False)
    gender = models.CharField(max_length=10,choices=(('male','Male'),('female','Female'),('other','Other')),blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('employees:staff')

class Attendance(models.Model):
    staff = models.OneToOneField(Staff,on_delete=models.CASCADE)
    attendance = fields.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)
    clock_ins = fields.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)


def create_attendance(sender, instance, created, **kwargs):
    if created:
        attendace = Attendance(staff=instance,attendance={},clock_ins={})
        attendace.save()
    else:
        try:
            attendace = Attendance.objects.get(staff=instance)

        except ObjectDoesNotExist:
            attendace = Attendance(staff=instance,attendance={},clock_ins={})
            attendace.save()

post_save.connect(create_attendance,sender=Staff)

class Education(models.Model):
    institution = models.CharField(max_length=300, blank=True, null=True)
    course_name = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # support_document = models.FileField()

    def __str__(self):
        return self.institution


class Experience(models.Model):
    organisation = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.organisation


class Skill(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title


class LeaveType(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class LeaveRequest(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leave_start_date = models.DateTimeField(auto_now_add=False)
    leave_end_date = models.DateTimeField(auto_now_add=False)
    number_of_days = models.IntegerField()
    remaining_days = models.IntegerField()
    leave_reason = models.TextField()



class Designation(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('employees:designation')


class Department(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employees:departments')


class Holidays(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employees:holiday')
