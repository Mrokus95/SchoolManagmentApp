from django.contrib import admin
from .models import WeeklySchedule, Lesson
# Register your models here.



@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
