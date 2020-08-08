from django.db import models
from project.models import Projects, Clients
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
import uuid
import random
import string
from django.conf import settings




ESTIMATE_STATUS = (
    ('accept', 'Accept'),
    ('reject', 'Reject'),
    ('pending', 'Pending'),

)

INVOICE_STATUS = (
    ('paid', 'Paid'),
    ('reject', 'Reject'),
    ('pending', 'Pending'),

)
PROVIDENCE_STATUS = (
    ('accept', 'Accept'),
    ('reject', 'Reject'),
    ('pending', 'Pending'),

)


class Taxes(models.Model):
    TAX_STATUS = ( ('pending', 'Pending'),('approved', 'Approved'),)
    tax_name = models.CharField(max_length=100)
    tax_percentage = models.IntegerField()
    tax_status = models.CharField(max_length=100, choices=TAX_STATUS)

    def __str__(self):
        return self.tax_name


def ran_gen(size=5, chars=string.ascii_letters + string.digits):
    est_id = ''.join(random.choice(chars) for x in range(size))
    return est_id


class Estimate(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)
    email = models.EmailField()
    taxes = models.ForeignKey(Taxes, on_delete=models.CASCADE)
    client_address = models.TextField()
    billing_address = models.TextField()
    extimate_date = models.DateField()
    expiry_date = models.DateField()

    amount = models.IntegerField(blank=True, null=True)
    estimate_id = models.CharField(
        max_length=10, default=ran_gen, unique=True)
    status = models.CharField(max_length=100, choices=ESTIMATE_STATUS)
    discount = models.FloatField(default=0, max_length=100, blank=True, null=True)
    other_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} Estimate"

    def get_absolute_url(self):
        return reverse('crm_accounts:estimates')

    def get_total(self):
        am = 0
        for i in self.items_set.all():
            amo = int(i.unit_cost*i.quantity)
            am+=amo
        return round(am,2)

    def get_taxes(self):
        am = 0
        for i in self.items_set.all():
            amo = int(i.unit_cost*i.quantity)
            am+=amo
        return round(am*(self.taxes.tax_percentage/100),2)

    def get_dis(self):
        am = 0
        for i in self.items_set.all():
            amo = int(i.unit_cost*i.quantity)
            am+=amo
        return round(am*float(self.discount)/100,2)



class Items(models.Model):
    estimate = models.ForeignKey(to=Estimate,on_delete=models.CASCADE)
    item_name = models.CharField("", max_length=200)
    item_description = models.CharField("", max_length=200)
    unit_cost = models.IntegerField("")
    quantity = models.IntegerField("")
    total = models.IntegerField(default=0)

# def cal_info(sender,instance,created,**extra):
#     if created:
#
#
# post_save.connect(cal_info,sender=Estimate)

class Invoice(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)
    email = models.EmailField()
    taxes = models.ForeignKey(Taxes, on_delete=models.CASCADE)
    client_address = models.TextField()
    billing_address = models.TextField()
    invoice_date = models.DateField()
    expiry_date = models.DateField()
    item_name = models.CharField("", max_length=200)
    item_description = models.CharField("", max_length=200)
    unit_cost = models.IntegerField("")
    quantity = models.IntegerField("")
    amount = models.IntegerField("")
    invoice_id = models.CharField(
        max_length=10, default=ran_gen, unique=True)
    status = models.CharField(max_length=100, choices=INVOICE_STATUS)
    discount = models.CharField("", max_length=100, blank=True, null=True)
    other_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} Invoice"

    def get_absolute_url(self):
        return reverse('crm_accounts:invoices')


class ProvidentType(models.Model):
    name = models.CharField("", max_length=100,)

    def __str__(self):
        return self.name


class ProvidentFund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    provident_type = models.ForeignKey(
        ProvidentType, on_delete=models.DO_NOTHING)
    employee_share_amount = models.IntegerField(
        verbose_name="Employee Share(amount)")
    company_share_amount = models.IntegerField(
        verbose_name="Company Share(amount)")
    employee_share = models.IntegerField(verbose_name="Employee Share(%)")
    company_share = models.IntegerField(
        verbose_name="Company Share(%)")
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=PROVIDENCE_STATUS)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} Provident Fund"

    def get_absolute_url(self):
        return reverse('accounts:providentfund')


class Expenses(models.Model):
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('transfer', 'Tranfer'),
        ('bank deposit', 'Bank Deposit'),
        ('cheque', 'Cheque'),
        ('others', 'Others'),
    )

    EXPENSES_STATUS = (
        ('inspect', 'Inspect'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    item_name = models.CharField(max_length=200)
    purchase_from = models.CharField(max_length=200)
    purchase_date = models.DateField(blank=True)
    purchase_by = models.CharField(max_length=200)
    amount = models.FloatField()
    paid_by = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=EXPENSES_STATUS)
    attachement = models.FileField(blank=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('accounts:expenses')
