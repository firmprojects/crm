import django.forms as forms
from .models import *

class MailForm(forms.ModelForm):
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'class':'form-control'}),required=False)
    class Meta:
        model = MailBody
        fields = ('to','cc','subject','body')
        widgets = {
        'body':forms.Textarea(),
        'to':forms.SelectMultiple(),
        'cc':forms.SelectMultiple(),
        }

class ReplyForm(forms.ModelForm):
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'class':'form-control'}),required=False)
    class Meta:
        model = MailBody
        fields = ('cc','subject','body')
        widgets = {
        'body':forms.Textarea(),
        }
