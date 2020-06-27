from django.conf import settings
from django.db import models
from project.models import Projects,Clients
from employees.models import Staff
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.crypto import get_random_string

def generate_task_id():
    id = get_random_string(length=6)
    return "TK-"+str(id)

class Task(models.Model):
    PRIORITY = ( ('high', 'High'), ('medium', 'Medium'), ('low', 'Low'), )
    STATUS = ( ('active', 'Active'), ('inactive', 'Inactive'),('completed',"Completed"))
    task_id = models.CharField(unique=True,max_length=10,default=generate_task_id)

    # project = models.ForeignKey(Projects,  on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=50, choices=PRIORITY)
    status = models.CharField(max_length=50, choices=STATUS)
    assign_to = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='task_asignee', blank=True, null=True)
    client = models.ForeignKey(Clients,on_delete=models.CASCADE,blank=True, null=True)
    task_followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_followers', blank=True)
    description = models.TextField()


    def __str__(self):
        return self.name

    def get_mins(self):
        try:
            duration = self.tasktracker.task_duration
            return "~ "+str(int((float(duration)/60)/1)*1) + " mins"
        except TypeError:
            return "0 mins"


    class Meta:
        ordering = ['task_id']

class ImageTask(models.Model):
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    image = models.FileField(blank=True,null=True,upload_to='images/')

class DocTask(models.Model):
    task = models.ForeignKey(to=Task,on_delete=models.CASCADE)
    doc = models.FileField(blank=True,null=True,upload_to='document/')

class TaskTracker(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    task_duration = models.FloatField(default=0.0)

    status = models.CharField(max_length=10,default="pause", choices=(('pause', 'pause'), ('working', 'Working'), ('terminate', 'Terminate'),))

    def __str__(self):
        return self.task.name

    def get_str(self):
        print(type(self.start_time))
        return {"start_time":str(self.start_time),"end_time":str(self.end_time)}

def create_tracker(sender, instance,created, **kwargs):
    if created:
        tracker = TaskTracker(task=instance,task_duration = 0)
        tracker.save()
    else:
        try:
            TaskTracker.objects.get(task=instance)
        except ObjectDoesNotExist:
            tracker = TaskTracker(task=instance,task_duration = 0)
            tracker.save()
post_save.connect(create_tracker,sender=Task)



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
