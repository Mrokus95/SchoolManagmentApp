from django.contrib import admin
from .models import Grades
# Register your models here.

@admin.register(Grades)
class Grades(admin.ModelAdmin):
    pass