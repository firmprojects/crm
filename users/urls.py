from django.contrib import admin
from django.urls import path
from .views import Users, Contacts, AddContacts, StaffDashboard, LoginPage

app_name = 'users'
urlpatterns = [
    path('all', Users.as_view(), name='users'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('add_contacts', AddContacts.as_view(), name='add_contacts'),
    path('staff/dashboard', StaffDashboard.as_view(), name='staff_dashboard'),
    path('', LoginPage.as_view(), name="home")
]