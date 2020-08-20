from django.shortcuts import render, redirect
from django.views.generic import TemplateView,DetailView, View
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
from users.decorators import employee_check, client_check
from django.contrib import messages
from dal import autocomplete
from users.models import CustomUser

from allauth.exceptions import ImmediateHttpResponse

class UsersAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CustomUser.objects.filter(is_employee=True)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        print(qs)
        return qs



class AssetView(View):
    def get(self, request):
        assets = Assets.objects.all()
        form = AssetForm()
        return render(request, 'users/assets.html', {'assets':assets, 'form':form})

    def post(self, request):
        if request.method == 'POST':
            form = AssetForm(request.POST)
            print("Form errors", form.errors)
            if form.is_valid():
                form.save()
                messages.success(request, "Asset was successfully created")

            else:
                form = AssetForm()
                messages.error(request, "Asset was not created")

            return HttpResponseRedirect(reverse('users:assets'))


def superuser_only(function):

   def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied
       return function(request, *args, **kwargs)
   return _inner


WEEKDAY = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

@method_decorator(superuser_only, name='dispatch')
class UserProfile(DetailView):
    template_name = 'users/profile_admin.html'
    model = CustomUser

@login_required
def user_profile(request):
    data = None
    if request.user.is_client:
        data = request.user.clients
    elif request.user.is_employee:
        data = request.user.staff
    return render(request, 'users/profile.html',{'data':data})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChange(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            print('pk')
            return redirect('users:user_edit')
        return render(request,'users/user_profile.html',{'form':form})

    return render(request,'users/user_profile.html',{'form':UserChange(instance=request.user)})

def edit_profile_admin(request,pk):
    user = CustomUser.objects.get(pk=pk)
    if user == request.user:
        return redirect('users:user_edit')
    if request.method == 'POST':
        print(request.FILES)
        if user.is_client:
            form = ClientForm(request.POST,request.FILES,user=user,instance=user.clients)
        elif user.is_employee:
            form = StaffForm(request.POST,request.FILES,user=user,instance=user.staff)
        if form.is_valid():
            form.save()
            return redirect('users:edit_profile_admin',pk=pk)
        return render(request,'users/client_staff.html',{'form':form})

    if user.is_client:
        form = ClientForm(instance=user.clients,user=user)
    elif user.is_employee:
        form = StaffForm(instance=user.staff,user=user)
    else:
        return redirect('users:user_edit')
    return render(request,'users/client_staff_admin.html',{'form':form})

@login_required
def staff_client(request):
    if request.user.is_employee and request.user.is_client:
        return redirect('users:select_role')
    elif request.user.is_client:
        return redirect('users:client_view')
    elif request.user.is_employee:
        return redirect('users:staff_view')
    else:
        return redirect('users:user_edit')

@login_required
def select(request):
    if request.user.is_employee and request.user.is_client:
        return render(request,'users/select.html')

@login_required
def staff_view(request):
    if request.user.is_employee:
        if request.method == 'POST':
            form = StaffForm(request.POST,request.FILES,instance=request.user.staff)
            if form.is_valid():
                form.save()
                print(form.cleaned_data)
                return redirect('users:staff_view')
            return render(request,'users/client_staff.html',{'form':form})
        form = StaffForm(instance=request.user.staff,user=request.user)
        return render(request,'users/client_staff.html',{'form':form})
    return HttpResponseRedirect('/dashboard/')

@login_required
def client_view(request):
    if request.user.is_client:
        if request.method == 'POST':
            form = ClientForm(request.POST,request.FILES,instance=request.user.clients)
            if form.is_valid():
                form.save()
                return redirect('users:client_view')
            return render(request,'users/client_staff.html',{'form':form})
        form = ClientForm(instance=request.user.clients,user=request.user)
        return render(request,'users/client_staff.html',{'form':form})
    return HttpResponseRedirect('/dashboard/')

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
        context['form'] = UserCreate(initial={'role':'is_employee'})

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

@method_decorator([client_check, login_required], name='dispatch')
class ClientDashboard(TemplateView):
    template_name = 'users/client_dashboard.html'


class LoginPage(LoginView):
    template_name = 'account/login.html'

# def red(request):
#     if request.user.is_employee:
#         return redirect('employees:staff')
#     elif request.user.is_superuser:
#         return redirect('users:users')
#     else:
#         return redirect('dashboard:home')


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

def change_staff_status(request,pk):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_superuser:
            if request.method == 'POST':
                data = request.POST
                print(data)
                user = CustomUser.objects.get(pk=pk)
                if data['status'] == 'suspended':
                    user.is_active = False
                    user.save()
                    return JsonResponse({'status':'suspended'})

                elif data['status'] == 'on_leave':
                    staff = user.staff
                    staff.on_leave = True
                    staff.save()
                    user.save()
                    return JsonResponse({'status':'leave'})
                else:
                    staff = user.staff
                    staff.on_leave = False
                    staff.save()
                    user.is_active = True
                user.save()
            return JsonResponse({'status':'active'})

    return JsonResponse({},status=404)
