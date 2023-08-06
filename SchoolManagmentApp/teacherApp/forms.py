from django import forms
from eventApp.models import LessonReport

class LessonRportFilter(forms.Form):

    subject = forms.ChoiceField()
    class_unit = forms.ChoiceField()
    start_date = forms.DateField()

class ClassSubjectChoiceForm(forms.Form):

    class_unit = forms.ChoiceField()    
    subject = forms.ChoiceField()    


class LessonReportText(forms.ModelForm):
    class Meta:
       model = LessonReport

       fields = {
           'lesson_description',
           'lesson_title'
       }






