from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'day_of_week', 'lesson_number', 'teacher', 'classroom', 'is_cancelled']

    def clean(self):
        cleaned_data = super().clean()
        day_of_week = cleaned_data.get('day_of_week')
        lesson_number = cleaned_data.get('lesson_number')


        if day_of_week is not None and lesson_number is not None:
            existing_lesson = Lesson.objects.filter(
                day_of_week=day_of_week,
                lesson_number=lesson_number,
                weeklyschedule__isnull=False
            ).first()

            if existing_lesson:
                raise forms.ValidationError(
                    f"A lesson already exists for Day {day_of_week} - Lesson Number {lesson_number}."
                )

        return cleaned_data
    