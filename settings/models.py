from django.db import models
from phonenumber_field.modelfields import PhoneNumberField



class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200,  blank=True, null=True)
    address = models.TextField( blank=True, null=True)
    Country = models.CharField(max_length=200)
    city = models.CharField(max_length=200,)
    state = models.CharField(max_length=200)
    postal_code = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company', default='logo.jpg', blank=True, null=True)

    def __str__(self):
        return self.company_name
    

