from django import forms
from django.forms.widgets import SelectDateWidget
from .models import CalendarEvents

class EventFilterStudentForm(forms.Form):

    subject = forms.ChoiceField()

    event_type = forms.ChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField()

    
    


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


