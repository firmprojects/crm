from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from allauth.account.forms import SignupForm
from .models import( Department, Designation, Holidays, LeaveRequest, LeaveType, Staff )



class StaffSignupForm(SignupForm):
     first_name = forms.CharField(required=True)
     last_name = forms.CharField(required=True)
     phone_number = forms.CharField(required=True)
     email = forms.EmailField(required=True)
     staff_id = forms.CharField(required=False)
     address = forms.CharField(required=True)
     join_date= forms.DateField(required=False)
     designation = forms.CharField(required=False)
     branch = forms.CharField(required=False)
     photo = forms.ImageField(required=False)
    
     @transaction.atomic
     def save(self, request):
        user = super(StaffSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_employee = True
        user.save()
        staff = Staff.objects.create(user=user)
        staff.address = self.cleaned_data.get('address')
        staff.phone_number = self.cleaned_data.get('phone_number')
        staff.staff_id = self.cleaned_data.get('staff_id')
        staff.join_date = self.cleaned_data.get('join_date')
        staff.branch = self.cleaned_data.get('branch')
        staff.designation = self.cleaned_data.get('designation')
        staff.phote = self.cleaned_data.get('address')
        staff.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class HolidaysForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = ['name', 'date']
        widgets = {
            'date': DateInput(format='%Y-%m-%d'),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title']


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['title']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee','leave_type', 'leave_start_date', 'leave_end_date',
                   'leave_reason']
        widgets = {
            'leave_start_date': DateInput(format='%Y-%m-%d'),
            'leave_end_date': DateInput(format='%Y-%m-%d'),
        }


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['title']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title']