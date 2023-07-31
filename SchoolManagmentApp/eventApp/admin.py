from django.contrib import admin
from eventApp.models import  Teacher, Subject, LessonReport
from eventApp.models import CalendarEvents


admin.site.register(CalendarEvents)
admin.site.register(Subject)
admin.site.register(LessonReport)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass