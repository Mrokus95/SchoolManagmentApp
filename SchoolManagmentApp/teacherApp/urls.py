from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('teacher_app_start/', views.teacher_app_start, name='teacherApp'),
]