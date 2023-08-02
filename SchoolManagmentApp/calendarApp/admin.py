from django.contrib import admin
from .models import Lesson
# Register your models here.


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'day_of_week','lesson_number','subject', 'date','is_base','id',]
    ordering = ['class_name', 'day_of_week','lesson_number', 'date','is_base','id',]
