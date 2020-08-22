from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from allauth.account.forms import SignupForm

from django.contrib.auth import get_user_model
from employees.models import Staff
from project.models import Clients
from .models import Assets, CustomUser

class UserCreate(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    # is_client = forms.CharField(widget=forms.CheckboxInput,required=False)
    # is_employee = forms.CharField(widget=forms.CheckboxInput,required=False)
    # is_admin = forms.CharField(widget=forms.CheckboxInput,required=False)
    role = forms.ChoiceField(choices = (('is_client','Client'),('is_employee','Employee'),('is_admin','Admin')),required=True,widget=forms.RadioSelect,)
    username = forms.CharField(required=True)


    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(cleaned_data)
    #     if not cleaned_data['is_client'] and not cleaned_data['is_admin'] and not cleaned_data['is_employee']:
    #         raise forms.ValidationError({'is_admin':'Select atleast one of is_client or is_admin or is_employee'})
    #
    #     return cleaned_data

    def save(self, request):
        user = super(UserCreate, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        print(self.cleaned_data.get('is_admin'))
        setattr(user,self.cleaned_data['role'],True)
        # user.is_admin = True if self.cleaned_data.get('is_admin') == 'True' else False
        # user.is_employee = True if self.cleaned_data.get('is_employee') == 'True'else False
        # user.is_client = True if self.cleaned_data.get('is_client') == 'True' else False
        if user.is_admin: user.is_superuser = True

        user.save()
        return user

class UserChange(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','last_name','email',)

    def __init__(self,*args,**kwargs):
        super(UserChange,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].disabled = True

        # self.fields['email'].required = True

class StaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150,required=False)
    photo = forms.ImageField()

    def __init__(self,*args,**kwargs):
        user = kwargs.get('user')
        if user:
            del kwargs['user']
        super(StaffForm,self).__init__(*args,**kwargs)
        self.fields['staff_id'].disabled = True
        self.fields['staff_id'].required = False
        self.fields['photo'].required = False

        if user:
            self.fields['username'].widget.attrs.update({'value': user.username,'disabled':'disabled'})
            self.fields['first_name'].widget.attrs.update({'value': user.first_name,})
            self.fields['last_name'].widget.attrs.update({'value': user.last_name,})
            self.fields['photo'].widget.attrs.update({'value': user.photo,})
        # self.fields['username'].disabled = True

    class Meta:
        model = Staff
        fields = ('staff_id', 'phone_number','designation','address','gender')

    def save(self,commit=True):
        staff = super().save(commit)
        user = staff.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.photo = self.cleaned_data.get('photo')
        user.save()


        return staff

class ClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150,required=False)
    photo = forms.ImageField()

    def __init__(self,*args,**kwargs):
        user = kwargs.get('user')
        if user:
            del kwargs['user']
        super(ClientForm,self).__init__(*args,**kwargs)
        self.fields['clients_id'].disabled = True
        self.fields['photo'].required = False
        if user:
            self.fields['username'].widget.attrs.update({'value': user.username,'disabled':'disabled'})
            self.fields['first_name'].widget.attrs.update({'value': user.first_name,})
            self.fields['last_name'].widget.attrs.update({'value': user.last_name,})
            self.fields['photo'].widget.attrs.update({'value': user.photo,})

    class Meta:
        model = Clients
        fields = ('clients_id','phone_number','company_name','address','gender')

    def save(self,commit=True):
        client = super().save(commit)
        user = client.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.photo = self.cleaned_data.get('photo')
        user.save()

        return client

class DateInput(forms.DateInput):
    input_type = 'date'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Assets
        fields = ['assigned_to', 'asset_name', 'asset_id', 'description', 'purchase_date', 'receipt', 'assigned_date',  'warranty_end', 'asset_amount']
        widgets = {
            'assigned_date': DateInput(format='%m-%d-%Y'),
            'purchase_date': DateInput(format='%m-%d-%Y'),
        }
