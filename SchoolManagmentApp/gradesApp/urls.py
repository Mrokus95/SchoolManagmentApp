from django.urls import path
from .views import view_grades, view_grades_teacher, view_grades_teacher_final

urlpatterns = [
    path("<int:semester>/", 
         view_grades, 
         name="view_grades"
         ),
    path("teacher/", 
         view_grades_teacher, 
         name="view_grades_teacher"
         ),
    path(
        "teacher/<int:semester>/<int:class_unit>/<int:subject>/",
        view_grades_teacher_final,
        name="view_grades_teacher_final",
    ),
    path("", 
         view_grades, 
         name="view_grades"
         ),
]
