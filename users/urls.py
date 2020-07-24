from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('all', Users.as_view(), name='users'),
    # path('redirect/',red,name='red'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('add_contacts', AddContacts.as_view(), name='add_contacts'),
    path('staff/dashboard', StaffDashboard.as_view(), name='staff_dashboard'),
    path('client/dashboard', ClientDashboard.as_view(), name='client_dashboard'),
    path('', LoginPage.as_view(), name="home"),
    path('clock_in/',clock_in,name='clock_in'),
    path('clock_out/',clock_out,name='clock_out'),
    path('get_date_on_refresh/',get_date_on_refresh,name='get_date_on_refresh'),
    path('get_weekly_report/',get_weekly_report,name='get_weekly_report'),
    path('delete_user/<pk>/',delete_user,name='delete_user')
]
