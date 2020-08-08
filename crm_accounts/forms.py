from django import forms
from .models import Expenses

class DateInput(forms.DateInput):
    input_type = 'date'


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['item_name', 'purchase_from', 'purchase_date',
                  'purchase_by', 'amount', 'paid_by', 'status', 'attachement' ]
        widgets = {
            'purchase_date': DateInput(format='%m-%d-%Y'),
        }
