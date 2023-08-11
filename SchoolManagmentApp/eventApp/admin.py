from django.contrib import admin
from eventApp.models import  Teacher, Subject, LessonReport, CalendarEvents

admin.site.register(CalendarEvents)
admin.site.register(Subject)
admin.site.register(LessonReport)
admin.site.register(Teacher)
