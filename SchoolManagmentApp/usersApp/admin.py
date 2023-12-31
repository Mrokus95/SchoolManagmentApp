from django.contrib import admin
from .models import ClassUnit, Parent, Profile, Student


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "photo", "phone_number", "account_type"]
    list_filter = ["user", "account_type", "phone_number"]
    search_fields = ["user", "phone_number"]
    ordering = ["account_type", "user"]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    pass


@admin.register(ClassUnit)
class ClassUnitAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
