from django.shortcuts import render, redirect,reverse
from django.views.generic import TemplateView, DetailView, View, ListView
from .forms import TicketForm,TaskForm
from .models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.dateparse import parse_datetime

class Tasks(TemplateView):
    template_name = 'tasks/tasklist.html'
    def get(self,request):
        form = TaskForm()
        return render(request, self.template_name,{"form":form,"tasks":Task.objects.all()})

    def post(self,request):
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tasks:tasks")

        return render(request, self.template_name,{"form":form})

def change_priority(request):
    if request.method == 'POST':
        task = Task.objects.get(pk = request.POST['pk'])
        task.priority = request.POST['pr']
        task.save()
        return JsonResponse({"priority":task.priority})

def change_status(request):
    if request.method == 'POST':
        task = Task.objects.get(pk = request.POST['pk'])
        task.status = request.POST['status']
        task.save()
        return JsonResponse({"status":task.status})

class StaffTask(ListView):
    template_name = 'tasks/staff_task.html'
    model = Task


class NewTask(TemplateView):
    template_name = 'tasks/new_task.html'


class TaskDetail(DetailView):
    template_name = 'tasks/task_detail.html'
    model = Task


class TicketingView(View):
    def get(self, request):
        form = TicketForm()
        tk = Ticketing.objects.all()
        return render(request, 'tasks/ticket.html', context={'form':form, 'tk':tk})

    def post(self, request):
        form = TicketForm(request.POST)
        if form.is_valid():
            tickets = form.save()
            return JsonResponse({'ticket': model_to_dict(tickets)}, status=200)
        else:
            return redirect('tasks:ticket')

class TicketCompletedView(View):
    def post(self, request, id):
        ticket = Ticketing.objects.get(id=id)
        ticket.completed = True
        ticket.save()
        return JsonResponse({'result':model_to_dict(ticket)}, status=200)


class TicketDeleteView(View):
    def post(self, request, id):
        ticket = Ticketing.objects.get(id=id)
        ticket.delete()
        return JsonResponse({'result': 'ok'}, status=200)

def start_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            task = Task.objects.get(pk=request.POST['pk'])
            tracker = task.tasktracker
            tracker.start_time = parse_datetime(request.POST['start_time']).isoformat()
            tracker.status = 'working'
            tracker.save()

            task.status = "active"
            task.save()
            return JsonResponse({"success":"Success"})


def end_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            task = Task.objects.get(pk=request.POST['pk'])
            tracker = task.tasktracker
            tracker.end_time = parse_datetime(value=request.POST['end_time']).isoformat()
            if tracker.task_duration is None: tracker.task_duration = 0.0

            if type(tracker.task_duration) is str: tracker.task_duration = float(tracker.task_duration)

            tracker.task_duration += (parse_datetime(tracker.end_time) - parse_datetime(tracker.start_time)).total_seconds()
            tracker.status = 'pause'
            tracker.save()

            task.status = "inactive"
            task.save()
            return JsonResponse({"success":"Success"})

def terminate_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            task = Task.objects.get(pk=request.POST['pk'])
            tracker = task.tasktracker
            tracker.status = 'terminate'
            tracker.save()

            task.status = "inactive"
            task.save()
            return JsonResponse({"success":"Success"})

def get_time(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            task = Task.objects.get(pk=request.POST['pk'])
            try:
                return JsonResponse({"start_time":parse_datetime(task.tasktracker.start_time)})

            except TypeError:
                return JsonResponse({"start_time":None})


def upload_image(request,pk):
    if request.method == "POST":

        image = request.FILES['image']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/images")
        image_file = fs.save(image.name,image)

        up_ = ImageTask(task = Task.objects.get(pk=pk))
        up_.image.name = "images/"+image_file
        up_.save()


        return redirect(reverse('tasks:detail',args=(pk,)))
def upload_doc(request,pk):
    if request.method == "POST":

        document = request.FILES['document']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/document")
        doc_file = fs.save(document.name,document)

        up_ = DocTask(task = Task.objects.get(pk=pk))
        up_.doc.name = "document/"+doc_file
        up_.save()


        return redirect(reverse('tasks:detail',args=(pk,)))
