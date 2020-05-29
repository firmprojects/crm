from django.contrib import admin
from django.urls import path
from .views import Users, Contacts, AddContacts

app_name = 'users'
urlpatterns = [
    path('all', Users.as_view(), name='users'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('add_contacts', AddContacts.as_view(), name='add_contacts'),
]