from django import forms
        # Add your own processing here.

        # You must return the original result.



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
        
        
    

