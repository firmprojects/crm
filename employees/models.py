from django.db import models
from django.conf import settings
from django.urls import reverse



class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    photo = models.ImageField(default='default.jpg', upload_to='users')
    staff_id = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse('employees:staff')


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
