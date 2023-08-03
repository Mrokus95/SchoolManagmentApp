from django import forms
from eventApp.models import Attendance

class LessonRportFilter(forms.Form):

    subject = forms.ChoiceField()
    class_unit = forms.ChoiceField()
    start_date = forms.DateField()

class ClassSubjectChoiceForm(forms.Form):

    class_unit = forms.ChoiceField()    
    subject = forms.ChoiceField()    


class AttendanceForm(forms.Form):
    
        fields = forms.BooleanField()




