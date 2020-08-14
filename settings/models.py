from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings




class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=200, blank=True, )
    contact_person = models.CharField(max_length=200,  blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, )
    city = models.CharField(max_length=200, blank=True, )
    state = models.CharField(max_length=200, blank=True, )
    postal_code = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, )
    phone_number = PhoneNumberField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company', default='logo.jpg', blank=True, null=True)

    def __str__(self):
        return self.company_name



    

