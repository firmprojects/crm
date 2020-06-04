from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse

class Users(TemplateView):
    template_name = 'users/users.html'


class Contacts(TemplateView):
    template_name = 'users/contacts.html'


class AddContacts(TemplateView):
    template_name = 'users/add_contacts.html'

class StaffDashboard(TemplateView):
    template_name = 'users/staff_dashboard.html'

class LoginPage(LoginView):
    template_name = 'account/login.html'

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.is_employee:
    #             return redirect('users/staff_dashboard.html')
                
    #     return HttpResponseRedirect(redirect('dashboard/index.html', args=[self.request.user.username]))



# def home(request):
#     if request.user.is_authenticated:
#         if request.user.is_employee:
#             return redirect('users/staff_dashboard.html')
#         else:
#            return redirect('dashboard/index.html')

#     return render(request, 'account/login.html')
    
        