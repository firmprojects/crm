from django.contrib import admin
from .models import *


class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'address', 'country',
                    'city', 'state', 'postal_code', 'email', 'phone_number', 'website']


admin.site.register(CompanyInfo, CompanyInfoAdmin)


class LocalizationAdmin(admin.ModelAdmin):
    list_display = ['default_country', 'date_format', 'timezone', 'default_language',
                    'currency_code', 'currency_symbol']


admin.site.register(Localization, LocalizationAdmin)

admin.site.register(ThemeSettings)
