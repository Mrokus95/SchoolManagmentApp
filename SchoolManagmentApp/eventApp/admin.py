from django.contrib import admin
from eventApp.models import  Teacher, Subject, Lesson, Day, LessonReport
from eventApp.models import CalendarEvents


admin.site.register(CalendarEvents)
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Day)



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass