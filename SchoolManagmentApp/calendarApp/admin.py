from django.contrib import admin
from .models import Lesson, Classroom, ClassroomReservation, TeacherReservation
# Register your models here.


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'day_of_week','lesson_number','subject', 'date','is_base','id',]
    ordering = ['class_name', 'day_of_week','lesson_number', 'date','is_base','id',]

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass

@admin.register(ClassroomReservation)
class ClassroomReservationAdmin(admin.ModelAdmin):
    pass

@admin.register(TeacherReservation)
class TeacherReservationAdmin(admin.ModelAdmin):
    pass
