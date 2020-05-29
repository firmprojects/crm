from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView

class Home(TemplateView):
    template_name = 'dashboard/index.html'

class Assets(TemplateView):
    template_name = 'dashboard/assets.html'

class Settings(TemplateView):
    template_name = 'dashboard/settings.html'
