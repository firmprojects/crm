from django.db import models
from django.db.models.signals import pre_save
from django.contrib.postgres import fields

# Create your models here.


class MailBody(models.Model):
    from_email = models.IntegerField()
    to = fields.ArrayField(base_field=models.IntegerField())
    cc = fields.ArrayField(base_field=models.IntegerField(),null=True,blank=True)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    open_ed = fields.JSONField(default=dict)

def open_ed(sender,instance,**kwargs):
    if instance._state.adding:
        data = {}
        for i in instance.to:
            data[i] = False
        instance.open_ed = data

pre_save.connect(open_ed,sender=MailBody)

class Files(models.Model):
    file = models.FileField(upload_to="document/")
    mail = models.ForeignKey(MailBody,on_delete=models.CASCADE)

class Mail(models.Model):
    body = models.OneToOneField(to=MailBody,on_delete=models.CASCADE)
    replies = fields.ArrayField(base_field=models.IntegerField(),default=list)
