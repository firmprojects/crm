from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('all', Users.as_view(), name='users'),
    path('user/<pk>/',UserProfile.as_view()),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('assets/', AssetView.as_view(), name='assets'),
    path('add_contacts', AddContacts.as_view(), name='add_contacts'),
    path('staff/dashboard', StaffDashboard.as_view(), name='staff_dashboard'),
    path('client/dashboard', ClientDashboard.as_view(), name='client_dashboard'),
    path('', LoginPage.as_view(), name="home"),
    path('clock_in/',clock_in,name='clock_in'),
    path('clock_out/',clock_out,name='clock_out'),
    path('get_date_on_refresh/',get_date_on_refresh,name='get_date_on_refresh'),
    path('get_weekly_report/',get_weekly_report,name='get_weekly_report'),
    path('delete_user/<pk>/',delete_user,name='delete_user'),
    path('profile/',staff_client,name='profile'),
    path('user/edit',profile,name='user_edit'),
    path('change/staff/',staff_view,name='staff_view'),
    path('change/client/',client_view,name='client_view'),
    path('users/profile', user_profile, name='user_profile_view'),
    path('change/select/',select,name='select_role'),
    path('change_staff_status/<pk>/',change_staff_status,name='change_staff_status')
]
