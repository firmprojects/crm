from django.db import models
from project.models import Projects, Clients
from django.urls import reverse
import uuid
import random
import string
from django.conf import settings
from django.utils.crypto import get_random_string




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


def generate_id():
    id = get_random_string(6)
    return id


class Estimate(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE)
    email = models.EmailField()
    taxes = models.ForeignKey(Taxes, on_delete=models.CASCADE)
    client_address = models.TextField()
    billing_address = models.TextField()
    extimate_date = models.DateField()
    expiry_date = models.DateField()
    item_name = models.CharField("", max_length=200)
    item_description = models.CharField("", max_length=200)
    unit_cost = models.IntegerField("")
    quantity = models.IntegerField("")
    amount = models.IntegerField("")
    estimate_id = models.CharField(
        max_length=10, default=generate_id(), unique=True)
    status = models.CharField(max_length=100, choices=ESTIMATE_STATUS)
    discount = models.CharField("", max_length=100, blank=True, null=True)
    other_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} Estimate"

    def get_absolute_url(self):
        return reverse('crm_accounts:estimates')


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
        max_length=10, default=generate_id(), unique=True)
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
        ('ca', 'Cash'),
        ('tf', 'Tranfer'),
        ('bd', 'Bank Deposit'),
        ('ch', 'Cheque'),
        ('ot', 'Ot'),
    )

    EXPENSES_STATUS = (
        ('pd', 'Pending'),
        ('ap', 'Approved'),
    )
    item_name = models.CharField(max_length=200)
    purchase_from = models.CharField(max_length=200)
    purchase_date = models.DateTimeField()
    purchase_by = models.CharField(max_length=200, blank=True, null=True)
    amount = models.FloatField()
    paid_by = models.CharField(max_length=100, choices=PAYMENT_METHOD, blank=True, null=True)
    status = models.CharField(max_length=100, choices=EXPENSES_STATUS, blank=True, null=True)
    attachement = models.FileField( blank=True, null=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('accounts:expenses')
