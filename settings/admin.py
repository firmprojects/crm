from django.contrib import admin
from .models import CompanyInfo

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'address', 'country', 'city', 'state', 'postal_code', 'email', 'phone_number', 'website', 'logo']


admin.site.register(CompanyInfo, CompanyInfoAdmin)
