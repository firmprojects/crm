from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account.views import LoginView,SignupView
from allauth.account import signals
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime,parse_date
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .models import *
from .forms import *
import json
import datetime
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from users.decorators import employee_check



def superuser_only(function):

   def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied
       return function(request, *args, **kwargs)
   return _inner


WEEKDAY = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
# class Users(TemplateView):
#     template_name = 'users/users.html'
#     form_class = UserCreate
#     success_url = '/all'
#     def get(self,request):
#         super().get(request)
#         context = super().get_context_data()
#         context['users'] = CustomUser.objects.all()
#         context['form'] = UserCreate
#         context['change_form'] = UserChangeForm
#         return render(request,self.template_name,context=context)
#
#     def post(self,request):
#
#         context = super().get_context_data()
#         form = UserCreate(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(request.build_absolute_uri())
#         context['users'] = CustomUser.objects.all()
#         context['form'] = form
#         return render(request,self.template_name,context=context)
#

class Users(TemplateView):
    template_name = 'users/users.html'
    form_class = UserCreate
    success_url = '/all'
    def get(self,request):
        super().get(request)
        context = super().get_context_data()
        context['users'] = CustomUser.objects.all()
        context['form'] = UserCreate
        context['change_form'] = UserChangeForm
        return render(request,self.template_name,context=context)

    def post(self,request):

        context = super().get_context_data()
        form = UserCreate(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(request.build_absolute_uri())
        context['users'] = CustomUser.objects.all()
        context['form'] = form
        return render(request,self.template_name,context=context)






@method_decorator(superuser_only, name='dispatch')
class Users(SignupView):
    model = CustomUser
    form_class = UserCreate
    template_name = 'users/users.html'
    redirect_field_name = 'next'
    success_url = '/all'

    def get(self,request):
        super().get(request)
        context = super().get_context_data()
        context['users'] = CustomUser.objects.all()
        context['change_form'] = UserChangeForm
        return render(request,self.template_name,context=context)

    def form_valid(self, form):
        self.user = form.save(self.request)
        try:
            signals.user_signed_up.send(
                sender=self.user.__class__,
                request=self.request,
                user=self.user,
                **{}
            )
            return HttpResponseRedirect(self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response



class Contacts(TemplateView):
    template_name = 'users/contacts.html'


class AddContacts(TemplateView):
    template_name = 'users/add_contacts.html'

@method_decorator([employee_check, login_required], name='dispatch')
class StaffDashboard(TemplateView):
    template_name = 'users/staff_dashboard.html'


class ClientDashboard(TemplateView):
    template_name = 'users/client_dashboard.html'


class LoginPage(LoginView):
    template_name = 'account/login.html'

    # def get(self, *args, **kwargs):
    #     super().get(*args,**kwargs)
    #     print("ok")
    #     if self.request.user.is_authenticated:
    #         if self.request.user.is_employee:
    #             return redirect('users/staff_dashboard.html')
    #
    #     return HttpResponseRedirect(redirect('dashboard/index.html', args=[self.request.user.username]))

@csrf_exempt
def clock_in(request):
    if request.user.is_authenticated:
        data = json.loads(request.POST['data'])
        today = data['today']

        time_now = parse_datetime(data['date']).isoformat()

        try:
            clocking = Clocking.objects.get(user=request.user)
        except ObjectDoesNotExist:
            clocking = Clocking(user=request.user,clockin_data={})
            clocking.save()

        if str(today) in clocking.clockin_data:
            clocking.clockin_data[str(today)].append({'clock_in':time_now,'pos':data['pos']})
        else:
            clocking.clockin_data[str(today)] = [{'clock_in':time_now,'pos':data['pos']}]

        clocking.save()
        return JsonResponse({"time_now":time_now})
    return JsonResponse({"error":"Authenticate"},status=404)

@csrf_exempt
def clock_out(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.POST['data'])
            today = data['today']
            time_now = timezone.now()
            clocking = Clocking.objects.get(user=request.user)
            if 'clock_out' in clocking.clockin_data[str(today)][-1]:
                return JsonResponse({"error":"Click clock in first"})
            clocking.clockin_data[str(today)][-1]['clock_out'] = time_now.isoformat()

            clocking.save()
        except ObjectDoesNotExist:
            pass

        return JsonResponse({})
    return JsonResponse({"error":"Authenticate"},status=404)

def get_date_on_refresh(request):
    if request.user.is_authenticated:
        try:
            today = timezone.localdate()

            clocking = Clocking.objects.get(user=request.user)
            if str(today) in clocking.clockin_data:
                if 'clock_out' in clocking.clockin_data[str(today)][-1]:
                    return JsonResponse({"time":"No"})
                return JsonResponse({"time":clocking.clockin_data[str(today)][-1]['clock_in']})

            return JsonResponse({"time":"No"})

        except ObjectDoesNotExist:
            return JsonResponse({"time":"No"})
    return JsonResponse({"error":"Authenticate"},status=404)

def get_weekly_report(request):

    if request.user.is_authenticated:
        try:
            clocking = Clocking.objects.get(user=request.user)
            time_delta = timezone.timedelta(days=7)
            start_date = parse_date(request.POST['start'])

            report = {}
            hours_spent = {}
            for date in (start_date + timezone.timedelta(days=i) for i in range(1,8)):
                try:

                    report[date.isoformat()] = clocking.clockin_data[date.strftime("%Y-%m-%d")]

                    hours_spent[date.isoformat()] = 0

                    for i in clocking.clockin_data[date.strftime("%Y-%m-%d")]:
                        if "clock_out" in i:
                            hours_spent[date.isoformat()] += (parse_datetime(i['clock_out'])-parse_datetime(i['clock_in'])).total_seconds()

                        else:
                            hours_spent[date.isoformat()] += 0
                except KeyError:
                    pass

            return JsonResponse({"report":report,'hours_spent':hours_spent})
        except Clocking.DoesNotExist:
            return JsonResponse({})

def delete_user(request,pk):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_superuser:
            CustomUser.objects.get(pk=pk).delete()
            print("ok")
            return HttpResponseRedirect('/all')

    return HttpResponse("NOT ALLOWED")
# def home(request):
#     if request.user.is_authenticated:
#         if request.user.is_employee:
#             return redirect('users/staff_dashboard.html')
#         else:
#            return redirect('dashboard/index.html')

#     return render(request, 'account/login.html')
