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


class SMTPEmailSettingsAdmin(admin.ModelAdmin):
    list_display = ['smtp_host', 'smtp_user', 'smtp_password', 'smtp_port',
                    'smtp_security', 'smtp_auth_domain']


admin.site.register(SMTPEmailSettings, SMTPEmailSettingsAdmin)


admin.site.register(ThemeSettings)

admin.site.register(InvoiceSettings)

admin.site.register(RoleAccess)

admin.site.register(SalarySettings)
