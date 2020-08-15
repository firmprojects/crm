from dal import autocomplete
from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
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
    def get(self,request,pk):
        self.object = self.get_object()
        form = ProjectForm(instance=self.object)
        context = self.get_context_data()
        context["form"] = form
        return render(request, 'project/project_detail.html', context)

    def post(self, request,pk):

        if 'team_member' in request.POST:
            staff = CustomUser.objects.get(pk=int(request.POST['team_member']))
            self.object = self.get_object()
            if staff not in self.object.team_member.all():
                self.object.team_member.add(staff)

        form = ProjectForm(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            self.object.name=form.cleaned_data['name']
            self.object.end_date=form.cleaned_data['end_date']
            self.object.project_cost = form.cleaned_data['project_cost']
            self.object.priority = form.cleaned_data['priority']
            self.object.project_leader = form.cleaned_data['project_leader']
            self.object.team_member.set(form.cleaned_data['team_member'])
            self.object.description = form.cleaned_data['description']

            self.object.save()

        else:
            print(form.errors)
            context = self.get_context_data()
            context["form"] = form
            return render(request, 'project/project_detail.html', context)

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
    template_name = 'project/clients.html'
    form_class = ClientSignupForm
    success_url = None

    def get_context_data(self, **kwargs):
        context = super(ClientsCreateView, self).get_context_data(**kwargs)
        context['clients'] = CustomUser.objects.filter(is_client=True)
        return context

    def form_valid(self, form):
        username = self.request.POST.get('username')
        h = CustomUser.objects.create(username)
        h.save()
        form.user = h
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid", form.errors)
        return super().form_invalid(form)



class UsersAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CustomUser.objects.all()
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        print(qs)
        return qs


class ClientAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CustomUser.objects.filter(is_client=True)
        if self.q:
            qs = qs.filter(username__istartswith=self.q)
        return qs

class CompanyAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CustomUser.objects.filter(is_client=True)
        if self.q:
            qs = qs.filter(clients__company_name__icontains=self.q)
        return qs

class ProjectAutocompletesView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Projects.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class MilestoneAuto(autocomplete.Select2QuerySetView):
    model = Projects
    def get_queryset(self):
        print(self.kwargs)
        qs = self.model.objects.get(pk=self.kwargs.get('pk')).milestone_set.all()
        if self.q:
            qs = qs.filter(task__istartswith=self.q)
        return qs

# class Milestones(TemplateView):
#     template_name =
def milestone_list(request,pk):
    pr = Projects.objects.get(pk=pk)
    milestones = pr.milestone_set.all()
    if "search" in request.GET:
        milestones = milestones.filter(task__contains = request.GET['search'])
    if request.method == 'POST':
        comment_ = request.POST['comment']
        obj = Comment(text=comment_,commented_by=request.user,project=pr)
        obj.save()
        return HttpResponseRedirect(reverse('project:milestones',args=(pk,)))
    return render(request,'project/milestones.html',{"pk":pk,"project":pr,"milestones":milestones,"comments":pr.comment_set.all().order_by('commented_on')})

def add_milestone(request):
    print("ok")
    if request.POST:
        print(request.POST)
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

def assign_(request,pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            milestone = Milestone.objects.get(pk=data['milestones'])
            user = CustomUser.objects.get(pk=data['staff'])
            print(user)

            if user not in milestone.milestone_assignes.all():
                milestone.milestone_assignes.add(user)
            else:
                 pass
            milestone.save()

            return HttpResponseRedirect(reverse('project:milestones',args=(pk,)))

    return HttpResponse("NOT ALLOWED")


def followers_(request,pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            milestone = Milestone.objects.get(pk=data['milestones'])
            # user = CustomUser.objects.get(pk=)
            # print(user)

            for i in data.getlist('staff'):
                user = CustomUser.objects.get(pk=i)
                if user not in milestone.milestone_followers.all():
                    milestone.milestone_followers.add(user)
            else:
                 pass
            milestone.save()

            return HttpResponseRedirect(reverse('project:milestones',args=(pk,)))

    return HttpResponse("NOT ALLOWED")
