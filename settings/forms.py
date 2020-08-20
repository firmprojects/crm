from django import forms
from .models import *


class settingsForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'


class LocalizationForm(forms.ModelForm):
    class Meta:
        model = Localization
        fields = '__all__'


class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = '__all__'


class RoleAccessForm(forms.ModelForm):
    class Meta:
        model = RoleAccess
        fields = '__all__'


class InvoiceSettingsForm(forms.ModelForm):
    class Meta:
        model = InvoiceSettings
        fields = '__all__'


class SMTPEmailSettingsForm(forms.ModelForm):
    class Meta:
        model = SMTPEmailSettings
        fields = '__all__'


class SalarySettingsForm(forms.ModelForm):
    class Meta:
        model = SalarySettings
        fields = '__all__'
