from django.shortcuts import render
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


def superuser_only(function):

   def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied
       return function(request, *args, **kwargs)
   return _inner


@method_decorator(superuser_only, name='dispatch')
class Home(TemplateView):
    template_name = 'dashboard/index.html'

class Assets(TemplateView):
    template_name = 'dashboard/assets.html'

class Settings(TemplateView):
    template_name = 'dashboard/settings.html'
