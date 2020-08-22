from django.shortcuts import render
from .models import Salary
from .forms import SalaryForm
from django.views.generic import View, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


class SalaryView(View):
    def get(self, request):
        salary = Salary.objects.all()
        form = SalaryForm()
        print("FORM", form)
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
