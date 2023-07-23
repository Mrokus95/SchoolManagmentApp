from django.contrib import admin
from .models import Profile, Parent, ClassUnit, Student
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'phone_number', 'account_type']
    list_filter = ['user', 'account_type', 'phone_number']
    search_fields = ['user', 'phone_number']
    ordering = ['account_type', 'user']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student']

@admin.register(ClassUnit)
class ClassUnitAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
