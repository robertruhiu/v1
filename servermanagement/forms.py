from django import forms
from django.forms.widgets import DateTimeInput

from servermanagement.models import Job



class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

# class DateTimeInput(DateTimeInput):
#     input_type = 'datetime-local'

class JobForm(forms.ModelForm):
    # time = forms.DateTimeField(widget=DateTimeInput())
    date = forms.DateField(widget=DateInput())
    time = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Job
        exclude = ('has_executed', 'user', 'data', 'type', 'project')
        widgets = {
            'time': DateTimeInput,
        }
