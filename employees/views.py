from django.shortcuts import render, get_object_or_404
from django.shortcuts import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (HolidaysForm, LeaveRequestForm, StaffSignupForm)
from .models import ( Education, Experience, Skill, Department, Designation, Holidays, LeaveRequest, LeaveType, Staff)
from allauth.account.views import SignupView

class StaffCreateView(SignupView):
    model = Staff
    form_class = StaffSignupForm
    template_name = 'employees/employees.html'

    def get_context_data(self, **kwargs):
        context = super(StaffCreateView, self).get_context_data(**kwargs)
        context['staff'] = Staff.objects.all()
        return context


class HolidayCreate(CreateView):
    model = Holidays
    template_name = "employees/holiday.html"
    form_class = HolidaysForm

    def get_context_data(self, **kwargs):
        context = super(HolidayCreate, self).get_context_data(**kwargs)
        context['holidays'] = Holidays.objects.all()
        return context


class HolidayUpdate(UpdateView):
    model = Holidays
    fields = ['name', 'date']


class HolidayDelete(DeleteView):
    model = Holidays
    success_url = '/employees/holiday'


class CreateDepartment(CreateView):
    model = Department
    template_name = "employees/department.html"
    fields = ['name', ]

    def get_context_data(self, **kwargs):
        context = super(CreateDepartment, self).get_context_data(**kwargs)
        context['dept'] = Department.objects.all()
        return context


class UpdateDepartment(UpdateView):
    model = Department
    fields = ['name']


class DeleteDepartment(DeleteView):
    model = Department
    success_url = '/employees/department'


class CreateDesignation(CreateView):
    model = Designation
    template_name = "employees/designation.html"
    fields = ['title', ]

    def get_context_data(self, **kwargs):
        context = super(CreateDesignation, self).get_context_data(**kwargs)
        context['designation'] = Designation.objects.all()
        return context


class UpdateDesignation(UpdateView):
    model = Designation
    fields = ['title']


class DeleteDesignation(DeleteView):
    model = Designation
    success_url = '/employees/designation'


class CreateLeave(CreateView):
    model = LeaveRequest
    template_name = "employees/leave.html"
    fields = ['employee','leave_type', 'leave_start_date', 'leave_end_date',
              'number_of_days', 'remaining_days', 'leave_reason']

    def get_context_data(self, **kwargs):
        context = super(CreateLeave, self).get_context_data(**kwargs)
        context['leave'] = LeaveRequest.objects.all()
        return context

class UpdateLeave(UpdateView):
    model = LeaveRequest
    fields = ['employee', 'leave_type', 'leave_start_date', 'leave_end_date',
              'number_of_days', 'remaining_days', 'leave_reason']


class DeleteLeave(LoginRequiredMixin, DeleteView):
    model = LeaveRequest
    success_url = '/employees/leave.html'


class CreateLeaveType(CreateView):
    model = LeaveType
    template_name = "employees/leave_type.html"
    fields = ['title', ]
    success_url = '/employees/leave'

    def get_context_data(self, **kwargs):
        context = super(CreateLeaveType, self).get_context_data(**kwargs)
        context['leave_type'] = LeaveType.objects.all()
        return context


class UpdateLeaveType(UpdateView):
    model = LeaveType
    fields = ['title']


class DeleteLeaveType(DeleteView):
    model = LeaveType
    success_url = '/employees/leave'


def attendance(request):
    return render(request, 'employees/attendance.html')


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
