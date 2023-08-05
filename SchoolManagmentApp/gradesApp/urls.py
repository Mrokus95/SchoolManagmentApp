from django.urls import path, re_path
from .views import view_grades

urlpatterns = [
    path('', view_grades, name='view_grades'),
    path('<int:semester>/', view_grades, name='view_grades'),
]
