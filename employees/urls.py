from django.urls import path, include

# from users.views import users_list
from .views import *
app_name = 'employees'

urlpatterns = [
    path('', StaffCreateView.as_view(), name='staff'),
#     path('<id>/update', edit_employee, name='employees_update'),
    path('holiday/', HolidayList.as_view(), name='holiday'),
    path('holiday/<int:pk>/update', HolidayUpdate.as_view(), name='holiday_update'),
    path('holiday/<int:pk>/delete', HolidayDelete.as_view(), name='delete_holiday'),
    path('department/', CreateDepartment.as_view(), name='departments'),
    path('department/<int:pk>/update',
         UpdateDepartment.as_view(), name='update_department'),
    path('department/<int:pk>/delete',
         DeleteDepartment.as_view(), name='delete_department'),
    path('designation/', CreateDesignation.as_view(), name='designation'),
    path('designation/<int:pk>/update', UpdateDesignation.as_view(), name='update_designation'),
    path('designation/<int:pk>/delete', DeleteDesignation.as_view(), name='delete_designation'),
    path('leave/', CreateLeave.as_view(), name='leave'),
    path('leave/<int:pk>/update',  UpdateLeave.as_view(), name='update_leave'),
    path('leave/<int:pk>/delete', DeleteLeave.as_view(), name='delete_leave'),
    path('leave_type/', CreateLeaveType.as_view(), name='leave_type'),
    path('leave_type/<int:pk>/update',
         UpdateLeaveType.as_view(), name='update_leavetype'),
    path('leave_type/<int:pk>/delete',
         DeleteLeaveType.as_view(), name='delete_leavetype'),
    path('attendance/', attendance, name='attendance'),
    path('tasks/', tasks, name='tasks'),
    path('leads/', leads, name='leads'),
    path('assets/', assets, name='assets'),
    path('activities/', activities, name='activities'),
    path('users/', users, name='users'),
    path('incoming_calls/', incoming_calls, name='incoming_calls'),
    path('voice_call/', voice_call, name='voice_call'),
    path('video_call/', video_call, name='video_call'),
    path('chat/', chat, name='chat'),

    path('get_attendance/',getAttendance,name='getAttendance'),

    path('staff_ac',StaffAC.as_view(),name='staff_ac')

]
