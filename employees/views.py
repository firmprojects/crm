from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (HolidaysForm, LeaveRequestForm,
                    StaffSignupForm, DepartmentForm, DesignationForm)
from .models import *
from allauth.account.views import SignupView
from users.models import Clocking
from django.utils import timezone
import datetime
from django.core.exceptions import ObjectDoesNotExist
from users.models import CustomUser
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib import messages

from dal import autocomplete


class StaffCreateView(SignupView):
    model = CustomUser
    template_name = 'employees/employees.html'

    def get_context_data(self, **kwargs):
        context = super(StaffCreateView, self).get_context_data(**kwargs)
        context['staff'] = CustomUser.objects.filter(is_employee=True)
        return context


class HolidayList(View):
    def get(self, request):
        form = HolidaysForm()
        holidays = Holidays.objects.all()
        return render(request, 'employees/holiday.html', {'form': form, 'holidays': holidays})

        return context


# class HolidayList(View):
#     def get(self, request):
#         form = HolidaysForm()
#         holidays = Holidays.objects.all()
#         return render(request, 'employees/holiday.html', {'form':form, 'holidays':holidays})


#     def post(self, request):
#         if request.method == 'POST':
#             form = HolidaysForm(request.POST)
#             if form.is_valid():
#                 new_holiday = form.save()
#                 return JsonResponse({'hols':model_to_dict(new_holiday)})


class HolidayCreate(View):
    def get(self, request):
        form = HolidaysForm()
        holidays = Holidays.objects.all()

        context = {'form': form, 'holidays': holidays}
        return render(self.request, 'employees/holiday.html', context)

    def post(self, request):
        form = HolidaysForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('employees:holiday'))

    def post(self, request):
        if request.method == 'POST':
            form = HolidaysForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Holiday was successfully created")
            return HttpResponseRedirect(reverse('employees:holiday'))


class DeleteHoliday(View):
    def get(self, request, id):
        holiday = Holidays.objects.get(id=id)
        holiday.delete()
        messages.success(request, "Holiday was successfully removed")
        return HttpResponseRedirect(reverse('employees:holiday'))


class UpdateHoliday(UpdateView):
    model = Holidays
    fields = '__all__'


class CreateDepartment(View):
    def get(self, request):
        form = DepartmentForm()
        dept = Department.objects.all()
        return render(request, 'employees/department.html', {'form': form, 'departments': dept})

    def post(self, request):
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Department was successfully created")
            return HttpResponseRedirect(reverse('employees:departments'))


class UpdateDepartment(UpdateView):
    model = Department
    fields = ['name']


class DeleteDepartment(View):
    def get(self, request, id):
        dept = Department.objects.get(id=id)
        dept.delete()
        messages.success(request, "Department was successfully removed")
        return HttpResponseRedirect(reverse('employees:departments'))


class CreateDesignation(View):
    def get(self, request):
        form = DesignationForm()
        designation = Designation.objects.all()
        return render(request, 'employees/designation.html', {'form': form, 'designations': designation})

    def post(self, request):
        if request.method == 'POST':
            form = DesignationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Designation was successfully created")
            return HttpResponseRedirect(reverse('employees:designation'))


class UpdateDesignation(UpdateView):
    model = Designation
    fields = ['title']


class DeleteDesignation(View):
    def get(self, request, id):
        designation = Designation.objects.get(id=id)
        designation.delete()
        messages.success(request, "Designation was successfully removed")
        return HttpResponseRedirect(reverse('employees:designation'))


class CreateLeave(View):
    def get(self, request):
        form = LeaveRequestForm()
        leave = LeaveRequest.objects.all()
        return render(request, 'employees/leave.html', {'form': form, 'leave': leave})

    def post(self, request):
        if request.method == 'POST':
            form = LeaveRequestForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Your leave request was successfull")
            return HttpResponseRedirect(reverse('employees:leave'))


class UpdateLeave(UpdateView):
    model = LeaveRequest
    fields = '__all__'
    success_url = '/employees/leave'


class DeleteLeave(View):
    def get(self, request, id):
        leave = LeaveRequest.objects.get(id=id)
        leave.delete()
        messages.success(request, "Leave Request was successfully removed")
        return HttpResponseRedirect(reverse('employees:leave'))


def change_status(request):
    if request.method == 'POST':
        leave = LeaveRequest.objects.get(pk=request.POST['pk'])
        leave.status = request.POST['status']
        leave.save()
        return JsonResponse({"status": leave.status})


