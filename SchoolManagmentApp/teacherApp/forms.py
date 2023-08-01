from django import forms
from eventApp.models import Subject
from usersApp.models import ClassUnit 




class LessonRportFilter(forms.Form):

    subject = forms.ChoiceField()
    class_unit = forms.ChoiceField()
    start_date = forms.DateField()

