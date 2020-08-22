from django.shortcuts import render
from .models import Salary
from .forms import SalaryForm
from django.views.generic import View, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from settings.models import CompanyInfo


class SalaryView(View):
    def get(self, request):
        salary = Salary.objects.all()
        form = SalaryForm()
        context = {'salary': salary, 'form': form}
        return render(request, 'payroll/salary.html', context)

    def post(self, request):
        form = SalaryForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.info(request, "Salary was successfully created")
            return HttpResponseRedirect(reverse('payroll:salary', ))


class SalaryDetailView(DetailView):
    model = Salary
    template_name = "payroll/salary-detail.html"

    def get_context_data(self, **kwargs):
        context = super(SalaryDetailView, self).get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.objects.all()
        return context
