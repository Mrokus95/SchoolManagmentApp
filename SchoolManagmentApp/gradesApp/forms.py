from django import forms
from .models import Grades

class GradesForm(forms.modelForm):
    class Meta:
        model = Grades

        fields = {
            'grade',
            'grade_sdiscriptions',
        }


 
