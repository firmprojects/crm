from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib import messages


def CreateCompany(request):
    if request.method == 'POST':
        form = settingsForm(instance=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details successfully created")
    else:
        form = settingsForm(request.POST)
    return render(request, 'settings/company_info.html', {'form': form})


class LocalizationView(View):
    def get(self, request):
        form = LocalizationForm()
        return render(request, 'settings/localization.html', {'form': form})

    def post(self, request):
        form = LocalizationForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Localization successfully created")
            return HttpResponseRedirect(reverse("settings:localization"))
        return render(request, 'settings/localization.html', {'form': form})


class ThemesettingView(View):
    def get(self, request):
        form = ThemeSettingsForm()
        return render(request, 'settings/theme-settings.html', {'form': form})

    def post(self, request):
        form = ThemeSettingsForm(request.POST or None, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Theme settings successfully created")
            return HttpResponseRedirect(reverse("settings:theme-settings"))
        return render(request, 'settings/theme-settings.html', {'form': form})


class RoleAccessView(View):
    def get(self, request):
        role = RoleAccess.objects.all()
        form = RoleAccessForm()
        return render(request, 'settings/role-access.html', {'form': form, 'role': role})

    def post(self, request):
        form = RoleAccessForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Role successfully created")
            return HttpResponseRedirect(reverse("settings:role-access"))


def role_delete(request, id):
    role = RoleAccess.objects.get(id=id)
    role.delete()
    messages.success(request, "Role successfully deleted")
    return HttpResponseRedirect(reverse("settings:role-access"))
