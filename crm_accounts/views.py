from dal import autocomplete
from django.shortcuts import render, get_object_or_404
from crm_accounts.models import Estimate, Taxes, Invoice, ProvidentFund, ProvidentType, Expenses,Items
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from project.models import Clients, Projects
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import json
from users.models import CustomUser
from .forms import ExpensesForm, ProvidentFundForm
from django import forms


class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = [
            'client', 'projects', 'email', 'taxes', 'extimate_date', 'expiry_date', 'client_address',
            # 'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
            # 'other_information'
            'billing_address',  'discount',
            'other_information'

        ]
    def __init__(self,*args,**kwargs):
        super(EstimateForm,self).__init__(*args,**kwargs)
        self.fields['discount'].widget = forms.NumberInput(attrs={'min':0,'max':100,'step':0.01})

# Estimate views
class EstimatesView(ListView):
    model = Estimate
    template_name = 'crm_accounts/estimate.html'

    def get_context_data(self, **kwargs):
        context = super(EstimatesView, self).get_context_data(**kwargs)
        context['estimate'] = Estimate.objects.all()
        return context


class CreateEstimate(TemplateView):

    template_name = 'crm_accounts/estimate_form.html'
    def get(self,request,*args,**kwargs):
        super().get(request,*args,**kwargs)
        conte = super().get_context_data()
        conte['form'] = EstimateForm
        return render(request,self.template_name,conte)


def get_tax(request,pk):
    return JsonResponse({'tax':Taxes.objects.get(pk=pk).tax_percentage})

def create_estimate(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        print(data.getlist('items'))

        es = Estimate.objects.create(
            client=Clients.objects.get(pk=int(data['client'])),projects=Projects.objects.get(pk=int(data['projects'])),email=data['email'],
            taxes=Taxes.objects.get(pk=int(data['taxes'])),extimate_date=data.get('extimate_date'),expiry_date=data.get('expiry_date'),
            client_address=data.get('client_address'),billing_address=data['billing_address'],
            discount=0 if data.get('discount') is None or data.get('discount')=='' else data.get('discount'),other_information=data['other_information']
        )
        items = json.loads(data['items'])
        for js in items:

            Items.objects.create(
                item_name=js['item_name'],item_description=js['item_description'],
                unit_cost=js['unit_cost'],quantity=js['quantity'],estimate=es
            )

        am = 0
        for i in es.items_set.all():
            amo = int(i.unit_cost*i.quantity)
            print(amo,i.quantity,i.unit_cost)
            i.total = amo
            i.save()
            am+=amo
        amo = am
        am = am*(1+(es.taxes.tax_percentage/100))
        am = am-amo*(float(es.discount)/100)
        es.amount = am

        es.save()
        return JsonResponse({'success':'success','pk':es.pk})

        # After creating estimate and it's associated Items, user your logic to calculate subtotal and save it.


class EstimateDetail(DetailView):
    model = Estimate


class EstimateDelete(DeleteView):
    model = Estimate
    success_url = "/crm_accounts/estimates"


class EstimateUpdate(UpdateView):
    model = Estimate
    fields = [
        'client', 'projects', 'email', 'taxes', 'extimate_date', 'expiry_date', 'client_address',
        'billing_address', 'item_name', 'item_description', 'unit_cost', 'quantity', 'amount', 'discount',
        'other_information'
    ]


def estimate_status(request):
    if request.method == 'POST':
        estimate = Estimate.objects.get(pk = request.POST['pk'])
        estimate.status = request.POST['status']
        estimate.save()
        return JsonResponse({"status":estimate.status})


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


class ProvidentFundView(View):
    def get(self, request):
        form = ProvidentFundForm()
        fund = ProvidentFund.objects.all()
        return render(request, 'crm_accounts/providentfund.html', {'form':form, 'fund':fund})


class ExpensesView(View):
    def get(self, request):
        expenses = Expenses.objects.all()
        form = ExpensesForm()
        return render(request, 'crm_accounts/expenses.html', {'form': form, 'expenses':expenses})

    def post(self, request):
        if request.method == 'POST':
            form = ExpensesForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Expense was successfully created")
            return HttpResponseRedirect(reverse('crm_accounts:expenses'))



class DeleteExpense(View):
    def get(self, request, id):
        expense = Expenses.objects.get(id=id)
        expense.delete()
        messages.success(request, "Expense was successfully removed")
        return HttpResponseRedirect(reverse('crm_accounts:expenses'))


class ExpenseUpdate(UpdateView):
    model = Expenses
    fields = '__all__'

def change_status(request):
    if request.method == 'POST':
        expenses = Expenses.objects.get(pk = request.POST['pk'])
        expenses.status = request.POST['status']
        expenses.save()
        return JsonResponse({"status":expenses.status})
    



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


class UsersAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CustomUser.objects.filter(is_employee=True)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        print(qs)
        return qs
