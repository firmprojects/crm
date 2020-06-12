from dal import autocomplete
from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.shortcuts import redirect
from users.models import CustomUser
from .models import *
from .forms import ProjectForm, ClientSignupForm
from allauth.account.views import SignupView
from django.core.files.storage import FileSystemStorage,File
from django.conf import settings
from django.db import models

class CreateProject(CreateView):
    model = Projects
    template_name = 'project/project.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        context['projects'] = Projects.objects.all()
        return context



class CreateProjectList(View):
    def get(self, request):
        form = ProjectForm()
        data = Projects.objects.all()
        return render(request, 'project/project-list.html', {"data": data, "form":form})


    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project:project-list')
        else:
            data = Projects.objects.all()
            print(form.errors)
            return render(request, 'project/project-list.html', {"data": data, "form":form})
        return redirect('project:project-list')

def delete_project(request,pk):
    Projects.objects.get(pk=pk).delete()
    return redirect('project:project-list')


class ProjectDetail(DetailView):
    model = Projects
    template_name = 'project/project_detail.html'
    def post(self, request,pk):

        staff = CustomUser.objects.get(pk=pk)
        self.object = self.get_object()
        if staff not in self.object.team_member.all():
            self.object.team_member.add(staff)
            print("ok")
        return redirect(request.build_absolute_uri())

def upload_image(request,pk):
    if request.method == "POST":

        image = request.FILES['image']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/images")
        image_file = fs.save(image.name,image)

        up_ = ImageUpload(project = Projects.objects.get(pk=pk))
        up_.image.name = "images/"+image_file
        up_.save()


        return redirect(reverse('project:project_detail',args=(pk,)))
def upload_doc(request,pk):
    if request.method == "POST":

        document = request.FILES['document']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/document")
        doc_file = fs.save(document.name,document)

        up_ = DocUpload(project = Projects.objects.get(pk=pk))
        up_.doc.name = "document/"+doc_file
        up_.save()


        return redirect(reverse('project:project_detail',args=(pk,)))

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


class UsersAutocompletesView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = CustomUser.objects.all().order_by('-id')
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs


class ClientAutocompletesView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Clients.objects.all().order_by('-company_name')
        if self.q:
            qs = qs.filter(company_name__istartswith=self.q)
        return qs


# class Milestones(TemplateView):
#     template_name =
def milestone_list(request,pk):
    return render(request,'project/milestones.html',{"pk":pk,"project":Projects.objects.get(pk=pk)})

def add_milestone(request):
    data = request.POST
    project = Projects.objects.get(pk=data['id'])

    milestone = Milestone(project=project,task=data['newTask'],completed=False)
    milestone.save()
    return JsonResponse({"success":"success"})

def delete_milestone(request):
    data = request.POST
    Milestone.objects.get(pk=data['id']).delete()
    return JsonResponse({"success":"success"})

def mark_complete(request):
    data = request.POST
    milestone = Milestone.objects.get(pk=data['id'])
    milestone.completed = True if request.POST['completed'] == 'true' else False
    milestone.save()
    print(milestone.completed,request.POST['completed'])
    return JsonResponse({"success":"success"})

def change_priority(request):
    data = request.POST
    project = Projects.objects.get(pk=data['id'])
    project.priority = data['priority']
    project.save()
    print("ok")
    # return JsonResponse({"success":"success"})
    return JsonResponse({"priority":project.priority})

def change_status(request):
    data = request.POST
    project = Projects.objects.get(pk=data['id'])
    project.status = data['status']
    project.save()
    print("ok")
    # return JsonResponse({"success":"success"})
    return JsonResponse({"status":project.status})
