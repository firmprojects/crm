from django.contrib import admin
from .models import *

class EmployyeeAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'

class EmployyeeAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'


class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'course_name',
                    'start_date', 'end_date']


admin.site.register(Education, EducationAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number', 'branch', 'designation', 'staff_id']


admin.site.register(Staff, StaffAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff','attendance']


admin.site.register(Attendance, AttendanceAdmin)

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'title',
                    'start_date', 'end_date']


admin.site.register(Experience, ExperienceAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Skill, SkillAdmin)


class HolidaysAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']


admin.site.register(Holidays, HolidaysAdmin)


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(LeaveType, LeaveTypeAdmin)


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['leave_type', 'leave_start_date', 'leave_end_date','leave_reason']

admin.site.register(LeaveRequest, LeaveRequestAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Department, DepartmentAdmin)


