from django import forms
from .models import Semester
from eventApp.models import Subject
from usersApp.models import ClassUnit
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError


class SemesterForm(forms.ModelForm):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Semester:')

    def clean(self):
        cleaned_data = super().clean()
        semester = cleaned_data.get('semester')

        try:
            get_object_or_404(Semester, id=semester.id)
        except Semester.DoesNotExist:
            raise ValidationError("This semester does not exists!")
        
        return cleaned_data
    
    class Meta:
        model = Semester
        fields = ['semester']


class GradesForm(forms.ModelForm):

    class_unit = forms.ModelChoiceField(queryset=ClassUnit.objects.all(), label='Class:')
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Subject:')
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Semester:')


    def clean(self):
        cleaned_data = super().clean()
        class_unit = cleaned_data.get('class_unit')
        subject = cleaned_data.get('subject')
        semester = cleaned_data.get('semester')

        try:
            get_object_or_404(ClassUnit, id=class_unit.id)
            get_object_or_404(Subject, id=subject.id)
            get_object_or_404(Semester, id=semester.id)
        except ClassUnit.DoesNotExist:
             messages.error('This class does not exists!')
             raise ValidationError("This class does not exists!")
        except Subject.DoesNotExist:
             messages.error('This subject does not exists!')
             raise ValidationError("This subject does not exists!")
        except Semester.DoesNotExist:
             messages.error('This semester does not exists!')
             raise ValidationError("This semester does not exists!'")
        
        return cleaned_data
    
    class Meta:
        model = ClassUnit
        fields = ['class_unit']
