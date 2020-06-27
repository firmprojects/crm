from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CompanyInfo

class CreateCompany(CreateView):
    model = CompanyInfo
    template_name = 'settings/company_info.html'
    fields = ['company_name']
    
