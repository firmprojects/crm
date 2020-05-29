from django.shortcuts import render, get_object_or_404
from crm_accounts.models import Estimate, Taxes, Invoice, ProvidentFund, ProvidentType, Expenses
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


# Estimate views
class EstimatesView(ListView):
    model = Estimate
    template_name = 'crm_accounts/estimate.html'

    def get_context_data(self, **kwargs):
        context = super(EstimatesView, self).get_context_data(**kwargs)
        context['estimate'] = Estimate.objects.all()
        return context


class CreateEstimate(CreateView):
    model = Estimate

    fields = [
        'client', 'projects', 'email', 'taxes', 'extimate_date', 'expiry_date', 'client_address',
        'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
        'other_information'
    ]


class EstimateDetail(DetailView):
    model = Estimate


class EstimateDelete(DeleteView):
    model = Estimate
    success_url = "/acct/estimates"


class EstimateUpdate(UpdateView):
    model = Estimate
    fields = [
        'client', 'projects', 'email', 'taxes', 'extimate_date', 'expiry_date', 'client_address',
        'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
        'other_information'
    ]

# Invoice views


class InvoiceView(ListView):
    model = Invoice
    template_name = 'crm_accounts/invoice.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        context['invoice'] = Invoice.objects.all()
        return context


class CreateInvoice(CreateView):
    model = Invoice

    fields = [
        'client', 'projects', 'email', 'taxes', 'invoice_date', 'expiry_date', 'client_address',
        'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
        'other_information'
    ]


class InvoiceDetail(DetailView):
    model = Invoice


class InvoiceDelete(DeleteView):
    model = Invoice
    success_url = "/acct/invoices"


class InvoiceUpdate(UpdateView):
    model = Invoice
    fields = [
        'client', 'projects', 'email', 'taxes', 'invoice_date', 'expiry_date', 'client_address',
        'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
        'other_information'
    ]


class PaymentsView(ListView):
    queryset = Invoice.objects.filter(status='paid')
    template_name = 'crm_accounts/payments.html'
    ordering = ['-invoice_date']


class ProvidentFundView(ListView):
    model = ProvidentFund
    template_name = 'crm_accounts/providentfund.html'
    fields = ['user', 'provident_type', 'employee_share', 'company_share',
              'employee_share', 'company_share', 'created', 'description']


class ExpensesView(ListView):
    model = Expenses
    template_name = 'crm_accounts/expenses.html'
    fields = ['item_name', 'purchase_from', 'purchase_date', 'purchase_by',
              'amount', 'paid_by', 'status', 'attachement']



class CreateTaxes(CreateView):
    model = Taxes
    template_name = 'crm_accounts/taxes.html'
    fields = ['tax_name', 'tax_percentage', 'tax_status']
    success_url = reverse_lazy('crm_accounts:taxes')

    def get_context_data(self, **kwargs):
        context = super(CreateTaxes, self).get_context_data(**kwargs)
        context['taxes'] = Taxes.objects.all()
        return context


class TaxUpdate(UpdateView):
    model = Taxes
    fields = ['tax_name', 'tax_percentage', 'tax_status']

class TaxDelete(DeleteView):
    model = Taxes


