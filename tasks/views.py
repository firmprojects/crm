from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import TicketForm
from .models import Ticketing
from django.http import JsonResponse
from django.forms.models import model_to_dict



class Tasks(TemplateView):
    template_name = 'tasks/tasklist.html'

class StaffTask(TemplateView):
    template_name = 'tasks/staff_task.html'


class NewTask(TemplateView):
    template_name = 'tasks/new_task.html'


class TaskDetail(TemplateView):
    template_name = 'tasks/task_detail.html'


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
        





