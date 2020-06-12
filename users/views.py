from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account.views import LoginView
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime,parse_date

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import datetime


WEEKDAY = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
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

# def home(request):
#     if request.user.is_authenticated:
#         if request.user.is_employee:
#             return redirect('users/staff_dashboard.html')
#         else:
#            return redirect('dashboard/index.html')

#     return render(request, 'account/login.html')
