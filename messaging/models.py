from django.db import models
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

class Files(models.Model):
    file = models.FileField(upload_to="document/")
    mail = models.ForeignKey(MailBody,on_delete=models.CASCADE)

class Mail(models.Model):
    body = models.OneToOneField(to=MailBody,on_delete=models.CASCADE)
    replies = fields.ArrayField(base_field=models.IntegerField(),default=list)
