from django.urls import path, re_path
from .views import create_lesson, edit_lesson, teachers, view_schedule

urlpatterns = [
    path("", view_schedule, name="view_schedule"),
    path("<int:class_id>/", view_schedule, name="view_schedule"),
    re_path(
        r"^create/(?P<class_id>\d+)/(?P<date>[-\w]+)/(?P<lesson_number>\d+)"
        r"/(?P<week_offset>-?\d+)/$",
        create_lesson,
        name="create_lesson",
    ),
    re_path(
        r"^(?P<class_id>\d+)/(?P<week_offset>-?\d+)/$",
        view_schedule,
        name="view_schedule",
    ),
    re_path(
        r"^edit/(?P<lesson_id>\d+)/(?P<date>[-\w]+)/(?P<week_offset>-?\d+)/$",
        edit_lesson,
        name="edit_lesson",
    ),
    path("get_teachers/<int:subject_id>/", 
         teachers, 
         name="teachers"),
]
