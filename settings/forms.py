from django import forms
from .models import CompanyInfo


class settingsForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = '__all__'