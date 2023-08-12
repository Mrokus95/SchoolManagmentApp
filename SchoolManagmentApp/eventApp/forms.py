from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget
from datetime import date, timedelta
from .models import CalendarEvents
from gradesApp.models import Semester

class EventFilterStudentForm(forms.Form):
  
    try:
        current_semester = Semester.objects.all().order_by(
            '-start_date'
            ).first()
        if not current_semester:
            current_semester = Semester(
                number=1,
                start_school_year=2023,
                start_date=date(2023, 1, 1),
                end_date=date(2023, 12,31)
                )
    except: 
        ValueError('No registred semester yet')

    SUBJECT_CHOICES = [
        ('All', 'All'),
        ('Mathematic', 'Mathematic'),
        ('English', 'English'),
        ('History', 'History'),
        ('Biology', 'Biology'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Philosophy', 'Philosophy'),
    ]
    EVENT_TYPE_CHOICES = [
        ('All', 'All'),
        ('Other', 'Other'),
        ('Small Test', 'Small Test'),
        ('Test', 'Test'),
        ('Essay', 'Essay'),
        ('Project', 'Project'),
    ]
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES)
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
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if end_date < self.current_semester.start_date: 
            raise forms.ValidationError("Date must be on current semester")
        if end_date > self.current_semester.end_date:
            raise forms.ValidationError("Date must be on current semester")
        if end_date < start_date:
            raise forms.ValidationError("Date must be past start date")
        return end_date
    
class AddEvent(forms.ModelForm):
    class Meta:
        model = CalendarEvents
        fields = (
            'description',
            'event_type',
            'realisation_time',
            'connected_to_lesson',           
        )
    realisation_time = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={'min': (timezone.now() + timedelta(days=1)).date()}
            )
    )
    def clean_realisation_time(self):
        realisation_time = self.cleaned_data.get('realisation_time')
        if realisation_time < (timezone.now() + timedelta(days=1)).date():
            raise ValidationError("End date must be tomorrow or further")
        return realisation_time