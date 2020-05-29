from django.shortcuts import render
from django.views.generic import TemplateView

class Users(TemplateView):
    template_name = 'users/users.html'


class Contacts(TemplateView):
    template_name = 'users/contacts.html'


class AddContacts(TemplateView):
    template_name = 'users/add_contacts.html'
