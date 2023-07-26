from django import forms
from django.forms.widgets import SelectDateWidget


class EventFilterStudentForm(forms.Form):

    subject = forms.ChoiceField()

    event_type = forms.ChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField()