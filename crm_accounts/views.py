from dal import autocomplete
from django.shortcuts import render, get_object_or_404
from crm_accounts.models import Estimate, Taxes, Invoice, ProvidentFund, ProvidentType, Expenses
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from project.models import Clients, Projects
from .forms import ExpensesForm


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


class CreateExpenses(View):
    def get(self, request):
        expenses = Expenses.objects.all()
        form = ExpensesForm()
        return render(request, 'crm_accounts/expenses.html', {'expenses':expenses, 'form':form})

    def post(self, request):
        if request.method == 'POST':
            form = ExpensesForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('crm_accounts:expenses'))
        


# class CreateExpenses(CreateView):
#     model = Expenses
#     template_name = 'crm_accounts/expenses.html'
#     fields = ['item_name', 'purchase_from', 'purchase_date', 'purchase_by',
#               'amount', 'paid_by', 'status', 'attachement']

#     def get_context_data(self, **kwargs):
#         context = super(CreateExpenses, self).get_context_data(**kwargs)
#         context['expenses'] = Expenses.objects.all()
#         return context

 

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


class ClientAutocompletesView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Clients.objects.all().order_by('-company_name')
        if self.q:
            qs = qs.filter(company_name__istartswith=self.q)
        return qs


class ProjectAutocompletesView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Projects.objects.all().order_by('-name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


