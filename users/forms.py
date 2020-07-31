from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from allauth.account.forms import SignupForm

from django.contrib.auth import get_user_model
from employees.models import Staff
from project.models import Clients

class UserCreate(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_client = forms.CharField(widget=forms.CheckboxInput,required=False)
    is_employee = forms.CharField(widget=forms.CheckboxInput,required=False)
    is_admin = forms.CharField(widget=forms.CheckboxInput,required=False)
    username = forms.CharField(required=True)


    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if not cleaned_data['is_client'] and not cleaned_data['is_admin'] and not cleaned_data['is_employee']:
            raise forms.ValidationError({'is_admin':'Select atleast one of is_client or is_admin or is_employee'})

        return cleaned_data

    def save(self, request):
        user = super(UserCreate, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        print(self.cleaned_data.get('is_admin'))
        user.is_admin = True if self.cleaned_data.get('is_admin') == 'True' else False
        user.is_employee = True if self.cleaned_data.get('is_employee') == 'True'else False
        user.is_client = True if self.cleaned_data.get('is_client') == 'True' else False
        if user.is_admin: user.is_superuser = True

        user.save()
        return user

class UserChange(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','last_name','email')

    def __init__(self,*args,**kwargs):
        super(UserChange,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

        # self.fields['email'].required = True

class StaffForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(StaffForm,self).__init__(*args,**kwargs)
        self.fields['staff_id'].disabled = True
        self.fields['staff_id'].required = False


    class Meta:
        model = Staff
        fields = ('staff_id','phone_number','designation',)

class ClientForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ClientForm,self).__init__(*args,**kwargs)
        self.fields['clients_id'].disabled = True
    class Meta:
        model = Clients
        fields = ('clients_id','phone_number','company_name')

# class ClientForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     clients_id = forms.CharField(required=False)
#     address = forms.CharField(required=True)
#     state = forms.CharField(required=False)
#     country = forms.CharField(required=False)
#     company_name = forms.CharField(required=False)
#     photo = forms.ImageField(required=False)

#     class Meta(UserCreationForm.Meta):
#         model: User

#     @transaction.atomic
#     def client_save(self):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.phone_number = self.cleaned_data.get('phone_number')
#         user.email = self.cleaned_data.get('email')
#         user.save()
#         client = Clients.objects.create(user=user)
#         client.address = self.cleaned_data.get('address')
#         client.state = self.cleaned_data.get('state')
#         client.country = self.cleaned_data.get('country')
#         client.company_name = self.cleaned_data.get('company_name')
#         client.phote = self.cleaned_data.get('address')
#         client.save()
#         return client
