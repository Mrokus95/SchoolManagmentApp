from django.contrib import admin
from eventApp.models import CalendarEvents, Teacher

# Register your models here.
admin.site.register(CalendarEvents)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass