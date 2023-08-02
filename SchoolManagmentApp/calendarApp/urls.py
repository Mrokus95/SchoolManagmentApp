from django.urls import path, re_path
from .views import view_schedule, create_lesson, edit_lesson

urlpatterns = [
    path('', view_schedule, name='view_schedule'),
    path('<int:class_id>/', view_schedule, name='view_schedule'),
    path('create/<int:class_id>/<str:date>/<int:lesson_number>/<int:week_offset>/', create_lesson, name='create_lesson'),
    path('edit/<int:lesson_id>/<int:week_offset>/', edit_lesson, name='edit_lesson'),
    re_path(r'^(?P<class_id>\d+)/(?P<week_offset>-?\d+)/$', view_schedule, name='view_schedule'),

 
]