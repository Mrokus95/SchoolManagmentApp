from django import forms
from django.shortcuts import get_object_or_404
from .models import Lesson
from eventApp.models import Teacher
from usersApp.models import ClassUnit

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'classroom', 'is_base']

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        teacher = cleaned_data.get('teacher')

        if subject not in teacher.lesson_type.all():

            raise forms.ValidationError("Selected subject is not taught by the selected teacher.")

        return cleaned_data
    


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'teacher', 'classroom', 'is_base', 'is_cancelled']


    def clean(self):
        cleaned_data = super().clean()
        is_base = cleaned_data.get('is_base')
        is_cancelled = cleaned_data.get('is_cancelled')
        subject = cleaned_data.get('subject')
        teacher = cleaned_data.get('teacher')

        if is_base and is_cancelled:
            raise forms.ValidationError("Both 'is base' and 'is cancelled' cannot be selected at the same time.")
        
        if subject not in teacher.lesson_type.all():

            raise forms.ValidationError("Selected subject is not taught by the selected teacher.")

        return cleaned_data
    
    

class ClassUnitForm(forms.ModelForm):
    class_unit = forms.ModelChoiceField(queryset=ClassUnit.objects.all(), label='Class:')
    class Meta:
        model = ClassUnit
        fields = ['class_unit']