from django import forms
from django.forms import formset_factory
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject','day_of_week', 'lesson_number', 'teacher', 'classroom', 'is_cancelled']


class WeeklyScheduleForm(forms.Form):
    DAYS_OF_WEEK = [
        (1, 'Poniedziałek'),
        (2, 'Wtorek'),
        (3, 'Środa'),
        (4, 'Czwartek'),
        (5, 'Piątek'),
    ]

    week_number = forms.IntegerField()
    class_name = forms.CharField(max_length=100)
    is_base_schedule = forms.BooleanField(required=False)
    day_of_week = forms.ChoiceField(choices=DAYS_OF_WEEK)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day_of_week'].label = "Dzień tygodnia"
        self.fields['lesson_formset'] = LessonFormFormSet()
