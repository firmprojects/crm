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
