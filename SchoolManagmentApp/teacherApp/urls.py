from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('teacher_app/', views.teacher_app_start, name='teacherApp'),
    path('teacher_app/reports', views.teacher_app_teacher, name='teacher_reports'),
    path('report_detail/<int:reportId>/', views.report_detail, name='report_detail'),

    #from event to raport
    path('event_raport/<int:eventId>', views.from_event_to_raport, name='from_event_to_raport'),

    #lesson delivery
    path('lesson_delivery_start/', views.lesson_delivery_start, name='lesson_delivery_start'),
]