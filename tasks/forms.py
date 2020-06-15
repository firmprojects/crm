from django import forms
from .models import Ticketing,Task


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticketing
        fields = ('project', 'deadline', 'total_hours', 'remaining_hours', 'date', 'hours', 'description')

        widgets = {
            'deadline' : forms.TextInput(attrs={'class':'form-control datetimepicker cal-icon'}),
            'date' : forms.TextInput(attrs={'class':'form-control datetimepicker cal-icon'})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            'start_date' : forms.DateInput(attrs={'class':'form-control cal-icon'}),
            'end_date' : forms.DateInput(attrs={'class':'form-control cal-icon'}),
            'task_id':forms.TextInput(attrs={"readonly":"readonly"}),
            # 'start_date':forms.SelectDateWidget(),
            # 'end_date':forms.SelectDateWidget(attrs={'class':'form-control'})

        }
