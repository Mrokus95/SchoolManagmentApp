from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from eventApp.models import LessonReport, CalendarEvents

class LessonRportFilterForm(forms.Form):

    subject = forms.ChoiceField()
    class_unit = forms.ChoiceField()
    start_date = forms.DateField()

class ClassSubjectChoiceForm(forms.Form):

    class_unit = forms.ChoiceField()    
    subject = forms.ChoiceField()    


class LessonReportTextForm(forms.ModelForm):
    class Meta:
       model = LessonReport

       fields = {
           'lesson_description',
           'lesson_title',
       }


class AddEventForm(forms.ModelForm):
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