class CreateLeaveType(View):
    def get(self, request):
        form = LeaveTypeForm()
        leave_type = LeaveType.objects.all()
        return render(request, 'employees/leave_type.html', {'form': form, 'leave_type': leave_type})

    def post(self, request):
        if request.method == 'POST':
            form = LeaveTypeForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Your leave type was successfully created")
            return HttpResponseRedirect(reverse('employees:leave_type'))


class UpdateLeaveType(UpdateView):
    model = LeaveType
    fields = ['title']
    success_url = '/employees/leave_type'


class DeleteLeaveType(View):
    def get(self, request, id):
        leave = LeaveType.objects.get(id=id)
        leave.delete()
        messages.success(request, "Leave type was successfully removed")
        return HttpResponseRedirect(reverse('employees:leave_type'))


def attendance(request):
    staffs = Staff.objects.all()
    # staffs = CustomUser.objects.all()

    for i in staffs:
        try:
            clock_in_data = Clocking.objects.get(user=i.user).clockin_data
            report = {}
            clockins = {}
            for date, data in clock_in_data.items():
                report[date] = "present" if data.__len__() > 0 else "absent"
                clockins[date] = data

            attend = Attendance.objects.get(staff=i)

            attend.attendance = report
            attend.clock_ins = clockins
            attend.save()
        except Clocking.DoesNotExist:
            pass

    return render(request, 'employees/attendance.html')


def getAttendance(request):
    print(request.POST)
    if request.method == "POST":
        year, month = int(request.POST['year']), int(request.POST['month'])
        print(year, month)
        data1 = present_absent(month=month, year=year)
        data2 = clockin_out(month=month, year=year)
        return JsonResponse({"present_absent": data1, "clockin_out": data2})
    return HttpResponseRedirect(reverse('employees:attendance'))


def tasks(request):
    return render(request, 'employees/tasks.html')


def leads(request):
    return render(request, 'employees/leads.html')


def users(request):
    return render(request, 'employees/users.html')


def assets(request):
    return render(request, 'employees/assets.html')


def activities(request):
    return render(request, 'employees/activities.html')


def incoming_calls(request):
    return render(request, 'employees/incoming-call.html')


def video_call(request):
    return render(request, 'employees/video-call.html')


def voice_call(request):
    return render(request, 'employees/voice-call.html')


def chat(request):
    return render(request, 'employees/chat.html')


def present_absent(month=None, year=None):
    month = month if month else datetime.date.today().month
    year = year if year else datetime.date.today().year

    data = {}
    date_start = datetime.date(int(year), int(month), 1)
    date_end = last_day_of_month(datetime.date(int(year), int(month), 1))
    for i in Staff.objects.all():
        attend = i.attendance
        data[i.user.username] = []
        for single_date in (date_start + datetime.timedelta(n) for n in range((date_end-date_start).days)):
            if str(single_date) in attend.attendance:
                data[i.user.username].append(
                    attend.attendance[str(single_date)])
            else:
                data[i.user.username].append("N/A")
    return data


def clockin_out(month=None, year=None):
    month = month if month else datetime.date.today().month
    year = year if year else datetime.date.today().year
    print(month, year)

    data = {}
    date_start = datetime.date(int(year), int(month), 1)
    date_end = last_day_of_month(datetime.date(int(year), int(month), 1))
    for i in Staff.objects.all():
        attend = i.attendance
        data[i.user.username] = []
        for single_date in (date_start + datetime.timedelta(n) for n in range((date_end-date_start).days)):
            if str(single_date) in attend.attendance:
                data[i.user.username].append(
                    attend.clock_ins[str(single_date)])
            else:
                data[i.user.username].append("N/A")

    return data


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

    # date_e


def filter_objects(date, month=None, year=None):

    if year and month:
        date = datetime.date.fromisoformat(date)

        if date.year == int(year) and date.month == int(month):
            return True

        return False

    elif month:
        date = datetime.date.fromisoformat(date)
        if date.month == int(month):
            return True
        return False
    elif year:
        date = datetime.date.fromisoformat(date)
        if date.year == int(year):
            return True
        return False
    else:
        return True


class StaffAC(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Staff.objects.all().order_by('user__username')
        if self.q:
            qs = qs.filter(user__username__istartswith=self.q)
        return qs
