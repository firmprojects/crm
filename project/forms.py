from dal import autocomplete
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Projects, Clients
from django import forms
from .models import Clients
from django.db import transaction
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField



class ClientSignupForm(SignupForm):
     first_name = forms.CharField(required=True)
     last_name = forms.CharField(required=True)
     phone_number = PhoneNumberField()
     email = forms.EmailField(required=True)
     clients_id = forms.CharField(required=False)
     address = forms.CharField(required=True)
     state = forms.CharField(required=False)
     country = forms.CharField(required=False)
     company_name = forms.CharField(required=False)
     photo = forms.ImageField(required=False)

     @transaction.atomic
     def save(self, request):
        user = super(ClientSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_client = True
        user.save()
        client = Clients.objects.create(user=user)
        client.address = self.cleaned_data.get('address')
        client.phone_number = self.cleaned_data.get('phone_number')
        client.client_id = self.cleaned_data.get('client_id')
        client.country = self.cleaned_data.get('country')
        client.state = self.cleaned_data.pop('state')
        client.company_name = self.cleaned_data.get('company_name')
        client.phote = self.cleaned_data.get('address')
        client.save()
        return user




class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['clients','name', 'start_date',
                  'end_date', 'project_cost', 'priority',
                  'project_leader', 'team_member',
                  'description'
                  ]
        widgets = {
            'start_date': DateInput(format='%m-%d-%Y'),
            'end_date': DateInput(format='%m-%d-%Y'),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['company_name','clients_id', 'address',  'photo']
