from django.conf import settings
from django.db import models
from project.models import Projects




class Task(models.Model):
    PRIORITY = ( ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), )
    STATUS = ( ('working', 'Working'), ('pending', 'Pending'), ('suspended', 'Suspended'), ('cancelled', 'cancelled'),)
    project = models.ForeignKey(Projects,  on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=50, choices=PRIORITY)
    status = models.CharField(max_length=50, choices=STATUS)
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_asignee', blank=True, null=True)
    task_followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_followers', blank=True)
    description = models.TextField()
    files = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class TaskTracker(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    task_duration = models.CharField (max_length=200, blank=True, null=True)

    def __str__(self):
        return self.task.name


class Ticketing(models.Model):
    project = models.ForeignKey(Projects,  on_delete=models.CASCADE)
    deadline = models.DateField(blank=True, null=True)
    total_hours = models.IntegerField(default=0)
    remaining_hours = models.IntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    hours = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.project.name
    

