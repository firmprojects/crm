from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib import messages


class CreateCompany(View):
    def get(self, request):
        form = CompanyinfoForm(self.request.POST, self.request.FILES)
        return render(request, 'settings/company_info.html', {'form': form})

    def post(self, request):
        form = CompanyinfoForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Company details successfully created")
            return HttpResponseRedirect(reverse('settings:company_info'))
        return render(request, 'settings/company_info.html')


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


class InvoicesettingView(View):
    def get(self, request):
        form = InvoiceSettingsForm()
        return render(request, 'settings/invoice-settings.html', {'form': form})

    def post(self, request):
        form = InvoiceSettingsForm(request.POST or None, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Invoice settings successfully created")
            return HttpResponseRedirect(reverse("settings:invoice-settings"))
        return render(request, 'settings/invoice-settings.html', {'form': form})


class SMTPEmailSettingsView(View):
    def get(self, request):
        form = SMTPEmailSettingsForm()
        return render(request, 'settings/smtp-settings.html', {'form': form})

    def post(self, request):
        form = SMTPEmailSettingsForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Email settings successfully created")
            return HttpResponseRedirect(reverse("settings:email-settings"))
        return render(request, 'settings/smtp-settings.html', {'form': form})


class SalarySettingsView(View):
    def get(self, request):
        form = SalarySettingsForm()
        return render(request, 'settings/salary-settings.html', {'form': form})

    def post(self, request):
        form = SalarySettingsForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Salary settings successfully created")
            return HttpResponseRedirect(reverse("settings:salary-settings"))
        return render(request, 'settings/salary-settings.html', {'form': form})


class NotificationSettings(View):
    def get(self, request):
        return render(request, 'settings/notifications.html')


class ModuleSettings(View):
    def get(self, request):
        return render(request, 'settings/module-settings.html')
