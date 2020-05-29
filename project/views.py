from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Projects, Clients
from .forms import ProjectForm, ClientSignupForm
from allauth.account.views import SignupView


class CreateProject(CreateView):
    model = Projects
    template_name = 'project/project.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        context['projects'] = Projects.objects.all()
        return context


class ProjectDetail(DetailView):
    model = Projects
    template_name = 'project/project_detail.html'



class ClientsCreateView(SignupView):
    model = Clients
    form_class = ClientSignupForm
    template_name = 'project/clients.html'
    redirect_field_name = 'next'
    view_name = 'client_sign_up'
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(ClientsCreateView, self).get_context_data(**kwargs)
        context['clients'] = Clients.objects.all()
        return context

    # def form_valid(self, form):
    #     username = self.request.POST.get('username')
    #     h = CustomUser.objects.create(username)
    #     h.save()
    #     form.user = h
    #     return super().form_valid(form)

    # def form_invalid(self, form):
    #     print("Invalid", form.errors)
    #     return super().form_invalid(form)


class ClientsDetailView(DetailView):
    model = Clients
    template_name = 'project/client_detail.html'


class ClientsUpdateView(UpdateView):
    model = Clients
    fields = ['company_name', 'client_email', 'clients_id', 'state', 'country',   'phone_number', 'contact_person', 'contact_person_designation',
              'address',  'photo']
    success_url = reverse_lazy('project:clients')

    # def form_valid(self, form):
    #     form.instance.author == self.request.user
    #     return super().form_valid(form)


class ClientDelete(DeleteView):
    model = Clients
    template_name = 'project/delete_client.html'
