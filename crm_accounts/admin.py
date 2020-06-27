from django.contrib import admin

from .models import Estimate, Taxes, Invoice, ProvidentFund, ProvidentType, Expenses


class EstimateAdmin(admin.ModelAdmin):
    list_display = [ 'projects', 'email', 'taxes', 'extimate_date', 'expiry_date']


admin.site.register(Estimate, EstimateAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['projects', 'email', 'taxes', 'invoice_date', 'expiry_date']


admin.site.register(Invoice, InvoiceAdmin)


class ProvidentFundAdmin(admin.ModelAdmin):
    list_display = ['provident_type', 'employee_share', 'company_share', 'employee_share', 'company_share']


admin.site.register(ProvidentFund, ProvidentFundAdmin)


class ProvidentTypeFundAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(ProvidentType, ProvidentTypeFundAdmin)


class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'purchase_from', 'purchase_date', 'purchase_by',
                    'amount', 'paid_by', 'status', 'attachement']


admin.site.register(Expenses, ExpensesAdmin)


class TaxesAdmin(admin.ModelAdmin):
    list_display = ['tax_name', 'tax_percentage', 'tax_status']


admin.site.register(Taxes, TaxesAdmin)
