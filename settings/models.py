import pytz
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django_countries.fields import CountryField
from timezone_field import TimeZoneField


CURRENCY_SYMBOL = (
    ('₦', '₦'),
    ('$', '$'),
    ('€', '€'),
    ('£', ('£'))
)

CURRENCY_CODE = (
    ('naira', 'Naira'),
    ('USD', 'USD'),
    ('pound', 'Pound'),
    ('euro', 'EURO')
)

LANGUAGES = (
    ('eng', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French')
)


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
    logo = models.ImageField(
        upload_to='company', default='logo.jpg', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Localization(models.Model):
    """Model definition for Localization."""
    default_country = CountryField(blank_label='(select country)')
    date_format = models.CharField(max_length=100, blank=True, null=True)
    timezone = TimeZoneField(default="Africa/Lagos")
    default_language = models.CharField(
        max_length=100, choices=LANGUAGES, default="eng", blank=True, null=True)
    currency_code = models.CharField(
        max_length=100, choices=CURRENCY_CODE, default="naira", blank=True, null=True)
    currency_symbol = models.CharField(
        max_length=100, choices=CURRENCY_SYMBOL, default="₦", blank=True, null=True)

    class Meta:
        """Meta definition for Localization."""
        verbose_name = 'Localization'
        verbose_name_plural = 'Localizations'


class ThemeSettings(models.Model):
    """Model definition for ThemeSettings."""
    website_name = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='company')
    favicon = models.ImageField(upload_to='company')

    def __str__(self):
        return self.website_name

    class Meta:
        """Meta definition for ThemeSettings."""
        verbose_name = 'Theme Settings'
        verbose_name_plural = 'Theme Settings'


class RoleAccess(models.Model):
    """Model definition for ModuleAccess."""
    row_name = models.CharField(max_length=150)

    class Meta:
        """Meta definition for ModuleAccess."""

        verbose_name = 'Module Access'
        verbose_name_plural = 'Module Access'

    def __str__(self):
        return self.row_access

        pass
