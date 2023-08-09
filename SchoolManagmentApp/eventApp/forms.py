from django import forms
from django.forms.widgets import SelectDateWidget
from .models import CalendarEvents
from gradesApp.models import Semester
from datetime import date

class EventFilterStudentForm(forms.Form):
  
    try:
        current_semester = Semester.objects.all().order_by('-start_date').first()
        if not current_semester:
            current_semester = Semester(
                number=1,
                start_school_year=2023,
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12,31)
                )
    except: 
        ValueError('No registred semester yet')

  
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


