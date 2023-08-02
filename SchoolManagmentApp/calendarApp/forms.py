from django import forms
from .models import Lesson
from usersApp.models import ClassUnit

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'classroom', 'is_base']


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'classroom', 'is_base', 'is_cancelled']


    def clean(self):
        cleaned_data = super().clean()
        is_base = cleaned_data.get('is_base')
        is_cancelled = cleaned_data.get('is_cancelled')

        if is_base and is_cancelled:
            raise forms.ValidationError("Both 'is_base' and 'is_cancelled' cannot be selected at the same time.")
        
        return cleaned_data


class ClassUnitForm(forms.ModelForm):
    class_unit = forms.ModelChoiceField(queryset=ClassUnit.objects.all(), label='Class:')
    class Meta:
        model = ClassUnit
        fields = ['class_unit']