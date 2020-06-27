from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

class UserCreate(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','first_name','last_name','email','password1','password2','is_client','is_employee','is_admin')

    def __init__(self,*args,**kwargs):
        super(UserCreate,self).__init__(*args,**kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if not cleaned_data['is_client'] and not cleaned_data['is_admin'] and not cleaned_data['is_employee']:
            raise forms.ValidationError({'is_admin':'Select atleast one of is_client or is_admin or is_employee'})

        return cleaned_data

    def save(self, commit=True):
        user = super(UserCreate, self).save(commit=False)
        data = self.clean()
        if data['is_admin']:
            user.is_superuser = True

        # Create client or staff here if you want to
        user.save()
        print(user)
        return user

# class UserChange(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('username','first_name','last_name','email','password1','password2','is_client','is_employee','is_admin')
#
#     def __init__(self,*args,**kwargs):
#         super(UserCreate,self).__init__(*args,**kwargs)
#         self.fields['first_name'].required = True
#         self.fields['email'].required = True
#         self.fields['username'].required = True
#
#     def clean(self):
#         cleaned_data = super().clean()
#         print(cleaned_data)
#         if not cleaned_data['is_client'] and not cleaned_data['is_admin'] and not cleaned_data['is_employee']:
#             raise forms.ValidationError({'is_admin':'Select atleast one of is_client or is_admin or is_employee'})
#
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super(UserCreate, self).save(commit=False)
#         data = self.clean()
#         if data['is_admin']:
#             user.is_superuser = True
#
#         # Create client or staff here if you want to
#         user.save()
#         print(user)
#         return user

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
