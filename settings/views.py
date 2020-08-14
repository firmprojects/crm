from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from .models import CompanyInfo
from .forms import settingsForm
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict

def CreateCompany(request):
    if request.method == 'POST':
        form = settingsForm(instance=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = settingsForm(request.POST)
    return render(request, 'settings/company_info.html', {'form':form})


    
 