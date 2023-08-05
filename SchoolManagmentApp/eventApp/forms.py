from django import forms
from django.forms.widgets import SelectDateWidget
from .models import CalendarEvents
from gradesApp.models import Semester
from datetime import date

class EventFilterStudentForm(forms.Form):

    current_semester = Semester.objects.all().order_by('-start_date').first()
    print(current_semester)
    subject = forms.ChoiceField()
    event_type = forms.ChoiceField()
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': current_semester.start_date,
            'max': current_semester.end_date,
            }), initial=date.today()
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': current_semester.start_date,
            'max': current_semester.end_date,
            }), initial=date.today()
    )

class AddEvent(forms.ModelForm):
    class Meta:
        model = CalendarEvents
        fields = (
            'description',
            'event_type',
            'realisation_time',
            'connected_to_lesson',           
        )

    realisation_time = forms.DateField(widget=forms.SelectDateWidget)


