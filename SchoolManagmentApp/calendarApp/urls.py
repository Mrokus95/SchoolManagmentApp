from django.urls import path, re_path
from .views import view_schedule, create_lesson, edit_lesson

urlpatterns = [
    path('', view_schedule, name='view_schedule'),
    path('<int:class_id>/', view_schedule, name='view_schedule'),
    # path('create/<int:class_id>/<str:date>/<int:lesson_number>/<int:week_offset>/', create_lesson, name='create_lesson'),
    re_path(r'^create/(?P<class_id>\d+)/(?P<date>[-\w]+)/(?P<lesson_number>\d+)/(?P<week_offset>-?\d+)/$', create_lesson, name='create_lesson'),
    re_path(r'^(?P<class_id>\d+)/(?P<week_offset>-?\d+)/$', view_schedule, name='view_schedule'),
    re_path(r'^edit/(?P<lesson_id>\d+)/(?P<date>[-\w]+)/(?P<week_offset>-?\d+)/$', edit_lesson, name='edit_lesson'),
]
