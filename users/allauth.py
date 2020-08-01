from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.shortcuts import redirect

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
         if request.user.is_employee:
            return reverse('users:staff_dashboard')
         elif request.user.is_customer:
             return reverse('users:customer_dashboard')
         elif request.user.is_client:
             return reverse('users:client_dashboard')
         else:
             return reverse('dashboard:home')