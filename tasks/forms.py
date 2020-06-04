from django import forms
from .models import Ticketing


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticketing
        fields = ('project', 'deadline', 'total_hours', 'remaining_hours', 'date', 'hours', 'description')

        widgets = {
            'deadline' : forms.TextInput(attrs={'class':'form-control datetimepicker cal-icon'}),
            'date' : forms.TextInput(attrs={'class':'form-control datetimepicker cal-icon'})
        }