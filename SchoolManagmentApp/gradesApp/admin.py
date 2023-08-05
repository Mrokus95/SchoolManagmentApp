from django.contrib import admin
from .models import Grades, Semester
# Register your models here.


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
 pass

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
 pass
