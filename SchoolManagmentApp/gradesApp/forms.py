from django import forms
from .models import Grades

class GradesForm(forms.Form):

    grade = forms.ChoiceField()
    grade_description = forms.CharField(max_length=250)
 
